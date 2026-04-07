# MTR Hop Map - wiki.mikrotik.com

## Contexto

- destino do mapa: `wiki.mikrotik.com`
- origem do MTR: `replay`
- arquivo de replay: `/srv/observabilidade-zabbix/mtr-hop-map/data/replays/wiki-mikrotik-com-route.json`
- run_id do lote: `20260407-030220-957449`
- slug do destino: `wiki-mikrotik-com`
- dry_run: `True`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - wiki.mikrotik.com`
- sysmapid: `None`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `True`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `wiki.mikrotik.com`
- target_slug: `wiki-mikrotik-com`
- mode: `replay`
- last_trace: `20260407-030220-957449`
- dry_run: `True`
- tags nativas no sysmap: `False`

## Plano de reconciliação

- hosts cria: `0`
- hosts reutiliza: `13`
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
- 07: `138.204.238.149` - `AS52320` - `GlobeNet Cabos Submarinos Colombia, S.A.S.` - origem `cache-ip`
- 08: `200.16.69.2` - `AS52320` - `GlobeNet Cabos Submarinos Colombia, S.A.S.` - origem `cache-ip`
- 09: `62.115.50.180` - `AS1299` - `TWELVE99 Arelion, fka Telia Carrier` - origem `cache-ip`
- 10: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 11: `80.91.254.90` - `AS1299` - `TWELVE99 Arelion, fka Telia Carrier` - origem `cache-ip`
- 12: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 13: `62.115.142.191` - `AS1299` - `TWELVE99 Arelion, fka Telia Carrier` - origem `cache-ip`
- 14: `213.248.84.33` - `AS1299` - `TWELVE99 Arelion, fka Telia Carrier` - origem `cache-ip`
- 15: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 16: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 17: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 18: `159.148.147.244` - `AS51894` - `AS_MIKROTIKLS` - origem `cache-ip`

## Hosts reconciliados

- criados na fase 1: `-`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10812, 10813, 10814, 10815, 10816, 10817, 10818`
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
- cache por IP: `7`
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
