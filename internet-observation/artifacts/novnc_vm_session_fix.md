# noVNC VM Session Fix

## Objetivo

Corrigir a sessão gráfica da VM por trás do noVNC, sem mexer na publicação já validada.

## Causa raiz

- a sessão `liveui` estava sendo iniciada com ambiente de usuário contaminado
- `DBUS_SESSION_BUS_ADDRESS` apontava para `unix:path=/run/user/0/bus`
- `XDG_RUNTIME_DIR` apontava para `/run/user/0`
- `~/.config` e `~/.vnc` estavam com ownership incorreto para o usuário `liveui`
- `light-locker` era carregado e reclamava de `XDG_SESSION_PATH` fora do contexto de LightDM

## Correções aplicadas

### Startup da sessão

Foi criado o startup local da sessão VNC:

- arquivo: `/home/liveui/.vnc/xstartup`
- conteúdo:
  - exporta `XDG_CONFIG_DIRS=/etc/xdg`
  - exporta `XDG_RUNTIME_DIR=/srv/liveui/session/runtime`
  - cria `~/.config` e `~/.cache` se necessário
  - inicia a sessão com `dbus-run-session -- startxfce4`

### Ownership

Diretórios corrigidos para o usuário `liveui`:

- `/home/liveui/.config`
- `/home/liveui/.vnc`
- `/home/liveui/.config/autostart`

### Autostart desabilitado

- `light-locker` foi desabilitado para essa sessão por meio de:
  - `/home/liveui/.config/autostart/light-locker.desktop`
  - conteúdo: `Hidden=true`

## Resultado

- a sessão XFCE sobe com `xfce4-session`
- `xfconfd` sobe corretamente
- `xfsettingsd` sobe corretamente
- `xfce4-panel` sobe corretamente
- `Thunar --daemon` sobe corretamente
- `xfdesktop` sobe corretamente

## Observação operacional

- ainda existem warnings de `at-spi` por ausência do socket da accessibility bus
- esses warnings não impedem a área de trabalho de subir no noVNC
- o que importava nesta rodada era restaurar a área gráfica estável
