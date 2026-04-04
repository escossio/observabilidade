# Grafana dashboard created

- dashboard uid: `observabilidade-grafana`
- title: `Observabilidade Zabbix - Grafana`
- URL: `http://127.0.0.1:3000/d/observabilidade-grafana/observabilidade-zabbix-grafana`
- panel count: `9`

## Painéis

- `Serviço apache2` - `stat`
- `Serviço unbound` - `stat`
- `Serviço emby-server` - `stat`
- `Web 127.0.0.1` - `table` (`Zabbix Problems`)
- `Web 127.0.0.1:8080` - `table` (`Zabbix Problems`)
- `DNS example.com` - `table` (`Zabbix Problems`)
- `DNS checks` - `table` (`Zabbix Problems`)
- `Resumo do host` - `stat`
- `Problemas ativos` - `table` (`Zabbix Problems`)

## Validação

- o dashboard foi salvo com sucesso no Grafana
- o datasource Zabbix está associado ao dashboard
- os painéis de serviço usam itens reais do Zabbix com filtro pelo nome do item, não pela `key_`
- os painéis de web/DNS foram adaptados para o painel `Zabbix Problems`, porque o plugin não renderizou os valores textuais como `stat`
- o painel `Resumo do host` usa o item numérico real `Zabbix agent availability`
