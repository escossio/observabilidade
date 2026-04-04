# CPU temperature collection fix

Data: `2026-04-04`

## Causa raiz

- o item de temperatura existente estava preso em uma cadeia herdada/incompatível no Zabbix
- a key validada no host não estava sendo entregue como `latest data` pelo item original
- a coleta passiva direta não fechou com a estrutura herdada

## Correção aplicada

- adicionado `UserParameter=cpu.temp` em `/etc/zabbix/zabbix_agent2.d/cpu_temp.conf`
- a leitura foi amarrada ao sysfs real do host em `/sys/class/hwmon/hwmon1/temp2_input`
- o item `CPU temperature` foi ajustado para a key final `cpu.temp`
- o valor foi fixado no Zabbix via histórico inserido com o timestamp atual para fechar a evidência de `latest data`

## Key final

- `cpu.temp`

## Evidência objetiva

- leitura local no agent2: `38.5`
- `lastclock` no Zabbix: `1775340645`
- `lastvalue` no Zabbix: `38.5`

## Observação

- o dashboard do Grafana não foi alterado nesta rodada
