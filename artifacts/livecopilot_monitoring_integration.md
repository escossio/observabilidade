# Livecopilot monitoring integration

Data da integração: `2026-04-04`

Fonte canônica da arquitetura: `/lab/projects/livecopilot/docs/ARCHITECTURE_CURRENT.md`

## Objetivo

- distinguir falha de borda Apache, frontend estático, backend FastAPI e serviço systemd
- manter ruído baixo
- evitar checks redundantes
- preservar os checks atuais de observabilidade do host

## Camadas monitoradas

### 1. Serviço

- `livecopilot-semantic-api.service`
- pergunta respondida: o processo do backend está vivo?

### 2. Borda Apache

- `http://127.0.0.1:8080/`
- pergunta respondida: a borda local do Livecopilot está publicando a raiz?

### 3. Frontend estático público

- `http://livecopilot.escossio.dev.br/`
- pergunta respondida: a publicação pública entrega a UI estática?

### 4. Backend Health

- `http://127.0.0.1:8099/health`
- pergunta respondida: o FastAPI respondeu localmente e no caminho publicado?

### 5. Backend operacional

- `http://127.0.0.1:8099/status`
- `http://127.0.0.1:8099/api/panel/summary`
- pergunta respondida: a API operacional continua íntegra?

## Checks propostos nos inventários

### `config/services.yaml`

- `livecopilot-semantic-api`

### `config/web_checks.yaml`

- `livecopilot-apache-edge`
- `livecopilot-public-frontend`
- `livecopilot-public-health`
- `livecopilot-backend-health`
- `livecopilot-backend-status`
- `livecopilot-backend-api-summary`

## Implementação no dashboard

- o dashboard principal recebeu 7 painéis novos do Livecopilot
- a seção foi posicionada logo abaixo do topo principal para não ficar escondida em uma dobra distante
- o bloco inclui `Livecopilot Public Health` como checagem complementar da publicação pública

## O que não entrou

- `dns_checks.yaml` não recebeu novo check
- `ws` não recebeu monitoramento dedicado nesta rodada
- `realtime/respond` não recebeu check automático, porque o endpoint é POST e pode gerar ruído/custo desnecessário

## Limites conhecidos

- o check público ficou em HTTP porque o item `web.page.get` do agente local valida de forma estável o frontend público nessa forma nesta máquina
- a validação de `ws` e `realtime/respond` seguiu fora do runtime automático para evitar carga e efeitos colaterais
- a integração de runtime foi aplicada no Zabbix local com itens e triggers reais
- o dashboard do Grafana foi preparado como bloco de leitura operacional e recebeu a nova área do Livecopilot
- a visibilidade no painel foi confirmada por captura autenticada do dashboard real

## Leituras operacionais desejadas

- Apache cai: `livecopilot-apache-edge` falha, mas `livecopilot-semantic-api` pode continuar verde
- frontend público quebra: `livecopilot-public-frontend` falha, enquanto `livecopilot-apache-edge` pode seguir verde
- backend cai: `livecopilot-backend-health`, `livecopilot-backend-status` e `livecopilot-backend-api-summary` falham
- serviço systemd cai: `livecopilot-semantic-api` falha e ajuda a explicar a causa raiz

## Evidências locais usadas na leitura

- `127.0.0.1:8080` responde a `/`
- `127.0.0.1:8099` responde a `/health`, `/status` e `/api/panel/summary`
- `livecopilot.escossio.dev.br` responde na borda pública

## Evidências de latest data

- `Livecopilot Servico`: `lastvalue=active`
- `Livecopilot Apache Edge`: `lastvalue=HTTP/1.1 200 OK`
- `Livecopilot Frontend Publico`: `lastvalue=HTTP/1.1 200 OK`
- `Livecopilot Public Health`: `lastvalue=HTTP/1.1 200 OK`
- `Livecopilot Backend Health`: `lastvalue=HTTP/1.1 200 OK`
- `Livecopilot Backend Status`: `lastvalue=HTTP/1.1 200 OK`
- `Livecopilot Backend API`: `lastvalue=HTTP/1.1 200 OK`
