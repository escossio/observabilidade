# noVNC Runtime Validation

## Estado local observado

Processos ativos:

- `Xvfb :20`
- `x11vnc` em `127.0.0.1:5901`
- `websockify` em `10.45.0.3:6081`

Sessão gráfica:

- desktop XFCE ativo no usuário `liveui`
- navegador já aberto dentro da sessão gráfica para uso posterior com Netflix

## Validação em camadas

### 1. Origem local do noVNC

UI direta:

```text
GET http://10.45.0.3:6081/vnc.html -> 200
```

WebSocket direto:

```text
wscat ws://10.45.0.3:6081/websockify -> Connected
RFB 003.008
```

### 2. Apache local com hostname dedicado

UI via Apache local:

```text
curl -H 'Host: novnc.escossio.dev.br' -u operator:*** http://127.0.0.1/ -> 200
curl -H 'Host: novnc.escossio.dev.br' -u operator:*** http://127.0.0.1/vnc.html -> 200
```

Proteção aplicada:

```text
curl -H 'Host: novnc.escossio.dev.br' http://127.0.0.1/vnc.html -> 401
```

WebSocket via Apache local:

```text
wscat ws://127.0.0.1/websockify --host novnc.escossio.dev.br --auth operator:*** -> Connected
RFB 003.008
```

Leitura da raiz:

```text
GET / -> entrega a UI do noVNC
```

Resultado:

- a raiz não mostra mais `Directory listing for /`
- a raiz passa a servir o `vnc.html` com `autoconnect=true&path=websockify`

### 3. Hostname público via Cloudflare Tunnel

UI pública:

```text
curl -k -u operator:*** https://novnc.escossio.dev.br/ -> 200
curl -k -u operator:*** https://novnc.escossio.dev.br/vnc.html -> 200
curl -k https://novnc.escossio.dev.br/ -> 401
curl -k https://novnc.escossio.dev.br/vnc.html -> 401
```

WebSocket público:

```text
wscat wss://novnc.escossio.dev.br/websockify --auth operator:*** -> Connected
RFB 003.008
```

DNS:

```text
novnc.escossio.dev.br -> Cloudflare proxy ativo
```

## Evidência de desktop no navegador

Validação feita com navegador real em modo headless:

```text
firefox --headless --screenshot /tmp/novnc-root-public.png \
  'https://operator:***@novnc.escossio.dev.br/?autoconnect=true&resize=remote&reconnect=false&view_only=true'

firefox --headless --screenshot /tmp/novnc-public.png \
  'https://operator:***@novnc.escossio.dev.br/vnc.html?autoconnect=true&resize=remote&reconnect=false&view_only=true'
```

Resultado:

- screenshot da raiz gerado com sucesso
- screenshot gerado com sucesso
- arquivo PNG `1600x900`
- handshake público de WebSocket confirmado com `RFB 003.008`

Leitura operacional:

- a raiz pública abre a interface do noVNC
- a página do noVNC abre externamente
- o WebSocket conecta externamente
- o canvas remoto foi carregado por navegador no hostname dedicado

## Limites e segurança mínima

- a proteção aplicada nesta rodada foi `Basic Auth` no Apache
- o segredo não foi registrado no repositório
- a publicação atual é suficiente para uso operacional controlado
- se a sessão precisar ficar exposta por mais tempo, vale considerar camada adicional fora do Apache
