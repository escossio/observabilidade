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


def write_promotion_outputs(output_dir: Path, promotion: dict[str, Any], zabbix_snapshot: dict[str, Any] | None = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "promoted_nodes.json").write_text(json.dumps(promotion["promoted_nodes"], indent=2, ensure_ascii=False))
    (output_dir / "promoted_edges.json").write_text(json.dumps(promotion["promoted_edges"], indent=2, ensure_ascii=False))
    (output_dir / "backbone_map_plan.json").write_text(json.dumps(promotion, indent=2, ensure_ascii=False))
    if zabbix_snapshot is not None:
        (output_dir / "zabbix_map_snapshot.json").write_text(json.dumps(zabbix_snapshot, indent=2, ensure_ascii=False))
    (output_dir / "report.md").write_text(_render_promotion_report(promotion, zabbix_snapshot))


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


def _render_promotion_report(promotion: dict[str, Any], zabbix_snapshot: dict[str, Any] | None) -> str:
    backbone = promotion["promoted_nodes"]["backbone_observed"]
    candidates = promotion["promoted_nodes"]["candidate_nodes"]
    watchlist = promotion["promoted_nodes"]["watchlist_nodes"]
    backbone_edges = promotion["promoted_edges"]["backbone_observed"]
    candidate_edges = promotion["promoted_edges"]["candidate_edges"]
    lines = [
        "# MTR Hop Map - Promoção Estrutural",
        "",
        "## Critérios",
        "",
        f"- nó backbone observado: runs >= {promotion['meta']['rules']['node']['min_runs']}, targets >= {promotion['meta']['rules']['node']['min_targets']}, recurrence >= {promotion['meta']['rules']['node']['min_ratio']}",
        f"- aresta canônica: runs >= {promotion['meta']['rules']['edge']['min_runs']}, targets >= {promotion['meta']['rules']['edge']['min_targets']}, estabilidade >= {promotion['meta']['rules']['edge']['min_ratio']}",
        "",
        "## Backbone observado",
        "",
    ]
    for node in backbone[:20]:
        lines.append(f"- `{node['ip']}` - runs `{node['run_count']}` - targets `{node['target_count']}` - confidence `{node['confidence']}`")
    lines += [
        "",
        "## Borda candidata",
        "",
    ]
    for node in [node for node in candidates if node["role"] == "edge_brisanet_candidate"][:10]:
        lines.append(
            f"- `{node['ip']}` - edge `{node['edge_count']}` - runs `{node['run_count']}` - confidence `{node['confidence']}`"
        )
    lines += [
        "",
        "## Saídas CDN",
        "",
    ]
    for node in [node for node in candidates if node["role"] == "cdn_candidate"][:10]:
        lines.append(f"- `{node['ip']}` - `{node['company']}` - confidence `{node['confidence']}`")
    lines += [
        "",
        "## Watchlist DNS",
        "",
    ]
    if watchlist:
        for node in watchlist:
            lines.append(f"- `{node['ip']}` - confidence `{node['confidence']}`")
    else:
        lines.append("- nenhum nó DNS observável no corpus atual")
    lines += [
        "",
        "## Arestas promovidas",
        "",
    ]
    for edge in backbone_edges[:20]:
        lines.append(f"- `{edge['source']} -> {edge['target']}` - backbone observado - confidence `{edge['confidence']}`")
    for edge in candidate_edges[:20]:
        lines.append(f"- `{edge['source']} -> {edge['target']}` - `{edge['role']}` - confidence `{edge['confidence']}`")
    if zabbix_snapshot:
        lines += [
            "",
            "## Zabbix",
            "",
            f"- sysmapid: `{zabbix_snapshot['sysmapid']}`",
            f"- elementos: `{zabbix_snapshot['selement_count']}`",
            f"- links: `{zabbix_snapshot['link_count']}`",
            f"- mapa: `{zabbix_snapshot['map_name']}`",
        ]
    lines += [
        "",
        "## Watchlist ausente do corpus",
        "",
        "- `177.37.220.17`",
        "- `177.37.220.18`",
        "",
        "## Distinção de camadas",
        "",
        "- backbone observado: nós e arestas com recorrência alta e estável",
        "- candidatos: nós/arestas com evidência forte mas ainda heurística",
        "- watchlist: itens observáveis ou ausentes que precisam de monitoramento separado",
    ]
    return "\n".join(lines) + "\n"


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
