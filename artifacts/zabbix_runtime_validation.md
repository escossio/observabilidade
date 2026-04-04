# Zabbix runtime validation

## API and login

- `apiinfo.version`: 7.4.8
- authentication token obtained after password rotation for `Admin`
- `Admin/zabbix` now fails to authenticate
- `user.get` and `host.get` worked with the token

## Services

- `zabbix-server`: active
- `zabbix-agent2`: active
- `apache2`: active

## Host

- host name: `agt01`
- hostid: `10776`
- host group: `Linux servers`
- template linked: `Linux by Zabbix agent`

## Frontend

- URL: `http://127.0.0.1:8081/`
- login page returned `200 OK`

## Dashboard

- dashboardid: `402`
- dashboard name: `Observabilidade Zabbix - resumo`
- widgets confirmed by API: `8`
- widget classes present:
  - service
  - web
  - DNS
  - URL/front-end shortcut

## Agent tests

- `proc.num[apache2]` returned `7`
- `proc.num[unbound]` returned `1`
- `proc.num[emby-server]` returned `0`
- `web.page.get[127.0.0.1,/,80]` returned `HTTP/1.1 200 OK`
- `web.page.get[127.0.0.1,/,8080]` returned `HTTP/1.1 200 OK`
- `net.dns.record[127.0.0.1,example.com,A]` returned two A records
- `net.dns.record[127.0.0.1,localhost,A]` returned `127.0.0.1`

## Grafana

- Grafana service: active
- Grafana URL: `http://127.0.0.1:3000/`
- plugin installed: `alexanderzobnin-zabbix-app v6.3.0`
- datasource `Zabbix` created and provisioned
- dashboard `Observabilidade Zabbix - Grafana` created with `9` panels
- consulta real do Grafana para o item `Service apache2 running` retornou série com dados reais do Zabbix
- consultas para os itens textuais de web/DNS ainda exigem adaptação de query/painel no plugin
