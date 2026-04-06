# Causal Tree State Mapping

## Objetivo

Definir como a árvore causal do Grafana sai da estrutura fixa e passa a refletir estado real conhecido sem inventar monitoramento onde ele não existe.

## Estratégia usada

- a árvore continua em SVG inline no painel 26
- o SVG é gerado já com classes de estado resolvidas antes de ser gravado no Grafana
- a fonte de verdade é o runtime atual do Zabbix via API local
- a classificação final cai em quatro classes:
  - `up`
  - `down`
  - `warn`
  - `unknown`

## Convenção visual

| classe | cor | regra |
|---|---|---|
| `up` | verde | binding real, item suportado, dado recente e valor operacional saudável |
| `down` | vermelho | binding real, item suportado, dado recente e valor operacional de falha |
| `warn` | amarelo | agregado misto, parcial ou atenção |
| `unknown` | cinza | sem binding direto, sem leitura atual ou item sem dado recente |

## Regras mínimas da rodada

- item com `status=0`, `state=0`, `lastclock` recente e valor saudável vira verde
- item com `status=0`, `state=0`, `lastclock` recente e valor de falha vira vermelho
- item sem `lastclock` útil ou sem binding direto vira cinza
- nós agregados viram amarelos quando misturam verde com cinza

## Janela de frescor

- leitura tratada como válida quando o `lastclock` está dentro de `900s`
- acima disso, o nó cai para `unknown`

## Mapeamento por nó

| nó da árvore | binding / item | regra | classe nesta rodada |
|---|---|---|---|
| `agt01` | `69621` `CPU temperature` | host só fica verde com leitura atual do item vinculado | `unknown` |
| `apache2` | `69485` | `proc.num > 0` | `up` |
| `unbound` | `69486` | `proc.num > 0` | `up` |
| `grafana-server` | `69617` | `proc.num > 0` | `up` |
| `zabbix-server` | `69615` | `proc.num > 0` | `up` |
| `zabbix-agent2` | `69616` | `proc.num > 0` | `up` |
| `cloudflared` | `69618` | `proc.num > 0` | `up` |
| `postgresql` | `69619` | `proc.num > 0` | `up` |
| `ssh` | `69620` | `proc.num > 0` | `up` |
| `br0` | sem binding direto | não inventar estado | `unknown` |
| `MikroTik RB3011` | `69657` `SNMP uptime` | uptime recente e maior que zero | `up` |
| `bridge` | `69690` | `ifOperStatus=1` | `up` |
| `ether1` | `69692` | `ifOperStatus=1` | `up` |
| `pppoe-out1` | `69701` | `ifOperStatus=1` | `up` |
| `wg0` | `69689` | `ifOperStatus=1`; overlay continua separado por estilo | `up` |
| `206.42.12.37` | sem binding direto | estrutural / observado | `unknown` |
| `AS28126 BRISANET` | sem binding direto | estrutural / upstream | `unknown` |
| `Frontend Público` | `69633` | item derivado = `1` | `up` |
| `cloudflared-livecopilot` | sem binding direto fechado no grafo | não inventar estado | `unknown` |
| `Apache Edge` | `69632` | item derivado = `1` | `up` |
| `Backend FastAPI` | `69635` + `69636` + `69637` | todos `1` = verde | `up` |
| `Livecopilot` | agregado de frontend + túnel + edge + backend | mistura verde com cinza => atenção | `warn` |

## Limites desta V1 dinâmica

- não existe cálculo ao vivo dentro do Grafana
- a cor é resolvida antes da gravação do painel
- `br0`, `cloudflared-livecopilot`, IP público e AS continuam cinza até existir binding real explícito
- a classe `down` fica disponível, mas não apareceu neste snapshot específico

