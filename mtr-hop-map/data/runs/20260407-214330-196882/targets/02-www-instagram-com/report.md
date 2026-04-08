# MTR Hop Map - www.instagram.com

## Contexto

- destino do mapa: `www.instagram.com`
- origem do MTR: `live`
- arquivo de replay: `-`
- run_id do lote: `20260407-214330-196882`
- slug do destino: `www-instagram-com`
- dry_run: `False`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - www.instagram.com`
- sysmapid: `13`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `False`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `www.instagram.com`
- target_slug: `www-instagram-com`
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
- 07: `177.37.221.191` - `AS28126` - `BRISANET SERVICOS DE TELECOMUNICACOES S.A` - origem `whois-cymru`
- 08: `147.75.214.158` - `AS???` - `Unknown ASN` - origem `fallback-unknown`
- 09: `129.134.60.178` - `AS32934` - `Facebook, Inc.` - origem `whois-cymru`
- 10: `163.77.194.43` - `AS???` - `Unknown ASN` - origem `fallback-unknown`
- 11: `57.144.128.34` - `AS32934` - `Facebook, Inc.` - origem `whois-cymru`

## Hosts reconciliados

- criados na fase 1: `10820, 10821, 10822, 10823, 10824`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `True`
- mapa criado na fase 2: `False`
- hostids fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10820, 10821, 10822, 10823, 10824`
- hostids fase 2: `10780, 10783, 10784, 10781, 10782, 10785, 10820, 10821, 10822, 10823, 10824`
- linkids fase 1: `230, 231, 232, 233, 234, 235, 236, 237, 238, 239`
- linkids fase 2: `230, 231, 232, 233, 234, 235, 236, 237, 238, 239`

## Enrichment ASN

- modo de lookup: `online`
- cache local: `/srv/observabilidade-zabbix/mtr-hop-map/data/cache/asn_company_cache.json`
- whois com sucesso: `3`
- cache por IP: `0`
- cache por ASN: `0`
- fallback por hint MTR: `0`
- fallback desconhecido: `2`

## Eventos de fallback

- whois sem linha util para 147.75.214.158
- fallback sem ASN para 147.75.214.158
- whois sem linha util para 163.77.194.43
- fallback sem ASN para 163.77.194.43

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
