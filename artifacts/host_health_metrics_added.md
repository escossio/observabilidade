# Host health metrics added

Data: `2026-04-04`

## Objetivo

- expandir o monitoramento principal com CPU, RAM e temperatura da CPU
- preservar a baseline de serviços, web, DNS e layout já estabilizada

## Descoberta local

- CPU usage: já existe nativamente via `system.cpu.util`
- RAM usage: já existe nativamente via `vm.memory.utilization` e `vm.memory.size[pavailable]`
- CPU temperature: fonte local validada via `lm-sensors`
  - `k10temp-pci-00c3`
  - leitura `temp1`
  - valor observado no host via `zabbix_agent2 -t`: `10.5`

## Zabbix

- item nativo existente de CPU mantido: `CPU utilization`
- item nativo existente de memória mantido: `Memory utilization`
- item nativo existente de memória mantido: `Available memory in %`
- item novo criado para temperatura:
  - name: `CPU temperature`
  - key: `sensor[k10temp-pci-00c3,temp1]`
  - unidade: `C`
  - tipo de dado: numérico flutuante
- validação operacional da temperatura ainda pendente em `history`

## Latest data validado

- `CPU utilization`: `18.283190000000005` em `2026-04-04 18:56:31-03`
- `Available memory in %`: `78.520667` em `2026-04-04 18:56:11-03`
- `Memory utilization`: `21.479332999999997` em `2026-04-04 18:56:11-03`

## Grafana

- dashboard principal não foi alterado nesta passagem
- o encaixe do bloco `CPU` / `RAM` / `CPU Temp` permanece pendente
- nenhum scroll adicional foi introduzido

## Bloqueio real

- a fonte de temperatura foi validada
- a persistência do item de temperatura no Zabbix ainda não gerou histórico
- o dashboard Grafana não foi editado nesta rodada por bloqueio operacional de acesso ao objeto do dashboard
