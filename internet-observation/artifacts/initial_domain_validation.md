# Initial Domain Validation

## Contexto

Validação inicial da camada 1 executada a partir do host de observabilidade em `2026-04-05`.

Escopo:

- resolução DNS via `127.0.0.1`
- `ping -c 1 -W 2`
- HTTPS simples com `curl -L` usando `GET`

Observação importante:

- ping e domínio público servem apenas como sinal grosso
- isso não substitui observação real do tráfego durante playback
- `HEAD` simples pode retornar `405` em alguns domínios públicos sem indicar indisponibilidade; nesta rodada a referência operacional ficou em `GET`

## Ferramentas presentes

- `tcpdump`: `/usr/bin/tcpdump`
- `curl`: `/usr/bin/curl`
- `dig`: `/usr/bin/dig`
- `mtr`: ausente
- `traceroute`: `/usr/sbin/traceroute`
- `chromium`: `/usr/bin/chromium`
- `firefox`: `/usr/bin/firefox`

## Resultados

| Domínio | DNS observado | Ping | HTTPS simples |
| --- | --- | --- | --- |
| `netflix.com` | `54.237.226.164`, `3.230.129.93`, `52.3.144.142` | falhou | `200`, redirect final para `https://www.netflix.com/br-en/` |
| `www.netflix.com` | `www.dradis.netflix.com` -> `www.us-east-1.internal.dradis.netflix.com` -> `54.160.93.182`, `3.211.157.115`, `3.225.92.8` | falhou | `200`, final em `https://www.netflix.com/br-en/` |
| `primevideo.com` | `108.139.134.129`, `108.139.134.94`, `108.139.134.67`, `108.139.134.15` | `19.0 ms` | `200`, redirect final para `https://www.primevideo.com/offers/nonprimehomepage/ref=dv_web_force_root` |
| `www.primevideo.com` | `3.174.37.212` | `21.1 ms` | `200`, final em `https://www.primevideo.com/offers/nonprimehomepage/ref=dv_web_force_root` |
| `google.com` | `172.217.172.14` | `55.4 ms` | `200`, final em `https://www.google.com/` |
| `www.google.com` | múltiplos A observados em `142.251.150.119` a `142.251.157.119` | `58.4 ms` | `200`, final em `https://www.google.com/` |
| `youtube.com` | `142.250.78.206` | `64.0 ms` | `200`, final em `https://www.youtube.com/` |
| `www.youtube.com` | `youtube-ui.l.google.com` -> múltiplos A observados | `61.0 ms` | `200`, final em `https://www.youtube.com/` |

## Leitura prática

- Netflix respondeu bem em HTTPS simples, mas não respondeu a ICMP nesta coleta
- Prime Video, Google e YouTube responderam a DNS, ICMP e HTTPS simples
- `www` e apex podem resolver para conjuntos diferentes de IPs ou CNAMEs
- o próximo passo útil para Netflix é captura real durante playback
