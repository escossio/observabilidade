#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ $# -eq 0 ]]; then
  set -- --target "${POC_TARGET:-observabilidade.escossio.dev.br}"
fi

exec python3 -m src.main "$@"
