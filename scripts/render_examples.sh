#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/artifacts/rendered_examples"
mkdir -p "$OUT_DIR"

cp -f "$ROOT_DIR/examples/services.example.yaml" "$OUT_DIR/services.example.yaml"
cp -f "$ROOT_DIR/examples/web_checks.example.yaml" "$OUT_DIR/web_checks.example.yaml"
cp -f "$ROOT_DIR/examples/dns_checks.example.yaml" "$OUT_DIR/dns_checks.example.yaml"

echo "saved examples to $OUT_DIR"
