# Handoff - MTR Hop Map Aggregation

## Rodada atual

- fonte de verdade:
  - traces live válidos para `www.primevideo.com`, `www.instagram.com`, `www.microsoft.com`, `account.microsoft.com`, `outlook.live.com`, `www.xbox.com`, `8.8.8.8` e `9.9.9.9`
  - corpus consolidado em `data/runs/20260407-214330-196882/` e `data/runs/20260407-214520-173289/`
- o mapa canônico único foi expandido no Zabbix:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- a última expansão anexou novos ramos para:
  - `www.primevideo.com` / Prime Video / Amazon
  - `www.instagram.com` / Instagram / Meta
  - `www.microsoft.com` / Microsoft via Akamai
  - `account.microsoft.com` / Microsoft via Akamai
  - `outlook.live.com` / Microsoft
  - `www.xbox.com` / Microsoft via Akamai
- o grafo final publicado ficou com:
  - `68` selements
  - `65` links
- o tronco comum até `172.16.128.181` permaneceu único
- a borda candidata `187.19.161.199` continua como candidato forte, não confirmação absoluta
- `177.37.220.17` e `177.37.220.18` continuam sem evidência observada no corpus atual
- a seleção Akamai foi validada por DNS:
  - `www.microsoft.com -> e13678.dscb.akamaiedge.net`
  - `account.microsoft.com -> e9412.b.akamaiedge.net`
  - `www.xbox.com -> e1822.dsca.akamaiedge.net`

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
