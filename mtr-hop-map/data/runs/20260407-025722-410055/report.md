# MTR Hop Map - Execução em lote

## Contexto

- run_id: `20260407-025722-410055`
- destinos solicitados: `4`
- destinos executados: `4`
- sucessos: `2`
- falhas: `2`
- modo dry-run: `False`

## Resultados por destino

- `8.8.8.8` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-025722-410055/targets/01-8-8-8-8` - mapa `MTR ASN - 8.8.8.8` / sysmapid `11`
- `9.9.9.9` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-025722-410055/targets/02-9-9-9-9` - mapa `MTR ASN - 9.9.9.9` / sysmapid `12`
- `dell.com` - status `error` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-025722-410055/targets/03-dell-com` - erro `Zabbix API error in map.create: {'code': -32500, 'message': 'Application error.', 'data': 'No permissions to referred object or it does not exist!'}`
- `wiki.mikrotik.com` - status `error` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-025722-410055/targets/04-wiki-mikrotik-com` - erro `Zabbix API error in map.create: {'code': -32500, 'message': 'Application error.', 'data': 'No permissions to referred object or it does not exist!'}`
