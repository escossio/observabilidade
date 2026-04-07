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
    execution: dict,
    asn_summary: dict,
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "mtr_raw.json").write_text(raw_mtr)
    (run_dir / "mtr_normalized.json").write_text(json.dumps([asdict(hop) for hop in hops], indent=2, ensure_ascii=False))
    (run_dir / "reconcile_phase1.json").write_text(json.dumps(asdict(reconcile_1), indent=2, ensure_ascii=False))
    (run_dir / "reconcile_phase2.json").write_text(json.dumps(asdict(reconcile_2), indent=2, ensure_ascii=False))
    (run_dir / "execution.json").write_text(json.dumps(execution, indent=2, ensure_ascii=False))
    (run_dir / "asn_summary.json").write_text(json.dumps(asn_summary, indent=2, ensure_ascii=False))

    created = [row["hostid"] for row in reconcile_1.host_actions if row["action"] == "created"]
    reused = [row["hostid"] for row in reconcile_1.host_actions if row["action"] == "reused"]
    updated = [row["hostid"] for row in reconcile_1.host_actions if row["action"] == "updated"]

    report = [
        f"# MTR Hop Map - {target}",
        "",
        "## Contexto",
        "",
        f"- destino do mapa: `{target}`",
        f"- origem do MTR: `{execution['mtr_source_kind']}`",
        f"- arquivo de replay: `{execution.get('mtr_source_path') or '-'}`",
        f"- modelo de identidade: `{execution['host_identity_model']}`",
        f"- mapa canônico: `{reconcile_1.map_name}`",
        f"- sysmapid: `{reconcile_1.sysmapid}`",
        f"- grupo de hosts: `{reconcile_1.host_groupid}`",
        f"- template: `{reconcile_1.templateid}`",
        "",
        "## Hops normalizados",
        "",
    ]
    for hop in hops:
        report.append(f"- {hop.order:02d}: `{hop.ip or '*'}` - `{hop.asn}` - `{hop.company}` - origem `{hop.source}`")

    report += [
        "",
        "## Hosts reconciliados",
        "",
        f"- criados na fase 1: `{', '.join(created) if created else '-'}`",
        f"- reaproveitados na fase 1: `{', '.join(reused) if reused else '-'}`",
        f"- atualizados na fase 1: `{', '.join(updated) if updated else '-'}`",
        "",
        "## Idempotencia",
        "",
        f"- mapa criado na fase 1: `{reconcile_1.created_map}`",
        f"- mapa criado na fase 2: `{reconcile_2.created_map}`",
        f"- hostids fase 1: `{', '.join(reconcile_1.hostids)}`",
        f"- hostids fase 2: `{', '.join(reconcile_2.hostids)}`",
        f"- linkids fase 1: `{', '.join(reconcile_1.linkids)}`",
        f"- linkids fase 2: `{', '.join(reconcile_2.linkids)}`",
        "",
        "## Enrichment ASN",
        "",
        f"- modo de lookup: `{asn_summary['lookup_mode']}`",
        f"- cache local: `{asn_summary['cache_path']}`",
        f"- whois com sucesso: `{asn_summary['stats']['whois_success']}`",
        f"- cache por IP: `{asn_summary['stats']['cache_ip_hit']}`",
        f"- cache por ASN: `{asn_summary['stats']['cache_asn_hit']}`",
        f"- fallback por hint MTR: `{asn_summary['stats']['hint_fallback']}`",
        f"- fallback desconhecido: `{asn_summary['stats']['unknown_fallback']}`",
    ]

    if asn_summary.get("events"):
        report += ["", "## Eventos de fallback", ""]
        for event in asn_summary["events"]:
            report.append(f"- {event}")

    report += [
        "",
        "## Artefatos",
        "",
        "- `mtr_raw.json`",
        "- `mtr_normalized.json`",
        "- `reconcile_phase1.json`",
        "- `reconcile_phase2.json`",
        "- `execution.json`",
        "- `asn_summary.json`",
    ]
    (run_dir / "report.md").write_text("\n".join(report) + "\n")
