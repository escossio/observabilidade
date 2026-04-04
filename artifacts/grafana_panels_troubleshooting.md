# Grafana panels troubleshooting

## Causa raiz do `N/A`

- os painéis numéricos do dashboard original estavam filtrando pelo `key_` do Zabbix
- o plugin `alexanderzobnin-zabbix-datasource` devolveu série apenas quando o filtro passou a usar o **nome do item** do Zabbix
- para web e DNS, os itens eram textuais e o painel `stat` não renderizou o valor como esperado

## Correção aplicada

- painel `Serviço apache2` passou a usar `Service apache2 running`
- painel `Serviço unbound` passou a usar `Service unbound running`
- painel `Serviço emby-server` passou a usar `Service emby-server running`
- painel `Resumo do host` passou a usar `Zabbix agent availability`
- painéis de web e DNS foram migrados para painéis de problema/status do plugin `Zabbix Problems`

## Evidência objetiva

- `api/ds/query` respondeu com `frames: 1` para:
  - `Service apache2 running`
  - `Zabbix agent availability`
- `api/dashboards/uid/observabilidade-grafana` confirmou a troca dos filtros:
  - item numérico por nome
  - web/DNS por trigger/status

## Itens que continuaram exigindo adaptação

- `web.page.get[127.0.0.1,/,80]`
- `web.page.get[127.0.0.1,/,8080]`
- `net.dns.record[127.0.0.1,example.com,A]`
- `net.dns.record[127.0.0.1,localhost,A]`

## Resultado

- o dashboard deixou de depender de `N/A` para os painéis centrais
- os painéis de serviço e resumo passaram a exibir dado real
- web e DNS ficaram representados por painéis de problema/status, que o plugin renderiza de forma estável
