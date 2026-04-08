# MTR Hop Map - account.microsoft.com

## Contexto

- destino do mapa: `account.microsoft.com`
- origem do MTR: `live`
- arquivo de replay: `-`
- run_id do lote: `20260407-214330-196882`
- slug do destino: `account-microsoft-com`
- dry_run: `False`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - account.microsoft.com`
- sysmapid: `15`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `False`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `account.microsoft.com`
- target_slug: `account-microsoft-com`
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
- 07: `187.19.162.195` - `AS28126` - `BRISANET SERVICOS DE TELECOMUNICACOES S.A` - origem `cache-ip`
- 08: `2.16.186.20` - `AS20940` - `AKAMAI-ASN1` - origem `whois-cymru`
- 09: `2.16.186.11` - `AS20940` - `AKAMAI-ASN1` - origem `whois-cymru`
- 10: `2.16.186.24` - `AS20940` - `AKAMAI-ASN1` - origem `whois-cymru`
- 11: `2.16.186.39` - `AS20940` - `AKAMAI-ASN1` - origem `cache-ip`
- 12: `23.194.181.154` - `AS16625` - `Akamai Technologies, Inc.` - origem `whois-cymru`

## Hosts reconciliados

- criados na fase 1: `10831, 10832, 10833, 10834`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10825, 10829`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `True`
- mapa criado na fase 2: `False`
- hostids fase 1: `10834, 10832, 10833, 10829, 10782, 10783, 10784, 10780, 10781, 10785, 10825, 10831`
- hostids fase 2: `10832, 10833, 10829, 10780, 10781, 10782, 10783, 10784, 10785, 10825, 10831, 10834`
- linkids fase 1: `251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261`
- linkids fase 2: `251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261`

## Enrichment ASN

- modo de lookup: `online`
- cache local: `/srv/observabilidade-zabbix/mtr-hop-map/data/cache/asn_company_cache.json`
- whois com sucesso: `4`
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
