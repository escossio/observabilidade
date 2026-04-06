#!/usr/bin/env python3
"""Explain causal meaning for a Zabbix item/trigger using local bindings.

This is a small offline CLI. It resolves an input against the documented
Zabbix bindings, maps the signal to a graph node, and prints an operational
reading grounded in the minimal causal correlation layer.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml


ROOT = Path(__file__).resolve().parents[1]
BINDINGS_PATH = ROOT / "models" / "zabbix_graph_bindings.yaml"
AGT_MODEL_PATH = ROOT / "models" / "agt_dependency_model.yaml"
MT_MODEL_PATH = ROOT / "models" / "mikrotik_rb3011_dependency_model.yaml"
RULES_PATH = ROOT / "models" / "causal_correlation_rules.yaml"


@dataclass(frozen=True)
class Match:
    source_kind: str
    source_value: str
    binding: dict[str, Any]
    item: Optional[dict[str, Any]] = None
    trigger: Optional[dict[str, Any]] = None


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def normalize(s: Any) -> str:
    return str(s).strip().lower()


def index_models() -> dict[str, dict[str, Any]]:
    models: dict[str, dict[str, Any]] = {}
    for path in (AGT_MODEL_PATH, MT_MODEL_PATH):
        data = load_yaml(path)
        models[data["cluster"].lower()] = data
    return models


def build_bindings(data: dict[str, Any]) -> list[dict[str, Any]]:
    return data.get("bindings", [])


def iter_items(binding: dict[str, Any]):
    for item in binding.get("bound_items", []) or []:
        yield item


def iter_triggers(binding: dict[str, Any]):
    for trig in binding.get("bound_triggers", []) or []:
        yield trig


def find_match(bindings: list[dict[str, Any]], args: argparse.Namespace) -> Match | None:
    itemid = normalize(args.itemid) if args.itemid is not None else None
    triggerid = normalize(args.triggerid) if args.triggerid is not None else None
    item_name = normalize(args.item_name) if args.item_name else None
    trigger_name = normalize(args.trigger_name) if args.trigger_name else None

    for binding in bindings:
        for item in iter_items(binding):
            if itemid and normalize(item.get("itemid")) == itemid:
                return Match("itemid", itemid, binding, item=item)
            if item_name and normalize(item.get("item_name")) == item_name:
                return Match("item-name", item_name, binding, item=item)
        for trig in iter_triggers(binding):
            if triggerid and normalize(trig.get("triggerid")) == triggerid:
                return Match("triggerid", triggerid, binding, trigger=trig)
            if trigger_name and normalize(trig.get("trigger_name")) == trigger_name:
                return Match("trigger-name", trigger_name, binding, trigger=trig)
    return None


def rule_for_semantics(rules: dict[str, Any], semantics: str) -> dict[str, Any]:
    profiles = rules.get("profiles", {})
    return profiles.get(semantics, {})


def build_reading(match: Match, models: dict[str, dict[str, Any]], rules: dict[str, Any]) -> dict[str, Any]:
    binding = match.binding
    cluster_name = binding.get("cluster", "")
    model = models.get(cluster_name.lower(), {})
    node_id = binding.get("graph_node_id")

    node = None
    if model:
        host = model.get("host")
        nodes = [host] if host else []
        nodes.extend(model.get("nodes", []) or [])
        for candidate in nodes:
            if candidate and candidate.get("id") == node_id:
                node = candidate
                break

    semantics = binding.get("failure_semantics_mapped") or (node or {}).get("failure_semantics") or "unknown"
    rule = rule_for_semantics(rules, semantics)
    impact_scope = rule.get("impact_scope_default") or (node or {}).get("impact_scope") or "unknown"
    blast_radius = rule.get("blast_radius_default") or (node or {}).get("blast_radius") or "unknown"
    interpretation = rule.get("interpretation_template") or "Semântica sem regra explícita."
    next_checks = rule.get("next_checks_recommended") or []

    source = {
        "kind": match.source_kind,
        "value": match.source_value,
    }
    if match.item:
        source["matched_item"] = match.item
    if match.trigger:
        source["matched_trigger"] = match.trigger

    return {
        "input": source,
        "binding": {
            "graph_node_id": node_id,
            "cluster": cluster_name,
            "node_role": binding.get("node_role"),
            "zabbix_host": binding.get("zabbix_host"),
            "observed_by_zabbix": binding.get("observed_by_zabbix", False),
            "binding_state": binding.get("binding_state", "unknown"),
        },
        "signal": {
            "item": match.item,
            "trigger": match.trigger,
        },
        "causal": {
            "failure_semantics": semantics,
            "impact_scope": impact_scope,
            "blast_radius": blast_radius,
            "interpretation_template": interpretation,
            "next_checks_recommended": next_checks,
        },
        "node": node or {},
    }


def format_text(reading: dict[str, Any]) -> str:
    binding = reading["binding"]
    causal = reading["causal"]
    node = reading["node"]
    signal = reading["signal"]

    lines = []
    lines.append("Entrada recebida")
    lines.append(f"- tipo: {reading['input']['kind']}")
    lines.append(f"- valor: {reading['input']['value']}")
    if signal.get("item"):
        lines.append(f"- item: {signal['item'].get('item_name')} ({signal['item'].get('itemid')})")
    if signal.get("trigger"):
        lines.append(f"- trigger: {signal['trigger'].get('trigger_name')} ({signal['trigger'].get('triggerid')})")

    lines.append("")
    lines.append("Binding encontrado")
    lines.append(f"- nó do grafo: {binding.get('graph_node_id')}")
    lines.append(f"- cluster: {binding.get('cluster')}")
    lines.append(f"- host Zabbix: {binding.get('zabbix_host')}")
    lines.append(f"- node_role: {binding.get('node_role')}")
    lines.append(f"- binding_state: {binding.get('binding_state')}")

    if node:
        lines.append("")
        lines.append("Leitura do nó")
        lines.append(f"- tipo: {node.get('type')}")
        lines.append(f"- camada: {node.get('layer')}")
        lines.append(f"- semântica do nó: {node.get('failure_semantics') or causal.get('failure_semantics')}")
        lines.append(f"- blast radius do nó: {node.get('blast_radius') or causal.get('blast_radius')}")

    lines.append("")
    lines.append("Leitura operacional")
    lines.append(f"- semântica: {causal.get('failure_semantics')}")
    lines.append(f"- escopo provável: {causal.get('impact_scope')}")
    lines.append(f"- blast radius provável: {causal.get('blast_radius')}")
    lines.append(f"- interpretação curta: {causal.get('interpretation_template').strip()}")

    lines.append("")
    lines.append("Próximos checks recomendados")
    for check in causal.get("next_checks_recommended", []):
        lines.append(f"- {check}")

    lines.append("")
    lines.append("Limites da conclusão")
    lines.append("- a leitura é documental e mínima")
    lines.append("- não fecha RCA completo")
    lines.append("- não inventa binding ausente")
    lines.append("- não promove overlay para cadeia principal sem evidência adicional")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Explain Zabbix signals with dependency-graph bindings.")
    parser.add_argument("--itemid")
    parser.add_argument("--triggerid")
    parser.add_argument("--item-name", dest="item_name")
    parser.add_argument("--trigger-name", dest="trigger_name")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args(argv)

    if not any([args.itemid, args.triggerid, args.item_name, args.trigger_name]):
        parser.error("Informe ao menos um de: --itemid, --triggerid, --item-name, --trigger-name")

    data = load_yaml(BINDINGS_PATH)
    bindings = build_bindings(data)
    models = index_models()
    rules = load_yaml(RULES_PATH)

    match = find_match(bindings, args)
    if not match:
        print("Nenhum binding encontrado para a entrada informada.", file=sys.stderr)
        return 2

    reading = build_reading(match, models, rules)
    if args.json:
        print(json.dumps(reading, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(format_text(reading))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
