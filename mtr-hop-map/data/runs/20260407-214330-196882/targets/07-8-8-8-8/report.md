# MTR Hop Map - 8.8.8.8

## Contexto

- destino do mapa: `8.8.8.8`
- origem do MTR: `live`
- arquivo de replay: `-`
- run_id do lote: `20260407-214330-196882`
- slug do destino: `8-8-8-8`
- dry_run: `False`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - 8.8.8.8`
- sysmapid: `11`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `False`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `8.8.8.8`
- target_slug: `8-8-8-8`
- mode: `live`
- last_trace: `20260407-214330-196882`
- dry_run: `False`
- tags nativas no sysmap: `False`

## Plano de reconciliação

- hosts cria: `0`
- hosts reutiliza: `0`
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
- 07: `142.250.166.72` - `AS15169` - `Google LLC` - origem `cache-ip`
- 08: `108.170.226.233` - `AS15169` - `Google LLC` - origem `cache-ip`
- 09: `192.178.110.171` - `AS15169` - `Google LLC` - origem `cache-ip`
- 10: `8.8.8.8` - `AS15169` - `Google LLC` - origem `cache-ip`

## Hosts reconciliados

- criados na fase 1: `-`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10795, 10796, 10797, 10798`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `False`
- mapa criado na fase 2: `False`
- hostids fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10795, 10796, 10797, 10798`
- hostids fase 2: `10780, 10781, 10782, 10783, 10784, 10785, 10795, 10796, 10797, 10798`
- linkids fase 1: `159, 160, 161, 162, 163, 164, 165, 166, 167`
- linkids fase 2: `159, 160, 161, 162, 163, 164, 165, 166, 167`

## Enrichment ASN

- modo de lookup: `online`
- cache local: `/srv/observabilidade-zabbix/mtr-hop-map/data/cache/asn_company_cache.json`
- whois com sucesso: `0`
- cache por IP: `4`
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
