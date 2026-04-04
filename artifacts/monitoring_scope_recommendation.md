# Monitoring scope recommendation

Data da recomendação: `2026-04-04`

Base: inventário real por `systemd`, `ss -tulpn` e `ps`.

## Critério usado

Monitore só o que:

- derruba a frente de observabilidade
- afeta acesso remoto ou publicação
- representa serviço de negócio realmente em uso
- tem valor claro para alerta operacional

## Monitorar já

| Serviço | Unit | Prioridade | Motivo |
|---|---|---:|---|
| `zabbix-server` | `zabbix-server.service` | crítica | backend da coleta e dos alertas. |
| `zabbix-agent2` | `zabbix-agent2.service` | crítica | coleta local no host. |
| `apache2` | `apache2.service` | crítica | frontend local e porta HTTP principal. |
| `grafana-server` | `grafana-server.service` | crítica | visualização operacional principal; faz parte da frente entregue. |
| `cloudflared` | `cloudflared.service` | crítica | túnel de publicação do Grafana; sem ele a publicação externa quebra. |
| `unbound` | `unbound.service` | crítica | DNS local em uso real. |
| `postgresql` | `postgresql@17-main.service` | crítica | dependência direta do Zabbix. |
| `ssh` | `ssh.service` | crítica | acesso administrativo e recuperação remota. |

## Monitorar depois

| Serviço | Unit | Prioridade | Motivo |
|---|---|---:|---|
| `emby-server` | `emby-server.service` | útil | aplicação real do host, mas fora do núcleo da observabilidade. |
| `cloudflared-livecopilot` | `cloudflared-livecopilot.service` | útil | túnel adicional, só se fizer parte da operação esperada. |
| `smbd` | `smbd.service` | útil | compartilhamento SMB ativo. |
| `nmbd` | `nmbd.service` | útil | complemento do Samba. |
| `winbind` | `winbind.service` | útil | suporte de identidade/rede para Samba. |
| `libvirtd` | `libvirtd.service` | útil | virtualização local ativa. |
| `livecopilot-semantic-api` | `livecopilot-semantic-api.service` | útil | API própria com porta exposta. |
| `liveui-novnc` | `liveui-novnc.service` | útil | gateway de acesso gráfico do ambiente liveui. |
| `liveui-x11vnc` | `liveui-x11vnc.service` | útil | bridge VNC do ambiente liveui. |
| `systemd-timesyncd` | `systemd-timesyncd.service` | baixa | bom para correlação de logs, mas sem item dedicado agora. |

## Não monitorar agora

| Serviço | Motivo |
|---|---|
| `dbus` | infraestrutura interna do sistema. |
| `polkit` | camada interna de autorização. |
| `systemd-journald` | ruído de sistema; não merece item dedicado. |
| `systemd-logind` | ruído de sistema. |
| `systemd-machined` | suporte interno a VMs/containers. |
| `systemd-udevd` | suporte interno de eventos de dispositivo. |
| `udisks2` | não é core da operação deste host. |
| `avahi-daemon` | mDNS/descoberta local, baixa prioridade. |
| `cron` | útil, mas não merece alerta dedicado. |
| `virtlockd` | suporte interno da stack libvirt. |
| `virtlogd` | suporte interno da stack libvirt. |
| `liveui-xfce` | sessão gráfica de suporte. |
| `liveui-xvfb` | display virtual de suporte. |
| `getty@tty1` | console local padrão. |
| `user@0` | sessão do root. |

## Classificação final por camada

### Obrigatórios

- `zabbix-server`
- `zabbix-agent2`
- `apache2`
- `unbound`
- `postgresql@17-main`
- `ssh`

### Segunda linha

- `grafana-server`
- `cloudflared`
- `cloudflared-livecopilot`
- `emby-server`
- `smbd`
- `nmbd`
- `winbind`
- `libvirtd`
- `livecopilot-semantic-api`
- `liveui-novnc`
- `liveui-x11vnc`
- `systemd-timesyncd`

### Não monitorar agora

- `dbus`
- `polkit`
- `systemd-*`
- `udisks2`
- `avahi-daemon`
- `cron`
- `virtlockd`
- `virtlogd`
- `liveui-xfce`
- `liveui-xvfb`
- `getty@tty1`
- `user@0`

## Achados operacionais

- `snmpd.service` está em `failed`
- `dnsmasq` está ativo por causa da rede da libvirt, mas é contexto de infraestrutura local, não serviço de negócio, então ficou fora da base mínima
- `grafana-server` foi tratado como crítico porque é parte da frente operacional entregue, não um extra opcional
- `cloudflared` foi tratado como crítico porque sustenta a publicação externa do Grafana
- há dois túneis `cloudflared` ativos, então a publicação externa está efetivamente em uso
- `emby-server` está escutando em `8096`, então vale monitoramento de disponibilidade, mas não entra como crítico

## Leitura prática para `config/services.yaml`

O arquivo atual está abaixo do escopo real do host. A lista mínima que deveria ser considerada na próxima revisão é:

- `apache2`
- `unbound`
- `zabbix-server`
- `zabbix-agent2`
- `postgresql@17-main`
- `ssh`
- `grafana-server`
- `cloudflared`
- `cloudflared-livecopilot`
- `emby-server`

Se a intenção for manter o YAML enxuto, o corte ainda precisa preservar:

- backend de observabilidade
- publicação web
- DNS local
- acesso remoto

## Leitura prática para `config/web_checks.yaml`

### Base mínima

- `observabilidade-public` em `https://observabilidade.escossio.dev.br/`

### Segunda linha

- `grafana-local` em `http://127.0.0.1:3000/`
- `zabbix-frontend-alt-port` em `http://127.0.0.1:8081/`

### Fora de escopo nesta rodada

- check público adicional de exemplo
- check local redundante do frontend Zabbix na porta `80`

## Leitura prática para `config/dns_checks.yaml`

### Base mínima

- `observabilidade-public-a` consultando `observabilidade.escossio.dev.br` via `127.0.0.1`

### Segunda linha

- `localhost-a` como diagnóstico local do resolvedor

### Fora de escopo nesta rodada

- `example.com` como check genérico herdado de exemplo antigo
