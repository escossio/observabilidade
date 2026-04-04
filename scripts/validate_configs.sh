#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - <<'PY'
from pathlib import Path
import sys
try:
    import yaml
except Exception as exc:
    print(f"PyYAML unavailable: {exc}")
    sys.exit(1)

base = Path("/srv/observabilidade-zabbix/config")
for name in ["services.yaml", "web_checks.yaml", "dns_checks.yaml"]:
    path = base / name
    with path.open() as fh:
        yaml.safe_load(fh)
    print(f"ok yaml: {path}")
PY

if command -v shellcheck >/dev/null 2>&1; then
  shellcheck "$ROOT_DIR/scripts/collect_env.sh" "$ROOT_DIR/scripts/render_examples.sh" "$ROOT_DIR/scripts/validate_configs.sh" "$ROOT_DIR/scripts/apply_or_generate_zabbix_plan.sh"
else
  echo "shellcheck not installed"
fi

echo "validation complete"
