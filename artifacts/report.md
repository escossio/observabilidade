# Relatório da rodada

## Objetivo

Auditar e normalizar os incidentes do ramo Dell/ATT, removendo a poluição gerada por triggers ICMP legadas e preservando a lógica sintética correta.

## Ações executadas

- hosts auditados:
  - `32.130.89.4`
  - `12.123.154.54`
  - `12.122.153.181`
  - `12.252.89.6`
- triggers legadas desabilitadas:
  - `32734` a `32749`
- triggers sintéticas mantidas:
  - `32934` a `32940`

## Antes da limpeza

- `32.130.89.4` tinha problema ativo em ICMP legado e também problemas sintéticos
- `12.123.154.54` tinha problema ativo em ICMP legado e problemas sintéticos
- `12.122.153.181` tinha problema ativo em ICMP legado e problemas sintéticos
- `12.252.89.6` já estava correto na lógica sintética, mas ainda carregava legado de ICMP habilitado

## Depois da limpeza

- todos os triggers ICMP legados dos quatro hosts ficaram desabilitados
- permaneceram apenas os triggers sintéticos do ramo Dell/ATT
- nenhum mapa, sysmap, layout ou topologia foi alterado

## Estado final

- `32.130.89.4`: 2 problemas sintéticos ativos
- `12.123.154.54`: 3 problemas sintéticos ativos
- `12.122.153.181`: 3 problemas sintéticos ativos
- `12.252.89.6`: 1 problema sintético ativo

## Conclusão

- a poluição vinha de triggers ICMP legadas ainda habilitadas
- a modelagem sintética passou a ser a única lógica ativa nesses hosts-alvo
