#!/usr/bin/env python3
"""Summarize recent Zabbix problems/events with causal explanations."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

from causal_explain import explain_signal  # noqa: E402


DB_PASSWORD = "4TSfGnAsf/Be5d5cBE+dp1H30bP80xvt"
DB_HOST = "127.0.0.1"
DB_NAME = "zabbix"
DB_USER = "zabbix"


@dataclass
class RecentProblem:
    clock: int
    ns: int
    r_clock: int | None
    r_ns: int | None
    eventid: int
    objectid: int
    name: str
    severity: int
    acknowledged: int
    host: str
    status: str


def psql_query(sql: str) -> list[list[str]]:
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD
    cmd = [
        "psql",
        "-h",
        DB_HOST,
        "-U",
        DB_USER,
        "-d",
        DB_NAME,
        "-P",
        "format=csv",
        "-P",
        "tuples_only=on",
        "-P",
        "null=",
        "-c",
        sql,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "psql falhou")
    reader = csv.reader(proc.stdout.splitlines())
    return [row for row in reader if row]


def fetch_recent_problems(minutes: int, limit: int, open_only: bool, host: str | None, severity: int | None) -> list[RecentProblem]:
    where = [f"p.clock >= extract(epoch from now())::int - ({minutes} * 60)"]
    if open_only:
        where.append("p.r_clock is null")
    if host:
        escaped_host = host.replace("'", "''")
        where.append(
            "exists (select 1 from triggers t join functions f on f.triggerid=t.triggerid "
            "join items i on i.itemid=f.itemid join hosts h on h.hostid=i.hostid "
            f"where t.triggerid = p.objectid and h.host = '{escaped_host}')"
        )
    if severity is not None:
        where.append(f"p.severity = {severity}")

    sql = f"""
        select p.clock, coalesce(p.ns,0), p.r_clock, coalesce(p.r_ns,0), p.eventid, p.objectid, p.name, p.severity, p.acknowledged,
               coalesce(string_agg(distinct h.host, ', ' order by h.host), 'unknown') as host,
               case when p.r_clock is null then 'open' else 'resolved' end as status
        from problem p
        left join triggers t on t.triggerid = p.objectid
        left join functions f on f.triggerid = t.triggerid
        left join items i on i.itemid = f.itemid
        left join hosts h on h.hostid = i.hostid
        where {' and '.join(where)}
        group by p.clock, p.ns, p.r_clock, p.r_ns, p.eventid, p.objectid, p.name, p.severity, p.acknowledged
        order by greatest(p.clock, coalesce(p.r_clock, p.clock)) desc, p.eventid desc
        limit {limit}
    """
    rows = psql_query(sql)
    out: list[RecentProblem] = []
    for row in rows:
        clock, ns, r_clock, r_ns, eventid, objectid, name, sev, ack, host_val, status = row
        out.append(
            RecentProblem(
                clock=int(clock),
                ns=int(ns or 0),
                r_clock=int(r_clock) if r_clock else None,
                r_ns=int(r_ns) if r_ns else None,
                eventid=int(eventid),
                objectid=int(objectid),
                name=name,
                severity=int(sev),
                acknowledged=int(ack),
                host=host_val,
                status=status,
            )
        )
    return out


def explain_problem(problem: RecentProblem) -> dict[str, Any] | None:
    try:
        reading = explain_signal(triggerid=str(problem.objectid))
    except KeyError:
        return None
    reading["event"] = {
        "clock": problem.clock,
        "r_clock": problem.r_clock,
        "name": problem.name,
        "severity": problem.severity,
        "acknowledged": problem.acknowledged,
        "host": problem.host,
        "status": problem.status,
        "eventid": problem.eventid,
        "triggerid": problem.objectid,
    }
    return reading


def format_timestamp(epoch: int) -> str:
    proc = subprocess.run(["date", "-d", f"@{epoch}", "+%Y-%m-%dT%H:%M:%S%z"], capture_output=True, text=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else str(epoch)


def render_text(results: list[dict[str, Any]], summary: dict[str, Any], *, minutes: int, limit: int, open_only: bool, host: str | None, severity: int | None) -> str:
    lines: list[str] = []
    lines.append("Eventos recentes do Zabbix")
    lines.append(f"- janela: últimos {minutes} minutos")
    lines.append(f"- limite: {limit}")
    lines.append(f"- open_only: {'sim' if open_only else 'não'}")
    if host:
        lines.append(f"- host: {host}")
    if severity is not None:
        lines.append(f"- severity: {severity}")

    lines.append("")
    for idx, reading in enumerate(results, 1):
        event = reading["event"]
        binding = reading["binding"]
        causal = reading["causal"]
        lines.append(f"#{idx} {format_timestamp(event['clock'])} - {event['host']} - {event['name']}")
        if event.get("r_clock"):
            lines.append(f"- status: resolved em {format_timestamp(event['r_clock'])}")
        else:
            lines.append(f"- status: open")
        lines.append(f"- nó: {binding.get('graph_node_id')} / {binding.get('cluster')}")
        lines.append(f"- semântica: {causal.get('failure_semantics')} / {causal.get('blast_radius')}")
        lines.append(f"- leitura: {causal.get('interpretation_template').strip()}")
        lines.append("")

    lines.append("Resumo consolidado")
    lines.append(f"- total de eventos: {summary['total_events']}")
    lines.append(f"- explicados: {summary['explained_events']}")
    lines.append(f"- sem binding: {summary['unbound_events']}")
    lines.append(f"- abertos: {summary['open_events']}")
    lines.append(f"- resolvidos: {summary['resolved_events']}")
    lines.append("- por semântica:")
    for semantics, count in summary["by_semantics"].items():
        lines.append(f"  - {semantics}: {count}")

    lines.append("")
    lines.append("Limites")
    lines.append("- consulta depende do conteúdo recente do runtime do Zabbix")
    lines.append("- problemas sem binding não são explicados")
    lines.append("- a ferramenta não substitui RCA completo")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Explain recent Zabbix problems with causal summaries.")
    parser.add_argument("--minutes", type=int, required=True)
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--host")
    parser.add_argument("--severity", type=int)
    parser.add_argument("--open-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    problems = fetch_recent_problems(args.minutes, args.limit, args.open_only, args.host, args.severity)
    results: list[dict[str, Any]] = []
    unbound = 0
    by_semantics: Counter[str] = Counter()
    open_events = 0
    resolved_events = 0

    for problem in problems:
        reading = explain_problem(problem)
        if reading is None:
            unbound += 1
            continue
        results.append(reading)
        sem = reading["causal"]["failure_semantics"]
        by_semantics[sem] += 1
        if reading["event"]["status"] == "open":
            open_events += 1
        else:
            resolved_events += 1

    summary = {
        "total_events": len(problems),
        "explained_events": len(results),
        "unbound_events": unbound,
        "open_events": open_events,
        "resolved_events": resolved_events,
        "by_semantics": dict(by_semantics),
    }

    if args.json:
        print(json.dumps({"results": results, "summary": summary}, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(results, summary, minutes=args.minutes, limit=args.limit, open_only=args.open_only, host=args.host, severity=args.severity))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
