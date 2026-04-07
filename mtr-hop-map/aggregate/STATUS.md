# Status

## 2026-04-07 - mapa unificado expandido com novos ramos publicados

- fonte de verdade da rodada:
  - `replay` controlado para `8.8.8.8`, `9.9.9.9`, `dell.com` e `wiki.mikrotik.com`
  - corpus consolidado no run `20260407-030220-957449`
- o mapa único `MTR Unified - Brisanet Observed` foi atualizado in-place no `sysmapid 10`
- a rodada anexou novos ramos para:
  - `8.8.8.8` / Google
  - `9.9.9.9` / Quad9
  - `dell.com` / Dell
  - `wiki.mikrotik.com` / Mikrotik
- o snapshot final do Zabbix ficou com:
  - `39` elementos
  - `38` links
- o tronco comum permaneceu único e sem duplicação de IPs equivalentes
- a borda candidata `187.19.161.199` continuou visível como candidato forte
- `177.37.220.17` e `177.37.220.18` continuam fora do backbone por ausência de evidência no corpus


## 2026-04-07 - mapa agregado unificado publicado no Zabbix

- o mapa agregado passou a ser único e canônico:
  - `MTR Unified - Brisanet Observed`
- o sysmap atualizado in-place foi o `10`
- a publicação consolidou no mesmo grafo:
  - tronco comum recorrente
  - borda Brisanet candidata
  - saídas CDN
  - watchlist DNS
- artefatos gerados na rodada:
  - `unified_nodes.json`
  - `unified_edges.json`
  - `unified_map_plan.json`
  - `report.md`
  - `zabbix_map_snapshot.json`
- validação real:
  - `15` nós
  - `13` links
  - `187.19.161.199` permanece como candidato fortíssimo de borda, não confirmação absoluta
  - `177.37.220.17` e `177.37.220.18` continuam fora do backbone por ausência de evidência no corpus

## 2026-04-07 - camada de agregação de traces criada

- loader robusto lendo múltiplos runs e replays existentes
- inventário agregado por IP/hop
- recorrência de caminhos e pares de hops
- classificação heurística com confiança explícita
- leitura dedicada para `177.37.220.17` e `177.37.220.18`
- saídas estruturadas em JSON/CSV e relatório humano
