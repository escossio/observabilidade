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

## Bindings confirmados

### Host e serviços do AGT

- `host-agt01`
  - host Zabbix: `agt01`
  - item: `CPU temperature` / `cpu.temp` / `69621`
  - semântica: `host_failure`
- `svc-zabbix-server`
  - item: `Service zabbix-server running`
  - trigger: `zabbix-server parado` `pending`
- `svc-zabbix-agent2`
  - item: `Service zabbix-agent2 running`
  - trigger: `zabbix-agent2 parado` `pending`
- `svc-apache2`
  - item: `Service apache2 running` / `proc.num[apache2]` / `69485`
  - item web: `Web apache 127.0.0.1` / `web.page.get[127.0.0.1,/,80]` / `69488`
  - triggers: `Apache2 parado` `32506`, `Web 127.0.0.1 indisponivel` `32507`
- `svc-cloudflared`
  - item: `Service cloudflared running`
- `svc-unbound`
  - item: `Service unbound running` / `proc.num[unbound]` / `69486`
  - trigger: `unbound parado` `32537`
- `svc-postgresql-17-main`
  - item: `Service postgresql running`
- `svc-ssh`
  - item: `Service ssh running`

### Livecopilot

- `svc-livecopilot-semantic-api`
  - item: `Livecopilot Serviço estado` / `69631`
- `svc-livecopilot-apache-edge`
  - items: `69632`, `69633`, `69634`
  - cobertura: Apache edge, frontend público, health público
  - semântica: `public_access_failure`
- `svc-livecopilot-backend-health`
  - items: `69635`, `69636`, `69637`
  - cobertura: health, status e API do backend
  - semântica: `service_failure`

### MikroTik RB3011

- `host-mikrotik-rb3011`
  - host Zabbix: `MikroTik RB3011`
  - itens: `SNMP system name`, `SNMP uptime`, `Memory size`, `Temperature`, `Voltage`, `PPPoE tunnel status`, `WireGuard tunnel status`
  - semântica: `external_edge_failure`
- `access-mikrotik-bridge`
  - item: `Interface operational status` da bridge
  - semântica: `local_edge_failure`
- `edge-mikrotik-ether1`
  - itens: `Interface operational status`, `Interface traffic in`, `Interface traffic out`
  - semântica: `wan_uplink_failure`
- `edge-mikrotik-pppoe-out1`
  - item: `PPPoE tunnel status`
  - semântica: `wan_primary_failure`
- `edge-mikrotik-wg0`
  - item: `WireGuard tunnel status`
  - semântica: `overlay_failure`

## Pendente nesta rodada

- `itemid` e `triggerid` exatos dos serviços `zabbix-server`, `zabbix-agent2`, `cloudflared`, `postgresql` e `ssh`
- `itemid` e `triggerid` exatos dos itens SNMP do MikroTik
- item de observabilidade para o upstream `AS28126 BRISANET`
- sinal Zabbix dedicado para `observed_delivery_node` da Netflix

## Regra prática

- um item do Zabbix aponta para o nó que ele observa
- uma trigger representa a falha semântica que deve ser lida no grafo
- o binding é documental e pode ser refinado com novas extrações sem alterar a estrutura do grafo
