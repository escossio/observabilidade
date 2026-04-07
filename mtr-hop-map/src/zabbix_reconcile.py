from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import Config
from .hop_policy import build_identity
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


@dataclass(frozen=True)
class MapNode:
    hop: Hop
    element: dict[str, Any]
    hostid: str | None


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


def _build_placeholder_element(label: str, imageid: str, x: int, y: int, order: int) -> dict[str, Any]:
    return {
        "elementtype": 0,
        "iconid_off": imageid,
        "iconid_on": imageid,
        "iconid_disabled": imageid,
        "iconid_maintenance": imageid,
        "label": label,
        "label_location": -1,
        "x": str(x),
        "y": str(y),
        "width": "96",
        "height": "96",
        "viewtype": 0,
        "use_iconmap": 0,
        "evaltype": 0,
        "show_label": -1,
        "zindex": str(max(0, order - 1)),
        "urls": [],
    }


def _ordered_hops(hops: list[Hop]) -> list[Hop]:
    return sorted(hops, key=lambda hop: hop.order)


def _build_nodes(
    api: ZabbixAPI,
    config: Config,
    hops: list[Hop],
    imageid: str,
    host_groupid: str,
    templateid: str,
) -> tuple[list[MapNode], list[str], list[dict[str, Any]]]:
    layout = build_layout(len(hops), config.left_margin, config.top_margin, config.hop_spacing)
    nodes: list[MapNode] = []
    hostids: list[str] = []
    host_actions: list[dict[str, Any]] = []

    for hop, (x, y) in zip(_ordered_hops(hops), layout):
        if hop.category == "no-response" or not hop.ip or hop.ip in {"*", ""}:
            nodes.append(MapNode(hop=hop, element=_build_placeholder_element(hop.label, imageid, x, y, hop.order), hostid=None))
            continue

        identity = build_identity(hop)
        host_result: HostEnsureResult = api.ensure_host(
            hostname=identity.hostname,
            visible_name=identity.visible_name,
            groupid=host_groupid,
            templateid=templateid,
            ip=hop.ip,
            tags=identity.tags,
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


def ensure_map_for_destination(
    api: ZabbixAPI,
    config: Config,
    hops: list[Hop],
    run_dir: str | None = None,
) -> ReconcileResult:
    host_group = api.ensure_host_group(config.hop_group_name)
    template = api.ensure_icmp_template(config.icmp_template_name, config.icmp_template_group)
    image = api.get_image(config.map_icon_name)
    if image is None:
        raise RuntimeError(f"Imagem do mapa ausente: {config.map_icon_name}")

    map_name = f"{config.map_prefix}{config.target}"
    desired_nodes, _hostids, host_actions = _build_nodes(
        api,
        config,
        hops,
        image["imageid"],
        host_group["groupid"],
        template["templateid"],
    )
    existing_map = api.get_map(map_name)
    created_map = existing_map is None

    if existing_map is None:
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
                "selements": [node.element for node in desired_nodes],
            },
        )
        existing_map = api.get_map(map_name)
        if existing_map is None:
            raise RuntimeError(f"Falha ao recuperar mapa criado: {map_name}")

    existing_by_hostid: dict[str, str] = {}
    for selement in existing_map.get("selements", []):
        for element in selement.get("elements", []):
            if "hostid" in element:
                existing_by_hostid[element["hostid"]] = selement["selementid"]

    merged_selements = _merge_selements(existing_by_hostid, desired_nodes)
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
    if current_map is None:
        raise RuntimeError(f"Falha ao recuperar mapa atualizado: {map_name}")

    current_by_hostid: dict[str, dict[str, Any]] = {}
    for selement in current_map.get("selements", []):
        for element in selement.get("elements", []):
            if "hostid" in element:
                current_by_hostid[element["hostid"]] = selement
    ordered_current_selements = [current_by_hostid[node.hostid] for node in desired_nodes if node.hostid and node.hostid in current_by_hostid]

    links = _build_links(ordered_current_selements, current_map.get("links", []))
    if links:
        api.call("map.update", {"sysmapid": current_map["sysmapid"], "links": links})

    final_map = api.get_map(map_name)
    if final_map is None:
        raise RuntimeError(f"Falha ao recuperar mapa final: {map_name}")

    selementids = [se["selementid"] for se in final_map.get("selements", [])]
    final_hostids: list[str] = []
    for selement in final_map.get("selements", []):
        for element in selement.get("elements", []):
            if "hostid" in element:
                final_hostids.append(element["hostid"])
    linkids = [link["linkid"] for link in final_map.get("links", [])]

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
    )
