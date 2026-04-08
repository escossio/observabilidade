# Relatório da rodada

## Objetivo

Habilitar um modo de teste seguro e reversível para validar triggers sintéticas no Zabbix com `zabbix_sender`, sem mexer no mapa, layout ou topologia.

## Host agregador de teste

- `hop-ip-192-205-32-109` (`hostid 10806`)

## Camada de teste criada

- itens trapper:
  - `synthetic.test.downstream1`
  - `synthetic.test.downstream2`
  - `synthetic.test.downstream3`
- triggers de teste:
  - `TESTE: downstreams degradados (2/3)`
  - `TESTE: downstreams indisponíveis (3/3)`

## Estratégia de teste

- cenário normal: `1,1,1`
- cenário warning: `0,0,1`
- cenário critical: `0,0,0`
- cenário recovery: `1,1,1`
- comando de injeção: `zabbix_sender`
- lógica separada da produtiva por naming explícito `TESTE`

## Validação objetiva

- os trapper items foram criados no host correto
- `zabbix_sender` processou 3 valores por cenário
- o warning apareceu em `0,0,1`
- a critical apareceu em `0,0,0`
- a recuperação fechou os eventos ao voltar para `1,1,1`
- o mapa `MTR Unified - Brisanet Observed` não foi alterado nesta rodada
