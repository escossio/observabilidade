from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MTRResult:
    raw_json: str
    parsed: dict
    source_kind: str
    source_path: str | None = None


def run_mtr(target: str) -> MTRResult:
    cmd = ["mtr", "-n", "-r", "-c", "1", "--report-wide", "--aslookup", "--json", target]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    raw_text = proc.stdout.strip()
    parsed = json.loads(raw_text)
    return MTRResult(raw_json=raw_text, parsed=parsed, source_kind="live")


def load_mtr_json(path: Path) -> MTRResult:
    raw_text = path.read_text().strip()
    parsed = json.loads(raw_text)
    return MTRResult(raw_json=raw_text, parsed=parsed, source_kind="replay", source_path=str(path))
