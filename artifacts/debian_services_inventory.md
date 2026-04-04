# Debian services inventory

Data da coleta: `2026-04-04`

Base de evidência usada:

- `systemctl list-units --type=service --state=running --no-pager --no-legend`
- `systemctl list-unit-files --type=service --state=enabled --no-pager --no-legend`
- `systemctl --failed --type=service --no-pager --no-legend`
- `ss -tulpn`
- `ps -eo pid,ppid,user,stat,comm,args --sort=comm`

## Resumo executivo

- serviços `systemd` em execução: `31`
- serviços `systemd` habilitados: `24`
- serviços em falha: `1`
- portas/daemons realmente relevantes: `22`, `53`, `80`, `10050`, `10051`, `3000`, `5432`, `8096`, `8099`, `137`, `138`, `5901`, `6081`, `67`

## Classificação operacional

### Críticos para monitorar

| Serviço | Unit | Status | Enabled | Porta/processo | Motivo |
|---|---|---:|---:|---|---|
| `zabbix-server` | `zabbix-server.service` | running | sim | `10051/tcp` | backend de coleta e alerta; se cair, a frente para. |
| `zabbix-agent2` | `zabbix-agent2.service` | running | sim | `10050/tcp` | agente local; base da coleta no host. |
| `apache2` | `apache2.service` | running | sim | `80/tcp` | frontend local e ponto de publicação HTTP. |
| `unbound` | `unbound.service` | running | sim | `53/tcp`, `53/udp` | DNS local em uso real. |
| `postgresql` | `postgresql@17-main.service` | running | sim | `5432/tcp` | dependência direta do Zabbix e do estado operacional. |
| `ssh` | `ssh.service` | running | sim | `22/tcp` | acesso remoto administrativo e caminho de recuperação. |

### Úteis para monitorar

| Serviço | Unit | Status | Enabled | Porta/processo | Motivo |
|---|---|---:|---:|---|---|
| `grafana-server` | `grafana-server.service` | running | sim | `3000/tcp` | visualização operacional; importante, mas não é backend de coleta. |
| `cloudflared` | `cloudflared.service` | running | sim | processo `cloudflared` | túnel de publicação do Grafana. |
| `cloudflared-livecopilot` | `cloudflared-livecopilot.service` | running | sim | processo `cloudflared` | túnel adicional; útil se esse acesso fizer parte da operação. |
| `emby-server` | `emby-server.service` | running | sim | `8096/tcp` | aplicação real do host; disponibilidade vale monitorar. |
| `smbd` | `smbd.service` | running | sim | `139/tcp`, `445/tcp` | compartilhamento SMB real. |
| `nmbd` | `nmbd.service` | running | sim | `137/udp`, `138/udp` | complemento do Samba/NetBIOS. |
| `winbind` | `winbind.service` | running | sim | sem porta visível | suporte de identidade/rede para Samba. |
| `libvirtd` | `libvirtd.service` | running | sim | sem porta visível | virtualização local ativa; útil se a stack fizer parte da operação. |
| `livecopilot-semantic-api` | `livecopilot-semantic-api.service` | running | sim | `8099/tcp` | aplicação própria em execução no host. |
| `liveui-novnc` | `liveui-novnc.service` | running | sim | `6081/tcp` | gateway noVNC do ambiente liveui. |
| `liveui-x11vnc` | `liveui-x11vnc.service` | running | sim | `5901/tcp` | bridge VNC do ambiente liveui. |
| `systemd-timesyncd` | `systemd-timesyncd.service` | running | sim | sem porta visível | sincronismo de tempo ajuda em logs e correlação. |

### Baixa prioridade

| Serviço | Unit | Status | Enabled | Porta/processo | Motivo |
|---|---|---:|---:|---|---|
| `cron` | `cron.service` | running | sim | sem porta | útil para manutenção, mas não merece item dedicado agora. |
| `avahi-daemon` | `avahi-daemon.service` | running | sim | `5353/udp` | descoberta local/mDNS, ruído para o escopo principal. |
| `virtlockd` | `virtlockd.service` | running | sim | sem porta | suporte interno da stack libvirt. |
| `virtlogd` | `virtlogd.service` | running | sim | sem porta | suporte interno da stack libvirt. |
| `liveui-xfce` | `liveui-xfce.service` | running | sim | sem porta | sessão gráfica de suporte. |
| `liveui-xvfb` | `liveui-xvfb.service` | running | sim | sem porta | display virtual de suporte. |
| `dnsmasq` | sem unit própria no inventário | processo ativo | n/a | `53/tcp/udp`, `67/udp` em `virbr0` | rede local da libvirt; vale como contexto, não como alerta dedicado. |

### Dispensáveis para item dedicado

| Serviço | Unit | Status | Enabled | Motivo |
|---|---|---:|---:|---|
| `dbus` | `dbus.service` | running | n/a | infraestrutura interna do sistema. |
| `polkit` | `polkit.service` | running | n/a | camada interna de autorização. |
| `systemd-journald` | `systemd-journald.service` | running | n/a | ruído de sistema; cobrir por saúde geral. |
| `systemd-logind` | `systemd-logind.service` | running | n/a | ruído de sistema. |
| `systemd-machined` | `systemd-machined.service` | running | n/a | suporte interno a containers/VMs. |
| `systemd-udevd` | `systemd-udevd.service` | running | n/a | suporte interno de eventos de dispositivo. |
| `udisks2` | `udisks2.service` | running | sim | camada de dispositivos/desktop sem valor de alerta dedicado. |
| `user@0` | `user@0.service` | running | n/a | sessão do root; não é alvo operacional. |
| `getty@tty1` | `getty@tty1.service` | running | n/a | console local padrão. |

## Achados de falha

| Serviço | Estado | Leitura operacional |
|---|---|---|
| `snmpd.service` | `failed` | falha real registrada, mas sem uso claro no escopo atual. Não corrigir nesta rodada. |

## Cruzamento com portas/processos

| Porta/processo | Associação | Leitura operacional |
|---|---|---|
| `22/tcp` | `sshd` | acesso administrativo remoto. |
| `53/tcp/udp` | `unbound`, `dnsmasq` | DNS local real e DNS/DHCP da libvirt. |
| `80/tcp` | `apache2` | frontend local e publicação HTTP. |
| `10050/tcp` | `zabbix-agent2` | coleta do agente local. |
| `10051/tcp` | `zabbix-server` | backend do Zabbix. |
| `3000/tcp` | `grafana` | visualização principal. |
| `5432/tcp` | `postgres` | banco local usado pelo Zabbix. |
| `8096/tcp` | `EmbyServer` | aplicação útil do host. |
| `8099/tcp` | `uvicorn` / `livecopilot-semantic-api` | API própria do host. |
| `137/138/udp` | `nmbd` | NetBIOS/Samba. |
| `5901/tcp` | `x11vnc` | acesso gráfico do ambiente liveui. |
| `6081/tcp` | `websockify` | acesso noVNC do ambiente liveui. |
| `67/udp` | `dnsmasq` | DHCP da bridge `virbr0`, contexto de libvirt. |

## Leitura direta para `config/services.yaml`

O arquivo atual está enxuto demais para refletir o host real. Hoje ele contém apenas:

- `apache2`
- `unbound`
- `emby-server`

O inventário real mostra que a próxima revisão deveria considerar pelo menos:

- `zabbix-server`
- `zabbix-agent2`
- `postgresql@17-main`
- `ssh`
- `grafana-server`
- `cloudflared`
- `cloudflared-livecopilot`

Sem isso, o monitoramento fica incompleto para a operação atual.
