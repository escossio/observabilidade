# Zabbix Binding README

## Objetivo

Explicar como a observabilidade real do Zabbix se conecta aos nós do `dependency-graph`.

## Fluxo de leitura

1. identificar o `graph_node_id`
2. conferir o `zabbix_host`
3. localizar `bound_items`
4. localizar `bound_triggers`
5. ler `failure_semantics_mapped`
6. decidir se a observação é de função, transporte ou entrega observada

## Tipos de binding

- `functional_node`: serviço, host, saúde de aplicação ou borda funcional
- `transport_node`: bridge, WAN, PPPoE, interface, gateway ou AS
- `observed_delivery_node`: endpoint observado em captura real
- `observed_auxiliary_node`: log, telemetria ou infra auxiliar capturada

## Estado do binding

- `complete`: item e, quando existir, trigger exatos já documentados
- `partial`: item real confirmado, mas `itemid` ou `triggerid` ainda pendente
- `pending`: o nó ainda não tem vínculo útil suficiente nesta rodada

## Como a trigger entra no modelo

- trigger de serviço parado vira leitura de `service_failure`
- trigger de borda pública ou frontend vira leitura de `public_access_failure`
- trigger de link WAN vira leitura de `wan_primary_failure` ou `wan_uplink_failure`
- trigger de overlay vira leitura de `overlay_failure`

## O que já está coberto

- `agt01` com `CPU temperature`
- serviços centrais do AGT com itens reais de serviço e web
- Livecopilot com itens derivados numéricos no Grafana e no Zabbix
- MikroTik RB3011 com inventário SNMP, PPPoE e WireGuard

## Cobertura nesta rodada

- `complete`
  - `host-agt01`
  - `svc-apache2`
  - `svc-unbound`
  - `svc-livecopilot-semantic-api`
  - `svc-livecopilot-apache-edge`
  - `svc-livecopilot-backend-health`
- `partial`
  - `svc-zabbix-server`
  - `svc-zabbix-agent2`
  - `svc-cloudflared`
  - `svc-postgresql-17-main`
  - `svc-ssh`
  - `host-mikrotik-rb3011`
  - `access-mikrotik-bridge`
  - `edge-mikrotik-ether1`
  - `edge-mikrotik-pppoe-out1`
  - `edge-mikrotik-wg0`
- `pending`
  - upstream `AS28126 BRISANET`
  - Netflix delivery recorrente

## O que ainda não está coberto

- itemid e triggerid exatos de todos os serviços base
- binding do upstream `AS28126 BRISANET`
- binding de endpoints observados da Netflix como sinal monitorável recorrente

## Regra de manutenção

- preferir bindings reais e documentados
- não inventar `itemid` ou `triggerid`
- manter o arquivo curto e legível
- quando um binding novo for confirmado, ele deve entrar aqui e no YAML auxiliar
