#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - <<'PY'
import json
import sys
from pathlib import Path

sys.path.insert(0, '/srv/observabilidade-zabbix/mtr-hop-map')
from src.config import load_config
from src.zabbix_api import ZabbixAPI

config_path = Path('/srv/observabilidade-zabbix/mtr-hop-map/sources/debian2-1.json')
cfg = json.loads(config_path.read_text())
z = cfg['zabbix_monitoring']

loaded = load_config('debian2-1')
api = ZabbixAPI(loaded.zabbix_api_url, loaded.zabbix_user, loaded.zabbix_password)
api.login()

group = api.ensure_host_group(z['group'])
template = api.ensure_icmp_template(z['template'], loaded.icmp_template_group)
result = api.ensure_host(
    hostname=z['host_name'],
    visible_name=z['visible_name'],
    groupid=group['groupid'],
    templateid=template['templateid'],
    ip=cfg['host'],
    tags=[
        {'tag': 'role', 'value': z['tag_role']},
        {'tag': 'source', 'value': cfg['name']},
        {'tag': 'monitoring', 'value': 'icmp'},
    ],
)

out = {
    'status': 'ok',
    'hostid': result.host['hostid'],
    'hostname': result.host['host'],
    'visible_name': result.host['name'],
    'action': result.action,
    'match_source': result.match_source,
    'warnings': result.warnings,
    'group': group['name'],
    'template': template['host'],
}
print(json.dumps(out, indent=2, ensure_ascii=False))
PY
