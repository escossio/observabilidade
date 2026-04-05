# Validação de importação Zabbix - MikroTik SNMP

## Resultado geral

- template importado com sucesso no Zabbix local
- host MikroTik criado e associado ao template
- itens SNMP principais com `latest data` real confirmados
- descoberta de interfaces corrigida e validada com itens reais no host

## Host criado

- nome no Zabbix: `MikroTik RB3011`
- hostid: `10778`
- grupo: `Network devices`
- interface SNMP: `10.45.0.1:161`
- SNMP version: `v2c`
- community: `public`

## Template importado

- nome: `MikroTik SNMP`
- templateid: `10777`
- grupo de template: `Templates/SNMP`

## Itens principais com latest data confirmado

- `SNMP system description`
  - lastvalue: `RouterOS RB3011UiAS`
  - units: vazio
- `SNMP system name`
  - lastvalue: `MikroTik`
  - units: vazio
- `SNMP uptime`
  - lastvalue: `28918200`
  - units: `s`
- `Interface count`
  - lastvalue: `15`
  - units: vazio
- `Memory size`
  - lastvalue: `1048576`
  - units: `B`
- `Host resources uptime`
  - lastvalue: `28918200`
  - units: `s`
- `Board name`
  - lastvalue: `RB3011UiAS`
  - units: vazio
- `RouterOS version`
  - lastvalue: `7.21.1`
  - units: vazio
- `Temperature`
  - lastvalue: `31`
  - units: `C`
- `Voltage`
  - lastvalue: `240`
  - units: `mV`
- `PPPoE tunnel status`
  - lastvalue: `1`
  - units: vazio
- `WireGuard tunnel status`
  - lastvalue: `1`
  - units: vazio

## Descoberta de interfaces

- a abordagem final deixou de usar `SNMP LLD` direta e passou a usar:
  - item mestre `mikrotik.if.walk` com `walk[]`
  - discovery rule `DEPENDENT`
  - preprocessing `SNMP_WALK_TO_JSON`
  - item prototypes `DEPENDENT` com `SNMP_WALK_VALUE`
- o item `mikrotik.if.discovery` saiu do estado `unsupported`
- a LLD gerou itens reais para interfaces como `bridge`, `ether1`, `pppoe-out1` e `wg0`
- latest data confirmado em itens descobertos:
  - `pppoe-out1 operational status` -> `1`
  - `wg0 operational status` -> `1`
  - `ether1 inbound traffic` -> `1490222658`
  - `ether1 outbound traffic` -> `540053278`
- o item mestre foi validado com `delay` temporariamente reduzido e depois devolvido para `1m`

## Evidência objetiva

- a API do Zabbix respondeu com autenticação válida usando `Admin` e a senha rotacionada local
- o host `MikroTik RB3011` foi criado e recebeu o template `MikroTik SNMP`
- `item.get` passou a retornar `lastclock` e `lastvalue` reais para os itens principais
- `discoveryrule.get` passou a retornar `state = 0` e `error` vazio para `mikrotik.if.discovery`
- `item.get` passou a retornar itens descobertos de interface com `lastvalue` real
