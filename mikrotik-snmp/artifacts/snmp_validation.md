# Validação SNMP MikroTik

## Alvo

- IP validado: `10.45.0.1`
- Tipo de teste: SNMP v2c
- Community testada: `public`
- Host de origem: host do Zabbix nesta máquina

## Resultado

- `ping` respondeu com sucesso
- `snmpget` de `sysDescr.0` respondeu com `RouterOS RB3011UiAS`
- `snmpwalk` nos blocos principais respondeu com dados reais
- a validação confirmou que a community de leitura testada é funcional

## Blocos consultados

- `1.3.6.1.2.1.1` system
- `1.3.6.1.2.1.2` interfaces
- `1.3.6.1.2.1.25` host/resources
- `1.3.6.1.4.1.14988` enterprise MikroTik

## Observações objetivas

- `sysName.0` retornou `MikroTik`
- `sysObjectID.0` retornou `.1.3.6.1.4.1.14988.1`
- `sysUpTime.0` retornou `3 days, 8:08:26.00`
- a interface `pppoe-out1` apareceu no bloco de interfaces
- a interface `wg0` apareceu no bloco de interfaces
- o bloco enterprise trouxe dados de board, RouterOS e sensores

## Arquivos brutos gerados

- `mikrotik-snmp/discovery/ping_10.45.0.1.txt`
- `mikrotik-snmp/discovery/sysDescr_10.45.0.1.txt`
- `mikrotik-snmp/discovery/walk_system_1.3.6.1.2.1.1.txt`
- `mikrotik-snmp/discovery/walk_interfaces_1.3.6.1.2.1.2.txt`
- `mikrotik-snmp/discovery/walk_host_resources_1.3.6.1.2.1.25.txt`
- `mikrotik-snmp/discovery/walk_mikrotik_enterprise_1.3.6.1.4.1.14988.txt`

## Leitura curta

- a MikroTik responde SNMP a partir do host do Zabbix
- a leitura inicial já mostra blocos úteis para monitoramento futuro
- a próxima etapa pode ser transformar essa base em template, mas ainda não nesta rodada
