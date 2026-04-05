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
- `RewriteRule` interna para que `/` entregue `vnc.html` com `autoconnect=true&path=websockify`
- proxy HTTP da UI para `http://10.45.0.3:6081/`
- proxy WebSocket para `ws://10.45.0.3:6081/websockify`
- autenticação básica no Apache com `AuthType Basic`

### Causa do directory listing na raiz

- a raiz `/` do vhost estava sendo proxied diretamente para a raiz do `websockify`
- o servidor embutido do noVNC responde a raiz com listagem de diretório
- `DirectoryIndex` e `Options -Indexes` locais não resolviam isso porque a resposta vinha do upstream proxied, não de um `DocumentRoot` local

### Fechamento da UX da raiz

- a raiz `/` deixou de cair no listing bruto
- o vhost agora reescreve internamente `/` para:

```text
/vnc.html?autoconnect=true&path=websockify
```

- isso mantém o hostname limpo e evita redirect externo com esquema errado atrás do Cloudflare

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
- a raiz `/` passou a abrir a interface do noVNC em vez de listagem de diretório
- o WebSocket passou a responder no mesmo hostname dedicado
- a sessão ficou pronta para a etapa seguinte:
  - login manual no Netflix
  - playback real
  - captura com `tcpdump`
  - observação com DevTools
