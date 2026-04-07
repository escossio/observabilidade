# Handoff - MTR Hop Map Aggregation

## Rodada atual

- fonte de verdade:
  - replay controlado para os 4 alvos desta rodada
  - corpus consolidado em `data/runs/20260407-030220-957449/`
- o mapa canônico único foi expandido no Zabbix:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- a última expansão anexou novos ramos para:
  - `8.8.8.8` / Google
  - `9.9.9.9` / Quad9
  - `dell.com` / Dell
  - `wiki.mikrotik.com` / Mikrotik
- o grafo final publicado ficou com:
  - `39` nós
  - `38` links
- o tronco comum permaneceu único
- a borda candidata `187.19.161.199` continua como candidato forte, não confirmação absoluta
- `177.37.220.17` e `177.37.220.18` continuam sem evidência observada no corpus atual

## O que foi entregue

- camada offline de agregação sobre os artifacts do `mtr-hop-map`
- inventário agregado por IP
- rankings de recorrência
- ranking de borda Brisanet
- classificação inicial de IX/PTT e CDN
- leitura explícita para `177.37.220.17` e `177.37.220.18`

## O que a camada não faz

- não altera os mapas do Zabbix
- não reexecuta reconciliação
- não cria uma plataforma nova
- não trata a classificação como verdade final

## Próximos passos

- aumentar o corpus com mais destinos
- calibrar heurísticas de IX/PTT e CDN com novos traces
- separar melhor os casos DNS infra Brisanet quando surgirem no corpus
