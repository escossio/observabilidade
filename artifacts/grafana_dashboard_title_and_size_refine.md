# Grafana dashboard title and size refine

Data: `2026-04-04`

## Objetivo

- encurtar os títulos dos cards para nomenclatura operacional mais limpa
- reduzir a altura dos cards para melhorar densidade visual
- preservar queries, thresholds e o comportamento funcional já validado

## Títulos ajustados

- `Zabbix Server` -> `Zabbix`
- `Apache2` -> `Apache`
- `Memória disponível` -> `Memória Livre`
- `localhost-a` -> `DNS Local`
- `CPU Temp` -> `Temperatura CPU`

## Compactação aplicada

- cards `stat` passaram para altura `1`
- cards `table` permaneceram com altura `2`
- o topo com `Resumo`, `Problemas`, `Web Público` e `DNS Público` foi preservado
- a grade principal foi reorganizada para preencher melhor os vazios

## Evidência técnica

- dashboard uid: `observabilidade-grafana`
- dashboard version: `14`
- queries mantidas sem alteração
- thresholds mantidos sem alteração
- painel `Temperatura CPU` continua usando `queryType: 3` com `itemids: 69621`

## Resultado

- títulos mais curtos e mais operacionais
- cards menores
- leitura mais densa e limpa
- painel principal permanece sem scroll
