# Grafana dashboard semantic threshold fix

Data: `2026-04-04`

## Objetivo

- corrigir a semântica operacional do dashboard principal do Grafana sem mexer na baseline de coleta
- ajustar `RAM`, `CPU Temp`, serviços que exibiam valor cru e o peso visual de `localhost-a`
- preservar a grade, a compactação e a hierarquia já aprovadas

## Correções aplicadas

- `RAM` foi rebatizada para `Memória disponível` porque a fonte é `vm.memory.size[pavailable]`
- o threshold de `Memória disponível` passou a favorecer valor alto como estado saudável
- `Apache2`, `PostgreSQL` e `Zabbix Frontend` passaram a mapear valor operacional para `Up/Down`
- `localhost-a` foi tratado como diagnóstico secundário com cor neutra/atenção leve
- `CPU Temp` foi mantido com unidade `celsius` e threshold térmico coerente, sem mexer na coleta do `cpu.temp`

## Evidência técnica

- dashboard uid: `observabilidade-grafana`
- dashboard title: `Observabilidade Zabbix - Grafana`
- painel `Memória disponível` usa `vm.memory.size[pavailable]`
- painel `CPU Temp` continua ligado ao item `CPU temperature` / `cpu.temp`
- os cards de serviço permanecem como `stat` com mapeamento operacional

## Resultado esperado

- memória disponível deixa de ser lida como falha quando o valor está alto
- temperatura fica visualmente separada de estado indisponível
- serviços principais deixam de mostrar contagem cru
- `localhost-a` deixa de competir com os painéis críticos
- o layout geral continua intacto e sem rolagem
