from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from json import JSONDecodeError
from pathlib import Path


@dataclass(frozen=True)
class MTRResult:
    raw_json: str
    parsed: dict
    source_kind: str
    source_path: str | None = None


def run_mtr(target: str) -> MTRResult:
    cmd = ["mtr", "-n", "-r", "-c", "1", "--report-wide", "--aslookup", "--json", target]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        error = proc.stderr.strip() or proc.stdout.strip() or f"mtr retornou {proc.returncode}"
        raise RuntimeError(f"falha ao executar mtr para {target}: {error}")
    raw_text = proc.stdout.strip()
    try:
        parsed = json.loads(raw_text)
    except JSONDecodeError as exc:
        snippet = raw_text[:200] if raw_text else proc.stderr.strip()
        raise RuntimeError(f"saida JSON invalida do mtr para {target}: {snippet}") from exc
    return MTRResult(raw_json=raw_text, parsed=parsed, source_kind="live")


def load_mtr_json(path: Path) -> MTRResult:
    raw_text = path.read_text().strip()
    try:
        parsed = json.loads(raw_text)
    except JSONDecodeError as exc:
        raise RuntimeError(f"arquivo de replay invalido: {path}") from exc
    return MTRResult(raw_json=raw_text, parsed=parsed, source_kind="replay", source_path=str(path))
