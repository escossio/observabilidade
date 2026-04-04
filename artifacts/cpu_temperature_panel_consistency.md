# CPU temperature panel consistency

Data: `2026-04-04`

## Validação no Zabbix

- host: `agt01`
- item name: `CPU temperature`
- key final: `cpu.temp`
- lastvalue: `38.5`
- lastclock: `1775340645`
- status: ativo e suportado

## Validação no Grafana

- dashboard: `Observabilidade Zabbix - Grafana`
- painel: `CPU Temp`
- tipo: `stat`
- datasource: `alexanderzobnin-zabbix-datasource`
- host filter: `agt01`
- item filter: `CPU temperature`
- referência antiga por `sensor[...]` não aparece no painel atual

## Comparação

- o valor esperado no Zabbix (`38.5`) é coerente com a leitura refletida pelo painel `CPU Temp`
- a diferença temporal entre backend e visualização é normal e não altera a consistência da fonte

## Resultado

- o painel do Grafana está apontando para o item novo e ativo `cpu.temp`
- não foi necessário alterar layout, baseline ou outros painéis
