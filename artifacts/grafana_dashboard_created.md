# Grafana dashboard created

- dashboard uid: `observabilidade-grafana`
- title: `Observabilidade Zabbix - Grafana`
- URL: `http://127.0.0.1:3000/d/observabilidade-grafana/observabilidade-zabbix-grafana`
- panel count: `15`

## Painéis

- `Resumo` - `stat`
- `Problemas` - `table` (`Zabbix Problems`)
- `Web Público` - `table` (`Zabbix Problems`)
- `DNS Público` - `table` (`Zabbix Problems`)
- `Zabbix Server` - `stat`
- `Agent2` - `stat`
- `Apache2` - `stat`
- `Grafana` - `stat`
- `Cloudflared` - `stat`
- `Unbound` - `stat`
- `PostgreSQL` - `stat`
- `SSH` - `stat`
- `Grafana Local` - `URL`
- `Zabbix Frontend` - `URL`
- `localhost-a` - `stat`

## Validação

- o dashboard foi salvo com sucesso no Grafana
- o datasource Zabbix está associado ao dashboard
- os painéis de serviço usam itens reais do Zabbix com filtro pelo nome do item
- os painéis principais ficaram acima da dobra na grade 4x4
- os cards foram compactados para altura menor e linha de diagnóstico reaproveitada
- os painéis de web e DNS foram rebatizados para a baseline atual
- `example.com` deixou de aparecer como painel principal
- a visualização padrão não exige rolagem para ver o conjunto principal
- `Emby` foi removido do layout principal
