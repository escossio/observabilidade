# MTR Hop Map - observabilidade.escossio.dev.br-fallback-validation

## Contexto

- destino do mapa: `observabilidade.escossio.dev.br-fallback-validation`
- origem do MTR: `replay`
- arquivo de replay: `/srv/observabilidade-zabbix/mtr-hop-map/data/replays/observabilidade-route-b.json`
- modelo de identidade: `global-ip`
- mapa canônico: `MTR ASN - observabilidade.escossio.dev.br-fallback-validation`
- sysmapid: `7`
- grupo de hosts: `25`
- template: `10564`

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
- 12: `187.19.161.199` - `AS28126` - `Unknown ASN` - origem `mtr-as-hint-fallback`
- 13: `172.67.131.172` - `AS13335` - `Unknown ASN` - origem `mtr-as-hint-fallback`

## Hosts reconciliados

- criados na fase 1: `-`
- reaproveitados na fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10792`
- atualizados na fase 1: `-`

## Idempotencia

- mapa criado na fase 1: `True`
- mapa criado na fase 2: `False`
- hostids fase 1: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10792`
- hostids fase 2: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10792`
- linkids fase 1: `93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104`
- linkids fase 2: `93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104`

## Enrichment ASN

- modo de lookup: `offline`
- cache local: `/srv/observabilidade-zabbix/mtr-hop-map/data/cache/offline-empty-cache.json`
- whois com sucesso: `0`
- cache por IP: `0`
- cache por ASN: `0`
- fallback por hint MTR: `2`
- fallback desconhecido: `0`

## Eventos de fallback

- fallback ASN hint usado para 187.19.161.199: AS28126
- fallback ASN hint usado para 172.67.131.172: AS13335

## Artefatos

- `mtr_raw.json`
- `mtr_normalized.json`
- `reconcile_phase1.json`
- `reconcile_phase2.json`
- `execution.json`
- `asn_summary.json`
