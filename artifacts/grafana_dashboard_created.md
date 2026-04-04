# Grafana dashboard created

- dashboard uid: `observabilidade-grafana`
- title: `Observabilidade Zabbix - Grafana`
- URL: `http://127.0.0.1:3000/d/observabilidade-grafana/observabilidade-zabbix-grafana`
- panel count: `9`

## Painéis

- `Serviço apache2` - `stat`
- `Serviço unbound` - `stat`
- `Serviço grafana-server` - `stat`
- `Web observabilidade public` - `table` (`Zabbix Problems`)
- `Web zabbix frontend alt port` - `table` (`Zabbix Problems`)
- `DNS observabilidade public` - `table` (`Zabbix Problems`)
- `DNS localhost` - `table` (`Zabbix Problems`)
- `Frontend público` - `URL`
- `Problemas ativos` - `table` (`Zabbix Problems`)

## Validação

- o dashboard foi salvo com sucesso no Grafana
- o datasource Zabbix está associado ao dashboard
- os painéis de serviço usam itens reais do Zabbix com filtro pelo nome do item
- os painéis de web e DNS foram rebatizados para a baseline atual
- `example.com` deixou de aparecer como painel principal
