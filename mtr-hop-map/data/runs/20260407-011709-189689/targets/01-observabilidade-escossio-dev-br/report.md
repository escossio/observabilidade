# MTR Hop Map - observabilidade.escossio.dev.br

## Contexto

- destino do mapa: `observabilidade.escossio.dev.br`
- origem do MTR: `live`
- arquivo de replay: `-`
- run_id do lote: `20260407-011709-189689`
- slug do destino: `observabilidade-escossio-dev-br`
- dry_run: `True`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - observabilidade.escossio.dev.br`
- sysmapid: `5`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `True`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `observabilidade.escossio.dev.br`
- target_slug: `observabilidade-escossio-dev-br`
- mode: `live`
- last_trace: `20260407-011709-189689`
- dry_run: `True`
- tags nativas no sysmap: `False`

## Plano de reconciliação

- hosts cria: `0`
- hosts reutiliza: `13`
- hosts atualiza: `0`
- hosts saem do mapa: `1`
- links cria: `0`
- links reutiliza: `11`
- links saem do mapa: `1`

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
- 13: `104.21.4.50` - `AS13335` - `Cloudflare, Inc.` - origem `cache-ip`

## Hosts reconciliados

- criados na fase 1: `-`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10793`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `False`
- mapa criado na fase 2: `False`
- hostids fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10792`
- hostids fase 2: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10792`
- linkids fase 1: `67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 119`
- linkids fase 2: `67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 119`

## Enrichment ASN

- modo de lookup: `online`
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
- `reconciliation_plan.json`
- `execution.json`
- `asn_summary.json`
- `map_metadata.json`
