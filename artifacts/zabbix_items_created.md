# Zabbix items created

## Host

- hostid: `10776`
- host: `agt01`

## Service items

- `69485` - `Service apache2 running` - `proc.num[apache2]`
- `69486` - `Service unbound running` - `proc.num[unbound]`
- `69487` - `Service emby-server running` - `proc.num[emby-server]`

## Web items

- `69488` - `Web apache 127.0.0.1` - `web.page.get[127.0.0.1,/,80]`
- `69489` - `Web apache 127.0.0.1:8080` - `web.page.get[127.0.0.1,/,8080]`

## DNS items

- `69490` - `DNS example.com A` - `net.dns.record[127.0.0.1,example.com,A]`
- `69491` - `DNS localhost A` - `net.dns.record[127.0.0.1,localhost,A]`

## Triggers

- `32506` - Apache2 parado
- `32507` - Web 127.0.0.1 indisponivel
- `32508` - DNS example.com sem resposta
- `32537` - unbound parado
- `32538` - Web 127.0.0.1:8080 indisponivel

## Validation notes

- `emby-server` permanece monitorado como item real, mas sem trigger ruidosa adicional
- os itens de web e DNS continuam adequados para operação por refletirem os alvos reais do host
