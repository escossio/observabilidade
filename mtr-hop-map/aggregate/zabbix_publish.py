from __future__ import annotations

import json
from typing import Any

from src.config import load_config
from src.hop_policy import normalize_ip
from src.zabbix_api import ZabbixAPI


MAP_NAME = "MTR Backbone - Brisanet Observed"


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


def build_backbone_plan(aggregate: dict[str, Any]) -> dict[str, Any]:
    promoted = aggregate["promote"]
    backbone = promoted["promoted_nodes"]["backbone_observed"]
    candidates = promoted["promoted_nodes"]["candidate_nodes"]
    watchlist = promoted["promoted_nodes"]["watchlist_nodes"]
    backbone_edges = promoted["promoted_edges"]["backbone_observed"]
    candidate_edges = promoted["promoted_edges"]["candidate_edges"]
    canonical_path = promoted["canonical_path"]

    placements: list[dict[str, Any]] = []
    x = 40
    for idx, node in enumerate(backbone):
        placements.append({"ip": node["ip"], "role": node["role"], "x": x, "y": 130, "zindex": idx, "label": node["label"]})
        x += 155

    if candidates:
        candidate_edge = next((node for node in candidates if node["role"] == "edge_brisanet_candidate"), None)
    else:
        candidate_edge = None
    if candidate_edge:
        placements.append({"ip": candidate_edge["ip"], "role": candidate_edge["role"], "x": x, "y": 130, "zindex": len(placements), "label": candidate_edge["label"]})
        x += 155

    cdn_nodes = [node for node in candidates if node["role"] == "cdn_candidate"]
    for idx, node in enumerate(cdn_nodes):
        placements.append({"ip": node["ip"], "role": node["role"], "x": 40 + idx * 185, "y": 285, "zindex": 50 + idx, "label": node["label"]})

    for idx, node in enumerate(watchlist):
        placements.append({"ip": node["ip"], "role": node["role"], "x": 40 + idx * 185, "y": 410, "zindex": 60 + idx, "label": node["label"]})

    return {
        "map_name": MAP_NAME,
        "canonical_path": canonical_path,
        "promoted_nodes": promoted["promoted_nodes"],
        "promoted_edges": promoted["promoted_edges"],
        "placements": placements,
        "meta": promoted["meta"],
        "counts": {
            "backbone_nodes": len(backbone),
            "candidate_nodes": len(candidates),
            "watchlist_nodes": len(watchlist),
            "backbone_edges": len(backbone_edges),
            "candidate_edges": len(candidate_edges),
        },
    }


def publish_backbone_map(plan: dict[str, Any]) -> dict[str, Any]:
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

    existing = api.get_map(plan["map_name"])
    width = max(1600, 40 * 2 + max(1, len([node for node in plan["placements"] if node["y"] == 130]) - 1) * 155 + 96)
    height = 520

    if existing is None:
        api.call("map.create", _create_map_payload(plan["map_name"], width, height, selements))
        existing = api.get_map(plan["map_name"])
    else:
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
    for edge in plan["promoted_edges"]["backbone_observed"]:
        src = host_lookup.get(edge["source"])
        dst = host_lookup.get(edge["target"])
        if not src or not dst or src not in existing_by_hostid or dst not in existing_by_hostid:
            continue
        links.append(
            {
                "selementid1": existing_by_hostid[src]["selementid"],
                "selementid2": existing_by_hostid[dst]["selementid"],
                "drawtype": "2",
                "color": "00A651",
            }
        )
    for edge in plan["promoted_edges"]["candidate_edges"]:
        src = host_lookup.get(edge["source"])
        dst = host_lookup.get(edge["target"])
        if not src or not dst or src not in existing_by_hostid or dst not in existing_by_hostid:
            continue
        links.append(
            {
                "selementid1": existing_by_hostid[src]["selementid"],
                "selementid2": existing_by_hostid[dst]["selementid"],
                "drawtype": "2",
                "color": "E67E22",
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
