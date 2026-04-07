# MTR Hop Map - one.one.one.one-replay-validation

## Contexto

- destino do mapa: `one.one.one.one-replay-validation`
- origem do MTR: `replay`
- arquivo de replay: `/srv/observabilidade-zabbix/mtr-hop-map/data/replays/one-one-one-one-route-a.json`
- run_id do lote: `20260407-003511`
- slug do destino: `one-one-one-one-replay-validation`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - one.one.one.one-replay-validation`
- sysmapid: `9`
- grupo de hosts: `25`
- template: `10564`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `one.one.one.one-replay-validation`
- target_slug: `one-one-one-one-replay-validation`
- mode: `replay`
- last_trace: `20260407-003511`
- tags nativas no sysmap: `False`

## Hops normalizados

- 01: `10.45.0.1` - `AS private` - `Private / local network` - origem `mtr-private`
- 02: `100.65.77.1` - `AS private` - `Private / local network` - origem `mtr-private`
- 03: `172.16.128.221` - `AS private` - `Private / local network` - origem `mtr-private`
- 04: `172.16.133.150` - `AS private` - `Private / local network` - origem `mtr-private`
- 05: `172.16.128.113` - `AS private` - `Private / local network` - origem `mtr-private`
- 06: `172.16.128.181` - `AS private` - `Private / local network` - origem `mtr-private`
- 07: `172.16.128.182` - `AS private` - `Private / local network` - origem `mtr-private`
- 08: `172.16.130.122` - `AS private` - `Private / local network` - origem `mtr-private`
- 09: `172.16.134.242` - `AS private` - `Private / local network` - origem `mtr-private`
- 10: `172.16.135.209` - `AS private` - `Private / local network` - origem `mtr-private`
- 11: `172.16.128.42` - `AS private` - `Private / local network` - origem `mtr-private`
- 12: `187.19.161.199` - `AS28126` - `BRISANET SERVICOS DE TELECOMUNICACOES S.A` - origem `cache-ip`
- 13: `1.0.0.1` - `AS13335` - `Cloudflare, Inc.` - origem `cache-ip`

## Hosts reconciliados

- criados na fase 1: `-`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10794`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `True`
- mapa criado na fase 2: `False`
- hostids fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10794`
- hostids fase 2: `10780, 10781, 10782, 10783, 10784, 10791, 10794, 10785, 10786, 10787, 10788, 10789, 10790`
- linkids fase 1: `120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131`
- linkids fase 2: `120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131`

## Enrichment ASN

- modo de lookup: `offline`
- cache local: `/srv/observabilidade-zabbix/mtr-hop-map/data/cache/asn_company_cache.json`
- whois com sucesso: `0`
- cache por IP: `2`
- cache por ASN: `0`
- fallback por hint MTR: `0`
- fallback desconhecido: `0`

## Artefatos

- `mtr_raw.json`
- `mtr_parsed.json`
- `mtr_normalized.json`
- `reconcile_phase1.json`
- `reconcile_phase2.json`
- `execution.json`
- `asn_summary.json`
- `map_metadata.json`
