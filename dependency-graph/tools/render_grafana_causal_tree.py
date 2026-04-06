#!/usr/bin/env python3
"""Render and optionally publish the causal tree panel with runtime state."""

from __future__ import annotations

import argparse
import base64
import json
import time
import urllib.request
from pathlib import Path

import yaml

ROOT = Path("/srv/observabilidade-zabbix")
GRAFANA_PASSWORD_FILE = ROOT / "backups" / "20260404-grafana-login" / "grafana_admin_password.secret"
GRAFANA_DASHBOARD_UID = "observabilidade-grafana"
GRAFANA_PANEL_ID = 26
GRAFANA_URL = "http://127.0.0.1:3000"
GRAFANA_HOST = "observabilidade.escossio.dev.br"
GRAFANA_STATIC_SVG_DIR = Path("/usr/share/grafana/public/img/observabilidade-zabbix")
GRAFANA_STATIC_SVG_FILE = GRAFANA_STATIC_SVG_DIR / "causal-tree-state.svg"
GRAFANA_STATIC_SVG_URL_PATH = "/public/img/observabilidade-zabbix/causal-tree-state.svg"
ZABBIX_DS_FILE = Path("/etc/grafana/provisioning/datasources/zabbix.yml")
ZABBIX_API_URL = "http://127.0.0.1:8081/api_jsonrpc.php"
STALE_SECONDS = 900

STATE_UP = "up"
STATE_DOWN = "down"
STATE_WARN = "warn"
STATE_UNKNOWN = "unknown"

NODE_RULES = {
    "agt01": {"mode": "single", "itemids": ["69621"], "role": "service"},
    "br0": {"mode": "none", "role": "transport"},
    "apache2": {"mode": "single", "itemids": ["69485"], "role": "service"},
    "cloudflared": {"mode": "single", "itemids": ["69618"], "role": "service"},
    "unbound": {"mode": "single", "itemids": ["69486"], "role": "service"},
    "grafana-server": {"mode": "single", "itemids": ["69617"], "role": "service"},
    "zabbix-server": {"mode": "single", "itemids": ["69615"], "role": "service"},
    "zabbix-agent2": {"mode": "single", "itemids": ["69616"], "role": "service"},
    "postgresql": {"mode": "single", "itemids": ["69619"], "role": "service"},
    "ssh": {"mode": "single", "itemids": ["69620"], "role": "service"},
    "mikrotik-rb3011": {"mode": "single", "itemids": ["69657"], "role": "service"},
    "bridge": {"mode": "ifstatus", "itemids": ["69690"], "role": "transport"},
    "ether1": {"mode": "ifstatus", "itemids": ["69692"], "role": "transport"},
    "pppoe-out1": {"mode": "ifstatus", "itemids": ["69701"], "role": "transport"},
    "wg0": {"mode": "ifstatus", "itemids": ["69689"], "role": "aux"},
    "public-ip": {"mode": "none", "role": "transport"},
    "brisanet": {"mode": "none", "role": "transport"},
    "livecopilot": {
        "mode": "aggregate",
        "depends_on": ["frontend-publico", "cloudflared-livecopilot", "apache-edge", "backend-fastapi"],
        "role": "service",
    },
    "frontend-publico": {"mode": "single", "itemids": ["69633"], "role": "service"},
    "cloudflared-livecopilot": {"mode": "none", "role": "service"},
    "apache-edge": {"mode": "single", "itemids": ["69632"], "role": "transport"},
    "backend-fastapi": {"mode": "aggregate", "itemids": ["69635", "69636", "69637"], "role": "service"},
}

ITEM_DETAILS = {
    "69621": "CPU temperature / host-agt01",
    "69485": "Service apache2 running",
    "69486": "Service unbound running",
    "69615": "Service zabbix-server running",
    "69616": "Service zabbix-agent2 running",
    "69617": "Service grafana-server running",
    "69618": "Service cloudflared running",
    "69619": "Service postgresql running",
    "69620": "Service ssh running",
    "69657": "SNMP uptime / host-mikrotik-rb3011",
    "69690": "bridge operational status",
    "69692": "ether1 operational status",
    "69701": "pppoe-out1 operational status",
    "69689": "wg0 operational status",
    "69632": "Livecopilot Apache Edge estado",
    "69633": "Livecopilot Frontend Público estado",
    "69635": "Livecopilot Backend Health estado",
    "69636": "Livecopilot Backend Status estado",
    "69637": "Livecopilot Backend API estado",
}

NODES = [
    {"id": "agt01", "x": 44, "y": 170, "w": 170, "h": 70, "label": "agt01", "small": "functional_node"},
    {"id": "br0", "x": 250, "y": 170, "w": 150, "h": 52, "label": "br0"},
    {"id": "apache2", "x": 44, "y": 275, "w": 150, "h": 52, "label": "apache2"},
    {"id": "cloudflared", "x": 208, "y": 275, "w": 170, "h": 52, "label": "cloudflared"},
    {"id": "unbound", "x": 44, "y": 342, "w": 150, "h": 52, "label": "unbound"},
    {"id": "grafana-server", "x": 208, "y": 342, "w": 170, "h": 52, "label": "grafana-server"},
    {"id": "zabbix-server", "x": 44, "y": 409, "w": 150, "h": 52, "label": "zabbix-server"},
    {"id": "zabbix-agent2", "x": 208, "y": 409, "w": 170, "h": 52, "label": "zabbix-agent2"},
    {"id": "postgresql", "x": 44, "y": 476, "w": 150, "h": 52, "label": "postgresql"},
    {"id": "ssh", "x": 208, "y": 476, "w": 170, "h": 52, "label": "ssh"},
    {"id": "mikrotik-rb3011", "x": 536, "y": 170, "w": 240, "h": 70, "label": "MikroTik RB3011", "small": "functional_node"},
    {"id": "bridge", "x": 560, "y": 275, "w": 180, "h": 52, "label": "bridge"},
    {"id": "ether1", "x": 560, "y": 342, "w": 180, "h": 52, "label": "ether1"},
    {"id": "pppoe-out1", "x": 560, "y": 409, "w": 180, "h": 52, "label": "pppoe-out1"},
    {"id": "wg0", "x": 560, "y": 476, "w": 180, "h": 52, "label": "wg0", "badge": "overlay separado"},
    {"id": "public-ip", "x": 770, "y": 342, "w": 170, "h": 52, "label": "206.42.12.37"},
    {"id": "brisanet", "x": 770, "y": 409, "w": 190, "h": 52, "label": "AS28126 BRISANET"},
    {"id": "livecopilot", "x": 1020, "y": 170, "w": 220, "h": 70, "label": "Livecopilot", "small": "surface pública"},
    {"id": "frontend-publico", "x": 980, "y": 275, "w": 190, "h": 52, "label": "Frontend Público"},
    {"id": "backend-fastapi", "x": 1190, "y": 275, "w": 170, "h": 52, "label": "Backend FastAPI"},
    {"id": "cloudflared-livecopilot", "x": 980, "y": 342, "w": 190, "h": 52, "label": "cloudflared-livecopilot"},
    {"id": "apache-edge", "x": 1190, "y": 342, "w": 170, "h": 52, "label": "Apache Edge"},
]

EDGES = [
    {"d": "M214 205 C228 205, 238 205, 250 205", "from": "agt01", "to": "br0"},
    {"d": "M119 345 C119 315, 119 272, 119 222", "from": "apache2", "to": "agt01"},
    {"d": "M293 345 C293 305, 309 285, 325 222", "from": "cloudflared", "to": "br0"},
    {"d": "M119 412 C119 388, 118 350, 119 327", "from": "zabbix-server", "to": "apache2"},
    {"d": "M293 412 C293 389, 293 370, 293 327", "from": "zabbix-agent2", "to": "cloudflared"},
    {"d": "M119 479 C119 456, 119 439, 119 379", "from": "postgresql", "to": "unbound"},
    {"d": "M293 479 C293 463, 293 450, 293 379", "from": "ssh", "to": "grafana-server"},
    {"d": "M400 196 C454 196, 476 196, 536 196", "from": "br0", "to": "mikrotik-rb3011"},
    {"d": "M325 222 C345 250, 410 262, 560 301", "from": "br0", "to": "bridge"},
    {"d": "M650 222 C650 248, 650 252, 650 275", "from": "mikrotik-rb3011", "to": "bridge"},
    {"d": "M650 327 C650 334, 650 336, 650 342", "from": "bridge", "to": "ether1"},
    {"d": "M650 394 C650 401, 650 403, 650 409", "from": "ether1", "to": "pppoe-out1"},
    {"d": "M650 461 C650 469, 650 471, 650 476", "from": "pppoe-out1", "to": "wg0"},
    {"d": "M740 368 C752 368, 760 368, 770 368", "from": "ether1", "to": "public-ip"},
    {"d": "M740 435 C752 435, 760 435, 770 435", "from": "pppoe-out1", "to": "brisanet"},
    {"d": "M964 368 C972 368, 976 368, 980 368", "from": "public-ip", "to": "cloudflared-livecopilot"},
    {"d": "M1142 301 C1155 301, 1162 301, 1190 301", "from": "frontend-publico", "to": "backend-fastapi"},
    {"d": "M1075 327 C1075 335, 1075 338, 1075 342", "from": "frontend-publico", "to": "cloudflared-livecopilot"},
    {"d": "M1170 368 C1178 368, 1182 368, 1190 368", "from": "cloudflared-livecopilot", "to": "apache-edge"},
    {"d": "M1145 327 C1178 327, 1210 327, 1240 342", "from": "livecopilot", "to": "apache-edge"},
]


def http_json(url: str, payload: dict, headers: dict[str, str]) -> dict:
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def zabbix_call(method: str, params: dict, token: str | None = None, request_id: int = 1) -> dict:
    headers = {"Content-Type": "application/json-rpc"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return http_json(ZABBIX_API_URL, {"jsonrpc": "2.0", "method": method, "params": params, "id": request_id}, headers)


def load_zabbix_password() -> str:
    data = yaml.safe_load(ZABBIX_DS_FILE.read_text())
    return data["datasources"][0]["secureJsonData"]["password"]


def fetch_items() -> dict[str, dict]:
    password = load_zabbix_password()
    token = zabbix_call("user.login", {"username": "Admin", "password": password})["result"]
    itemids = sorted({itemid for rule in NODE_RULES.values() for itemid in rule.get("itemids", [])})
    result = zabbix_call(
        "item.get",
        {"output": ["itemid", "name", "key_", "lastvalue", "lastclock", "state", "status", "error", "value_type"], "itemids": itemids},
        token=token,
        request_id=2,
    )["result"]
    return {item["itemid"]: item for item in result}


def coerce_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def stale(item: dict) -> bool:
    lastclock = coerce_int(item.get("lastclock"))
    if lastclock == 0:
        return True
    return (int(time.time()) - lastclock) > STALE_SECONDS


def item_state(item: dict, mode: str) -> str:
    if item.get("status") != "0" or item.get("state") != "0":
        return STATE_UNKNOWN
    if stale(item):
        return STATE_UNKNOWN
    value = coerce_int(item.get("lastvalue"))
    if mode == "ifstatus":
        if value == 1:
            return STATE_UP
        if value == 2:
            return STATE_DOWN
        return STATE_WARN
    if value > 0:
        return STATE_UP
    return STATE_DOWN


def aggregate_state(states: list[str]) -> str:
    if not states:
        return STATE_UNKNOWN
    if all(state == STATE_UNKNOWN for state in states):
        return STATE_UNKNOWN
    if any(state == STATE_DOWN for state in states):
        return STATE_DOWN
    if any(state == STATE_WARN for state in states):
        return STATE_WARN
    if any(state == STATE_UNKNOWN for state in states):
        return STATE_WARN
    return STATE_UP


def resolve_states(items: dict[str, dict]) -> dict[str, dict]:
    resolved: dict[str, dict] = {}
    deferred: dict[str, dict] = {}
    for node_id, rule in NODE_RULES.items():
        mode = rule["mode"]
        if mode == "none":
            resolved[node_id] = {"state": STATE_UNKNOWN, "reason": "sem binding real direto", "sources": []}
            continue
        if mode == "aggregate" and rule.get("depends_on"):
            deferred[node_id] = rule
            continue
        if mode == "aggregate":
            node_states: list[str] = []
            sources: list[str] = []
            for itemid in rule["itemids"]:
                item = items.get(itemid)
                if not item:
                    node_states.append(STATE_UNKNOWN)
                    continue
                node_states.append(item_state(item, "single"))
                sources.append(itemid)
            resolved[node_id] = {
                "state": aggregate_state(node_states),
                "reason": "agregado de múltiplos itens reais",
                "sources": sources,
            }
            continue
        itemid = rule["itemids"][0]
        item = items.get(itemid)
        if not item:
            resolved[node_id] = {"state": STATE_UNKNOWN, "reason": "item não encontrado", "sources": [itemid]}
            continue
        resolved[node_id] = {
            "state": item_state(item, mode),
            "reason": item["name"],
            "sources": [itemid],
            "item": item,
        }
    for node_id, rule in deferred.items():
        states = [resolved[dep]["state"] for dep in rule["depends_on"]]
        resolved[node_id] = {
            "state": aggregate_state(states),
            "reason": "agregado dos nós dependentes",
            "sources": list(rule["depends_on"]),
        }
    return resolved


def node_css(node_id: str, state_map: dict[str, dict]) -> str:
    role = NODE_RULES[node_id]["role"]
    role_class = {
        "service": "service-shape",
        "transport": "transport-shape",
        "aux": "aux-shape",
    }[role]
    state_class = {
        STATE_UP: "state-up",
        STATE_DOWN: "state-down",
        STATE_WARN: "state-warn",
        STATE_UNKNOWN: "state-unknown",
    }[state_map[node_id]["state"]]
    return f"node {role_class} {state_class}"


def edge_css(edge: dict, state_map: dict[str, dict]) -> str:
    states = [state_map[edge["from"]]["state"], state_map[edge["to"]]["state"]]
    state = aggregate_state(states)
    return {
        STATE_UP: "edge edge-up",
        STATE_DOWN: "edge edge-down",
        STATE_WARN: "edge edge-warn",
        STATE_UNKNOWN: "edge edge-unknown",
    }[state]


def legend_line(state_map: dict[str, dict]) -> str:
    greens = sorted(node_id for node_id, info in state_map.items() if info["state"] == STATE_UP)
    unknowns = sorted(node_id for node_id, info in state_map.items() if info["state"] == STATE_UNKNOWN)
    return (
        f"Verdes: {', '.join(greens)}. "
        f"Cinzas: {', '.join(unknowns)}."
    )


def render_svg(state_map: dict[str, dict]) -> str:
    parts: list[str] = [
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 720' width='100%' height='100%' role='img' aria-label='Árvore causal AGT, MikroTik RB3011 e Livecopilot com estado'>",
        "<defs>",
        "<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0%' stop-color='#0f172a'/><stop offset='100%' stop-color='#111827'/></linearGradient>",
        "<filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='4' stdDeviation='8' flood-color='#000000' flood-opacity='0.22'/></filter>",
        "<marker id='arrowUp' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto' markerUnits='strokeWidth'><path d='M0,0 L10,5 L0,10 z' fill='#34d399'/></marker>",
        "<marker id='arrowDown' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto' markerUnits='strokeWidth'><path d='M0,0 L10,5 L0,10 z' fill='#f87171'/></marker>",
        "<marker id='arrowWarn' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto' markerUnits='strokeWidth'><path d='M0,0 L10,5 L0,10 z' fill='#fbbf24'/></marker>",
        "<marker id='arrowUnknown' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto' markerUnits='strokeWidth'><path d='M0,0 L10,5 L0,10 z' fill='#94a3b8'/></marker>",
        "<style>",
        ".title { font: 700 30px sans-serif; fill: #f8fafc; }",
        ".subtitle { font: 400 15px sans-serif; fill: #cbd5e1; }",
        ".cluster { font: 700 20px sans-serif; fill: #e2e8f0; letter-spacing: 0.5px; }",
        ".label { font: 600 15px sans-serif; fill: #0f172a; }",
        ".small { font: 500 13px sans-serif; fill: #0f172a; }",
        ".badge { font: 700 11px sans-serif; fill: #334155; }",
        ".node { rx: 16; ry: 16; filter: url(#shadow); stroke-width: 2; }",
        ".service-shape { }",
        ".transport-shape { }",
        ".aux-shape { stroke-dasharray: 6 4; }",
        ".state-up { fill: #bbf7d0; stroke: #22c55e; }",
        ".state-down { fill: #fecaca; stroke: #ef4444; }",
        ".state-warn { fill: #fde68a; stroke: #f59e0b; }",
        ".state-unknown { fill: #e2e8f0; stroke: #64748b; }",
        ".edge { fill: none; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }",
        ".edge-up { stroke: #34d399; marker-end: url(#arrowUp); }",
        ".edge-down { stroke: #f87171; marker-end: url(#arrowDown); }",
        ".edge-warn { stroke: #fbbf24; marker-end: url(#arrowWarn); }",
        ".edge-unknown { stroke: #94a3b8; stroke-dasharray: 8 6; marker-end: url(#arrowUnknown); }",
        ".legend { font: 600 12px sans-serif; fill: #cbd5e1; }",
        "</style>",
        "</defs>",
        "<rect x='0' y='0' width='1440' height='720' rx='28' fill='url(#bg)'/>",
        "<text x='44' y='56' class='title'>Árvore Causal / Dependência por Clusters</text>",
        "<text x='44' y='84' class='subtitle'>Snapshot real do runtime Zabbix. Verde = saudável, vermelho = falha, amarelo = atenção, cinza = sem leitura ou sem binding.</text>",
        "<text x='64' y='140' class='cluster'>AGT</text>",
        "<text x='590' y='140' class='cluster'>MikroTik RB3011</text>",
        "<text x='1040' y='140' class='cluster'>Livecopilot</text>",
    ]
    for edge in EDGES:
        parts.append(f"<path class='{edge_css(edge, state_map)}' d='{edge['d']}'/>")
    for node in NODES:
        parts.append(
            f"<rect id='node-{node['id']}' x='{node['x']}' y='{node['y']}' width='{node['w']}' height='{node['h']}' class='{node_css(node['id'], state_map)}'/>"
        )
        cx = node["x"] + (node["w"] / 2)
        if node["h"] >= 70:
            parts.append(f"<text x='{cx}' y='{node['y'] + 30}' text-anchor='middle' class='label'>{node['label']}</text>")
            parts.append(f"<text x='{cx}' y='{node['y'] + 50}' text-anchor='middle' class='small'>{node.get('small', state_map[node['id']]['state'])}</text>")
        else:
            parts.append(f"<text x='{cx}' y='{node['y'] + 31}' text-anchor='middle' class='label'>{node['label']}</text>")
        if node.get("badge"):
            parts.append(f"<text x='{cx}' y='{node['y'] + 48}' text-anchor='middle' class='badge'>{node['badge']}</text>")
    parts.extend(
        [
            "<rect x='44' y='590' width='1346' height='82' rx='18' fill='#0b1220' stroke='#1e293b' stroke-width='1'/>",
            "<text x='72' y='625' class='legend'>Leitura:</text>",
            "<text x='142' y='625' class='legend'>A cor agora vem do runtime do Zabbix quando existe binding real. Nós sem binding direto continuam cinza por regra.</text>",
            "<text x='72' y='652' class='legend'>O overlay wg0 continua fora da cadeia principal, mas agora reflete o status operacional real do item SNMP.</text>",
            f"<text x='72' y='679' class='legend'>{legend_line(state_map)}</text>",
            "</svg>",
        ]
    )
    return "".join(parts)


def write_static_svg(svg: str) -> Path:
    GRAFANA_STATIC_SVG_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = GRAFANA_STATIC_SVG_FILE.with_suffix(".svg.tmp")
    temp_file.write_text(svg, encoding="utf-8")
    temp_file.replace(GRAFANA_STATIC_SVG_FILE)
    return GRAFANA_STATIC_SVG_FILE


def render_panel_html(cache_bust: int) -> str:
    src = f"{GRAFANA_STATIC_SVG_URL_PATH}?v={cache_bust}"
    return (
        "<div style='width:100%;height:100%;display:flex;align-items:center;justify-content:center;"
        "padding:12px;background:#0b1220;border-radius:20px;overflow:auto'>"
        f"<img src='{src}' alt='Árvore causal AGT, MikroTik RB3011 e Livecopilot com estado' "
        "style='display:block;width:100%;height:100%;object-fit:contain' />"
        "</div>"
    )


def grafana_headers(password: str) -> dict[str, str]:
    token = base64.b64encode(f"admin:{password}".encode()).decode()
    return {"Host": GRAFANA_HOST, "X-Forwarded-Proto": "https", "Authorization": f"Basic {token}"}


def load_dashboard(password: str) -> dict:
    headers = grafana_headers(password)
    req = urllib.request.Request(f"{GRAFANA_URL}/api/dashboards/uid/{GRAFANA_DASHBOARD_UID}", headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.load(response)


def update_dashboard(password: str, cache_bust: int) -> dict:
    headers = grafana_headers(password)
    dashboard = load_dashboard(password)["dashboard"]
    for panel in dashboard["panels"]:
        if panel["id"] == GRAFANA_PANEL_ID:
            panel["title"] = "Árvore Causal / Dependência"
            panel["type"] = "text"
            panel["options"] = {"mode": "html", "content": render_panel_html(cache_bust)}
            panel["gridPos"] = {"h": 10, "w": 24, "x": 0, "y": 20}
            panel["pluginVersion"] = "12.4.2"
            panel["transparent"] = False
            break
    payload = {"dashboard": dashboard, "folderId": 0, "overwrite": True, "message": "fix: render grafana causal tree via static svg embed"}
    req = urllib.request.Request(
        f"{GRAFANA_URL}/api/dashboards/db",
        data=json.dumps(payload).encode(),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        return json.load(response)


def build_snapshot() -> dict:
    items = fetch_items()
    return resolve_states(items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render and optionally publish the Grafana causal tree with runtime state.")
    parser.add_argument("--apply-grafana", action="store_true", help="Update panel 26 on the Grafana dashboard.")
    parser.add_argument("--print-json", action="store_true", help="Print the computed state snapshot as JSON.")
    parser.add_argument("--print-svg", action="store_true", help="Print the rendered SVG.")
    args = parser.parse_args()

    state_map = build_snapshot()
    svg = render_svg(state_map)
    write_static_svg(svg)

    if args.apply_grafana:
        password = GRAFANA_PASSWORD_FILE.read_text().strip()
        result = update_dashboard(password, int(time.time()))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.print_json:
        print(json.dumps(state_map, ensure_ascii=False, indent=2, sort_keys=True))
    if args.print_svg:
        print(svg)
    if not any([args.apply_grafana, args.print_json, args.print_svg]):
        print(json.dumps(state_map, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
