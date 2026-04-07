# Mapa visual AGT no Zabbix

## Resumo

- mapa: `AGT - Visão Visual`
- `sysmapid`: `2`
- host principal: `agt01`
- host adicional solto: `MikroTik RB3011`

## Link AGT -> RB3011

- `linkid`: `1`
- origem: `AGT / 10.45.0.3`
- destino: `MikroTik RB3011`
- tipo: `trigger`
- cor OK: `00AA00`
- label final:
  - `Down {?last(/agt01/net.if.in["br0"])}`
  - `Up {?last(/agt01/net.if.out["br0"])}`
- `show_label`: `always`
- `drawtype`: `2` (`DRAWTYPE_BOLD_LINE`)
- item base do tráfego: `br0` do host `agt01`
- download: `Interface br0: Bits received` / `69515`
- upload: `Interface br0: Bits sent` / `69527`
- unidade: `bps`
- gatilhos associados:
  - `32532` - `Linux: Interface br0: Link down`
  - `32566` - `RB3011 bridge down`
  - `32567` - `RB3011 ether1 down`
  - `32568` - `RB3011 pppoe-out1 down`
- leitura operacional:
  - o link mostra o throughput do `br0` do AGT como proxy do enlace entre AGT e borda
  - os gatilhos da RB3011 foram adicionados para cobrir o caminho principal sem misturar `wg0`
  - a validação no frontend autenticado mostrou o rótulo resolvido em duas linhas, com leitura visual mais limpa
  - o label ficou acima da linha de forma aproximada, que é o melhor equivalente nativo nesta versão
  - a linha ficou visualmente mais grossa com `DRAWTYPE_BOLD_LINE`
  - este formato passa a ser o padrão visual para os próximos links

## AGT

- host Zabbix: `agt01`
- `hostid`: `10776`
- label: `AGT / 10.45.0.3`
- ícone: `Server_(96)`
- `imageid`: `151`
- comportamento: elemento ligado ao host real do Zabbix

## RB3011

- host Zabbix: `MikroTik RB3011`
- `hostid`: `10778`
- label: `MikroTik RB3011`
- ícone: `Router_(96)`
- `imageid`: `126`
- comportamento: elemento solto, sem ligação com o AGT
- porte visual: equivalente ao do AGT por usar a mesma família de ícone `_(96)`

## Navegação

- rota usada no mapa: `zabbix.php?action=host.dashboard.view&hostid={HOST.ID}`
- decisão: manter o host dashboard nativo como detalhe operacional

## Validação

- `map.update` respondeu com sucesso para o link
- `map.update` respondeu com sucesso
- `map.get` confirmou `2` elementos no sysmap
- `map.get` confirmou `1` link entre os dois elementos
- `trigger.get` confirmou os quatro gatilhos do link
- o frontend autenticado em `zabbix.php?action=map.view&sysmapid=2` exibiu o label resolvido em duas linhas e a linha mais grossa
- o AGT permaneceu intacto
- a RB3011 apareceu sem link/dependência nesta rodada
