# MTR Hop Map - Execução em lote

## Contexto

- run_id: `20260407-214330-196882`
- destinos solicitados: `8`
- destinos executados: `8`
- sucessos: `5`
- falhas: `3`
- modo dry-run: `False`

## Resultados por destino

- `www.primevideo.com` - status `error` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/01-www-primevideo-com` - erro `Zabbix API error in map.create: {'code': -32500, 'message': 'Application error.', 'data': 'No permissions to referred object or it does not exist!'}`
- `www.instagram.com` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/02-www-instagram-com` - mapa `MTR ASN - www.instagram.com` / sysmapid `13`
- `www.microsoft.com` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/03-www-microsoft-com` - mapa `MTR ASN - www.microsoft.com` / sysmapid `14`
- `account.microsoft.com` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/04-account-microsoft-com` - mapa `MTR ASN - account.microsoft.com` / sysmapid `15`
- `outlook.live.com` - status `error` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/05-outlook-live-com` - erro `Zabbix API error in map.create: {'code': -32500, 'message': 'Application error.', 'data': 'No permissions to referred object or it does not exist!'}`
- `www.xbox.com` - status `error` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/06-www-xbox-com` - erro `Zabbix API error in map.create: {'code': -32500, 'message': 'Application error.', 'data': 'No permissions to referred object or it does not exist!'}`
- `8.8.8.8` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/07-8-8-8-8` - mapa `MTR ASN - 8.8.8.8` / sysmapid `11`
- `9.9.9.9` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-214330-196882/targets/08-9-9-9-9` - mapa `MTR ASN - 9.9.9.9` / sysmapid `12`
