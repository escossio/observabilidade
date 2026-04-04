# Grafana public domain validation

## Validação local

- `http://127.0.0.1:3000/` responde com `301` para `https://observabilidade.escossio.dev.br/`
- `grafana-server` continua ativo

## Validação DNS

- `observabilidade.escossio.dev.br` resolve para IPs de borda da Cloudflare
- a rota DNS foi criada pelo `cloudflared` no túnel existente

## Validação HTTPS

- `https://observabilidade.escossio.dev.br/` responde com `302` para `/login`
- a resposta vem de `cloudflare` e chega ao Grafana
- a página carregada contém os recursos e marcações do Grafana

## Ajuste aplicado no Grafana

- `domain = observabilidade.escossio.dev.br`
- `enforce_domain = true`
- `root_url = https://observabilidade.escossio.dev.br/`

## Evidência objetiva

- headers retornados incluem `server: cloudflare`
- o HTML carregado contém o título e os assets do Grafana
- o backend local continua íntegro com Zabbix funcional

## Pendência observada

- a interface pública está operacional, mas o login ainda exige autenticação normal do Grafana
