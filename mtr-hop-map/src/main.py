from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import Any

from .asn_enrichment import ASNResolver
from .config import ROOT_DIR, load_config
from .hop_policy import slugify
from .mtr_parser import parse_hops
from .mtr_runner import load_mtr_json, run_mtr
from .report import write_batch_artifacts, write_target_artifacts, write_target_branch_analysis, write_target_failure_artifacts
from .zabbix_api import ZabbixAPI
from .zabbix_reconcile import ensure_map_for_destination


DEFAULT_TARGET = "observabilidade.escossio.dev.br"


def _new_run_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def run_poc(
    target: str | None,
    mtr_json_path: str | None = None,
    asn_lookup_mode: str | None = None,
    asn_cache_path: str | None = None,
    dry_run: bool = False,
    run_root: Path | None = None,
    run_id: str | None = None,
    target_index: int = 1,
) -> dict[str, Any]:
    config = load_config(target)
    if asn_lookup_mode:
        config = replace(config, asn_lookup_mode=asn_lookup_mode)
    if asn_cache_path:
        config = replace(config, asn_cache_path=Path(asn_cache_path))

    batch_run_id = run_id or _new_run_id()
    run_dir = run_root or (ROOT_DIR / "data" / "runs" / batch_run_id)

    if mtr_json_path:
        mtr = load_mtr_json(Path(mtr_json_path))
    else:
        mtr = run_mtr(config.target)

    effective_target = config.target or mtr.parsed["report"]["mtr"]["dst"]
    config = replace(config, target=effective_target)
    target_slug = slugify(config.target)
    target_dir = run_dir / "targets" / f"{target_index:02d}-{target_slug}"
    target_dir.mkdir(parents=True, exist_ok=True)

    resolver = ASNResolver(
        cache_path=config.asn_cache_path,
        lookup_mode=config.asn_lookup_mode,
        timeout_seconds=config.asn_lookup_timeout_seconds,
    )
    hops = parse_hops(mtr.parsed, resolver)

    api = ZabbixAPI(config.zabbix_api_url, config.zabbix_user, config.zabbix_password, dry_run=dry_run)
    api.login()

    reconcile_1 = ensure_map_for_destination(api, config, hops, run_dir=str(target_dir), dry_run=dry_run)
    reconcile_2 = ensure_map_for_destination(api, config, hops, run_dir=str(target_dir), dry_run=dry_run)

    map_metadata = {
        "source": "mtr-hop-map",
        "target": config.target,
        "target_slug": target_slug,
        "mode": mtr.source_kind,
        "last_trace": batch_run_id,
        "dry_run": dry_run,
        "native_tags_supported": False,
        "map_name": reconcile_1.map_name,
        "sysmapid": reconcile_1.sysmapid,
    }
    execution = {
        "run_id": batch_run_id,
        "target": config.target,
        "target_slug": target_slug,
        "dry_run": dry_run,
        "mtr_source_kind": mtr.source_kind,
        "mtr_source_path": mtr.source_path,
        "host_identity_model": config.host_identity_model,
        "asn_lookup_mode": config.asn_lookup_mode,
        "asn_cache_path": str(config.asn_cache_path),
    }
    asn_summary = resolver.summary()
    write_target_artifacts(
        target_dir,
        config.target,
        mtr.raw_json,
        mtr.parsed,
        hops,
        reconcile_1,
        reconcile_2,
        execution,
        asn_summary,
        map_metadata,
    )

    return {
        "status": "ok",
        "target": config.target,
        "target_slug": target_slug,
        "run_id": batch_run_id,
        "run_dir": str(run_dir),
        "target_dir": str(target_dir),
        "mode": mtr.source_kind,
        "hop_count": len(hops),
        "mtr_source_kind": mtr.source_kind,
        "mtr_source_path": mtr.source_path,
        "host_identity_model": config.host_identity_model,
        "dry_run": dry_run,
        "asn_summary": asn_summary,
        "map_name": reconcile_1.map_name,
        "sysmapid": reconcile_1.sysmapid,
        "created_map": reconcile_1.created_map,
        "hostids": reconcile_1.hostids,
        "selementids": reconcile_1.selementids,
        "linkids": reconcile_1.linkids,
        "host_actions": reconcile_1.host_actions,
        "map_metadata": map_metadata,
    }


def _target_artifact_paths(target_dir: str) -> dict[str, str]:
    path = Path(target_dir)
    return {
        "target_dir": str(path),
        "report_md": str(path / "report.md"),
        "execution_json": str(path / "execution.json"),
        "reconciliation_plan_json": str(path / "reconciliation_plan.json") if (path / "reconciliation_plan.json").exists() else None,
        "map_metadata_json": str(path / "map_metadata.json"),
        "batch_failure_json": str(path / "error.json") if (path / "error.json").exists() else None,
    }


def _target_stdout_result(result: dict[str, Any], run_dir: str) -> dict[str, Any]:
    artifacts = _target_artifact_paths(result["target_dir"])
    return {
        "target": result["target"],
        "status": result["status"],
        "dry_run": result["dry_run"],
        "mode": result["mode"],
        "map": (
            {
                "name": result["map_name"],
                "sysmapid": result["sysmapid"],
                "created": result.get("created_map", False),
            }
            if result["status"] == "ok"
            else None
        ),
        "actions": {
            "hosts": {
                "reused": len([row for row in result.get("host_actions", []) if row["action"] in {"reused", "planned-reuse"}]),
                "created": len([row for row in result.get("host_actions", []) if row["action"] in {"created", "planned-create"}]),
                "updated": len([row for row in result.get("host_actions", []) if row["action"] in {"updated", "planned-update"}]),
            },
            "selements": {
                "reused": len(result.get("selementids", [])),
                "created": max(0, len(result.get("hostids", [])) - len(result.get("selementids", []))),
                "detached": 0,
            },
            "links": {
                "reused": len(result.get("linkids", [])),
                "created": 0,
                "detached": 0,
            },
            "metadata": result.get("map_metadata", {}),
        },
        "counters": {
            "hop_count": result.get("hop_count", 0),
            "host_count": len(result.get("hostids", [])),
            "selement_count": len(result.get("selementids", [])),
            "link_count": len(result.get("linkids", [])),
        },
        "artifacts": artifacts,
        "error": None,
    }


def _failed_stdout_result(result: dict[str, Any], run_dir: str) -> dict[str, Any]:
    artifacts = _target_artifact_paths(result["target_dir"])
    return {
        "target": result["target"],
        "status": "failed",
        "dry_run": result["dry_run"],
        "mode": result["mode"],
        "map": None,
        "actions": {
            "hosts": {"reused": 0, "created": 0, "updated": 0},
            "selements": {"reused": 0, "created": 0, "detached": 0},
            "links": {"reused": 0, "created": 0, "detached": 0},
            "metadata": {},
        },
        "counters": {
            "hop_count": 0,
            "host_count": 0,
            "selement_count": 0,
            "link_count": 0,
        },
        "artifacts": artifacts,
        "error": result.get("error"),
    }


def build_stdout_json(batch_result: dict[str, Any]) -> dict[str, Any]:
    run_dir = batch_result["run_dir"]
    results: list[dict[str, Any]] = []
    for target_result in batch_result["targets"]:
        if target_result["status"] == "ok":
            results.append(_target_stdout_result(target_result, run_dir))
        elif target_result["status"] == "error":
            results.append(_failed_stdout_result(target_result, run_dir))
        else:
            results.append(target_result)

    summary = {
        "targets_total": batch_result["requested_targets"],
        "targets_succeeded": batch_result["successful_targets"],
        "targets_failed": batch_result["failed_targets"],
        "maps_created": sum(1 for row in results if row.get("map") and row["status"] == "ok" and row["map"].get("created")),
        "maps_updated": sum(1 for row in results if row.get("map") and row["status"] == "ok" and not row["map"].get("created")),
        "hosts_reused": sum(row["actions"]["hosts"]["reused"] for row in results),
        "hosts_created": sum(row["actions"]["hosts"]["created"] for row in results),
        "writes_executed": 0 if batch_result.get("dry_run") else sum(1 for row in results if row["status"] == "ok"),
    }
    mode_set = {row["mode"] for row in results if row.get("mode")}
    mode = "mixed" if len(mode_set) > 1 else (next(iter(mode_set)) if mode_set else "live")
    started_at = batch_result.get("started_at")
    finished_at = batch_result.get("finished_at")
    return {
        "run_id": batch_result["run_id"],
        "mode": mode,
        "dry_run": batch_result["dry_run"],
        "started_at": started_at,
        "finished_at": finished_at,
        "summary": summary,
        "results": results,
        "artifacts": {
            "run_dir": run_dir,
            "batch_execution_json": str(Path(run_dir) / "batch_execution.json"),
            "batch_summary_json": str(Path(run_dir) / "batch_summary.json"),
            "report_md": str(Path(run_dir) / "report.md"),
        },
    }


def _parse_targets_file(path: Path) -> list[tuple[str, str | None]]:
    rows: list[tuple[str, str | None]] = []
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" in line:
            target, replay_path = [part.strip() for part in line.split("\t", 1)]
            rows.append((target, replay_path))
            continue
        if "|" in line:
            target, replay_path = [part.strip() for part in line.split("|", 1)]
            rows.append((target, replay_path))
            continue
        rows.append((line, None))
    return rows


def _collect_targets(args: argparse.Namespace) -> list[tuple[str, str | None]]:
    specs: list[tuple[str, str | None]] = []
    for target in args.target or []:
        specs.append((target, None))
    if args.targets_file:
        specs.extend(_parse_targets_file(Path(args.targets_file)))

    replay_path = args.replay or args.mtr_json
    if replay_path:
        if not specs:
            raise RuntimeError("--replay/--mtr-json exige um --target explícito")
        if len(specs) != 1:
            raise RuntimeError("--replay/--mtr-json só pode ser usado com um único destino explícito")
        specs = [(specs[0][0], replay_path)]

    if not specs:
        specs.append((DEFAULT_TARGET, None))
    return specs


def run_batch(
    specs: list[tuple[str, str | None]],
    asn_lookup_mode: str | None = None,
    asn_cache_path: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    run_id = _new_run_id()
    run_root = ROOT_DIR / "data" / "runs" / run_id
    (run_root / "targets").mkdir(parents=True, exist_ok=True)
    started_at = datetime.now().isoformat()

    target_results: list[dict[str, Any]] = []
    for index, (target, replay_path) in enumerate(specs, start=1):
        target_slug = slugify(target)
        target_dir = run_root / "targets" / f"{index:02d}-{target_slug}"
        try:
            result = run_poc(
                target=target,
                mtr_json_path=replay_path,
                asn_lookup_mode=asn_lookup_mode,
                asn_cache_path=asn_cache_path,
                dry_run=dry_run,
                run_root=run_root,
                run_id=run_id,
                target_index=index,
            )
            target_results.append(result)
        except Exception as exc:
            execution = {
                "run_id": run_id,
                "target": target,
                "target_slug": target_slug,
                "mtr_source_kind": "replay" if replay_path else "live",
                "mtr_source_path": replay_path,
            }
            write_target_failure_artifacts(target_dir, execution, str(exc))
            target_results.append(
                {
                    "status": "error",
                    "target": target,
                    "target_slug": target_slug,
                    "run_id": run_id,
                    "target_dir": str(target_dir),
                    "mode": execution["mtr_source_kind"],
                    "dry_run": dry_run,
                    "error": str(exc),
                }
            )

    batch_execution = {
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(),
        "requested_targets": len(specs),
        "processed_targets": len(target_results),
        "successful_targets": sum(1 for row in target_results if row["status"] == "ok"),
        "failed_targets": sum(1 for row in target_results if row["status"] == "error"),
        "dry_run": dry_run,
        "host_identity_model": "global-ip",
        "specs": [{"target": target, "replay_path": replay_path} for target, replay_path in specs],
    }
    write_batch_artifacts(run_root, batch_execution, target_results)
    write_target_branch_analysis(run_root, _build_target_branch_analysis(target_results))

    return {
        "run_id": run_id,
        "run_dir": str(run_root),
        "targets": target_results,
        **batch_execution,
    }


def _build_target_branch_analysis(target_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    paths: list[tuple[dict[str, Any], list[str], list[dict[str, Any]]]] = []
    for result in target_results:
        target_dir = Path(result["target_dir"])
        normalized_path = target_dir / "mtr_normalized.json"
        if not normalized_path.exists():
            paths.append((result, [], []))
            continue
        hops = json.loads(normalized_path.read_text())
        path = [hop["ip"] for hop in hops if hop.get("ip")]
        paths.append((result, path, hops))

    shared_trunk: list[str] = []
    valid_paths = [path for result, path, hops in paths if result["status"] == "ok" and path]
    if valid_paths:
        shared_trunk = list(valid_paths[0])
        for path in valid_paths[1:]:
            prefix: list[str] = []
            for left, right in zip(shared_trunk, path):
                if left != right:
                    break
                prefix.append(left)
            shared_trunk = prefix

    analysis: list[dict[str, Any]] = []
    for result, path, hops in paths:
        if result["status"] != "ok" or not path:
            analysis.append(
                {
                    "target": result["target"],
                    "run_source": result["mode"],
                    "path_detected": path,
                    "intersects_backbone": False,
                    "shared_trunk_until": shared_trunk,
                    "new_branch_detected": False,
                    "new_nodes": [],
                    "new_edges": [],
                    "external_family_detected": "unknown",
                    "notes": result.get("error", "no normalized trace"),
                }
            )
            continue

        prefix_len = 0
        for left, right in zip(shared_trunk, path):
            if left != right:
                break
            prefix_len += 1
        branch_nodes = path[prefix_len:]
        branch_edges = [{"source": a, "target": b} for a, b in zip(path[max(0, prefix_len - 1) :], path[prefix_len:])]
        last_company = str(hops[-1].get("company", "")).lower() if hops else ""
        family = "unknown"
        for needle, label in [
            ("google", "google"),
            ("quad9", "quad9"),
            ("dell", "dell"),
            ("mikrotik", "mikrotik"),
            ("att", "att"),
            ("at&t", "att"),
            ("twelve99", "twelve99"),
            ("telia", "twelve99"),
        ]:
            if needle in last_company:
                family = label
                break
        analysis.append(
            {
                "target": result["target"],
                "run_source": result["mode"],
                "path_detected": path,
                "intersects_backbone": prefix_len > 0,
                "shared_trunk_until": shared_trunk,
                "new_branch_detected": bool(branch_nodes),
                "new_nodes": branch_nodes,
                "new_edges": branch_edges,
                "external_family_detected": family,
                "notes": f"prefix_len={prefix_len}; branch_len={len(branch_nodes)}",
            }
        )

    return analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate persistent Zabbix hop maps from MTR + ASN.")
    parser.add_argument("--target", action="append", help="Destino canônico do mapa no Zabbix; pode ser repetido")
    parser.add_argument("--targets-file", help="Arquivo texto com um destino por linha ou destino<TAB>replay.json")
    parser.add_argument("--replay", required=False, help="Alias de --mtr-json para replay de um destino único")
    parser.add_argument("--mtr-json", required=False, help="Arquivo JSON de replay para um destino único")
    parser.add_argument("--dry-run", action="store_true", help="Planeja a reconciliação sem escrever no Zabbix")
    parser.add_argument("--json", action="store_true", help="Emite um JSON canônico de saída para automação")
    parser.add_argument("--asn-lookup-mode", choices=["online", "offline"], required=False, help="Modo do enrichment ASN")
    parser.add_argument("--asn-cache-path", required=False, help="Caminho do cache local de ASN/empresa")
    args = parser.parse_args()

    specs = _collect_targets(args)
    result = run_batch(specs, asn_lookup_mode=args.asn_lookup_mode, asn_cache_path=args.asn_cache_path, dry_run=args.dry_run)
    output = build_stdout_json(result) if args.json else result
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if result["failed_targets"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
