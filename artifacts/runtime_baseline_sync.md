# Runtime baseline sync

Data: `2026-04-04`

## O que foi sincronizado no runtime

### Zabbix

- itens de serviço criados para a baseline atual:
  - `zabbix-server`
  - `zabbix-agent2`
  - `grafana-server`
  - `cloudflared`
  - `postgresql`
  - `ssh`
- item de DNS legado `example.com` reaproveitado para `observabilidade.escossio.dev.br`
- item web legado de `127.0.0.1` reaproveitado para `observabilidade.escossio.dev.br`
- trigger de DNS atualizada para o domínio público real
- trigger de web atualizada para o check público real

### Grafana

- dashboard `Observabilidade Zabbix - Grafana` foi atualizado para refletir a baseline atual
- painel de serviço passou a destacar `grafana-server`
- painéis de web passaram a apontar para `observabilidade-public` e `zabbix-frontend-alt-port`
- painéis de DNS passaram a apontar para `observabilidade-public-a` e `localhost-a`

## O que deixou de ser referência principal

- `example.com` deixou de aparecer como check principal
- checagens antigas de `127.0.0.1` e `8080` como referência genérica foram rebatizadas para o escopo atual

## Notas operacionais

- `grafana-server` e `cloudflared` seguem tratados como críticos na baseline do projeto
- `localhost-a` permanece apenas como diagnóstico local de segunda linha
- `snmpd.service` continua apenas registrado como falho; não houve correção nesta rodada
