# MTR Hop Map POC - observabilidade.escossio.dev.br

## Contexto

- destino: `observabilidade.escossio.dev.br`
- mapa canônico: `MTR ASN - observabilidade.escossio.dev.br`
- sysmapid: `4`
- grupo de hosts: `25`
- template: `10564`
- mapa criado na primeira execução: `True`
- mapa criado na segunda execução: `False`

## Hops normalizados

- 01: `10.45.0.1` - `AS private` - `Private / local network`
- 02: `100.65.77.1` - `AS private` - `Private / local network`
- 03: `172.16.128.221` - `AS private` - `Private / local network`
- 04: `172.16.133.150` - `AS private` - `Private / local network`
- 05: `172.16.128.113` - `AS private` - `Private / local network`
- 06: `172.16.128.181` - `AS private` - `Private / local network`
- 07: `172.16.128.182` - `AS private` - `Private / local network`
- 08: `172.16.130.122` - `AS private` - `Private / local network`
- 09: `172.16.134.242` - `AS private` - `Private / local network`
- 10: `172.16.135.209` - `AS private` - `Private / local network`
- 11: `172.16.128.42` - `AS private` - `Private / local network`
- 12: `187.19.161.199` - `AS28126` - `BRISANET SERVICOS DE TELECOMUNICACOES S.A`
- 13: `104.21.4.50` - `AS13335` - `Cloudflare, Inc.`

## Idempotência

- hostids na primeira execução: `10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10793`
- hostids na segunda execução: `10790, 10791, 10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10793`
- selementids na primeira execução: `21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33`
- selementids na segunda execução: `31, 32, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33`
- linkids na primeira execução: `53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64`
- linkids na segunda execução: `53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 65, 66`

## Artefatos

- `mtr_raw.json`
- `mtr_normalized.json`
- `reconcile_phase1.json`
- `reconcile_phase2.json`
