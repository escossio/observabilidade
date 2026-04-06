# Cluster MikroTik RB3011

## Escopo

Cluster dedicado da borda de conectividade consumida pelo `AGT`.

O objetivo deste cluster é separar o que pertence ao host `agt01` do que pertence estruturalmente ao equipamento de borda e à cadeia WAN observada.

## Equipamento principal

- `MikroTik RB3011`
- papel: `functional_node`
- IP de gestão / next-hop observado: `10.45.0.1`
- host no Zabbix: `MikroTik RB3011`
- hostid: `10778`
- template Zabbix: `MikroTik SNMP`
- templateid: `10777`
- `sysDescr`: `RouterOS RB3011UiAS`
- versão RouterOS validada: `7.21.1`

## Interfaces e papéis observados

- `bridge`: `transport_node`, domínio L2 local usado como borda imediata do AGT
- `ether1`: `transport_node`, uplink físico observado da WAN principal
- `pppoe-out1`: `transport_node`, sessão WAN principal observada ativa
- `wg0`: `observed_auxiliary_node`, túnel / overlay observado ativo, fora da cadeia causal principal

## Cadeia operacional principal

- equipamento `MikroTik RB3011`
- nó funcional de borda, não destino final
- `ether1`
- `pppoe-out1`
- IP público `206.42.12.37`
- operadora / AS `AS28126 BRISANET`
- nuvem / destino
- `Netflix delivery observado` como folha observacional separada, não como cadeia principal

## Relações de dependência

- `bridge` depende do equipamento `MikroTik RB3011`
- o next-hop `10.45.0.1` depende do equipamento `MikroTik RB3011`
- `ether1` depende do equipamento `MikroTik RB3011`
- `pppoe-out1` depende de `ether1`
- o IP público `206.42.12.37` depende de `pppoe-out1`
- a leitura até `AS28126 BRISANET` sobe a partir do IP público observado
- `wg0` depende do equipamento `MikroTik RB3011`, mas não sustenta a saída principal do AGT
- o cluster `AGT` depende deste cluster pela ligação `br0 -> bridge / next-hop`

## Regras de impacto

- falha em `MikroTik RB3011`:
  - impacta a borda do AGT
  - pode afetar publicação e egress do AGT
  - não implica morte do host `agt01`
- falha em `bridge`:
  - impacta a ligação local do AGT com a borda
  - não implica queda total da WAN por si só
- falha em `ether1`:
  - impacta o uplink físico da WAN principal
  - pode propagar para `pppoe-out1`
- falha em `pppoe-out1`:
  - impacta a WAN principal observada
  - pode afetar caminho público e egress do AGT
- falha em `wg0`:
  - impacta apenas overlays dependentes
  - não derruba automaticamente a cadeia principal
- falha em `AS28126 BRISANET`:
  - impacta o caminho acima da MikroTik
  - não implica falha do AGT nem da RB3011
- falha em `nuvem / destino`:
  - representa falha acima do provedor
  - deve ser distinguida de falha local, de borda e de upstream

## Leitura conceitual de impacto

- se a `MikroTik RB3011` cair, o `AGT` perde a borda externa mesmo que o host continue em execução
- se `bridge` falhar, o AGT pode perder a borda local mesmo com a RB3011 ainda respondendo
- se `ether1` ou `pppoe-out1` degradarem, a saída WAN principal pode falhar sem implicar queda total do equipamento
- se `wg0` cair, a conectividade overlay pode ser afetada sem caracterizar perda da WAN principal
- se a operadora / AS degradar, a borda pode permanecer ativa localmente e ainda assim perder alcance externo
- se `nuvem / destino` falhar, a quebra é externa ao ambiente local
- na árvore por salto, a MikroTik é funcional na borda e os demais elementos são transporte
- a folha observacional da Netflix fica fora da cadeia principal até repetição em capturas adicionais

## Observação

- a leitura continua causal e documental, não uma reprodução literal do forwarding interno do RouterOS
- `wg0` permanece como overlay observado
- overlay e cadeia causal principal continuam separados explicitamente
- `nuvem / destino` continua inferido porque não há um destino único confirmado
