# Handoff - MTR Hop Map Aggregation

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

