# Handoff da rodada

## Fechado

- host agregador de teste confirmado: `hop-ip-192-205-32-109` (`hostid 10806`)
- itens trapper criados:
  - `synthetic.test.downstream1`
  - `synthetic.test.downstream2`
  - `synthetic.test.downstream3`
- triggers de teste criadas:
  - `TESTE: downstreams degradados (2/3)`
  - `TESTE: downstreams indisponíveis (3/3)`
- ferramenta de envio validada:
  - `zabbix_sender`

## Cenários validados

- normal: `1,1,1`
- warning: `0,0,1`
- critical: `0,0,0`
- recovery: `1,1,1`

## Evidência

- o warning abriu com `0,0,1`
- a crítica abriu com `0,0,0`
- a recuperação fechou os eventos ao voltar para `1,1,1`
- a lógica de teste ficou isolada da lógica produtiva por naming explícito `TESTE`

## Observação

- o modo de teste continua disponível para repetir os cenários ou remover os itens/triggers se houver limpeza explícita futura
