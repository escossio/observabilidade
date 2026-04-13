from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class HostEnsureResult:
    host: dict[str, Any]
    action: str
    match_source: str
    warnings: list[str]


@dataclass
class ZabbixAPI:
    url: str
    user: str
    password: str
    dry_run: bool = False

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.token: str | None = None
        self._request_id = 1

    def login(self) -> str:
        result = self.call("user.login", {"username": self.user, "password": self.password}, include_auth=False)
        self.token = result
        return result

    def call(self, method: str, params: Any, include_auth: bool = True) -> Any:
        if self.dry_run and method in {
            "hostgroup.create",
            "templategroup.create",
            "template.create",
            "item.create",
            "trigger.create",
            "host.create",
            "host.update",
            "map.create",
            "map.update",
        }:
            raise RuntimeError(f"dry-run bloqueou escrita no Zabbix: {method}")
        headers = {"Content-Type": "application/json-rpc"}
        payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": self._request_id}
        self._request_id += 1
        if include_auth:
            if self.token is None:
                self.login()
            headers["Authorization"] = f"Bearer {self.token}"
        response = self.session.post(self.url, headers=headers, data=json.dumps(payload), timeout=60)
        response.raise_for_status()
        payload_out = response.json()
        if "error" in payload_out:
            raise RuntimeError(f"Zabbix API error in {method}: {payload_out['error']}")
        return payload_out["result"]

    def get_host_group(self, name: str) -> dict | None:
        result = self.call("hostgroup.get", {"output": "extend", "filter": {"name": [name]}})
        return result[0] if result else None

    def ensure_host_group(self, name: str) -> dict:
        group = self.get_host_group(name)
        if group:
            return group
        if self.dry_run:
            return {"groupid": None, "name": name}
        groupid = self.call("hostgroup.create", {"name": name})["groupids"][0]
        return self.get_host_group(name) or {"groupid": groupid, "name": name}

    def get_template_group(self, name: str) -> dict | None:
        result = self.call("templategroup.get", {"output": "extend", "filter": {"name": [name]}})
        return result[0] if result else None

    def ensure_template_group(self, name: str) -> dict:
        group = self.get_template_group(name)
        if group:
            return group
        if self.dry_run:
            return {"groupid": None, "name": name}
        groupid = self.call("templategroup.create", {"name": name})["groupids"][0]
        return self.get_template_group(name) or {"groupid": groupid, "name": name}

    def get_template(self, name: str) -> dict | None:
        result = self.call("template.get", {"output": "extend", "filter": {"host": [name]}})
        return result[0] if result else None

    def ensure_icmp_template(self, template_name: str, template_group_name: str) -> dict:
        template = self.get_template(template_name)
        if template is not None:
            return template

        if self.dry_run:
            return {"templateid": None, "host": template_name, "name": template_name, "dry_run": True}

        self.ensure_template_group(template_group_name)
        group = self.get_template_group(template_group_name)
        templateid = self.call(
            "template.create",
            {
                "host": template_name,
                "name": template_name,
                "groups": [{"groupid": group["groupid"]}],
                "tags": [
                    {"tag": "source", "value": "mtr-hop-map"},
                    {"tag": "role", "value": "transit-hop-icmp"},
                ],
            },
        )["templateids"][0]
        template = self.get_template(template_name)
        if template is None:
            template = {"templateid": templateid, "host": template_name, "name": template_name}
        self._ensure_icmp_template_items(templateid)
        self._ensure_icmp_template_trigger(templateid, template_name)
        return self.get_template(template_name) or template

    def _ensure_icmp_template_items(self, templateid: str) -> None:
        desired = [
            {
                "name": "ICMP ping",
                "key_": "icmpping",
                "type": 3,
                "value_type": 3,
                "delay": "30s",
                "history": "7d",
                "trends": "0",
                "units": "",
            },
            {
                "name": "ICMP response time",
                "key_": "icmppingsec",
                "type": 3,
                "value_type": 0,
                "delay": "30s",
                "history": "7d",
                "trends": "30d",
                "units": "s",
            },
            {
                "name": "ICMP packet loss",
                "key_": "icmppingloss",
                "type": 3,
                "value_type": 0,
                "delay": "30s",
                "history": "7d",
                "trends": "30d",
                "units": "%",
            },
        ]
        existing = self.call("item.get", {"output": ["itemid", "key_"], "hostids": templateid})
        existing_keys = {row["key_"] for row in existing}
        for item in desired:
            if item["key_"] in existing_keys:
                continue
            self.call("item.create", {"hostid": templateid, **item})

    def _ensure_icmp_template_trigger(self, templateid: str, template_name: str) -> None:
        expression = f"last(/{template_name}/icmpping)=0"
        existing = self.call("trigger.get", {"output": ["triggerid", "description"], "templateids": templateid})
        if any(item["description"] == "ICMP unreachable" for item in existing):
            return
        try:
            self.call(
                "trigger.create",
                {
                    "description": "ICMP unreachable",
                    "expression": expression,
                    "priority": 3,
                },
            )
        except Exception:
            fallback_expression = f"{{{template_name}:icmpping.last()}}=0"
            self.call(
                "trigger.create",
                {
                    "description": "ICMP unreachable",
                    "expression": fallback_expression,
                    "priority": 3,
                },
            )

    def get_host(self, hostname: str) -> dict | None:
        result = self.call(
            "host.get",
            {
                "output": "extend",
                "filter": {"host": [hostname]},
                "selectInterfaces": ["interfaceid", "ip", "main", "type", "useip", "port"],
                "selectTags": "extend",
                "selectParentTemplates": ["templateid", "host"],
                "selectHostGroups": ["groupid", "name"],
            },
        )
        return result[0] if result else None

    def get_hosts_by_ip(self, ip: str, groupid: str) -> list[dict]:
        interfaces = self.call("hostinterface.get", {"output": ["hostid", "ip"], "filter": {"ip": [ip]}})
        hostids = sorted({row["hostid"] for row in interfaces})
        if not hostids:
            return []
        return self.call(
            "host.get",
            {
                "output": "extend",
                "hostids": hostids,
                "groupids": [groupid],
                "selectInterfaces": ["interfaceid", "ip", "main", "type", "useip", "port"],
                "selectTags": "extend",
                "selectParentTemplates": ["templateid", "host"],
                "selectHostGroups": ["groupid", "name"],
                "sortfield": "hostid",
            },
        )

    def get_host_by_id(self, hostid: str) -> dict:
        result = self.call(
            "host.get",
            {
                "output": "extend",
                "hostids": [hostid],
                "selectInterfaces": ["interfaceid", "ip", "main", "type", "useip", "port"],
                "selectTags": "extend",
                "selectParentTemplates": ["templateid", "host"],
                "selectHostGroups": ["groupid", "name"],
            },
        )
        if not result:
            raise RuntimeError(f"Host inexistente: {hostid}")
        return result[0]

    def ensure_host(
        self,
        hostname: str,
        visible_name: str,
        groupid: str,
        templateid: str,
        ip: str,
        tags: list[dict[str, str]],
        template_mode: str = "link",
    ) -> HostEnsureResult:
        warnings: list[str] = []
        existing = self.get_host(hostname)
        match_source = "hostname"
        if existing is None:
            candidates = self.get_hosts_by_ip(ip, groupid)
            if candidates:
                if len(candidates) > 1:
                    warnings.append(f"mais de um host encontrado para {ip}; menor hostid reaproveitado")
                existing = self._choose_host_candidate(candidates, hostname)
                match_source = "ip"

        if existing:
            if self.dry_run:
                action = self._preview_existing_host_action(
                    existing,
                    hostname,
                    visible_name,
                    groupid,
                    templateid,
                    ip,
                    tags,
                    template_mode,
                )
                return HostEnsureResult(
                    host=existing,
                    action=action,
                    match_source=match_source,
                    warnings=warnings,
                )
            action = self._update_existing_host(
                existing,
                hostname,
                visible_name,
                groupid,
                templateid,
                ip,
                tags,
                template_mode,
            )
            return HostEnsureResult(
                host=self.get_host_by_id(existing["hostid"]),
                action=action,
                match_source=match_source,
                warnings=warnings,
            )

        if self.dry_run:
            synthetic_host = {
                "hostid": None,
                "host": hostname,
                "name": visible_name,
                "interfaces": [{"ip": ip, "main": "1", "type": "1", "useip": "1", "port": "10050"}],
                "tags": tags,
            }
            return HostEnsureResult(host=synthetic_host, action="planned-create", match_source="dry-run", warnings=warnings)

        result = self.call(
            "host.create",
            {
                "host": hostname,
                "name": visible_name,
                "groups": [{"groupid": groupid}],
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": "10050",
                    }
                ],
                "tags": tags,
            },
        )
        hostid = result["hostids"][0]
        if template_mode == "link" and templateid:
            self.call("host.update", {"hostid": hostid, "templates": [{"templateid": templateid}]})
        return HostEnsureResult(
            host=self.get_host_by_id(hostid),
            action="created",
            match_source="created",
            warnings=warnings,
        )

    def _preview_existing_host_action(
        self,
        existing: dict,
        hostname: str,
        visible_name: str,
        groupid: str,
        templateid: str,
        ip: str,
        tags: list[dict[str, str]],
        template_mode: str,
    ) -> str:
        planned = existing.get("host") != hostname or existing.get("name") != visible_name

        current_tags = {(item.get("tag"), item.get("value")) for item in existing.get("tags", [])}
        desired_tags = {(item.get("tag"), item.get("value")) for item in tags}
        planned = planned or current_tags != desired_tags

        current_groups = existing.get("hostgroups", [])
        groupids = {row["groupid"] for row in current_groups}
        planned = planned or groupid not in groupids

        current_templates = existing.get("parentTemplates", [])
        templateids = {row["templateid"] for row in current_templates}
        if template_mode == "link":
            planned = planned or templateid not in templateids
        elif template_mode == "clear":
            planned = planned or templateid in templateids

        interface = next((row for row in existing.get("interfaces", []) if row.get("main") == "1"), None)
        if interface is None:
            planned = True
        elif interface.get("ip") != ip or interface.get("port") != "10050":
            planned = True

        return "planned-update" if planned else "planned-reuse"

    def _choose_host_candidate(self, candidates: list[dict], canonical_hostname: str) -> dict:
        def rank(item: dict) -> tuple[int, int, int]:
            tags = {(tag.get("tag"), tag.get("value")) for tag in item.get("tags", [])}
            has_global_identity = ("identity_scope", "global-ip") in tags
            return (
                0 if has_global_identity else 1,
                0 if item.get("host") == canonical_hostname else 1,
                int(item["hostid"]),
            )

        return sorted(candidates, key=rank)[0]

    def _update_existing_host(
        self,
        existing: dict,
        hostname: str,
        visible_name: str,
        groupid: str,
        templateid: str,
        ip: str,
        tags: list[dict[str, str]],
        template_mode: str,
    ) -> str:
        updates: dict[str, Any] = {"hostid": existing["hostid"]}

        if existing.get("host") != hostname:
            updates["host"] = hostname
        if existing.get("name") != visible_name:
            updates["name"] = visible_name

        current_tags = {(item.get("tag"), item.get("value")) for item in existing.get("tags", [])}
        desired_tags = {(item.get("tag"), item.get("value")) for item in tags}
        if current_tags != desired_tags:
            updates["tags"] = tags

        current_groups = existing.get("hostgroups", [])
        groupids = {row["groupid"] for row in current_groups}
        if groupid not in groupids:
            updates["groups"] = [{"groupid": row["groupid"]} for row in current_groups] + [{"groupid": groupid}]

        current_templates = existing.get("parentTemplates", [])
        templateids = {row["templateid"] for row in current_templates}
        if template_mode == "link" and templateid not in templateids:
            updates["templates"] = [{"templateid": row["templateid"]} for row in current_templates] + [{"templateid": templateid}]
        elif template_mode == "clear" and templateid in templateids:
            updates["templates_clear"] = [{"templateid": templateid}]

        interface = next((row for row in existing.get("interfaces", []) if row.get("main") == "1"), None)
        if interface is None:
            updates["interfaces"] = [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050",
                }
            ]
        elif interface.get("ip") != ip or interface.get("port") != "10050":
            updates["interfaces"] = [
                {
                    "interfaceid": interface["interfaceid"],
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050",
                }
            ]

        if len(updates) == 1:
            return "reused"

        self.call("host.update", updates)
        return "updated"

    def plan_host(
        self,
        hostname: str,
        visible_name: str,
        groupid: str,
        templateid: str,
        ip: str,
        tags: list[dict[str, str]],
        template_mode: str = "link",
    ) -> HostEnsureResult:
        dry_run_api = ZabbixAPI(self.url, self.user, self.password, dry_run=True)
        dry_run_api.session = self.session
        dry_run_api.token = self.token
        dry_run_api._request_id = self._request_id
        return dry_run_api.ensure_host(hostname, visible_name, groupid, templateid, ip, tags, template_mode=template_mode)

    def get_image(self, name: str) -> dict | None:
        result = self.call("image.get", {"output": "extend", "filter": {"name": [name]}})
        return result[0] if result else None

    def get_map(self, name: str) -> dict | None:
        result = self.call(
            "map.get",
            {"output": "extend", "selectSelements": "extend", "selectLinks": "extend", "filter": {"name": [name]}},
        )
        return result[0] if result else None
