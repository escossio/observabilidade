from __future__ import annotations

import json
from typing import Any

from src.config import load_config
from src.hop_policy import normalize_ip
from src.zabbix_api import ZabbixAPI


UNIFIED_MAP_NAME = "MTR Unified - Brisanet Observed"
LEGACY_MAP_NAME = "MTR Backbone - Brisanet Observed"


def _resolve_image(api: ZabbixAPI, names: list[str], fallback: str | None = None) -> dict[str, Any]:
    for name in names:
        image = api.get_image(name)
        if image is not None:
            return image
    if fallback:
        image = api.get_image(fallback)
        if image is not None:
            return image
    raise RuntimeError(f"Imagens do mapa ausentes: {names}")


def _resolve_host(api: ZabbixAPI, ip: str, groupid: str) -> dict[str, Any] | None:
    hostname = f"hop-ip-{normalize_ip(ip)}"
    host = api.get_host(hostname)
    if host:
        return host
    candidates = api.get_hosts_by_ip(ip, groupid)
    if candidates:
        return candidates[0]
    return None


def _label_for(role: str, row: dict[str, Any]) -> str:
    if role == "backbone_observed":
        return f"{row['ip']}\nbackbone observed\nruns {row['run_count']}/{row['target_count']}"
    if role == "edge_brisanet_candidate":
        return f"{row['ip']}\n[candidate]\nedge {row['edge_count']} conf {row['confidence']}"
    if role == "cdn_candidate":
        return f"{row['ip']}\nCDN candidate\n{row['company']}\nconf {row['confidence']}"
    if role == "dns_watchlist":
        return f"{row['ip']}\nDNS watchlist\nconf {row['confidence']}"
    return row["ip"]


def _image_for(role: str) -> str:
    return {
        "backbone_observed": "Server_(96)",
        "edge_brisanet_candidate": "Router_(96)",
        "cdn_candidate": "Cloud_(96)",
        "dns_watchlist": "Notebook_(96)",
    }.get(role, "Server_(96)")


def _build_element(imageid: str, x: int, y: int, label: str, hostid: str | None, zindex: int) -> dict[str, Any]:
    element = {
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
        "zindex": str(zindex),
        "urls": [],
    }
    if hostid:
        element["elements"] = [{"hostid": hostid}]
    return element


def _create_map_payload(name: str, width: int, height: int, selements: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": name,
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
        "selements": selements,
    }


def _node_for_plan(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "ip": node["ip"],
        "role": node["role"],
        "class_name": node["class_name"],
        "label": node["label"],
        "company": node["company"],
        "confidence": node["confidence"],
        "evidence": node["evidence"],
        "observations": node["observations"],
        "target_count": node["target_count"],
        "run_count": node["run_count"],
        "recurrence_ratio": node["recurrence_ratio"],
        "edge_count": node["edge_count"],
        "last_internal_count": node["last_internal_count"],
    }


def _class_role(class_name: str) -> str:
    return {
        "internal_brisanet": "backbone_observed",
        "edge_brisanet_candidate": "edge_brisanet_candidate",
        "cdn_candidate": "cdn_candidate",
        "dns_infra_candidate": "dns_watchlist",
        "destination": "destination",
        "unknown": "unknown",
        "ix_ptt_candidate": "ix_ptt_candidate",
    }.get(class_name, "unknown")


def _image_role(role: str) -> str:
    return {
        "backbone_observed": "backbone_observed",
        "edge_brisanet_candidate": "edge_brisanet_candidate",
        "cdn_candidate": "cdn_candidate",
        "dns_watchlist": "dns_watchlist",
        "destination": "backbone_observed",
        "unknown": "backbone_observed",
        "ix_ptt_candidate": "cdn_candidate",
    }.get(role, "backbone_observed")


def _branch_paths(aggregate: dict[str, Any]) -> list[list[str]]:
    canonical = tuple(aggregate["promote"]["canonical_path"])
    paths = []
    for path, count in aggregate["path_counter"].items():
        if tuple(path) == canonical:
            continue
        if count <= 0:
            continue
        paths.append(list(path))
    paths.sort(key=lambda path: (-len(path), path))
    return paths


def _common_prefix_len(left: list[str], right: list[str]) -> int:
    length = 0
    for l, r in zip(left, right):
        if l != r:
            break
        length += 1
    return length


def build_unified_plan(aggregate: dict[str, Any]) -> dict[str, Any]:
    promoted = aggregate["promote"]
    backbone = promoted["promoted_nodes"]["backbone_observed"]
    candidates = promoted["promoted_nodes"]["candidate_nodes"]
    watchlist = promoted["promoted_nodes"]["watchlist_nodes"]
    backbone_edges = promoted["promoted_edges"]["backbone_observed"]
    candidate_edges = promoted["promoted_edges"]["candidate_edges"]
    canonical_path = promoted["canonical_path"]
    inventory = {row["ip"]: row for row in aggregate["inventory"]}
    branch_paths = _branch_paths(aggregate)

    node_by_ip: dict[str, dict[str, Any]] = {}
    edge_by_pair: dict[tuple[str, str], dict[str, Any]] = {}

    def add_node(ip: str, role: str | None = None) -> None:
        if ip in node_by_ip:
            return
        row = inventory.get(ip, {})
        classification = row.get("classification", {})
        label = row.get("ip", ip)
        if role == "backbone_observed" and row:
            label = f"{ip}\nbackbone observed\nruns {row['run_count']}/{row['target_count']}"
        elif role == "edge_brisanet_candidate" and row:
            label = f"{ip}\n[candidate]\nedge {row['edge_count']} conf {classification.get('confidence', 'low')}"
        elif role == "cdn_candidate" and row:
            label = f"{ip}\nCDN candidate\n{row['company']}\nconf {classification.get('confidence', 'low')}"
        elif role == "dns_watchlist" and row:
            label = f"{ip}\nDNS watchlist\nconf {classification.get('confidence', 'low')}"
        elif role == "destination" and row:
            label = f"{ip}\n{row['company']}\ndestination"
        elif role == "unknown" and row:
            label = f"{ip}\nunknown"
        elif row and row.get("hostname") and row.get("company"):
            label = f"{ip}\n{row['company']}"
        node_by_ip[ip] = {
            "ip": ip,
            "role": role or _class_role(classification.get("primary_class", "unknown")),
            "class_name": classification.get("primary_class", "unknown"),
            "label": label,
            "company": row.get("company", "Unknown"),
            "confidence": classification.get("confidence", "low"),
            "evidence": classification.get("evidence", []),
            "observations": row.get("observations", 0),
            "target_count": row.get("target_count", 0),
            "run_count": row.get("run_count", 0),
            "recurrence_ratio": row.get("recurrence_ratio", 0.0),
            "edge_count": row.get("edge_count", 0),
            "last_internal_count": row.get("last_internal_count", 0),
        }

    def add_edge(source: str, target: str, role: str | None = None, label: str | None = None) -> None:
        key = (source, target)
        if key in edge_by_pair:
            return
        src_row = inventory.get(source, {})
        dst_row = inventory.get(target, {})
        classification = dst_row.get("classification", {})
        edge_by_pair[key] = {
            "source": source,
            "target": target,
            "role": role or classification.get("primary_class", "unknown"),
            "label": label or f"{source} -> {target}",
            "confidence": classification.get("confidence", "low"),
            "evidence": classification.get("evidence", []),
            "observations": min(src_row.get("observations", 0), dst_row.get("observations", 0)) if src_row and dst_row else 0,
            "target_count": min(src_row.get("target_count", 0), dst_row.get("target_count", 0)) if src_row and dst_row else 0,
            "run_count": min(src_row.get("run_count", 0), dst_row.get("run_count", 0)) if src_row and dst_row else 0,
            "stability_ratio": min(src_row.get("recurrence_ratio", 0.0), dst_row.get("recurrence_ratio", 0.0)) if src_row and dst_row else 0.0,
        }

    for path in [canonical_path] + branch_paths:
        for ip in path:
            row = inventory.get(ip)
            role = None
            if row:
                class_name = row.get("classification", {}).get("primary_class", "unknown")
                role = _class_role(class_name)
                if ip in {node["ip"] for node in backbone}:
                    role = "backbone_observed"
                elif ip in {node["ip"] for node in candidates}:
                    role = _class_role(class_name)
                elif ip in {node["ip"] for node in watchlist}:
                    role = "dns_watchlist"
            add_node(ip, role)
        for left, right in zip(path, path[1:]):
            left_role = node_by_ip.get(left, {}).get("role")
            right_role = node_by_ip.get(right, {}).get("role")
            edge_role = "backbone_observed" if left in canonical_path and right in canonical_path else "branch"
            if right_role == "edge_brisanet_candidate":
                edge_role = "candidate_edge"
            elif right_role == "cdn_candidate":
                edge_role = "cdn_exit"
            elif right_role == "destination":
                edge_role = "destination_edge"
            add_edge(left, right, edge_role)

    unified_nodes = list(node_by_ip.values())
    unified_nodes.sort(key=lambda node: (
        0 if node["role"] == "backbone_observed" else 1 if node["role"] == "edge_brisanet_candidate" else 2 if node["role"] == "cdn_candidate" else 3 if node["role"] == "destination" else 4,
        node["ip"],
    ))
    unified_edges = list(edge_by_pair.values())
    unified_edges.sort(key=lambda edge: (edge["source"], edge["target"]))

    placements: list[dict[str, Any]] = []
    trunk_positions = {ip: (40 + idx * 155, 120) for idx, ip in enumerate(canonical_path)}
    for idx, ip in enumerate(canonical_path):
        node = node_by_ip.get(ip)
        if not node:
            continue
        placements.append({"ip": ip, "role": node["role"], "x": trunk_positions[ip][0], "y": trunk_positions[ip][1], "zindex": idx, "label": node["label"]})

    branch_index = 0
    for path in branch_paths:
        split = _common_prefix_len(list(canonical_path), path)
        anchor_ip = canonical_path[max(0, split - 1)] if split else canonical_path[0]
        anchor_x, _anchor_y = trunk_positions.get(anchor_ip, (40, 120))
        branch_y = 280 + branch_index * 120
        branch_index += 1
        x = anchor_x
        for offset, ip in enumerate(path[split:]):
            node = node_by_ip.get(ip)
            if not node:
                continue
            if ip in trunk_positions:
                x, _ = trunk_positions[ip]
                continue
            x += 155 if offset > 0 else 155
            placements.append({"ip": ip, "role": node["role"], "x": x, "y": branch_y, "zindex": 40 + branch_index * 10 + offset, "label": node["label"]})

    return {
        "map_name": UNIFIED_MAP_NAME,
        "legacy_map_name": LEGACY_MAP_NAME,
        "canonical_path": canonical_path,
        "promoted_nodes": promoted["promoted_nodes"],
        "promoted_edges": promoted["promoted_edges"],
        "unified_nodes": unified_nodes,
        "unified_edges": unified_edges,
        "placements": placements,
        "meta": promoted["meta"],
        "counts": {
            "backbone_nodes": len(backbone),
            "candidate_nodes": len(candidates),
            "watchlist_nodes": len(watchlist),
            "backbone_edges": len(backbone_edges),
            "candidate_edges": len(candidate_edges),
            "unified_nodes": len(unified_nodes),
            "unified_edges": len(unified_edges),
        },
    }


def publish_unified_map(plan: dict[str, Any]) -> dict[str, Any]:
    config = load_config("aggregate")
    api = ZabbixAPI(config.zabbix_api_url, config.zabbix_user, config.zabbix_password)
    api.login()

    group = api.get_host_group(config.hop_group_name)
    if not group:
        raise RuntimeError(f"Grupo ausente para publicação: {config.hop_group_name}")

    images = {
        "backbone_observed": _resolve_image(api, ["Server_(96)", "Router_(96)"], fallback=config.map_icon_name),
        "edge_brisanet_candidate": _resolve_image(api, ["Router_(96)", "Server_(96)"], fallback=config.map_icon_name),
        "cdn_candidate": _resolve_image(api, ["Cloud_(96)", "Server_(96)"], fallback=config.map_icon_name),
        "dns_watchlist": _resolve_image(api, ["Notebook_(96)", "Server_(96)"], fallback=config.map_icon_name),
        "destination": _resolve_image(api, ["Server_(96)", "Router_(96)"], fallback=config.map_icon_name),
        "unknown": _resolve_image(api, ["Server_(96)", "Router_(96)"], fallback=config.map_icon_name),
        "ix_ptt_candidate": _resolve_image(api, ["Cloud_(96)", "Router_(96)"], fallback=config.map_icon_name),
    }

    selements: list[dict[str, Any]] = []
    host_lookup: dict[str, str] = {}
    skipped: list[dict[str, Any]] = []
    for placement in plan["placements"]:
        role = placement["role"]
        ip = placement["ip"]
        host = _resolve_host(api, ip, group["groupid"])
        if host is None:
            skipped.append({"ip": ip, "role": role, "reason": "host_not_found"})
            continue
        host_lookup[ip] = host["hostid"]
        selements.append(_build_element(images[role]["imageid"], placement["x"], placement["y"], placement["label"], host["hostid"], placement["zindex"]))

    existing = api.get_map(plan["map_name"]) or api.get_map(plan.get("legacy_map_name", ""))
    width = max(1900, 40 * 2 + max(1, len([node for node in plan["placements"] if node["y"] == 120]) - 1) * 155 + 96)
    height = 560

    if existing is None:
        api.call("map.create", _create_map_payload(plan["map_name"], width, height, selements))
        existing = api.get_map(plan["map_name"])
    else:
        if existing.get("name") != plan["map_name"]:
            api.call("map.update", {"sysmapid": existing["sysmapid"], "name": plan["map_name"]})
            existing = api.get_map(plan["map_name"]) or existing
        existing_by_hostid: dict[str, str] = {}
        for selement in existing.get("selements", []):
            for element in selement.get("elements", []):
                if "hostid" in element:
                    existing_by_hostid[element["hostid"]] = selement["selementid"]
        merged = []
        for element in selements:
            element = dict(element)
            if element.get("elements"):
                hostid = element["elements"][0]["hostid"]
                if hostid in existing_by_hostid:
                    element["selementid"] = existing_by_hostid[hostid]
            merged.append(element)
        api.call("map.update", {"sysmapid": existing["sysmapid"], "width": str(width), "height": str(height), "selements": merged})
        existing = api.get_map(plan["map_name"])

    if existing is None:
        raise RuntimeError(f"Falha ao criar/atualizar mapa agregado: {plan['map_name']}")

    existing_by_hostid: dict[str, dict[str, Any]] = {}
    for selement in existing.get("selements", []):
        for element in selement.get("elements", []):
            if "hostid" in element:
                existing_by_hostid[element["hostid"]] = selement

    links: list[dict[str, Any]] = []
    for edge in plan["unified_edges"]:
        src = host_lookup.get(edge["source"])
        dst = host_lookup.get(edge["target"])
        if not src or not dst or src not in existing_by_hostid or dst not in existing_by_hostid:
            continue
        edge_color = {
            "backbone_observed": "00A651",
            "candidate_edge": "E67E22",
            "cdn_exit": "7F8C8D",
            "destination_edge": "2980B9",
            "branch": "5B6B7A",
        }.get(edge["role"], "5B6B7A")
        links.append(
            {
                "selementid1": existing_by_hostid[src]["selementid"],
                "selementid2": existing_by_hostid[dst]["selementid"],
                "drawtype": "2",
                "color": edge_color,
            }
        )

    if links:
        api.call("map.update", {"sysmapid": existing["sysmapid"], "links": links})
        existing = api.get_map(plan["map_name"])

    snapshot = {
        "sysmapid": existing["sysmapid"],
        "map_name": existing["name"],
        "selement_count": len(existing.get("selements", [])),
        "link_count": len(existing.get("links", [])),
        "host_lookup": host_lookup,
        "skipped": skipped,
    }
    return snapshot


def build_backbone_plan(aggregate: dict[str, Any]) -> dict[str, Any]:
    return build_unified_plan(aggregate)


def publish_backbone_map(plan: dict[str, Any]) -> dict[str, Any]:
    return publish_unified_map(plan)
