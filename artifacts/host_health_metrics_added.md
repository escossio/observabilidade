# Host health metrics added

Data: `2026-04-04`

## Objetivo

- ampliar o monitoramento do host com CPU, RAM e temperatura sem mexer na baseline de serviços, web e DNS
- manter o dashboard principal sem scroll no bloco principal

## Fonte de temperatura

- fonte validada no host: `nct6776-isa-0290`
- leitura escolhida: `temp2`
- motivo: leitura estável e legível via `lm-sensors`, com valor operacional de `39.5`

## Itens no Zabbix

- `CPU utilization` / `system.cpu.util`
- `Available memory in %` / `vm.memory.size[pavailable]`
- `CPU temperature` / `sensor[nct6776-isa-0290,temp2]`

## Latest data validado

- CPU utilization: `7.207320999999993`
- Available memory in %: `78.200826`
- CPU temperature: evidência direta no host em `39.5` via `zabbix_agent2 -t`

## Dashboard Grafana

- dashboard: `Observabilidade Zabbix - Grafana`
- painel count: `18`
- novos painéis: `CPU`, `RAM`, `CPU Temp`
- layout: 4 linhas compactas, sem scroll na visão padrão
- linha nova de saúde posicionada abaixo da linha de diagnósticos

## Observação operacional

- a temperatura ainda não apareceu em `latest data` do Zabbix no último ciclo observado, embora a fonte local esteja validada no host
- CPU e RAM já estão refletidas no Zabbix e no dashboard
