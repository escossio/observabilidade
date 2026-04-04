# Grafana dashboard created

- dashboard uid: `observabilidade-grafana`
- title: `Observabilidade Zabbix - Grafana`
- URL: `http://127.0.0.1:3000/d/observabilidade-grafana/observabilidade-zabbix-grafana`
- panel count: `9`

## Painéis

- `Serviço apache2` - `stat`
- `Serviço unbound` - `stat`
- `Serviço emby-server` - `stat`
- `Web 127.0.0.1:80` - `stat`
- `Web 127.0.0.1:8080` - `stat`
- `DNS example.com` - `stat`
- `DNS localhost` - `stat`
- `Resumo do host` - `stat`
- `Problemas ativos` - `table` (`Zabbix Problems`)

## Validação

- o dashboard foi salvo com sucesso no Grafana
- o datasource Zabbix está associado ao dashboard
- os painéis de serviço e problemas usam o plugin do Zabbix com itens e triggers reais
- os painéis de web/DNS permaneceram provisionados como parte do painel operacional, mas a visualização textual precisa de adaptação adicional do tipo de query para esse plugin
