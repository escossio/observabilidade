# Zabbix Bindings

## Objetivo

Este documento liga sinais reais do Zabbix aos nós do `dependency-graph`.

## Como ler

- `graph_node_id`: nó do grafo
- `cluster`: cluster dono do nó
- `node_role`: papel semântico do nó
- `zabbix_host`: host observado no Zabbix
- `bound_items`: itens que observam o nó
- `bound_triggers`: triggers que representam a falha do nó
- `observation_kind`: tipo de observação, por exemplo serviço, transporte, saúde do host ou entrega pública
- `failure_semantics_mapped`: semântica de falha do grafo acionada por esse binding
- `observed_by_zabbix`: indica binding real já documentado
- `correlation_profile`: perfil mínimo de correlação associado ao nó

## Bindings confirmados

### Convenção de estado

- `complete`: item e trigger exatos documentados
- `partial`: item real confirmado, mas `itemid` ou `triggerid` ainda pendente
- `pending`: vínculo útil ainda não fechado

### Host e serviços do AGT

- `host-agt01`
  - host Zabbix: `agt01`
  - item: `CPU temperature` / `cpu.temp` / `69621`
  - semântica: `host_failure`
  - estado: `complete`
- `svc-zabbix-server`
  - item: `Service zabbix-server running` / `proc.num[zabbix_server]` / `69615`
  - trigger: inexistente na base consultada
  - estado: `complete`
- `svc-zabbix-agent2`
  - item: `Service zabbix-agent2 running` / `proc.num[zabbix_agent2]` / `69616`
  - trigger: inexistente na base consultada
  - estado: `complete`
- `svc-apache2`
  - item: `Service apache2 running` / `proc.num[apache2]` / `69485`
  - item web: `Web apache 127.0.0.1` / `web.page.get[127.0.0.1,/,80]` / `69488`
  - triggers: `Apache2 parado` `32506`, `Web 127.0.0.1 indisponivel` `32507`
  - estado: `complete`
- `svc-grafana-server`
  - item: `Service grafana-server running` / `proc.num[grafana]` / `69617`
  - trigger: inexistente na base consultada
  - estado: `complete`
- `svc-cloudflared`
  - item: `Service cloudflared running` / `proc.num[cloudflared]` / `69618`
  - trigger: inexistente na base consultada
  - estado: `complete`
- `svc-unbound`
  - item: `Service unbound running` / `proc.num[unbound]` / `69486`
  - trigger: `unbound parado` `32537`
  - estado: `complete`
- `svc-postgresql-17-main`
  - item: `Service postgresql running` / `proc.num[postgres]` / `69619`
  - trigger: inexistente na base consultada
  - estado: `complete`
- `svc-ssh`
  - item: `Service ssh running` / `proc.num[sshd]` / `69620`
  - trigger: inexistente na base consultada
  - estado: `complete`

### Livecopilot

- `svc-livecopilot-semantic-api`
  - item: `Livecopilot Serviço estado` / `69631`
  - estado: `complete`
- `svc-livecopilot-apache-edge`
  - items: `69632`, `69633`, `69634`
  - cobertura: Apache edge, frontend público, health público
  - semântica: `public_access_failure`
  - estado: `complete`
- `svc-livecopilot-backend-health`
  - items: `69635`, `69636`, `69637`
  - cobertura: health, status e API do backend
  - semântica: `service_failure`
  - estado: `complete`

### MikroTik RB3011

- `host-mikrotik-rb3011`
  - host Zabbix: `MikroTik RB3011`
  - itens: `SNMP system name` / `69656`, `SNMP uptime` / `69657`, `Memory size` / `69659`, `Board name` / `69661`, `RouterOS version` / `69662`, `Temperature` / `69663`, `Voltage` / `69664`, `PPPoE tunnel status` / `69665`, `WireGuard tunnel status` / `69666`
  - semântica: `external_edge_failure`
  - estado: `complete`
- `access-mikrotik-bridge`
  - item: `bridge operational status` / `mikrotik.ifOperStatus[13]` / `69690`
  - semântica: `local_edge_failure`
  - estado: `complete`
- `edge-mikrotik-ether1`
  - itens: `ether1 operational status` / `69692`, `ether1 inbound traffic` / `69707`, `ether1 outbound traffic` / `69722`
  - semântica: `wan_uplink_failure`
  - estado: `complete`
- `edge-mikrotik-pppoe-out1`
  - item: `pppoe-out1 operational status` / `69701`
  - semântica: `wan_primary_failure`
  - estado: `complete`
- `edge-mikrotik-wg0`
  - item: `wg0 operational status` / `69689`
  - semântica: `overlay_failure`
  - estado: `complete`

## Pendente nesta rodada

- item de observabilidade para o upstream `AS28126 BRISANET`
- sinal Zabbix dedicado para `observed_delivery_node` da Netflix

## Regra prática

- um item do Zabbix aponta para o nó que ele observa
- uma trigger representa a falha semântica que deve ser lida no grafo
- o binding é documental e pode ser refinado com novas extrações sem alterar a estrutura do grafo
- a interpretação causal mínima vive em `CORRELATION.md`
- as regras mínimas de leitura estão em `models/causal_correlation_rules.yaml`
