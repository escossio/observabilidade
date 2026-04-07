from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .mtr_parser import Hop
from .zabbix_reconcile import ReconcileResult


def write_run_artifacts(
    run_dir: Path,
    target: str,
    raw_mtr: str,
    mtr_json: dict,
    hops: list[Hop],
    reconcile_1: ReconcileResult,
    reconcile_2: ReconcileResult,
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "mtr_raw.json").write_text(raw_mtr)
    (run_dir / "mtr_normalized.json").write_text(json.dumps([asdict(hop) for hop in hops], indent=2, ensure_ascii=False))
    (run_dir / "reconcile_phase1.json").write_text(json.dumps(asdict(reconcile_1), indent=2, ensure_ascii=False))
    (run_dir / "reconcile_phase2.json").write_text(json.dumps(asdict(reconcile_2), indent=2, ensure_ascii=False))
    report = [
        f"# MTR Hop Map POC - {target}",
        "",
        "## Contexto",
        "",
        f"- destino: `{target}`",
        f"- mapa canônico: `{reconcile_1.map_name}`",
        f"- sysmapid: `{reconcile_1.sysmapid}`",
        f"- grupo de hosts: `{reconcile_1.host_groupid}`",
        f"- template: `{reconcile_1.templateid}`",
        f"- mapa criado na primeira execução: `{reconcile_1.created_map}`",
        f"- mapa criado na segunda execução: `{reconcile_2.created_map}`",
        "",
        "## Hops normalizados",
        "",
    ]
    for hop in hops:
        report.append(f"- {hop.order:02d}: `{hop.ip}` - `{hop.asn}` - `{hop.company}`")
    report += [
        "",
        "## Idempotência",
        "",
        f"- hostids na primeira execução: `{', '.join(reconcile_1.hostids)}`",
        f"- hostids na segunda execução: `{', '.join(reconcile_2.hostids)}`",
        f"- selementids na primeira execução: `{', '.join(reconcile_1.selementids)}`",
        f"- selementids na segunda execução: `{', '.join(reconcile_2.selementids)}`",
        f"- linkids na primeira execução: `{', '.join(reconcile_1.linkids)}`",
        f"- linkids na segunda execução: `{', '.join(reconcile_2.linkids)}`",
        "",
        "## Artefatos",
        "",
        "- `mtr_raw.json`",
        "- `mtr_normalized.json`",
        "- `reconcile_phase1.json`",
        "- `reconcile_phase2.json`",
    ]
    (run_dir / "report.md").write_text("\n".join(report) + "\n")
