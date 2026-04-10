#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=/srv/validator
BIN_DIR="$ROOT_DIR/bin"
RUNS_DIR="$ROOT_DIR/runs"
CHROMIUM_BIN=/usr/bin/chromium
NODE_SCRIPT="$BIN_DIR/browser_probe.mjs"

usage() {
  cat <<'EOF'
Uso:
  run-validator.sh --url <url> --iface <interface> --name <nome-logico>
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "comando ausente: $1" >&2
    exit 1
  }
}

slugify() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//; s/-+/-/g'
}

capture_prefix() {
  if command -v sudo >/dev/null 2>&1; then
    printf 'sudo\0-n\0'
    return 0
  fi
  if [[ ${EUID:-$(id -u)} -eq 0 ]]; then
    return 0
  fi
  echo "nem sudo -n nem root disponiveis para tcpdump" >&2
  exit 1
}

URL=""
IFACE=""
RUN_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --url)
      URL="${2:-}"
      shift 2
      ;;
    --iface)
      IFACE="${2:-}"
      shift 2
      ;;
    --name)
      RUN_NAME="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "parametro invalido: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "$URL" && -n "$IFACE" && -n "$RUN_NAME" ]] || {
  usage >&2
  exit 2
}

require_cmd tcpdump
require_cmd node
require_cmd jq
[[ -x "$CHROMIUM_BIN" ]] || {
  echo "chromium ausente em $CHROMIUM_BIN" >&2
  exit 1
}
[[ -f "$NODE_SCRIPT" ]] || {
  echo "script ausente: $NODE_SCRIPT" >&2
  exit 1
}
ip link show "$IFACE" >/dev/null 2>&1 || {
  echo "interface invalida: $IFACE" >&2
  exit 1
}

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
run_slug="$(slugify "$RUN_NAME")"
run_dir="$RUNS_DIR/${timestamp}-${run_slug}"
mkdir -p "$run_dir"

capture_pcap="$run_dir/capture.pcap"
capture_log="$run_dir/capture.log"
console_json="$run_dir/browser-console.json"
network_json="$run_dir/browser-network.json"
summary_json="$run_dir/browser-summary.json"
page_png="$run_dir/page.png"
summary_md="$run_dir/summary.md"

declare -a tcp_cmd=()
while IFS= read -r -d '' token; do
  tcp_cmd+=("$token")
done < <(capture_prefix)

cleanup() {
  if [[ -n "${TCPDUMP_PID:-}" ]] && kill -0 "$TCPDUMP_PID" >/dev/null 2>&1; then
    kill -INT "$TCPDUMP_PID" >/dev/null 2>&1 || true
    wait "$TCPDUMP_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

"${tcp_cmd[@]}" tcpdump -i "$IFACE" -nn -s 0 -U -w "$capture_pcap" \
  '(port 53) or (tcp port 80) or (tcp port 443) or (udp port 443)' \
  >"$capture_log" 2>&1 &
TCPDUMP_PID=$!

sleep 2
kill -0 "$TCPDUMP_PID" >/dev/null 2>&1 || {
  echo "tcpdump nao subiu" >&2
  exit 1
}

browser_rc=0
(cd "$ROOT_DIR" && node "$NODE_SCRIPT" --url "$URL" --out-dir "$run_dir" --chromium "$CHROMIUM_BIN") || browser_rc=$?

cleanup
trap - EXIT

[[ -f "$capture_pcap" ]] || {
  echo "capture.pcap nao gerado" >&2
  exit 1
}
[[ -f "$console_json" ]] || {
  echo "browser-console.json nao gerado" >&2
  exit 1
}
[[ -f "$network_json" ]] || {
  echo "browser-network.json nao gerado" >&2
  exit 1
}
[[ -f "$summary_json" ]] || {
  echo "browser-summary.json nao gerado" >&2
  exit 1
}
[[ -f "$page_png" ]] || {
  echo "page.png nao gerado" >&2
  exit 1
}

request_count="$(jq 'length' "$network_json")"
console_errors="$(jq '[.[] | select(.type == "error" or .type == "pageerror")] | length' "$console_json")"
network_failures="$(jq '[.[] | select(.event == "requestfailed" or (.event == "response" and .ok == false))] | length' "$network_json")"
final_status="$(jq -r '.status // "null"' "$summary_json")"
final_url="$(jq -r '.finalUrl // ""' "$summary_json")"

status_label="ok"
verdict="PASS"
if [[ "$browser_rc" -ne 0 ]]; then
  status_label="browser_failed"
  verdict="FAIL"
fi
if [[ "$request_count" -eq 0 ]]; then
  status_label="no_requests"
  verdict="FAIL"
fi

cat >"$summary_md" <<EOF
# Summary

- alvo: $URL
- horario_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- interface: $IFACE
- nome_logico: $RUN_NAME
- pasta_saida: $run_dir
- final_url: $final_url
- quantidade_requests: $request_count
- erros_console: $console_errors
- falhas_rede: $network_failures
- status_final: $status_label
- http_status_inicial: $final_status
- veredito: $verdict
EOF

printf '%s\n' "$run_dir"
