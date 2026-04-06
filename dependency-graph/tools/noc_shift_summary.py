#!/usr/bin/env python3
"""Generate a shift/NOC summary from recent Zabbix problems."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any

from explain_recent_events import explain_problem, fetch_recent_problems


def build_summary(results: list[dict[str, Any]], problems: list[Any]) -> dict[str, Any]:
    by_semantics = Counter()
    by_cluster = Counter()
    by_host = Counter()
    by_trigger = Counter()
    unexplained = 0
    open_events = 0
    resolved_events = 0
    public_surface = False
    wan_primary = False
    unbound_present = False
    apache_present = False

    for problem in problems:
        by_trigger[problem.name] += 1

    for reading in results:
        event = reading["event"]
        binding = reading["binding"]
        causal = reading["causal"]
        sem = causal["failure_semantics"]
        cluster = binding.get("cluster", "unknown")
        host = event.get("host", "unknown")

        by_semantics[sem] += 1
        by_cluster[cluster] += 1
        by_host[host] += 1

        if event.get("status") == "open":
            open_events += 1
        else:
            resolved_events += 1

        if sem == "public_access_failure":
            public_surface = True
        if sem == "wan_primary_failure":
            wan_primary = True
        if event["name"].lower().startswith("unbound"):
            unbound_present = True
        if event["name"].lower().startswith("apache2"):
            apache_present = True

    unexplained = len(problems) - len(results)
    dominant_semantics = by_semantics.most_common(1)[0][0] if by_semantics else "none"
    most_affected_cluster = by_cluster.most_common(1)[0][0] if by_cluster else "none"
    most_affected_host = by_host.most_common(1)[0][0] if by_host else "none"
    top_triggers = by_trigger.most_common(5)

    return {
        "total_events": len(problems),
        "explained_events": len(results),
        "unexplained_events": unexplained,
        "open_events": open_events,
        "resolved_events": resolved_events,
        "dominant_semantics": dominant_semantics,
        "most_affected_cluster": most_affected_cluster,
        "most_affected_host": most_affected_host,
        "public_surface_issues_present": public_surface,
        "wan_primary_issues_present": wan_primary,
        "unbound_events_present": unbound_present,
        "apache_events_present": apache_present,
        "by_semantics": dict(by_semantics),
        "by_cluster": dict(by_cluster),
        "by_host": dict(by_host),
        "top_triggers": [{"name": name, "count": count} for name, count in top_triggers],
    }


def render_text(period: dict[str, Any], summary: dict[str, Any], results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("Resumo de turno / NOC")
    lines.append(f"- janela: últimos {period['minutes']} minutos")
    lines.append(f"- limite: {period['limit']}")
    lines.append(f"- open_only: {'sim' if period['open_only'] else 'não'}")
    if period.get("host"):
        lines.append(f"- host: {period['host']}")
    if period.get("severity") is not None:
        lines.append(f"- severity: {period['severity']}")

    lines.append("")
    lines.append("Totais")
    lines.append(f"- total de eventos: {summary['total_events']}")
    lines.append(f"- explicados: {summary['explained_events']}")
    lines.append(f"- sem binding: {summary['unexplained_events']}")
    lines.append(f"- abertos: {summary['open_events']}")
    lines.append(f"- resolvidos: {summary['resolved_events']}")

    lines.append("")
    lines.append("Por semântica")
    for sem, count in sorted(summary["by_semantics"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {sem}: {count}")

    lines.append("")
    lines.append("Por cluster")
    for cluster, count in sorted(summary["by_cluster"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {cluster}: {count}")

    lines.append("")
    lines.append("Por host")
    for host, count in sorted(summary["by_host"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {host}: {count}")

    lines.append("")
    lines.append("Top triggers/eventos")
    for item in summary["top_triggers"]:
        lines.append(f"- {item['name']}: {item['count']}")

    lines.append("")
    lines.append("Leitura final")
    lines.append(f"- semântica dominante no período: {summary['dominant_semantics']}")
    lines.append(f"- principal área afetada: {summary['most_affected_cluster']}")
    lines.append(f"- host mais afetado: {summary['most_affected_host']}")
    lines.append(f"- houve evidência de problema público: {'sim' if summary['public_surface_issues_present'] else 'não'}")
    lines.append(f"- houve evidência de WAN principal: {'sim' if summary['wan_primary_issues_present'] else 'não'}")
    lines.append(f"- houve eventos de unbound: {'sim' if summary['unbound_events_present'] else 'não'}")
    lines.append(f"- houve eventos de apache: {'sim' if summary['apache_events_present'] else 'não'}")
    lines.append(f"- eventos sem binding: {summary['unexplained_events']}")

    lines.append("")
    lines.append("Detalhe resumido")
    for reading in results:
        event = reading["event"]
        binding = reading["binding"]
        causal = reading["causal"]
        lines.append(f"- {event['name']} -> {binding.get('graph_node_id')} / {causal.get('failure_semantics')} / {binding.get('cluster')}")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate a NOC/shift summary from recent Zabbix events.")
    parser.add_argument("--minutes", type=int, required=True)
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--host")
    parser.add_argument("--severity", type=int)
    parser.add_argument("--open-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    problems = fetch_recent_problems(args.minutes, args.limit, args.open_only, args.host, args.severity)
    results: list[dict[str, Any]] = []
    for problem in problems:
        reading = explain_problem(problem)
        if reading is not None:
            results.append(reading)

    summary = build_summary(results, problems)
    period = {
        "minutes": args.minutes,
        "limit": args.limit,
        "host": args.host,
        "severity": args.severity,
        "open_only": args.open_only,
    }

    if args.json:
        print(json.dumps({"period": period, "summary": summary, "results": results}, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(period, summary, results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
