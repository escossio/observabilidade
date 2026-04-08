# MTR Hop Map - www.primevideo.com

## Contexto

- destino do mapa: `www.primevideo.com`
- origem do MTR: `live`
- arquivo de replay: `-`
- run_id do lote: `20260407-214520-173289`
- slug do destino: `www-primevideo-com`
- dry_run: `True`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - www.primevideo.com`
- sysmapid: `None`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `True`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `www.primevideo.com`
- target_slug: `www-primevideo-com`
- mode: `live`
- last_trace: `20260407-214520-173289`
- dry_run: `True`
- tags nativas no sysmap: `False`

## Plano de reconciliação

- hosts cria: `0`
- hosts reutiliza: `7`
- hosts atualiza: `0`
- hosts saem do mapa: `0`
- links cria: `0`
- links reutiliza: `0`
- links saem do mapa: `0`

## Hops normalizados

- 01: `10.45.0.1` - `AS private` - `Private / local network` - origem `mtr-private`
- 02: `100.65.77.1` - `AS private` - `Private / local network` - origem `mtr-private`
- 03: `172.16.128.221` - `AS private` - `Private / local network` - origem `mtr-private`
- 04: `172.16.133.150` - `AS private` - `Private / local network` - origem `mtr-private`
- 05: `172.16.128.113` - `AS private` - `Private / local network` - origem `mtr-private`
- 06: `172.16.128.181` - `AS private` - `Private / local network` - origem `mtr-private`
- 07: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 08: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 09: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 10: `3.174.37.212` - `AS16509` - `Amazon.com, Inc.` - origem `cache-ip`

## Hosts reconciliados

- criados na fase 1: `-`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10819`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `True`
- mapa criado na fase 2: `True`
- hostids fase 1: ``
- hostids fase 2: ``
- linkids fase 1: ``
- linkids fase 2: ``

## Enrichment ASN

- modo de lookup: `online`
- cache local: `/srv/observabilidade-zabbix/mtr-hop-map/data/cache/asn_company_cache.json`
- whois com sucesso: `0`
- cache por IP: `1`
- cache por ASN: `0`
- fallback por hint MTR: `0`
- fallback desconhecido: `0`

## Artefatos

- `mtr_raw.json`
- `mtr_parsed.json`
- `mtr_normalized.json`
- `reconcile_phase1.json`
- `reconcile_phase2.json`
- `reconciliation_plan.json`
- `execution.json`
- `asn_summary.json`
- `map_metadata.json`
