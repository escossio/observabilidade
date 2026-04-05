# Livecopilot Grafana panel fix

Data: `2026-04-05`

## Causa raiz

- os cards do Livecopilot já estavam visíveis no dashboard principal
- a renderização mostrava `N/A` porque os itens usados na query eram strings HTTP/systemd
- o datasource `alexanderzobnin-zabbix-datasource` respondeu com `frames: 0` para a query anterior dos cards

## Correção aplicada

- foram criados itens numéricos derivados no Zabbix para cada camada do Livecopilot
- o dashboard principal do Grafana foi regravado para ancorar os cards nesses `itemids`
- os cards mantiveram o mesmo layout e a mesma posição no dashboard

## Itens derivados usados no Grafana

- `69631` `Livecopilot Serviço estado`
- `69632` `Livecopilot Apache Edge estado`
- `69633` `Livecopilot Frontend Público estado`
- `69634` `Livecopilot Public Health estado`
- `69635` `Livecopilot Backend Health estado`
- `69636` `Livecopilot Backend Status estado`
- `69637` `Livecopilot Backend API estado`

## Query final

- `queryType: 3`
- `resultFormat: time_series`
- `itemids` explícito em cada card
- mapeamento numérico:
  - `1 -> Up`
  - `0 -> Down`
  - `Livecopilot Backend Status`: `1 -> OK`

## Evidência por API

- `api/ds/query` passou a retornar `frames: 1` para todos os cards do bloco
- o dashboard principal foi salvo na versão `17`

## Evidência visual

- captura autenticada do dashboard mostra todos os cards do Livecopilot em verde, com leitura operacional real
- nenhum card do bloco permaneceu em `N/A`
