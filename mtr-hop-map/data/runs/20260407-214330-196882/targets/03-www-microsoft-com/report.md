# MTR Hop Map - www.microsoft.com

## Contexto

- destino do mapa: `www.microsoft.com`
- origem do MTR: `live`
- arquivo de replay: `-`
- run_id do lote: `20260407-214330-196882`
- slug do destino: `www-microsoft-com`
- dry_run: `False`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - www.microsoft.com`
- sysmapid: `14`
- grupo de hosts: `25`
- template: `10564`
- nenhuma escrita foi executada: `False`

## Metadata operacional do mapa

- source: `mtr-hop-map`
- target: `www.microsoft.com`
- target_slug: `www-microsoft-com`
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
- 07: `187.19.162.195` - `AS28126` - `BRISANET SERVICOS DE TELECOMUNICACOES S.A` - origem `whois-cymru`
- 08: `2.16.186.19` - `AS20940` - `AKAMAI-ASN1` - origem `whois-cymru`
- 09: `2.16.186.7` - `AS20940` - `AKAMAI-ASN1` - origem `whois-cymru`
- 10: `2.16.186.23` - `AS20940` - `AKAMAI-ASN1` - origem `whois-cymru`
- 11: `2.16.186.39` - `AS20940` - `AKAMAI-ASN1` - origem `whois-cymru`
- 12: `23.194.182.92` - `AS16625` - `Akamai Technologies, Inc.` - origem `whois-cymru`

## Hosts reconciliados

- criados na fase 1: `10825, 10826, 10827, 10828, 10829, 10830`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `True`
- mapa criado na fase 2: `False`
- hostids fase 1: `10784, 10785, 10825, 10780, 10781, 10782, 10783, 10826, 10827, 10828, 10829, 10830`
- hostids fase 2: `10829, 10780, 10781, 10782, 10783, 10784, 10785, 10825, 10826, 10827, 10828, 10830`
- linkids fase 1: `240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250`
- linkids fase 2: `240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250`

## Enrichment ASN

- modo de lookup: `online`
- cache local: `/srv/observabilidade-zabbix/mtr-hop-map/data/cache/asn_company_cache.json`
- whois com sucesso: `6`
- cache por IP: `0`
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
