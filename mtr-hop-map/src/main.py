from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .config import ROOT_DIR, load_config
from .mtr_parser import parse_hops
from .mtr_runner import run_mtr
from .report import write_run_artifacts
from .zabbix_api import ZabbixAPI
from .zabbix_reconcile import ensure_map_for_destination


def run_poc(target: str) -> dict:
    config = load_config(target)
    run_dir = ROOT_DIR / "data" / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    mtr = run_mtr(config.target)
    hops = parse_hops(mtr.parsed)

    api = ZabbixAPI(config.zabbix_api_url, config.zabbix_user, config.zabbix_password)
    api.login()

    reconcile_1 = ensure_map_for_destination(api, config, hops)
    reconcile_2 = ensure_map_for_destination(api, config, hops)

    write_run_artifacts(run_dir, config.target, mtr.raw_json, mtr.parsed, hops, reconcile_1, reconcile_2)

    return {
        "target": config.target,
        "run_dir": str(run_dir),
        "hop_count": len(hops),
        "mtr": mtr.parsed,
        "hops": [hop.__dict__ for hop in hops],
        "reconcile_phase1": reconcile_1.__dict__,
        "reconcile_phase2": reconcile_2.__dict__,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a persistent Zabbix hop map from MTR + ASN.")
    parser.add_argument("--target", required=False, help="Destination hostname/IP for the POC")
    args = parser.parse_args()
    result = run_poc(args.target or "observabilidade.escossio.dev.br")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
