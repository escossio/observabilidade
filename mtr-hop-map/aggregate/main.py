from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from .graph_build import build_aggregate
from .loader import load_samples
from .report import write_outputs


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS_ROOT = ROOT / "data" / "runs"
DEFAULT_OUTPUT_ROOT = ROOT / "aggregate" / "data" / "runs"


def _now_run_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def _top_rows(counter: Counter, inventory: list[dict[str, Any]], key: str, limit: int = 10) -> list[dict[str, Any]]:
    lookup = {row["ip"]: row for row in inventory}
    rows: list[dict[str, Any]] = []
    for ip, count in counter.most_common(limit):
        row = lookup.get(ip)
        if not row:
            continue
        rows.append(
            {
                "ip": ip,
                "observations": count,
                "asn": row["asn"],
                "company": row["company"],
                "primary_class": row["classification"]["primary_class"],
                "confidence": row["classification"]["confidence"],
                "evidence": row["classification"]["evidence"],
                key: row.get(key, 0),
                "last_internal_count": row.get("last_internal_count", 0),
            }
        )
    return rows


def _analysis_for_ip(inventory: list[dict[str, Any]], ip: str) -> dict[str, Any]:
    matches = [row for row in inventory if row["ip"] == ip]
    if not matches:
        return {
            "ip": ip,
            "status": "absent_from_current_corpus",
            "confidence": "low",
            "observations": 0,
            "evidence": ["not_observed_in_current_runs"],
            "source_type": "external_hint",
        }
    row = matches[0]
    return {
        "ip": ip,
        "status": row["classification"]["primary_class"],
        "confidence": row["classification"]["confidence"],
        "observations": row["observations"],
        "evidence": row["classification"]["evidence"],
        "source_type": row["classification"]["source_type"],
        "asn": row["asn"],
        "company": row["company"],
    }


def build_output(samples: list[Any], aggregate: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    inventory = aggregate["inventory"]
    path_counter = aggregate["path_counter"]
    classification_summary = {
        "inventory": inventory,
        "edge_rankings": aggregate["edge_rankings"],
        "internal_rankings": aggregate["internal_rankings"],
        "cdn_rankings": aggregate["cdn_rankings"],
        "ix_rankings": aggregate["ix_rankings"],
        "dns_rankings": aggregate["dns_rankings"],
    }
    summary = {
        "total_runs_lidos": len({sample.run_id for sample in samples}),
        "total_targets": len(samples),
        "total_unique_hops": len(inventory),
        "total_unique_paths": len(path_counter),
        "hops_mais_recorrentes": _top_rows(Counter({row["ip"]: row["observations"] for row in inventory}), inventory, "observations", 15),
        "candidatos_borda_brisanet": _top_rows(Counter({row["ip"]: row["edge_count"] for row in inventory if row["edge_count"] > 0}), inventory, "edge_count", 10),
        "candidatos_ix_ptt": [
            {
                "ip": row["ip"],
                "asn": row["asn"],
                "company": row["company"],
                "confidence": row["classification"]["confidence"],
                "evidence": row["classification"]["evidence"],
                "observations": row["observations"],
            }
            for row in inventory
            if row["classification"]["primary_class"] == "ix_ptt_candidate"
        ],
        "candidatos_cdn": [
            {
                "ip": row["ip"],
                "asn": row["asn"],
                "company": row["company"],
                "confidence": row["classification"]["confidence"],
                "evidence": row["classification"]["evidence"],
                "observations": row["observations"],
            }
            for row in inventory
            if row["classification"]["primary_class"] == "cdn_candidate"
        ],
        "analise_dns_177_37_220_17": _analysis_for_ip(inventory, "177.37.220.17"),
        "analise_dns_177_37_220_18": _analysis_for_ip(inventory, "177.37.220.18"),
        "top_targets": dict(aggregate["target_counter"].most_common()),
        "top_runs": dict(aggregate["run_counter"].most_common()),
        "class_counter": dict(aggregate["class_counter"]),
    }
    return {
        "generated_at": datetime.now().isoformat(),
        "runs_root": str(DEFAULT_RUNS_ROOT),
        "output_dir": str(output_dir),
        "summary": summary,
        "classification_summary": classification_summary,
        "inventory": inventory,
        "edge_rankings": aggregate["edge_rankings"],
        "internal_rankings": aggregate["internal_rankings"],
        "cdn_rankings": aggregate["cdn_rankings"],
        "ix_rankings": aggregate["ix_rankings"],
        "dns_rankings": aggregate["dns_rankings"],
        "path_counter": path_counter.most_common(20),
        "sample_pairs": aggregate["sample_pairs"].most_common(20),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate MTR hop-map traces into recurrence and boundary candidates.")
    parser.add_argument("--runs-root", default=str(DEFAULT_RUNS_ROOT), help="Root dos runs do mtr-hop-map")
    parser.add_argument("--output-dir", help="Diretório de saída da agregação")
    parser.add_argument("--limit", type=int, default=15, help="Limite de linhas nos rankings principais")
    args = parser.parse_args()

    runs_root = Path(args.runs_root)
    samples = load_samples(runs_root)
    aggregate = build_aggregate(samples)
    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_ROOT / _now_run_id()
    output = build_output(samples, aggregate, output_dir)
    write_outputs(output_dir, output)
    print(json.dumps(output["summary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
