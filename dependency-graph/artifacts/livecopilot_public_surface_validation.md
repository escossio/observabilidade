# Livecopilot Public Surface Validation

## Hipótese anterior

- a frente pública do Livecopilot foi testada derrubando `cloudflared.service`
- essa hipótese falhou porque `cloudflared.service` publica outros domínios e não é o túnel dedicado do Livecopilot

## Caminho público real mapeado

- domínio público: `livecopilot.escossio.dev.br`
- túnel dedicado: `cloudflared-livecopilot.service`
- config do túnel: `/etc/cloudflared/livecopilot-config.yml`
- destino do túnel: `http://127.0.0.1:8080`
- vhost local: `/etc/apache2/sites-available/livecopilot.conf`
- backend FastAPI: `http://127.0.0.1:8099`

## Checks por camada

- serviço do backend: `69623` `Livecopilot Servico`
- borda Apache local: `69624` `Livecopilot Apache Edge`
- frontend público: `69625` `Livecopilot Frontend Publico`
- health público: `69630` `Livecopilot Public Health`
- backend health: `69626` `Livecopilot Backend Health`
- backend status: `69627` `Livecopilot Backend Status`
- backend API: `69628` `Livecopilot Backend API Summary`

## Fault injection usada

- comando: `systemctl stop cloudflared-livecopilot`
- rollback: `systemctl start cloudflared-livecopilot`
- janela de observação: 60s após stop e 25s após start

## Efeito observado

- `69625` `Livecopilot Frontend Publico` caiu de `1` para `0`
- `69630` `Livecopilot Public Health` caiu de `1` para `0`
- `69624` `Livecopilot Apache Edge` permaneceu `1`
- `69626` `Livecopilot Backend Health` permaneceu `1`
- `69627` `Livecopilot Backend Status` permaneceu `1`
- `69628` `Livecopilot Backend API Summary` não entrou como falha nesta janela

## Conclusão

- o ponto real de falha observável da superfície pública é o túnel dedicado `cloudflared-livecopilot`
- `cloudflared.service` genérico era um fault injection errado para este cenário
- a semântica `public_access_failure` continua válida
- o efeito correto é acoplado à publicação pública, não ao backend FastAPI

## Ajuste prático

- o cenário de validação público agora deve derrubar `cloudflared-livecopilot.service`
- a leitura causal da superfície pública deve acompanhar `Livecopilot Frontend Público` e `Livecopilot Public Health`
- `Livecopilot Apache Edge` e os checks de backend seguem como camadas distintas
