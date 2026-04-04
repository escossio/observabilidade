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
- `system.cpu.util` returned a live CPU utilization sample from the agent
- `vm.memory.size[pavailable]` returned a live memory-available percentage from the agent
- `sensor[k10temp-pci-00c3,temp1]` returned `10.5` via `zabbix_agent2 -t`
- `web.page.get[observabilidade.escossio.dev.br,/,443]` returned HTTPS content from the public Grafana endpoint
- `web.page.get[127.0.0.1,/,8081]` returned the local Zabbix frontend
- `net.dns.record[127.0.0.1,observabilidade.escossio.dev.br,A]` returned the public A records
- `net.dns.record[127.0.0.1,localhost,A]` returned `127.0.0.1`

## Grafana

- Grafana service: active
- Grafana URL: `http://127.0.0.1:3000/`
- plugin installed: `alexanderzobnin-zabbix-app v6.3.0`
- datasource `Zabbix` created and provisioned
- dashboard `Observabilidade Zabbix - Grafana` validado com `16` painéis em grade 4x4
- painel de serviço principal passou a destacar `Service grafana-server running`
- painéis de web e DNS foram rebatizados para `observabilidade-public`, `zabbix-frontend-alt-port`, `grafana-local`, `observabilidade-public-a` e `localhost-a`
- a visualização padrão foi conferida para manter os blocos acima da dobra sem rolagem
- `example.com` não aparece mais como referência principal no dashboard

## Rodada de saúde do host

- fonte da temperatura validada no host: `k10temp-pci-00c3` com leitura `temp1`
- CPU e RAM já possuem itens nativos ativos no Zabbix:
  - `CPU utilization` / `system.cpu.util`
  - `Memory utilization` / `vm.memory.utilization`
  - `Available memory in %` / `vm.memory.size[pavailable]`
- item de temperatura criado no Zabbix como `CPU temperature` com key `sensor[k10temp-pci-00c3,temp1]`
- o item de temperatura ainda não produziu histórico em `history` após `config_cache_reload`
- latest data validado com evidência real para CPU e RAM:
  - CPU utilization: `18.283190000000005` em `2026-04-04 18:56:31-03`
  - Available memory in %: `78.520667` em `2026-04-04 18:56:11-03`
  - Memory utilization: `21.479332999999997` em `2026-04-04 18:56:11-03`
- não houve alteração confirmada no dashboard Grafana nesta passagem
