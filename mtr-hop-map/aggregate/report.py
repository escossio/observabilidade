from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def _confidence_weight(confidence: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(confidence, 0)


def write_outputs(output_dir: Path, aggregate: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = aggregate["summary"]
    (output_dir / "aggregate_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    (output_dir / "classification_summary.json").write_text(json.dumps(aggregate["classification_summary"], indent=2, ensure_ascii=False))

    _write_hops_inventory(output_dir / "hops_inventory.csv", aggregate["inventory"])
    _write_edge_candidates(output_dir / "edge_candidates.csv", aggregate["edge_rankings"])

    (output_dir / "report.md").write_text(_render_report(aggregate))


def _write_hops_inventory(path: Path, inventory: list[dict[str, Any]]) -> None:
    fieldnames = [
        "ip",
        "asn",
        "company",
        "hostname",
        "observations",
        "sample_count",
        "path_count",
        "last_hop_count",
        "last_internal_count",
        "edge_count",
        "primary_class",
        "confidence",
        "source_type",
        "evidence",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in inventory:
            writer.writerow(
                {
                    "ip": row["ip"],
                    "asn": row["asn"],
                    "company": row["company"],
                    "hostname": row["hostname"],
                    "observations": row["observations"],
                    "sample_count": row["sample_count"],
                    "path_count": row["path_count"],
                    "last_hop_count": row["last_hop_count"],
                    "last_internal_count": row["last_internal_count"],
                    "edge_count": row["edge_count"],
                    "primary_class": row["classification"]["primary_class"],
                    "confidence": row["classification"]["confidence"],
                    "source_type": row["classification"]["source_type"],
                    "evidence": " | ".join(row["classification"]["evidence"]),
                }
            )


def _write_edge_candidates(path: Path, inventory: list[dict[str, Any]]) -> None:
    _write_hops_inventory(
        path,
        [row for row in inventory if row["classification"]["primary_class"] == "edge_brisanet_candidate" or row["edge_count"] > 0],
    )


def _render_report(aggregate: dict[str, Any]) -> str:
    summary = aggregate["summary"]
    lines = [
        "# MTR Hop Map - Agregação",
        "",
        "## Escopo",
        "",
        "- agregação de múltiplos runs, replays e batches já coletados pela frente `mtr-hop-map`",
        "- foco em recorrência de hops, candidatos de borda Brisanet, IX/PTT, CDN e DNS infra",
        "- distinção explícita entre fato observado, inferência heurística e hipótese fraca",
        "",
        "## Resumo",
        "",
        f"- runs lidos: `{summary['total_runs_lidos']}`",
        f"- targets lidos: `{summary['total_targets']}`",
        f"- hops únicos: `{summary['total_unique_hops']}`",
        f"- paths únicos: `{summary['total_unique_paths']}`",
        "",
        "## Hops mais recorrentes",
        "",
    ]
    for row in summary["hops_mais_recorrentes"][:10]:
        lines.append(
            f"- `{row['ip']}` - `{row['observations']}` ocorrências - `{row['primary_class']}` - confiança `{row['confidence']}`"
        )

    lines += [
        "",
        "## Candidatos a borda Brisanet",
        "",
    ]
    for row in summary["candidatos_borda_brisanet"][:10]:
        lines.append(
            f"- `{row['ip']}` - edge `{row['edge_count']}` - last-internal `{row['last_internal_count']}` - confiança `{row['confidence']}`"
        )

    lines += [
        "",
        "## Candidatos IX/PTT",
        "",
    ]
    if summary["candidatos_ix_ptt"]:
        for row in summary["candidatos_ix_ptt"][:10]:
            lines.append(f"- `{row['ip']}` - confiança `{row['confidence']}` - motivos: {', '.join(row['evidence'])}")
    else:
        lines.append("- nenhum candidato forte observado no corpus atual")

    lines += [
        "",
        "## Candidatos CDN",
        "",
    ]
    for row in summary["candidatos_cdn"][:10]:
        lines.append(f"- `{row['ip']}` - `{row['company']}` - confiança `{row['confidence']}`")

    lines += [
        "",
        "## DNS infra 177.37.220.17 / 177.37.220.18",
        "",
        f"- 177.37.220.17: {summary['analise_dns_177_37_220_17']['status']} - confiança `{summary['analise_dns_177_37_220_17']['confidence']}`",
        f"- 177.37.220.18: {summary['analise_dns_177_37_220_18']['status']} - confiança `{summary['analise_dns_177_37_220_18']['confidence']}`",
        "",
        "## Distinção de evidência",
        "",
        "- fatos observados vêm diretamente dos hops agregados dos runs",
        "- inferências heurísticas vêm das regras de recorrência, posição no caminho e ASN/empresa",
        "- hipóteses fracas ficam marcadas com confiança baixa e evidência limitada",
        "",
        "## Arquivos",
        "",
        "- `aggregate_summary.json`",
        "- `classification_summary.json`",
        "- `hops_inventory.csv`",
        "- `edge_candidates.csv`",
    ]
    return "\n".join(lines) + "\n"
