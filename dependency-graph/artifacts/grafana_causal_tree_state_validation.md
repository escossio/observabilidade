# Grafana Causal Tree State Validation

## Objetivo

Validar a evolução da árvore causal estrutural para uma árvore com cor de estado baseada no runtime atual do Zabbix.

## Dashboard alterado

- título: `Observabilidade Zabbix - Grafana`
- uid: `observabilidade-grafana`
- painel: `26`
- título do painel: `Árvore Causal / Dependência`
- versão antes: `27`
- versão depois: `28`

## Estratégia usada

- helper local: `dependency-graph/tools/render_grafana_causal_tree.py`
- leitura do runtime do Zabbix via API local
- classificação local em `up`, `down`, `warn` e `unknown`
- regravação do SVG já colorido no painel 26

## Nós com estado real nesta rodada

### Verdes

- `apache2`
- `cloudflared`
- `unbound`
- `grafana-server`
- `zabbix-server`
- `zabbix-agent2`
- `postgresql`
- `ssh`
- `MikroTik RB3011`
- `bridge`
- `ether1`
- `pppoe-out1`
- `wg0`
- `Frontend Público`
- `Apache Edge`
- `Backend FastAPI`

### Amarelos

- `Livecopilot`

### Vermelhos

- nenhum nó caiu como `down` neste snapshot

### Cinzas

- `agt01`
- `br0`
- `cloudflared-livecopilot`
- `206.42.12.37`
- `AS28126 BRISANET`

## Leitura operacional do snapshot

- `agt01` ficou cinza porque o binding atual do host aponta para `69621` (`cpu.temp`) e o item está sem `lastclock` útil
- `Livecopilot` ficou amarelo porque os sinais públicos e de backend estão verdes, mas o nó causal do túnel dedicado continua sem binding direto fechado
- `wg0` ficou verde por estado operacional real, mas continua fora da cadeia principal por estilo auxiliar
- IP público e upstream continuam cinza por honestidade estrutural

## Evidência técnica

- `item.get` do Zabbix confirmou dados recentes e saudáveis para os serviços principais e para a borda MikroTik
- o dashboard foi regravado com sucesso via API do Grafana
- o painel 26 passou a conter classes explícitas `state-up`, `state-down`, `state-warn` e `state-unknown`

## Evidência visual

- screenshot headless do SVG atualizado: `/tmp/causal_tree_state_preview.png`
- a árvore mostra AGT, MikroTik RB3011 e Livecopilot com cor coerente por nó
- a validação no ambiente gráfico da VM confirmou a página real do dashboard carregada no Chromium em `DISPLAY=:20`
- a sessão gráfica confirmou:
  - título do dashboard carregado
  - presença da árvore
  - presença da legenda `sem leitura ou sem binding`

## Limitações

- o painel continua snapshot-driven
- a cor não muda automaticamente sem nova execução do helper
- a árvore ainda não usa trigger aberta para piscar ou destacar falha em tempo real
- nós sem binding direto continuam cinza mesmo quando a cadeia ao redor está saudável

