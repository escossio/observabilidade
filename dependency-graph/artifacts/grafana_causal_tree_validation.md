# Grafana Causal Tree Validation

## Objetivo

Validar a troca do bloco textual por uma árvore causal visual no dashboard principal do Grafana.

## Dashboard alterado

- título: `Observabilidade Zabbix - Grafana`
- uid: `observabilidade-grafana`
- versão antes: `26`
- versão depois: `27`

## Estratégia usada

- painel nativo `text`
- modo `html`
- SVG embutido no conteúdo do painel
- sem plugin novo
- sem serviço contínuo novo

## Layout final

- painel 26
- título: `Árvore Causal / Dependência`
- posição: `x=0, y=20, w=24, h=10`
- ocupação total do bloco inferior do dashboard

## Elementos exibidos

- AGT
  - `agt01`
  - `br0`
  - `apache2`
  - `cloudflared`
  - `unbound`
  - `grafana-server`
  - `zabbix-server`
  - `zabbix-agent2`
  - `postgresql`
  - `ssh`
- MikroTik RB3011
  - `bridge`
  - `ether1`
  - `pppoe-out1`
  - `wg0`
  - `206.42.12.37`
  - `AS28126 BRISANET`
- Livecopilot
  - `Frontend Público`
  - `cloudflared-livecopilot`
  - `Apache Edge`
  - `Backend FastAPI`

## Evidência técnica

- dashboard regravado com sucesso via `POST /api/dashboards/db`
- resposta da API do Grafana retornou `status=success`
- o JSON do dashboard passou a conter o painel 26 como HTML/SVG
- o painel textual antigo deixou de ser a peça principal
- a sessão gráfica XFCE da VM em `DISPLAY=:20` abriu uma janela Chromium real do dashboard
- o título da janela ficou `Observabilidade Zabbix - Grafana - Dashboards - Grafana - Chromium`
- a aba carregada na sessão gráfica ficou na URL do dashboard `observabilidade-grafana`
- a inspeção via DevTools da própria instância Chromium confirmou o painel `Árvore Causal / Dependência` no DOM renderizado

## Validação visual

- render local do SVG confirmado com a árvore completa
- o desenho separa AGT, MikroTik RB3011 e Livecopilot em blocos distintos
- `wg0` aparece como overlay separado da cadeia principal
- Livecopilot aparece como cadeia própria com túnel, edge HTTP e backend
- a validação final foi reforçada no ambiente gráfico da VM, não só por HTML isolado

## Limitações

- V1 é majoritariamente estrutural
- cores e posição são fixas no SVG, não calculadas em tempo real no Grafana
- a leitura dinâmica de falha continua vindo da camada causal já validada fora do painel

## Próximo passo natural

- calcular cor por estado a partir dos bindings do `dependency-graph` e gerar a árvore automaticamente a cada nova rodada validada
