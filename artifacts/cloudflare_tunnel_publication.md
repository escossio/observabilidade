# Cloudflare Tunnel publication

## Hostname publicado

- `observabilidade.escossio.dev.br`

## Tunnel identificado

- nome: `agente`
- id: `6394a032-08e8-4bc7-a957-44c77e743c49`
- arquivo principal: `/etc/cloudflared/config.yml`

## Regra de ingress criada

- `observabilidade.escossio.dev.br` -> `http://127.0.0.1:3000`
- fallback final mantido: `http_status:404`
- hostnames anteriores preservados:
  - `livecopilot.escossio.dev.br`
  - `agente.escossio.dev.br`

## Método usado para DNS

- comando usado: `cloudflared tunnel route dns agente observabilidade.escossio.dev.br`
- resultado: CNAME criado e vinculado ao túnel existente

## Arquivos alterados

- `/etc/cloudflared/config.yml`
- `/etc/grafana/grafana.ini`

## Backups

- `/srv/observabilidade-zabbix/backups/20260404-cloudflare-publication/config.yml.bak`
- `/srv/observabilidade-zabbix/backups/20260404-cloudflare-publication/grafana.ini.bak`

## Rollback simples

1. restaurar `/etc/cloudflared/config.yml` a partir do backup
2. restaurar `/etc/grafana/grafana.ini` a partir do backup
3. reiniciar `cloudflared` e `grafana-server`
4. remover a rota DNS com o comando apropriado do Cloudflare, se necessário

## Validação resumida

- `cloudflared` ficou ativo após a mudança
- `grafana-server` ficou ativo após a mudança
- o hostname resolve para Cloudflare
- o acesso HTTPS retorna o Grafana e redireciona para `/login`
