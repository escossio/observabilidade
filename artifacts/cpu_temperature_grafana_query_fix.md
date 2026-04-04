# CPU temperature Grafana query fix

Data: `2026-04-04`

## Causa raiz

- o painel `CPU Temp` estava em modo `Metrics` (`queryType: "0"`)
- a descoberta por nome de item não estava devolvendo série para esse item no datasource Zabbix
- a validação por `/api/ds/query` retornava `frames: 0`
- a mesma métrica passou a responder quando foi ancorada diretamente pelo `itemid`

## Query antiga

- `queryType: "0"`
- `host.filter: "agt01"`
- `group.filter: "Linux servers"`
- `application.filter: "General"`
- `item.filter: "CPU temperature"`
- sem `itemids`

## Query final

- `queryType: "3"`
- `host.filter: "agt01"`
- `group.filter: "Linux servers"`
- `application.filter: ""`
- `item.filter: ""`
- `itemids: "69621"`

## Evidência do datasource

- `/api/ds/query` passou a retornar `frames: 1`
- label retornada pelo datasource:
  - host: `agt01`
  - item: `CPU temperature`
  - item_key: `cpu.temp`
- valor retornado:
  - `38.5`

## Evidência do painel

- dashboard: `Observabilidade Zabbix - Grafana`
- painel: `CPU Temp`
- unidade: `celsius`
- valor validado: `38.5 C`
- referência antiga por nome não foi mantida como fonte de dados

## Resultado

- o painel deixou de depender da descoberta por nome para essa métrica
- a série voltou a aparecer no Grafana
- a correção ficou restrita ao painel `CPU Temp`, sem impacto no layout geral ou nos demais cards
