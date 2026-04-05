# Análise de lacuna - template oficial MikroTik

## Fonte oficial consultada

- Zabbix integrations: `Mikrotik monitoring and integration with Zabbix`
- Template oficial genérico: `Mikrotik by SNMP`
- Template oficial por família RB: `MikroTik RB3011UiAS by SNMP`

## O que o template oficial genérico cobre

- `CPU Frequency`
- `Disk Space Total`
- `Disk Space Used`
- `Disk Space Utilisation`
- `Firmware`
- `ICMP Ping`
- `ICMP Packet Loss`
- `ICMP Latency`
- `Identity`
- `Memory Total`
- `Memory Used`
- `Memory Utilisation`
- `Model`
- `Temperature`
- `Uptime`
- `Voltage`
- `SNMP Availability`
- LLD de `CPU`
- LLD de `Interfaces`

## O que já validamos no nosso ambiente

- `SNMP system description`
- `SNMP system name`
- `SNMP uptime`
- `Interface count`
- `Memory size`
- `Host resources uptime`
- `Board name`
- `RouterOS version`
- `Temperature`
- `Voltage`
- `PPPoE tunnel status`
- `WireGuard tunnel status`

## Lacunas úteis para a próxima rodada

- `ICMP Ping`
- `ICMP Packet Loss`
- `ICMP Latency`
- `SNMP Availability`
- `Model`
- `Identity`
- `Firmware`
- `CPU Frequency`
- LLD de `CPU`
- LLD de `Interfaces` no formato oficial do Zabbix

## Leitura operacional

- a nossa base atual já valida inventário e saúde mínima
- o template oficial adiciona disponibilidade e LLD padronizada
- a próxima melhoria mais valiosa é alinhar a LLD de interfaces ao padrão oficial e incluir disponibilidade SNMP/ICMP
