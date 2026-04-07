from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from .asn_enrichment import ASNResolver
from .config import ROOT_DIR, load_config
from .mtr_parser import parse_hops
from .mtr_runner import load_mtr_json, run_mtr
from .report import write_run_artifacts
from .zabbix_api import ZabbixAPI
from .zabbix_reconcile import ensure_map_for_destination


def run_poc(
    target: str | None,
    mtr_json_path: str | None = None,
    asn_lookup_mode: str | None = None,
    asn_cache_path: str | None = None,
) -> dict:
    config = load_config(target)
    if asn_lookup_mode:
        config = replace(config, asn_lookup_mode=asn_lookup_mode)
    if asn_cache_path:
        config = replace(config, asn_cache_path=Path(asn_cache_path))

    run_dir = ROOT_DIR / "data" / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    if mtr_json_path:
        mtr = load_mtr_json(Path(mtr_json_path))
    else:
        mtr = run_mtr(config.target)

    effective_target = config.target or mtr.parsed["report"]["mtr"]["dst"]
    config = replace(config, target=effective_target)

    resolver = ASNResolver(
        cache_path=config.asn_cache_path,
        lookup_mode=config.asn_lookup_mode,
        timeout_seconds=config.asn_lookup_timeout_seconds,
    )
    hops = parse_hops(mtr.parsed, resolver)

    api = ZabbixAPI(config.zabbix_api_url, config.zabbix_user, config.zabbix_password)
    api.login()

    reconcile_1 = ensure_map_for_destination(api, config, hops)
    reconcile_2 = ensure_map_for_destination(api, config, hops)

    execution = {
        "target": config.target,
        "mtr_source_kind": mtr.source_kind,
        "mtr_source_path": mtr.source_path,
        "host_identity_model": config.host_identity_model,
        "asn_lookup_mode": config.asn_lookup_mode,
        "asn_cache_path": str(config.asn_cache_path),
    }
    asn_summary = resolver.summary()
    write_run_artifacts(run_dir, config.target, mtr.raw_json, mtr.parsed, hops, reconcile_1, reconcile_2, execution, asn_summary)

    return {
        "target": config.target,
        "run_dir": str(run_dir),
        "hop_count": len(hops),
        "mtr_source_kind": mtr.source_kind,
        "mtr_source_path": mtr.source_path,
        "host_identity_model": config.host_identity_model,
        "asn_summary": asn_summary,
        "mtr": mtr.parsed,
        "hops": [hop.__dict__ for hop in hops],
        "reconcile_phase1": reconcile_1.__dict__,
        "reconcile_phase2": reconcile_2.__dict__,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a persistent Zabbix hop map from MTR + ASN.")
    parser.add_argument("--target", required=False, help="Destino canônico do mapa no Zabbix")
    parser.add_argument("--mtr-json", required=False, help="Arquivo JSON de replay para o MTR")
    parser.add_argument("--asn-lookup-mode", choices=["online", "offline"], required=False, help="Modo do enrichment ASN")
    parser.add_argument("--asn-cache-path", required=False, help="Caminho do cache local de ASN/empresa")
    args = parser.parse_args()
    result = run_poc(
        target=args.target or "observabilidade.escossio.dev.br",
        mtr_json_path=args.mtr_json,
        asn_lookup_mode=args.asn_lookup_mode,
        asn_cache_path=args.asn_cache_path,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
