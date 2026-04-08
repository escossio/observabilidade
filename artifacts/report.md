# Relatório da rodada

## Objetivo

Aplicar no ramo Dell/ATT a mesma estratégia de trigger sintética cross-host usada na rodada anterior, sem mexer no mapa, layout ou topologia.

## Hosts agregadores tratados

- `hop-ip-192-205-32-109` (`hostid 10806`)
- `hop-ip-32-130-89-4` (`hostid 10807`)
- `hop-ip-12-123-154-54` (`hostid 10808`)
- `hop-ip-12-122-153-181` (`hostid 10809`)

## Cadeia validada

- `84.16.6.34`
- `94.142.98.175`
- `192.205.32.109`
- `32.130.89.4`
- `12.123.154.54`
- `12.122.153.181`
- `12.252.89.6`
- `143.166.30.172`

## Estratégia aplicada

- hosts `192.205.32.109`, `32.130.89.4` e `12.123.154.54`: warning `2/3` + critical `3/3`
- host `12.122.153.181`: critical `2/2` por falta de três hosts úteis adiante
- item usado em todos os posteriores: `icmpping`
- janela: `5m`

## Triggers antigas tratadas

- triggers ICMP herdadas desabilitadas nos quatro hosts agregadores tratados

## Validação objetiva

- os hosts foram confirmados por API usando os IPs do trecho
- os itens `icmpping` dos hosts posteriores estavam habilitados e suportados
- as expressões cross-host foram aceitas pelo backend do Zabbix
- o mapa `MTR Unified - Brisanet Observed` não foi alterado nesta rodada
