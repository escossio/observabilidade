# Grafana dashboard density rollback

Data: `2026-04-04`

## Motivo

- a compactação anterior deixou os cards stat com leitura visual fraca
- o valor passou a competir menos do que deveria com o título
- a organização estava boa, mas a legibilidade caiu em telas menores

## Ajuste aplicado

- cards `stat` principais voltaram para altura `2`
- o topo com `Resumo`, `Problemas`, `Web Público` e `DNS Público` foi preservado
- os títulos curtos permanecem
- queries, thresholds, datasource e itens permaneceram intactos

## Evidência técnica

- dashboard uid: `observabilidade-grafana`
- dashboard version: `15`
- cards `stat` com altura `2`
- cards `table` com altura `2`
- painel `Temperatura CPU` continua usando `queryType: 3` com `itemids: 69621`

## Resultado

- valores voltaram a ter protagonismo visual
- o dashboard segue organizado
- a compactação continua moderada, sem voltar ao tamanho pesado antigo
- não houve alteração na lógica do painel
