# MTR Hop Map - dell.com

## Contexto

- destino do mapa: `dell.com`
- origem do MTR: `replay`
- arquivo de replay: `/srv/observabilidade-zabbix/mtr-hop-map/data/replays/dell-com-route.json`
- run_id do lote: `20260407-025947-416316`
- slug do destino: `dell-com`
- dry_run: `True`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - dell.com`
- sysmapid: `None`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `True`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `dell.com`
- target_slug: `dell-com`
- mode: `replay`
- last_trace: `20260407-025947-416316`
- dry_run: `True`
- tags nativas no sysmap: `False`

## Plano de reconciliação

- hosts cria: `0`
- hosts reutiliza: `17`
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
- 07: `172.16.128.182` - `AS private` - `Private / local network` - origem `mtr-private`
- 08: `172.16.128.62` - `AS private` - `Private / local network` - origem `mtr-private`
- 09: `172.16.128.178` - `AS private` - `Private / local network` - origem `mtr-private`
- 10: `84.16.6.34` - `AS12956` - `TELXIUS TELXIUS Cable` - origem `cache-ip`
- 11: `94.142.98.175` - `AS12956` - `TELXIUS TELXIUS Cable` - origem `cache-ip`
- 12: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 13: `192.205.32.109` - `AS7018` - `AT&T Enterprises, LLC` - origem `cache-ip`
- 14: `32.130.89.4` - `AS7018` - `AT&T Enterprises, LLC` - origem `cache-ip`
- 15: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 16: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 17: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 18: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 19: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 20: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 21: `12.123.154.54` - `AS7018` - `AT&T Enterprises, LLC` - origem `cache-ip`
- 22: `12.122.153.181` - `AS7018` - `AT&T Enterprises, LLC` - origem `cache-ip`
- 23: `12.252.89.6` - `AS7018` - `AT&T Enterprises, LLC` - origem `cache-ip`
- 24: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 25: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 26: `*` - `AS???` - `No response` - origem `mtr-no-response`
- 27: `143.166.30.172` - `AS3614` - `Dell, Inc.` - origem `cache-ip`

## Hosts reconciliados

- criados na fase 1: `-`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10802, 10803, 10804, 10805, 10806, 10807, 10808, 10809, 10810, 10811`
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
- cache por IP: `8`
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
