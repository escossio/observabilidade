# Relatório da rodada

## Objetivo

Habilitar a execução de Global scripts no Zabbix Server para que os scripts "Ping" e "Traceroute" funcionem a partir do menu do host no mapa.

## Mudança aplicada

- arquivo ajustado:
  - `/etc/zabbix/zabbix_server.conf`
- parâmetro alterado:
  - `EnableGlobalScripts=0` -> `EnableGlobalScripts=1`
- serviço reiniciado:
  - `zabbix-server`

## Validação no frontend

- login autenticado no frontend em `http://127.0.0.1:8081/`
- `menu.popup` do host `10806` retornou os scripts:
  - `Ping`
  - `Traceroute`
- `popup.scriptexec` executou `Ping` com saída bem-sucedida
- `popup.scriptexec` executou `Traceroute` com saída bem-sucedida

## Evidência textual

- valor anterior de `EnableGlobalScripts`: `0`
- valor final de `EnableGlobalScripts`: `1`
- o `zabbix-server` ficou `active (running)` após o restart
- Ping retornou:
  - `100% packet loss`
- Traceroute retornou uma rota completa até `192.205.32.109`

## Observação de permissão

- para validar a execução no frontend com a conta `Admin`, foi necessário liberar a regra `actions.execute_scripts=1` no role `3`
- isso não alterou mapa, sysmap, layout, hosts, itens ou triggers

## Conclusão

- o problema era de configuração do servidor e de permissão de execução da conta usada na UI
- os scripts globais passaram a executar no frontend sem mexer no mapa ou na topologia
