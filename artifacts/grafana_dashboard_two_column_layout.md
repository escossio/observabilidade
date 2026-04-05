# Grafana dashboard two-column layout

Data: `2026-04-05`

## Estado inicial

- o topo do dashboard já estava consolidado com `Resumo`, `Problemas`, `Web Público` e `DNS Público`
- os cards de serviços e telemetria funcionavam, mas a leitura ainda estava distribuída em blocos misturados
- a meta desta rodada foi reorganizar somente a posição visual dos painéis

## Layout final

### Coluna esquerda

- `Zabbix`
- `Agent2`
- `Apache`
- `Grafana`
- `Cloudflared`
- `Unbound`
- `PostgreSQL`
- `SSH`
- `Livecopilot Serviço`
- `Livecopilot Apache Edge`
- `Livecopilot Frontend Público`
- `Livecopilot Public Health`
- `Livecopilot Backend Health`
- `Livecopilot Backend Status`
- `Livecopilot Backend API`
- `Grafana Local`
- `Zabbix Frontend`
- `DNS Local`

### Coluna direita

- `CPU`
- `Memória Livre`
- `Temperatura CPU`

## Regras visuais preservadas

- serviços continuam exibindo nome + estado dentro da própria caixa
- telemetria continua exibindo valor numérico real
- o bloco Livecopilot permanece íntegro na coluna de serviços
- o topo do dashboard não foi alterado

## Evidência técnica

- o dashboard foi salvo com sucesso na versão `18`
- a captura autenticada confirmou a separação visual em duas colunas
- a telemetria ficou isolada à direita
- os serviços ficaram agrupados à esquerda sem mexer em coleta, items ou triggers
