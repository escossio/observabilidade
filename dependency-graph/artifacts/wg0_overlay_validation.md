# wg0 Overlay Validation

## Objetivo

Fechar o cenário `wg0` no alvo correto da MikroTik RB3011 com evidência real, sem elevar o impacto para a cadeia causal principal.

## Binding confirmado

- nó do grafo: `edge-mikrotik-wg0`
- host Zabbix: `MikroTik RB3011`
- hostid: `10778`
- itemid: `69689`
- item: `wg0 operational status`
- key: `mikrotik.ifOperStatus[16]`
- lastvalue atual no Zabbix: `1`
- lastclock atual no Zabbix: `1775440813`
- trigger dedicada para `wg0`: inexistente na base consultada
- semântica mapeada: `overlay_failure`
- blast radius esperado: `overlay-only`

## Tentativa de validação

- o endereço `10.45.0.1` responde a `ping` a partir deste host
- a rota passa por `br0`
- `22/tcp` em `10.45.0.1` recusou conexão
- `161/tcp` em `10.45.0.1` recusou conexão
- não foi encontrada credencial ou CLI administrativa segura para executar alteração no RouterOS

## Resultado

- ação real provocável com segurança nesta frente: não disponível
- evento `wg0` derrubado de verdade: não executado
- observação no Zabbix: apenas leitura estática do item, sem transição causada nesta rodada
- classificação final: `BLOCKED`

## Razão objetiva do bloqueio

- o alvo correto foi identificado
- o item real foi identificado
- a rota até o equipamento existe
- não existe acesso administrativo utilizável nesta frente para provocar a mudança em `wg0`
- derrubar `wg0` sem acesso de controle no RouterOS seria arriscado e fora do escopo seguro desta execução

## Leitura causal

- a semântica permanece `overlay_failure`
- o impacto segue restrito ao overlay observado no grafo
- não houve evidência para promover o evento à cadeia causal principal
- não houve evidência de falha em `pppoe-out1`, `ether1`, `bridge` ou `MikroTik RB3011`

## Conclusão

- o alvo correto foi validado documentalmente
- a validação dinâmica ficou bloqueada por falta de caminho operacional seguro
- a bateria causal fica fechada para os cenários principais, mas o `wg0` permanece `BLOCKED` nesta rodada

