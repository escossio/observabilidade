# MTR Hop Map POC - observabilidade.escossio.dev.br

## Contexto

- destino: `observabilidade.escossio.dev.br`
- mapa canônico: `MTR ASN - observabilidade.escossio.dev.br`
- sysmapid: `3`
- grupo de hosts: `25`
- template: `10564`
- mapa criado na primeira execução: `False`
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

- hostids na primeira execução: `10785, 10786, 10787, 10788, 10789, 10790, 10791, 10793, 10780, 10781, 10782, 10783, 10784`
- hostids na segunda execução: `10784, 10785, 10786, 10787, 10793, 10788, 10789, 10790, 10791, 10780, 10781, 10782, 10783`
- selementids na primeira execução: `12, 13, 14, 15, 16, 17, 18, 20, 7, 8, 9, 10, 11`
- selementids na segunda execução: `11, 12, 13, 14, 20, 15, 16, 17, 18, 7, 8, 9, 10`
- linkids na primeira execução: `29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40`
- linkids na segunda execução: `41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52`

## Artefatos

- `mtr_raw.json`
- `mtr_normalized.json`
- `reconcile_phase1.json`
- `reconcile_phase2.json`
