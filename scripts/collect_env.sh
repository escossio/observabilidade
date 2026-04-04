#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARTIFACTS_DIR="$ROOT_DIR/artifacts"
mkdir -p "$ARTIFACTS_DIR"

timestamp="$(date -Is)"

{
  echo "timestamp: $timestamp"
  echo "hostname: $(hostname -f 2>/dev/null || hostname)"
  echo "kernel: $(uname -r)"
  echo "os_release:"
  sed 's/^/  /' /etc/os-release
  echo "packages:"
  dpkg -l | awk 'BEGIN{print "  zabbix:"} /zabbix/ {print "  - " $2 " " $3}'
  echo "services:"
  systemctl list-units --type=service --all | awk '/zabbix|apache2|nginx|postfix|dovecot/ {print "  - " $1 " " $4 " " $5 " " $6}'
  echo "ports:"
  ss -ltnp | awk 'NR==1 || /:80|:443|:10050|:10051|:53/ {print "  - " $0}'
  echo "configs:"
  find /etc /opt /usr/local -maxdepth 3 \( -name 'zabbix_server.conf' -o -name 'zabbix_agent2.conf' -o -name 'zabbix.conf.php' -o -name '*zabbix*' \) 2>/dev/null | sort | sed 's/^/  - /'
} > "$ARTIFACTS_DIR/environment_inventory.txt"

echo "saved $ARTIFACTS_DIR/environment_inventory.txt"
