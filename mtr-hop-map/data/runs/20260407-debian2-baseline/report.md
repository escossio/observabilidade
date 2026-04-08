# Baseline de monitoramento do debian2

## Resumo
- host de referência: `agt01`
- host final no Zabbix: `debian2`
- hostid reaproveitado: `10844`
- SSH sem senha validado em `10.45.0.2`
- agent remoto ativo em `/etc/zabbix/zabbix_agentd.conf.d/90-debian2-baseline.conf`
- checks diretos validados com `zabbix_get`

## O que foi espelhado do AGT
- grupo `Linux servers`
- template `Linux by Zabbix agent`
- interface passiva `10.45.0.2:10050`
- inventário desabilitado (`-1`)
- sem tags e sem macros específicas
- modelo de agente passivo, alinhado ao host `agt01`

## Ajustes feitos no debian2
- instalado `zabbix-agent 6.0.14`
- criado override em `conf.d` com:
  - `Server=10.45.0.3`
  - `ServerActive=10.45.0.3`
  - `Hostname=debian2`
- reiniciado `zabbix-agent`
- host Zabbix atualizado para `debian2` sem duplicar IP

## Validação real
- `ssh root@10.45.0.2` funcionou sem senha
- `zabbix_get -s 10.45.0.2 -k agent.ping` retornou `1`
- `zabbix_get -s 10.45.0.2 -k agent.version` retornou `6.0.14`
- `zabbix_get -s 10.45.0.2 -k system.uptime` retornou valor numérico
- `zabbix_get -s 10.45.0.2 -k system.cpu.load[all,avg1]` retornou valor numérico
- o host `debian2` existe no Zabbix e está com o baseline correto

## Diferenças restantes
- o host de origem no Zabbix era `debian2-1` e foi normalizado para `debian2`
- o hostname remoto real continua sendo `debian2-1.escossio.dev.br`
- a coleta via polling do Zabbix ainda depende do próximo ciclo para popular `lastvalue` no frontend, embora a resposta do agent já esteja validada por `zabbix_get`
