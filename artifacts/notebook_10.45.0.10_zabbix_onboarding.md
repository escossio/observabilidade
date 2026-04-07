# Onboarding do notebook `10.45.0.10` no Zabbix

## Objetivo

- validar o notebook Debian preparado para monitoramento
- cadastrar ou atualizar o host no Zabbix com o hostname real
- confirmar coleta básica e habilitar a descoberta de rede

## Identidade real

- IP: `10.45.0.10`
- hostname: `note-leo`
- FQDN: `note-leo.escossio.dev.br`
- kernel: `6.12.74+deb12-amd64`
- distribuição observada no `uname`: Debian 12 / kernel backports

## Acesso e serviço

- acesso SSH como `root` funcionou
- `zabbix-agent2` estava `active`
- `zabbix-agent2` estava `enabled`
- o agent escuta em `*:10050`
- o notebook estava com `firewalld` ativo
- a zona `public` não liberava `10050/tcp` inicialmente
- foi adicionada uma rich rule liberando `10050/tcp` apenas para `10.45.0.3`

## Validação do agent

- `agent.ping` retornou `1`
- `system.hostname` retornou `note-leo`
- `system.uname` retornou `Linux note-leo 6.12.74+deb12-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.74-2~bpo12+1 (2026-03-13) x86_64`

## Cadastro no Zabbix

- host técnico: `note-leo`
- visible name: `note-leo / 10.45.0.10`
- `hostid`: `10779`
- grupo: `Linux servers`
- `groupid`: `2`
- template: `Linux by Zabbix agent`
- `templateid`: `10001`
- interface agent: `10.45.0.10:10050`
- status: `enabled`

## Estado da coleta

- a interface do host já aparece como `available=1`
- itens base do template já começaram a preencher `latest data`
- `system.cpu.util` já tem leitura válida no Zabbix
- `system.cpu.load[all,avg1]`, `system.cpu.load[all,avg5]` e `system.cpu.load[all,avg15]` já retornam valores
- `system.boottime` já está sendo atualizado
- a regra de discovery `net.if.discovery` existe no template
- a regra de discovery está configurada com `delay=1h`
- os prototypes de interface incluem:
  - `net.if.in["{#IFNAME}"]`
  - `net.if.out["{#IFNAME}"]`
- no agent, `net.if.discovery` retornou as interfaces:
  - `lo`
  - `enp43s0`
  - `virbr0`
  - `wlp42s0`
  - `vnet0`
  - `wg0`
- no agent, a interface principal `wlp42s0` devolveu tráfego real em:
  - `net.if.in["wlp42s0"]`
  - `net.if.out["wlp42s0"]`

## Limitação

- a coleta de rede está pronta e validada no agent
- os itens derivados de interface ainda dependem do próximo ciclo de discovery do template, que está em `1h`
- não houve mudança no Grafana

## Resultado

- notebook cadastrado no Zabbix com o hostname real
- agent validado com `agent.ping`
- template Linux vinculado
- monitoramento base iniciado
- descoberta de rede pronta para materializar os itens derivados no próximo ciclo
