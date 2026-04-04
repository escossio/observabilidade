# Zabbix runtime validation

## API and login

- `apiinfo.version`: `7.4.8`
- login válido por API com `Admin` e a credencial rotacionada já armazenada localmente
- `Admin/zabbix` continua falhando na autenticação
- `user.get` e `host.get` funcionam com a sessão autenticada

## Host

- host name: `agt01`
- hostid: `10776`
- host group: `Linux servers`
- template linked: `Linux by Zabbix agent`

## Services

- itens de serviço sincronizados com a baseline atual:
  - `Service apache2 running`
  - `Service unbound running`
  - `Service grafana-server running`
  - `Service zabbix-server running`
  - `Service zabbix-agent2 running`
  - `Service cloudflared running`
  - `Service postgresql running`
  - `Service ssh running`
- `Service emby-server running` continua presente como segunda linha

## Web

- `Web observabilidade public`
- `Web zabbix frontend alt port`
- `Web grafana local`
- `observabilidade.escossio.dev.br` passou a ser o check principal
- `example.com` deixou de ser o check principal

## DNS

- `DNS observabilidade public A`
- `DNS localhost A`
- `example.com` foi reaproveitado no runtime para o domínio público real

## Dashboard

- dashboardid: `402`
- dashboard name: `Observabilidade Zabbix - resumo`
- widgets confirmados por API: `8`
- widget classes presentes:
  - service
  - web
  - DNS
  - URL/front-end shortcut

## Agent tests

- `proc.num[apache2]` returned `11`
- `proc.num[unbound]` returned `1`
- `proc.num[emby-server]` returned `0`
- `web.page.get[observabilidade.escossio.dev.br,/,443]` returned HTTPS content from the public Grafana endpoint
- `web.page.get[127.0.0.1,/,8081]` returned the local Zabbix frontend
- `net.dns.record[127.0.0.1,observabilidade.escossio.dev.br,A]` returned the public A records
- `net.dns.record[127.0.0.1,localhost,A]` returned `127.0.0.1`

## Grafana

- Grafana service: active
- Grafana URL: `http://127.0.0.1:3000/`
- plugin installed: `alexanderzobnin-zabbix-app v6.3.0`
- datasource `Zabbix` created and provisioned
- dashboard `Observabilidade Zabbix - Grafana` created with `9` panels
- painel de serviço principal passou a destacar `Service grafana-server running`
- painéis de web e DNS foram rebatizados para `observabilidade-public`, `zabbix-frontend-alt-port`, `grafana-local`, `observabilidade-public-a` e `localhost-a`
