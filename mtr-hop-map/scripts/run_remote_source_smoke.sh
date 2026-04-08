#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_CONFIG="${1:-$ROOT_DIR/sources/debian2-1.json}"
TARGET="${2:-8.8.8.8}"
RUN_ID="${RUN_ID:-$(date +%Y%m%d-%H%M%S-%f)}"
RUN_DIR="$ROOT_DIR/data/runs/${RUN_ID}-debian2-1-smoke"
mkdir -p "$RUN_DIR"

python3 - "$SOURCE_CONFIG" "$TARGET" "$RUN_DIR" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
target = sys.argv[2]
run_dir = Path(sys.argv[3])
cfg = json.loads(config_path.read_text())

ssh_args = ["ssh", *cfg["ssh_options"], f"{cfg['ssh_user']}@{cfg['host']}"]
remote_script = f"""
set -euo pipefail
whoami
hostname -f
uname -a
printf 'MTR=%s\\n' "$(command -v mtr)"
{cfg['mtr_command']} {target}
"""

proc = subprocess.run(
    [*ssh_args, "bash", "-lc", remote_script],
    capture_output=True,
    text=True,
    check=True,
)

(run_dir / "source_config.json").write_text(config_path.read_text())
(run_dir / "smoke_output.txt").write_text(proc.stdout)
print(run_dir)
print(proc.stdout)
PY
