# Relatório da rodada

## Objetivo

Substituir o status visual do host `187.19.161.199` por uma trigger sintética baseada nos três hosts posteriores do ramo, sem mexer no mapa, layout, topologia ou links.

## Host agregador confirmado

- host técnico: `hop-ip-187-19-161-199`
- hostid: `10791`
- interface principal: `187.19.161.199:10050`
- grupo: `Transit / Hop`
- template base: `ICMP Ping`

## Três hosts posteriores confirmados

- `hop-ip-104-21-4-50` (`hostid 10793`)
- `hop-ip-172-67-131-172` (`hostid 10792`)
- `hop-ip-1-0-0-1` (`hostid 10794`)

## Itens validados

- item usado nos três hosts: `icmpping`
- estado dos itens: habilitados e suportados
- últimos valores lidos na validação:
  - `hop-ip-104-21-4-50`: `1`
  - `hop-ip-172-67-131-172`: `1`
  - `hop-ip-1-0-0-1`: `1`

## Trigger sintética criada

- `Saídas após 187.19.161.199 degradadas (2/3)` com severidade `Warning`
- `Saídas após 187.19.161.199 indisponíveis (3/3)` com severidade `High`
- janela operacional: `5m`

## Triggers antigas tratadas

- `32670` - `ICMP Ping: Unavailable by ICMP ping` - desabilitada
- `32671` - `ICMP Ping: High ICMP ping loss` - desabilitada
- `32672` - `ICMP Ping: High ICMP ping response time` - desabilitada
- `32673` - `ICMP unreachable` - desabilitada

## Validação objetiva

- o host correto foi resolvido por API como `10791`
- os três hosts posteriores foram resolvidos por API a partir das ligações do sysmap `10`
- as expressões novas foram gravadas e retornadas pelo Zabbix com referências cross-host válidas
- o sysmap não foi alterado nesta rodada

## Observação

- a resolução interna das expressões do Zabbix substituiu os nomes técnicos pelos `itemid` associados, o que confirma que os itens foram aceitos pelo mecanismo do backend
