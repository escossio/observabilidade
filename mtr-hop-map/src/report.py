from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .mtr_parser import Hop
from .zabbix_reconcile import ReconcileResult


def write_target_artifacts(
    target_dir: Path,
    target: str,
    raw_mtr: str,
    mtr_json: dict,
    hops: list[Hop],
    reconcile_1: ReconcileResult,
    reconcile_2: ReconcileResult,
    execution: dict,
    asn_summary: dict,
    map_metadata: dict[str, Any],
) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "mtr_raw.json").write_text(raw_mtr)
    (target_dir / "mtr_parsed.json").write_text(json.dumps(mtr_json, indent=2, ensure_ascii=False))
    (target_dir / "mtr_normalized.json").write_text(json.dumps([asdict(hop) for hop in hops], indent=2, ensure_ascii=False))
    (target_dir / "reconcile_phase1.json").write_text(json.dumps(asdict(reconcile_1), indent=2, ensure_ascii=False))
    (target_dir / "reconcile_phase2.json").write_text(json.dumps(asdict(reconcile_2), indent=2, ensure_ascii=False))
    (target_dir / "execution.json").write_text(json.dumps(execution, indent=2, ensure_ascii=False))
    (target_dir / "asn_summary.json").write_text(json.dumps(asn_summary, indent=2, ensure_ascii=False))
    (target_dir / "map_metadata.json").write_text(json.dumps(map_metadata, indent=2, ensure_ascii=False))
    if reconcile_1.plan is not None:
        (target_dir / "reconciliation_plan.json").write_text(json.dumps(reconcile_1.plan, indent=2, ensure_ascii=False))

    dry_run = bool(execution.get("dry_run", False))
    created_actions = {"created", "planned-create"}
    reused_actions = {"reused", "planned-reuse"}
    updated_actions = {"updated", "planned-update"}
    created = [row["hostid"] for row in reconcile_1.host_actions if row["action"] in created_actions]
    reused = [row["hostid"] for row in reconcile_1.host_actions if row["action"] in reused_actions]
    updated = [row["hostid"] for row in reconcile_1.host_actions if row["action"] in updated_actions]

    report = [
        f"# MTR Hop Map - {target}",
        "",
        "## Contexto",
        "",
        f"- destino do mapa: `{target}`",
        f"- origem do MTR: `{execution['mtr_source_kind']}`",
        f"- arquivo de replay: `{execution.get('mtr_source_path') or '-'}`",
        f"- run_id do lote: `{execution['run_id']}`",
        f"- slug do destino: `{execution['target_slug']}`",
        f"- dry_run: `{execution.get('dry_run', False)}`",
        f"- modelo de identidade: `{execution['host_identity_model']}`",
        f"- mapa canônico: `{reconcile_1.map_name}`",
        f"- sysmapid: `{reconcile_1.sysmapid}`",
        f"- grupo de hosts: `{reconcile_1.host_groupid}`",
        f"- template: `{reconcile_1.templateid}`",
        f"- nenhuma escrita foi executada: `{dry_run}`",
        "",
        "## Metadata operacional do mapa",
        "",
        f"- source: `{map_metadata['source']}`",
        f"- target: `{map_metadata['target']}`",
        f"- target_slug: `{map_metadata['target_slug']}`",
        f"- mode: `{map_metadata['mode']}`",
        f"- last_trace: `{map_metadata['last_trace']}`",
        f"- dry_run: `{map_metadata.get('dry_run', False)}`",
        f"- tags nativas no sysmap: `{map_metadata['native_tags_supported']}`",
        "",
        "## Plano de reconciliação",
        "",
        f"- hosts cria: `{reconcile_1.plan['counters']['host_create'] if reconcile_1.plan else 0}`",
        f"- hosts reutiliza: `{reconcile_1.plan['counters']['host_reuse'] if reconcile_1.plan else 0}`",
        f"- hosts atualiza: `{reconcile_1.plan['counters']['host_update'] if reconcile_1.plan else 0}`",
        f"- hosts saem do mapa: `{reconcile_1.plan['counters']['host_detach'] if reconcile_1.plan else 0}`",
        f"- links cria: `{reconcile_1.plan['counters']['link_create'] if reconcile_1.plan else 0}`",
        f"- links reutiliza: `{reconcile_1.plan['counters']['link_reuse'] if reconcile_1.plan else 0}`",
        f"- links saem do mapa: `{reconcile_1.plan['counters']['link_detach'] if reconcile_1.plan else 0}`",
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
        "- `mtr_parsed.json`",
        "- `mtr_normalized.json`",
        "- `reconcile_phase1.json`",
        "- `reconcile_phase2.json`",
        "- `reconciliation_plan.json`",
        "- `execution.json`",
        "- `asn_summary.json`",
        "- `map_metadata.json`",
    ]
    (target_dir / "report.md").write_text("\n".join(report) + "\n")


def write_target_failure_artifacts(target_dir: Path, execution: dict, error_message: str) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "execution.json").write_text(json.dumps(execution, indent=2, ensure_ascii=False))
    (target_dir / "error.json").write_text(
        json.dumps({"target": execution["target"], "error": error_message}, indent=2, ensure_ascii=False)
    )
    report = [
        f"# MTR Hop Map - {execution['target']}",
        "",
        "## Falha",
        "",
        f"- run_id do lote: `{execution['run_id']}`",
        f"- slug do destino: `{execution['target_slug']}`",
        f"- origem pretendida: `{execution['mtr_source_kind']}`",
        f"- erro: `{error_message}`",
    ]
    (target_dir / "report.md").write_text("\n".join(report) + "\n")


def write_batch_artifacts(run_dir: Path, batch_execution: dict, target_results: list[dict[str, Any]]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "batch_execution.json").write_text(json.dumps(batch_execution, indent=2, ensure_ascii=False))
    (run_dir / "batch_summary.json").write_text(json.dumps(target_results, indent=2, ensure_ascii=False))

    report = [
        "# MTR Hop Map - Execução em lote",
        "",
        "## Contexto",
        "",
        f"- run_id: `{batch_execution['run_id']}`",
        f"- destinos solicitados: `{batch_execution['requested_targets']}`",
        f"- destinos executados: `{batch_execution['processed_targets']}`",
        f"- sucessos: `{batch_execution['successful_targets']}`",
        f"- falhas: `{batch_execution['failed_targets']}`",
        f"- modo dry-run: `{batch_execution['dry_run']}`",
        "",
        "## Resultados por destino",
        "",
    ]
    for result in target_results:
        line = (
            f"- `{result['target']}` - status `{result['status']}` - modo `{result['mode']}` "
            f"- target_dir `{result['target_dir']}`"
        )
        if result["status"] == "ok":
            line += f" - mapa `{result['map_name']}` / sysmapid `{result['sysmapid']}`"
        else:
            line += f" - erro `{result['error']}`"
        report.append(line)

    (run_dir / "report.md").write_text("\n".join(report) + "\n")


def write_target_branch_analysis(run_dir: Path, analysis: list[dict[str, Any]]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "target_branch_analysis.json").write_text(json.dumps(analysis, indent=2, ensure_ascii=False))
