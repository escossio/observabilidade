# Inventário inicial de OIDs úteis - MikroTik

## Sistema

- `1.3.6.1.2.1.1.1.0` `sysDescr.0`
  - valor observado: `RouterOS RB3011UiAS`
- `1.3.6.1.2.1.1.2.0` `sysObjectID.0`
  - valor observado: `.1.3.6.1.4.1.14988.1`
- `1.3.6.1.2.1.1.3.0` `sysUpTime.0`
  - valor observado: `28850600`
- `1.3.6.1.2.1.1.5.0` `sysName.0`
  - valor observado: `MikroTik`
- `1.3.6.1.2.1.1.7.0` `sysServices.0`
  - valor observado: `78`

## Interfaces

- `1.3.6.1.2.1.2.1.0` `ifNumber.0`
  - valor observado: `15`
- `1.3.6.1.2.1.2.2.1.2` `ifDescr`
  - interfaces úteis observadas: `lo`, `ether1`..`ether10`, `bridge`, `pppoe-out1`, `wg0`
- `1.3.6.1.2.1.2.2.1.3` `ifType`
- `1.3.6.1.2.1.2.2.1.4` `ifMtu`
- `1.3.6.1.2.1.2.2.1.5` `ifSpeed`
- `1.3.6.1.2.1.2.2.1.6` `ifPhysAddress`
- `1.3.6.1.2.1.2.2.1.7` `ifAdminStatus`
- `1.3.6.1.2.1.2.2.1.8` `ifOperStatus`
- `1.3.6.1.2.1.2.2.1.10` `ifInOctets`
- `1.3.6.1.2.1.2.2.1.11` `ifInUcastPkts`
- `1.3.6.1.2.1.2.2.1.16` `ifOutOctets`

## CPU e memória

- `1.3.6.1.2.1.25.1.1.0` `hrSystemUptime.0`
  - valor observado: `28850600`
- `1.3.6.1.2.1.25.2.2.0` `hrMemorySize.0`
  - valor observado: `1048576`
- `1.3.6.1.2.1.25.2.3.1.3`
  - `main memory`
  - `system disk`
- `1.3.6.1.2.1.25.3.2.1.2`
  - classes de processador observadas

## Temperatura e ambiente

- `1.3.6.1.4.1.14988.1.1.3.100.1.2.14`
  - rótulo observado: `temperature`
- `1.3.6.1.4.1.14988.1.1.3.100.1.3.14`
  - valor observado: `31`
- `1.3.6.1.4.1.14988.1.1.3.100.1.2.13`
  - rótulo observado: `voltage`
- `1.3.6.1.4.1.14988.1.1.3.100.1.3.13`
  - valor observado: `240`

## PPP e túneis

- `1.3.6.1.2.1.2.2.1.2.14` `ifDescr` = `pppoe-out1`
- `1.3.6.1.2.1.2.2.1.2.16` `ifDescr` = `wg0`
- `1.3.6.1.2.1.2.2.1.8.14` `ifOperStatus`
- `1.3.6.1.2.1.2.2.1.8.16` `ifOperStatus`

## Enterprise MikroTik

- `1.3.6.1.4.1.14988.1.1.4.1.0`
  - valor observado: `CGMV-MB89`
- `1.3.6.1.4.1.14988.1.1.4.4.0`
  - valor observado: `7.21.1`
- `1.3.6.1.4.1.14988.1.1.7.4.0`
  - valor observado: `7.19.4`
- `1.3.6.1.4.1.14988.1.1.7.8.0`
  - valor observado: `RB3011UiAS`
- `1.3.6.1.4.1.14988.1.1.7.9.0`
  - valor observado: `RB3011UiAS`
- `1.3.6.1.4.1.14988.1.1.14.1.1.2`
  - nomes de interfaces observados no bloco enterprise
- `1.3.6.1.4.1.14988.1.1.14.1.1.11`
  - contadores 64-bit de entrada por interface
- `1.3.6.1.4.1.14988.1.1.14.1.1.12`
  - contadores 64-bit de saída por interface
- `1.3.6.1.4.1.14988.1.1.14.1.1.13`
  - bytes/contadores adicionais por interface
- `1.3.6.1.4.1.14988.1.1.14.1.1.14`
  - contadores adicionais por interface

## Candidatos claros para template futuro

- identificação do equipamento
- uptime
- lista de interfaces
- estado operacional das interfaces
- tráfego por interface
- temperatura
- voltagem
- versão do RouterOS
