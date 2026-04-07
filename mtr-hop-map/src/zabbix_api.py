from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ZabbixAPI:
    url: str
    user: str
    password: str

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.token: str | None = None
        self._request_id = 1

    def login(self) -> str:
        result = self.call("user.login", {"username": self.user, "password": self.password}, include_auth=False)
        self.token = result
        return result

    def call(self, method: str, params: dict, include_auth: bool = True) -> dict:
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
        groupid = self.call("hostgroup.create", {"name": name})["groupids"][0]
        return self.get_host_group(name) or {"groupid": groupid, "name": name}

    def get_template_group(self, name: str) -> dict | None:
        result = self.call("templategroup.get", {"output": "extend", "filter": {"name": [name]}})
        return result[0] if result else None

    def ensure_template_group(self, name: str) -> dict:
        group = self.get_template_group(name)
        if group:
            return group
        groupid = self.call("templategroup.create", {"name": name})["groupids"][0]
        return self.get_template_group(name) or {"groupid": groupid, "name": name}

    def get_template(self, name: str) -> dict | None:
        result = self.call("template.get", {"output": "extend", "filter": {"host": [name]}})
        return result[0] if result else None

    def ensure_icmp_template(self, template_name: str, template_group_name: str) -> dict:
        self.ensure_template_group(template_group_name)
        template = self.get_template(template_name)
        if template is None:
            group = self.get_template_group(template_group_name)
            templateid = self.call(
                "template.create",
                {
                    "host": template_name,
                    "name": template_name,
                    "groups": [{"groupid": group["groupid"]}],
                },
            )["templateids"][0]
            template = self.get_template(template_name)
            if template is None:
                template = {"templateid": templateid, "host": template_name, "name": template_name}
        templateid = template["templateid"]
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
        result = self.call("host.get", {"output": "extend", "filter": {"host": [hostname]}})
        return result[0] if result else None

    def ensure_host(
        self,
        hostname: str,
        visible_name: str,
        groupid: str,
        templateid: str,
        ip: str,
        tags: list[dict[str, str]],
    ) -> dict:
        existing = self.get_host(hostname)
        if existing:
            updates: dict[str, object] = {"hostid": existing["hostid"]}
            if existing.get("name") != visible_name:
                updates["name"] = visible_name
            if tags:
                existing_tags = existing.get("tags") or []
                existing_pairs = {(item.get("tag"), item.get("value")) for item in existing_tags}
                desired_pairs = {(item.get("tag"), item.get("value")) for item in tags}
                if not desired_pairs.issubset(existing_pairs):
                    updates["tags"] = tags
            if len(updates) > 1:
                self.call("host.update", updates)
                return self.get_host(hostname) or existing
            return existing
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
                "templates": [{"templateid": templateid}],
                "tags": tags,
            },
        )
        hostid = result["hostids"][0]
        return self.call("host.get", {"output": "extend", "hostids": hostid})[0]

    def get_image(self, name: str) -> dict | None:
        result = self.call("image.get", {"output": "extend", "filter": {"name": [name]}})
        return result[0] if result else None

    def get_map(self, name: str) -> dict | None:
        result = self.call("map.get", {"output": "extend", "selectSelements": "extend", "selectLinks": "extend", "filter": {"name": [name]}})
        return result[0] if result else None

    def create_or_update_map(self, params: dict[str, Any]) -> dict:
        existing = self.get_map(params["name"])
        if existing is None:
            result = self.call("map.create", params)
            sysmapid = result["sysmapids"][0]
            created = self.get_map(params["name"])
            if created is None:
                raise RuntimeError(f"Falha ao recuperar mapa criado: {params['name']}")
            return created
        params = {k: v for k, v in params.items() if k != "name"}
        params["sysmapid"] = existing["sysmapid"]
        self.call("map.update", params)
        updated = self.get_map(existing["name"])
        if updated is None:
            raise RuntimeError(f"Falha ao recuperar mapa atualizado: {existing['name']}")
        return updated
