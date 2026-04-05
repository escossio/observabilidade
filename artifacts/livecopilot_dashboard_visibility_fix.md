# Livecopilot dashboard visibility fix

Data: `2026-04-04`

## Causa raiz

- os itens e triggers do Livecopilot já existiam no Zabbix
- o bloco do Livecopilot não existia no JSON do dashboard principal do Grafana servido à UI
- por isso a documentação e o runtime davam a impressão de integração, mas a tela real não mostrava nada do Livecopilot

## O que estava errado

- o dashboard principal estava com 18 painéis sem nenhuma seção Livecopilot
- os painéis visíveis no topo continuavam os blocos do host principal
- o Livecopilot não aparecia nem por título nem por `gridPos` no JSON exportado

## Correção aplicada

- o dashboard principal foi regravado via API do Grafana autenticado
- foi criada uma seção dedicada do Livecopilot logo abaixo do topo principal
- a seção recebeu 7 painéis:
  - `Livecopilot Serviço`
  - `Livecopilot Apache Edge`
  - `Livecopilot Frontend Público`
  - `Livecopilot Public Health`
  - `Livecopilot Backend Health`
  - `Livecopilot Backend Status`
  - `Livecopilot Backend API`

## Posição final

- o bloco ficou logo após a linha superior do dashboard, antes dos blocos inferiores do host
- a área visível confirma que o Livecopilot não ficou escondido abaixo de uma dobra distante

## Evidências por API

- `GET /api/dashboards/uid/observabilidade-grafana`
- versão do dashboard: `16`
- total de painéis: `25`
- painéis Livecopilot presentes no JSON com `gridPos` confirmada

## Evidência visual

- captura autenticada do dashboard mostrou a seção Livecopilot no corpo da página
- a imagem foi validada localmente com o navegador headless autenticado

## Observação operacional

- os dados de serviço, borda e backend já estavam corretos no Zabbix
- o ajuste necessário era de dashboard, não de coleta
