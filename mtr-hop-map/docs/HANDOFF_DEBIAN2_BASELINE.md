# Handoff - debian2 baseline

## Resultado

- o host `debian2` foi alinhado ao baseline do host `agt01`
- o host reaproveitou o `hostid 10844`
- o baseline no Zabbix ficou com:
  - grupo `Linux servers`
  - template `Linux by Zabbix agent`
  - interface `10.45.0.2:10050`
  - inventário `-1`
  - sem tags e sem macros específicas

## Remoto

- host: `10.45.0.2`
- usuário SSH: `root`
- serviço: `zabbix-agent`
- override aplicado em:
  - `/etc/zabbix/zabbix_agentd.conf.d/90-debian2-baseline.conf`
- parâmetros efetivos:
  - `Server=10.45.0.3`
  - `ServerActive=10.45.0.3`
  - `Hostname=debian2`

## Validação

- `ssh` sem senha validado
- `zabbix_get` validado com:
  - `agent.ping`
  - `agent.version`
  - `system.uptime`
  - `system.cpu.load[all,avg1]`

## Artefatos

- `data/runs/20260407-debian2-baseline/agt_monitoring_baseline.json`
- `data/runs/20260407-debian2-baseline/debian2_monitoring_diff.json`
- `data/runs/20260407-debian2-baseline/debian2_smoke_validation.json`
- `data/runs/20260407-debian2-baseline/report.md`
- `data/runs/20260407-debian2-baseline/zabbix_host_update.json`
- `data/runs/20260407-debian2-baseline/zabbix_validation.json`

## Observação

- nenhum mapa do Zabbix foi alterado nesta rodada
