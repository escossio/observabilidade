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
from .report import write_batch_artifacts, write_target_artifacts, write_target_failure_artifacts
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
        "hostids": reconcile_1.hostids,
        "selementids": reconcile_1.selementids,
        "linkids": reconcile_1.linkids,
        "host_actions": reconcile_1.host_actions,
        "map_metadata": map_metadata,
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
        "requested_targets": len(specs),
        "processed_targets": len(target_results),
        "successful_targets": sum(1 for row in target_results if row["status"] == "ok"),
        "failed_targets": sum(1 for row in target_results if row["status"] == "error"),
        "dry_run": dry_run,
        "host_identity_model": "global-ip",
        "specs": [{"target": target, "replay_path": replay_path} for target, replay_path in specs],
    }
    write_batch_artifacts(run_root, batch_execution, target_results)

    return {
        "run_id": run_id,
        "run_dir": str(run_root),
        "targets": target_results,
        **batch_execution,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate persistent Zabbix hop maps from MTR + ASN.")
    parser.add_argument("--target", action="append", help="Destino canônico do mapa no Zabbix; pode ser repetido")
    parser.add_argument("--targets-file", help="Arquivo texto com um destino por linha ou destino<TAB>replay.json")
    parser.add_argument("--replay", required=False, help="Alias de --mtr-json para replay de um destino único")
    parser.add_argument("--mtr-json", required=False, help="Arquivo JSON de replay para um destino único")
    parser.add_argument("--dry-run", action="store_true", help="Planeja a reconciliação sem escrever no Zabbix")
    parser.add_argument("--asn-lookup-mode", choices=["online", "offline"], required=False, help="Modo do enrichment ASN")
    parser.add_argument("--asn-cache-path", required=False, help="Caminho do cache local de ASN/empresa")
    args = parser.parse_args()

    specs = _collect_targets(args)
    result = run_batch(specs, asn_lookup_mode=args.asn_lookup_mode, asn_cache_path=args.asn_cache_path, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["failed_targets"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
