# Handoff da rodada

## Fechado

- host agregador confirmado: `hop-ip-187-19-161-199` (`hostid 10791`)
- três hosts posteriores confirmados por API:
  - `hop-ip-104-21-4-50` (`hostid 10793`)
  - `hop-ip-172-67-131-172` (`hostid 10792`)
  - `hop-ip-1-0-0-1` (`hostid 10794`)
- trigger sintética criada no host agregador:
  - warning `2/3`
  - critical `3/3`
- triggers ICMP herdadas do host desabilitadas para não poluir o estado visual

## Evidência

- o Zabbix aceitou as expressões cross-host
- o mapa `MTR Unified - Brisanet Observed` não foi tocado
- não houve recálculo de topologia, mudança de layout ou alteração de links

## Limitação restante

- o host ainda possui os itens ICMP, mas agora eles deixaram de ser a fonte visual principal do estado do nó no mapa
