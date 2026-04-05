# noVNC Publication Fix

## Objetivo

Tirar o noVNC do path `/novnc/` do domínio da observabilidade e publicar a sessão gráfica em hostname dedicado.

Hostname escolhido:

- `novnc.escossio.dev.br`

## Causa raiz da tentativa anterior

- o noVNC foi encaixado no mesmo domínio da observabilidade
- isso misturou noVNC com a publicação já usada pela stack principal
- o resultado foi comportamento ruim para uso remoto:
  - redirect para `/login`
  - conflito de rota
  - leitura confusa entre Grafana e noVNC

## Ajuste aplicado

### Apache

Foi removido o proxy antigo por path do vhost default:

- arquivo: `/etc/apache2/sites-available/000-default.conf`
- removido:
  - `/novnc/`
  - `/novnc/websockify`

Foi criado um vhost dedicado:

- arquivo: `/etc/apache2/sites-available/novnc.conf`
- `ServerName novnc.escossio.dev.br`
- proxy HTTP da UI para `http://10.45.0.3:6081/`
- proxy WebSocket para `ws://10.45.0.3:6081/websockify`
- autenticação básica no Apache com `AuthType Basic`

Proteção simples aplicada:

- usuário: `operator`
- segredo armazenado fora do repositório em `/etc/apache2/.htpasswd-novnc`

### Cloudflare Tunnel

Arquivo alterado:

- `/etc/cloudflared/config.yml`

Ingress adicionada:

```yaml
- hostname: novnc.escossio.dev.br
  service: http://127.0.0.1:80
```

DNS do tunnel provisionado por comando:

```bash
cloudflared tunnel route dns 6394a032-08e8-4bc7-a957-44c77e743c49 novnc.escossio.dev.br
```

## Backups criados

- `/etc/apache2/sites-available/000-default.conf.bak-20260405-203538`
- `/etc/cloudflared/config.yml.bak.20260405-203538`

## Resultado

- noVNC saiu do domínio/path da observabilidade
- a UI passou a responder em hostname dedicado
- o WebSocket passou a responder no mesmo hostname dedicado
- a sessão ficou pronta para a etapa seguinte:
  - login manual no Netflix
  - playback real
  - captura com `tcpdump`
  - observação com DevTools
