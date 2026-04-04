# Web and DNS scope alignment

Data: `2026-04-04`

Base de decisão: baseline de serviços consolidada, publicação pública do Grafana e resolvedor local `unbound`.

## Web

### Base mínima

- `observabilidade-public` -> `https://observabilidade.escossio.dev.br/`

### Segunda linha

- `grafana-local` -> `http://127.0.0.1:3000/`
- `zabbix-frontend-alt-port` -> `http://127.0.0.1:8081/`

### Fora de escopo nesta rodada

- check público adicional herdado de exemplo antigo
- check local redundante do Zabbix na porta `80`

## DNS

### Base mínima

- `observabilidade-public-a` -> `observabilidade.escossio.dev.br` consultado no resolvedor `127.0.0.1`

### Segunda linha

- `localhost-a` -> verificação técnica local do resolvedor

### Fora de escopo nesta rodada

- `example.com` como check genérico de exemplo

## Justificativa curta

- o domínio público publicado é o ponto mais relevante de operação e acesso externo
- `grafana-server` continua importante, mas o check local entra como segunda linha porque o domínio público já cobre a operação principal
- `zabbix-frontend-alt-port` é útil como acesso administrativo, não como foco principal
- DNS genérico de exemplo não agrega valor operacional direto neste host
- `localhost` fica apenas como diagnóstico local do resolvedor
