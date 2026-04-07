#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-${POC_TARGET:-observabilidade.escossio.dev.br}}"

exec python3 -m src.main --target "$TARGET"
