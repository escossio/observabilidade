# Mapa visual AGT no Zabbix

## Resumo

- mapa: `AGT - Visão Visual`
- `sysmapid`: `2`
- host principal: `agt01`
- host adicional solto: `MikroTik RB3011`

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

- `map.update` respondeu com sucesso
- `map.get` confirmou `2` elementos no sysmap
- o AGT permaneceu intacto
- a RB3011 apareceu sem link/dependência nesta rodada
