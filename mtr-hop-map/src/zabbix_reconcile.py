from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import Config
from .hop_policy import build_identity, classify_hop_role, monitoring_mode_for_role, slugify
from .map_layout import build_layout, compute_map_size
from .mtr_parser import Hop
from .zabbix_api import HostEnsureResult, ZabbixAPI


@dataclass(frozen=True)
class ReconcileResult:
    target: str
    map_name: str
    sysmapid: str
    host_groupid: str
    templateid: str
    hostids: list[str]
    selementids: list[str]
    linkids: list[str]
    created_map: bool
    host_actions: list[dict[str, Any]]
    plan: dict[str, Any] | None = None


@dataclass(frozen=True)
class MapNode:
    hop: Hop
    element: dict[str, Any]
    hostid: str | None


@dataclass(frozen=True)
class MapDiff:
    current_map: dict[str, Any] | None
    desired_map_name: str
    desired_nodes: list[MapNode]
    current_hostids: list[str]
    desired_hostids: list[str]
    host_actions: list[dict[str, Any]]
    selement_reuse: list[dict[str, Any]]
    selement_create: list[dict[str, Any]]
    selement_detach: list[dict[str, Any]]
    link_reuse: list[dict[str, Any]]
    link_create: list[dict[str, Any]]
    link_detach: list[dict[str, Any]]
    map_actions: list[dict[str, Any]]
    counters: dict[str, int]


def _map_label(hop: Hop) -> str:
    return hop.label


def _build_host_element(
    hop: Hop,
    imageid: str,
    x: int,
    y: int,
    hostid: str,
) -> dict[str, Any]:
    return {
        "elementtype": 0,
        "iconid_off": imageid,
        "iconid_on": imageid,
        "iconid_disabled": imageid,
        "iconid_maintenance": imageid,
        "label": _map_label(hop),
        "label_location": -1,
        "x": str(x),
        "y": str(y),
        "width": "96",
        "height": "96",
        "viewtype": 0,
        "use_iconmap": 0,
        "evaltype": 0,
        "show_label": -1,
        "zindex": str(max(0, hop.order - 1)),
        "elements": [{"hostid": hostid}],
        "urls": [],
    }


def _ordered_hops(hops: list[Hop]) -> list[Hop]:
    return sorted(hops, key=lambda hop: hop.order)


def _mapable_hops(hops: list[Hop]) -> list[Hop]:
    return [hop for hop in _ordered_hops(hops) if hop.category != "no-response" and hop.ip not in {"", "*"}]


def _build_nodes(
    api: ZabbixAPI,
    config: Config,
    hops: list[Hop],
    imageid: str,
    host_groupid: str,
    templateid: str,
) -> tuple[list[MapNode], list[str], list[dict[str, Any]]]:
    nodes: list[MapNode] = []
    hostids: list[str] = []
    host_actions: list[dict[str, Any]] = []

    mapable_hops = _mapable_hops(hops)
    destination_ip = mapable_hops[-1].ip if mapable_hops else None
    layout = build_layout(len(mapable_hops), config.left_margin, config.top_margin, config.hop_spacing)

    for hop, (x, y) in zip(mapable_hops, layout):

        identity = build_identity(hop)
        role = classify_hop_role(hop, destination_ip)
        template_mode = monitoring_mode_for_role(role)
        host_result: HostEnsureResult = api.ensure_host(
            hostname=identity.hostname,
            visible_name=identity.visible_name,
            groupid=host_groupid,
            templateid=templateid,
            ip=hop.ip,
            tags=identity.tags,
            template_mode=template_mode,
        )
        hostid = host_result.host["hostid"]
        hostids.append(hostid)
        host_actions.append(
            {
                "ip": hop.ip,
                "hostid": hostid,
                "hostname": host_result.host["host"],
                "action": host_result.action,
                "match_source": host_result.match_source,
                "warnings": host_result.warnings,
            }
        )
        nodes.append(MapNode(hop=hop, element=_build_host_element(hop, imageid, x, y, hostid), hostid=hostid))

    return nodes, hostids, host_actions


def _plan_nodes(
    api: ZabbixAPI,
    config: Config,
    hops: list[Hop],
    imageid: str,
    host_groupid: str,
    templateid: str,
) -> tuple[list[MapNode], list[str], list[dict[str, Any]]]:
    nodes: list[MapNode] = []
    hostids: list[str] = []
    host_actions: list[dict[str, Any]] = []

    mapable_hops = _mapable_hops(hops)
    destination_ip = mapable_hops[-1].ip if mapable_hops else None
    layout = build_layout(len(mapable_hops), config.left_margin, config.top_margin, config.hop_spacing)

    for hop, (x, y) in zip(mapable_hops, layout):

        identity = build_identity(hop)
        role = classify_hop_role(hop, destination_ip)
        template_mode = monitoring_mode_for_role(role)
        host_result: HostEnsureResult = api.plan_host(
            hostname=identity.hostname,
            visible_name=identity.visible_name,
            groupid=host_groupid,
            templateid=templateid,
            ip=hop.ip,
            tags=identity.tags,
            template_mode=template_mode,
        )
        hostid = host_result.host.get("hostid") if host_result.host else None
        if hostid:
            hostids.append(str(hostid))
        host_actions.append(
            {
                "ip": hop.ip,
                "hostid": hostid,
                "hostname": host_result.host.get("host") if host_result.host else identity.hostname,
                "action": host_result.action,
                "match_source": host_result.match_source,
                "warnings": host_result.warnings,
                "planned": True,
            }
        )
        nodes.append(MapNode(hop=hop, element=_build_host_element(hop, imageid, x, y, str(hostid or "planned")), hostid=str(hostid) if hostid else None))

    return nodes, hostids, host_actions


def _merge_selements(existing_by_hostid: dict[str, str], desired_nodes: list[MapNode]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for node in desired_nodes:
        element = dict(node.element)
        if node.hostid and node.hostid in existing_by_hostid:
            element["selementid"] = existing_by_hostid[node.hostid]
        merged.append(element)
    return merged


def _build_links(selements: list[dict[str, Any]], existing_links: list[dict[str, Any]]) -> list[dict[str, str]]:
    existing_pairs = {
        (link.get("selementid1"), link.get("selementid2")): link.get("linkid")
        for link in existing_links
        if link.get("selementid1") and link.get("selementid2")
    }
    links: list[dict[str, str]] = []
    ordered = [se for se in selements if se.get("selementid")]
    for left, right in zip(ordered, ordered[1:]):
        payload = {
            "selementid1": left["selementid"],
            "selementid2": right["selementid"],
            "drawtype": "2",
            "color": "00AA00",
        }
        linkid = existing_pairs.get((left["selementid"], right["selementid"]))
        if linkid:
            payload["linkid"] = linkid
        links.append(payload)
    return links


def _compare_map(
    current_map: dict[str, Any] | None,
    desired_nodes: list[MapNode],
    current_by_hostid: dict[str, dict[str, Any]],
) -> MapDiff:
    existing_hostids = set(current_by_hostid.keys())
    desired_hostids = [node.hostid for node in desired_nodes if node.hostid]
    desired_hostid_set = set(desired_hostids)

    selement_reuse: list[dict[str, Any]] = []
    selement_create: list[dict[str, Any]] = []
    selement_detach: list[dict[str, Any]] = []
    for node in desired_nodes:
        if node.hostid and node.hostid in existing_hostids:
            selement_reuse.append({"hostid": node.hostid, "status": "reuse"})
        elif node.hostid:
            selement_create.append({"hostid": node.hostid, "status": "create"})
        else:
            selement_create.append({"hostid": None, "status": "create-placeholder"})

    for hostid, selement in current_by_hostid.items():
        if hostid not in desired_hostid_set:
            selement_detach.append({"hostid": hostid, "selementid": selement["selementid"], "status": "detach-from-map"})

    current_link_pairs = {}
    current_links = current_map.get("links", []) if current_map else []
    for link in current_links:
        if link.get("selementid1") and link.get("selementid2"):
            current_link_pairs[(link["selementid1"], link["selementid2"])] = link

    ordered_current = [current_by_hostid[node.hostid] for node in desired_nodes if node.hostid and node.hostid in current_by_hostid]
    desired_links = _build_links(ordered_current, current_links)
    link_reuse: list[dict[str, Any]] = []
    link_create: list[dict[str, Any]] = []
    for link in desired_links:
        if "linkid" in link:
            link_reuse.append({"linkid": link["linkid"], "status": "reuse", **link})
        else:
            link_create.append({"status": "create", **link})

    desired_link_pairs = {(link["selementid1"], link["selementid2"]) for link in desired_links}
    link_detach = []
    for pair, link in current_link_pairs.items():
        if pair not in desired_link_pairs:
            link_detach.append({"linkid": link["linkid"], "status": "detach-from-map", **link})

    map_actions = []
    if current_map is None:
        map_actions.append({"action": "create", "map_name": None})
    else:
        map_actions.append({"action": "update", "sysmapid": current_map["sysmapid"]})

    counters = {
        "host_reuse": len([row for row in desired_nodes if row.hostid and row.hostid in existing_hostids]),
        "host_create": len([row for row in desired_nodes if row.hostid and row.hostid not in existing_hostids]),
        "host_detach": len(selement_detach),
        "link_reuse": len(link_reuse),
        "link_create": len(link_create),
        "link_detach": len(link_detach),
    }
    return MapDiff(
        current_map=current_map,
        desired_map_name="",
        desired_nodes=desired_nodes,
        current_hostids=sorted(existing_hostids),
        desired_hostids=desired_hostids,
        host_actions=[],
        selement_reuse=selement_reuse,
        selement_create=selement_create,
        selement_detach=selement_detach,
        link_reuse=link_reuse,
        link_create=link_create,
        link_detach=link_detach,
        map_actions=map_actions,
        counters=counters,
    )


def ensure_map_for_destination(
    api: ZabbixAPI,
    config: Config,
    hops: list[Hop],
    run_dir: str | None = None,
    dry_run: bool = False,
) -> ReconcileResult:
    host_group = api.ensure_host_group(config.hop_group_name)
    template = api.ensure_icmp_template(config.icmp_template_name, config.icmp_template_group)
    image = api.get_image(config.map_icon_name)
    if image is None:
        raise RuntimeError(f"Imagem do mapa ausente: {config.map_icon_name}")

    map_name = f"{config.map_prefix}{config.target}"
    existing_map = api.get_map(map_name)
    created_map = existing_map is None
    if dry_run:
        desired_nodes, _hostids, host_actions = _plan_nodes(
            api,
            config,
            hops,
            image["imageid"],
            host_group.get("groupid"),
            template.get("templateid"),
        )
    else:
        desired_nodes, _hostids, host_actions = _build_nodes(
            api,
            config,
            hops,
            image["imageid"],
            host_group["groupid"],
            template["templateid"],
        )

    if existing_map is None and not dry_run:
        width, height = compute_map_size(len(hops), config.left_margin, config.hop_spacing, config.icon_size, config.map_height)
        api.call(
            "map.create",
            {
                "name": map_name,
                "width": str(width),
                "height": str(height),
                "backgroundid": "0",
                "label_type": "0",
                "label_location": "0",
                "highlight": "1",
                "expandproblem": "1",
                "markelements": "0",
                "show_unack": "0",
                "grid_size": "50",
                "grid_show": "1",
                "grid_align": "1",
                "label_format": "0",
                "label_type_host": "2",
                "label_type_hostgroup": "2",
                "label_type_trigger": "2",
                "label_type_map": "2",
                "label_type_image": "2",
                "label_string_host": "",
                "label_string_hostgroup": "",
                "label_string_trigger": "",
                "label_string_map": "",
                "label_string_image": "",
                "iconmapid": "0",
                "expand_macros": "1",
                "severity_min": "0",
                "private": "1",
                "show_suppressed": "0",
                "background_scale": "1",
                "show_element_label": "1",
                "show_link_label": "0",
            },
        )
        existing_map = api.get_map(map_name)
        if existing_map is None:
            raise RuntimeError(f"Falha ao recuperar mapa criado: {map_name}")
    elif existing_map is None and dry_run:
        existing_map = {
            "sysmapid": None,
            "name": map_name,
            "selements": [],
            "links": [],
        }

    existing_by_hostid: dict[str, str] = {}
    for selement in existing_map.get("selements", []):
        for element in selement.get("elements", []):
            if "hostid" in element:
                existing_by_hostid[element["hostid"]] = selement["selementid"]

    merged_selements = _merge_selements(existing_by_hostid, desired_nodes)
    if not dry_run:
        api.call(
            "map.update",
            {
                "sysmapid": existing_map["sysmapid"],
                "width": str(compute_map_size(len(hops), config.left_margin, config.hop_spacing, config.icon_size, config.map_height)[0]),
                "height": str(config.map_height),
                "selements": merged_selements,
            },
        )

    current_map = api.get_map(map_name)
    if current_map is None and not dry_run:
        raise RuntimeError(f"Falha ao recuperar mapa atualizado: {map_name}")
    if current_map is None and dry_run:
        current_map = existing_map

    current_by_hostid: dict[str, dict[str, Any]] = {}
    for selement in current_map.get("selements", []):
        for element in selement.get("elements", []):
            if "hostid" in element:
                current_by_hostid[element["hostid"]] = selement
    ordered_current_selements = [current_by_hostid[node.hostid] for node in desired_nodes if node.hostid and node.hostid in current_by_hostid]

    links = _build_links(ordered_current_selements, current_map.get("links", []))
    if links and not dry_run:
        api.call("map.update", {"sysmapid": current_map["sysmapid"], "links": links})

    final_map = api.get_map(map_name) if not dry_run else current_map
    if final_map is None:
        raise RuntimeError(f"Falha ao recuperar mapa final: {map_name}")

    selementids = [se["selementid"] for se in final_map.get("selements", []) if se.get("selementid")]
    final_hostids: list[str] = []
    for selement in final_map.get("selements", []):
        for element in selement.get("elements", []):
            if "hostid" in element:
                final_hostids.append(element["hostid"])
    linkids = [link["linkid"] for link in final_map.get("links", []) if link.get("linkid")]

    plan = None
    if dry_run:
        desired_hostids = [node.hostid for node in desired_nodes if node.hostid]
        current_hostids = [hostid for hostid in final_hostids if hostid]
        current_link_pairs = {(link["selementid1"], link["selementid2"]): link for link in current_map.get("links", []) if link.get("selementid1") and link.get("selementid2")}
        desired_links_plan: list[dict[str, Any]] = []
        for left, right in zip(desired_nodes, desired_nodes[1:]):
            desired_links_plan.append(
                {
                    "left": left.hop.order,
                    "right": right.hop.order,
                    "left_hostid": left.hostid,
                    "right_hostid": right.hostid,
                    "status": "reuse" if left.hostid and right.hostid and left.hostid in current_by_hostid and right.hostid in current_by_hostid else "create",
                }
            )
        desired_link_pairs = {
            (current_by_hostid[left.hostid]["selementid"], current_by_hostid[right.hostid]["selementid"])
            for left, right in zip(desired_nodes, desired_nodes[1:])
            if left.hostid and right.hostid and left.hostid in current_by_hostid and right.hostid in current_by_hostid
        }
        plan = {
            "target": config.target,
            "map_name": map_name,
            "dry_run": True,
            "current_map": {
                "sysmapid": current_map.get("sysmapid"),
                "name": current_map.get("name"),
                "selementids": [se.get("selementid") for se in current_map.get("selements", []) if se.get("selementid")],
                "hostids": current_hostids,
                "linkids": [link.get("linkid") for link in current_map.get("links", []) if link.get("linkid")],
            },
            "predicted_actions": {
                "hosts": {
                    "create": [row for row in host_actions if row["action"] == "planned-create"],
                    "reuse": [row for row in host_actions if row["action"] == "planned-reuse"],
                    "update": [row for row in host_actions if row["action"] == "planned-update"],
                },
                "selements": {
                    "reuse": [row for row in host_actions if row["action"] in {"planned-reuse", "planned-update"}],
                    "create": [row for row in host_actions if row["action"] == "planned-create"],
                    "detach_from_map": [hostid for hostid in current_hostids if hostid not in desired_hostids],
                    "keep": [hostid for hostid in current_hostids if hostid in desired_hostids],
                },
                "links": {
                    "reuse": [link for link in desired_links_plan if link["status"] == "reuse"],
                    "create": [link for link in desired_links_plan if link["status"] == "create"],
                    "detach_from_map": [
                        {"linkid": link["linkid"], "selementid1": a, "selementid2": b}
                        for (a, b), link in current_link_pairs.items()
                        if (a, b) not in desired_link_pairs
                    ],
                    "keep": [link for link in desired_links_plan if link["status"] == "reuse"],
                },
                "metadata": {
                    "source": "mtr-hop-map",
                    "target": config.target,
                    "target_slug": slugify(config.target),
                    "mode": "dry-run",
                    "last_trace": run_dir or "",
                },
            },
            "counters": {
                "host_create": len([row for row in host_actions if row["action"] == "planned-create"]),
                "host_reuse": len([row for row in host_actions if row["action"] == "planned-reuse"]),
                "host_update": len([row for row in host_actions if row["action"] == "planned-update"]),
                "host_detach": len([hostid for hostid in current_hostids if hostid not in desired_hostids]),
                "link_create": len([link for link in links if not link.get("linkid")]),
                "link_reuse": len([link for link in links if link.get("linkid")]),
                "link_detach": len([1 for (a, b) in current_link_pairs if (a, b) not in desired_link_pairs]),
            },
        }

    return ReconcileResult(
        target=config.target,
        map_name=map_name,
        sysmapid=final_map["sysmapid"],
        host_groupid=host_group["groupid"],
        templateid=template["templateid"],
        hostids=final_hostids,
        selementids=selementids,
        linkids=linkids,
        created_map=created_map,
        host_actions=host_actions,
        plan=plan,
    )
