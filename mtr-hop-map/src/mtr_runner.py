from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class MTRResult:
    raw_json: str
    parsed: dict
    raw_text: str


def run_mtr(target: str) -> MTRResult:
    cmd = ["mtr", "-n", "-r", "-c", "1", "--report-wide", "--aslookup", "--json", target]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    raw_text = proc.stdout.strip()
    parsed = json.loads(raw_text)
    return MTRResult(raw_json=raw_text, parsed=parsed, raw_text=raw_text)
