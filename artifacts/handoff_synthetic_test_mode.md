# Handoff da rodada

## Fechado

- `EnableGlobalScripts` foi habilitado em `/etc/zabbix/zabbix_server.conf`
- o `zabbix-server` foi reiniciado com sucesso e ficou `active (running)`
- a validação no frontend confirmou a execução dos scripts globais:
  - `Ping`
  - `Traceroute`

## Evidência objetiva

- valor anterior de `EnableGlobalScripts`: `0`
- valor final de `EnableGlobalScripts`: `1`
- `menu.popup` do host `10806` retornou os scripts `Ping` e `Traceroute`
- `popup.scriptexec` executou `Ping` com saída de `100% packet loss`
- `popup.scriptexec` executou `Traceroute` com saída de rota completa até o destino

## Observação de acesso

- a conta `Admin` precisou da regra `actions.execute_scripts=1` no role `3` para validar a execução
- isso ficou restrito à permissão de execução e não mexeu em mapa, sysmap, layout, hosts, itens ou triggers

## Arquivos atualizados

- `STATUS.md`
- `artifacts/report.md`
- `artifacts/handoff_synthetic_test_mode.md`

