# Status

## 2026-04-07 - acabamento visual aplicado ao mapa unificado

- o mapa canônico único continua sendo:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- a rodada foi visual בלבד:
  - canvas ampliado para `2440x1846`
  - ícones padronizados por classe
  - labels encurtados
  - famílias externas separadas em bandas
- o tronco principal continua horizontal e legível
- as ligações foram preservadas, sem recálculo da topologia
- snapshot visual final disponível em `visual_layout_plan.json` e `zabbix_map_snapshot.json`


## 2026-04-07 - mapa unificado expandido com novos ramos e Akamai validado por DNS

- o mapa canônico único permaneceu:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- a rodada incorporou traces live válidos e consolidou novos ramos para:
  - `www.primevideo.com` / Prime Video / Amazon
  - `www.instagram.com` / Instagram / Meta
  - `www.microsoft.com` / Microsoft via Akamai
  - `account.microsoft.com` / Microsoft via Akamai
  - `outlook.live.com` / Microsoft
  - `www.xbox.com` / Microsoft via Akamai
- a pré-seleção Akamai foi baseada em hostname final de edge:
  - `www.microsoft.com -> e13678.dscb.akamaiedge.net`
  - `account.microsoft.com -> e9412.b.akamaiedge.net`
  - `www.xbox.com -> e1822.dsca.akamaiedge.net`
- a publicação final no Zabbix ficou com:
  - `68` selements
  - `65` links
- `8.8.8.8` e `9.9.9.9` reforçaram famílias já existentes sem criar duplicação de IP
- o tronco comum até `172.16.128.181` permaneceu estável
- os mapas por destino permaneceram intactos


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
- o snapshot e o plano unificado foram conferidos no diretório `data/runs/20260407-030253-324917/`


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
