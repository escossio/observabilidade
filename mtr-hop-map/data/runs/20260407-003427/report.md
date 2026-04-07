# MTR Hop Map - Execução em lote

## Contexto

- run_id: `20260407-003427`
- destinos solicitados: `3`
- destinos executados: `3`
- sucessos: `2`
- falhas: `1`
- modo dry-run: `False`

## Resultados por destino

- `observabilidade.escossio.dev.br` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-003427/targets/01-observabilidade-escossio-dev-br` - mapa `MTR ASN - observabilidade.escossio.dev.br` / sysmapid `5`
- `one.one.one.one` - status `ok` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-003427/targets/02-one-one-one-one` - mapa `MTR ASN - one.one.one.one` / sysmapid `8`
- `invalid.invalid` - status `error` - modo `live` - target_dir `/srv/observabilidade-zabbix/mtr-hop-map/data/runs/20260407-003427/targets/03-invalid-invalid` - erro `saida JSON invalida do mtr para invalid.invalid: mtr: Failed to resolve host: invalid.invalid: Name or service not known`
