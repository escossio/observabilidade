# Netflix Session IP Classification

## Contexto da rodada

Sessão Netflix repetida na VM noVNC já preparada. O Firefox do ambiente estava autenticado e abriu o browse sem exigir novo login manual.

O objetivo desta rodada foi repetir a observação real da sessão e separar:

- entrega/CDN da Netflix
- telemetria/logs
- assets auxiliares
- ruído paralelo da VM

## Captura e evidências

- captura tcpdump:
  - `internet-observation/captures/20260406-230119-netflix-session/netflix-session.pcap`
- imagens de evidência do DevTools:
  - `internet-observation/captures/20260406-230119-netflix-session/devtools-network-home.png`
  - `internet-observation/captures/20260406-230119-netflix-session/devtools-network-watch.png`
- observação operacional:
  - o painel Network exibiu requests reais enquanto a página Netflix era navegada
  - a página de watch abriu, mas o plugin Widevine do Firefox crashou durante a tentativa de reprodução estável

## Hostnames observados no DevTools

- `web.prod.cloud.netflix.com`
- `web.ws.prod.cloud.netflix.com`
- `logs.netflix.com`
- `assets.nflxext.com`
- `help.nflxext.com`
- `occ-0-1119-3851.1.nflxso.net`
- `ae.nflximg.net`
- `push.prod.netflix.com`
- `ichnaea-web.netflix.com`

## Classificação dos endpoints Netflix

### Entrega / CDN / edge

- `occ-0-1119-3851.1.nflxso.net`
  - IP resolvido: `177.37.221.41`
  - ASN: `AS28126` (`BRISANET SERVICOS DE TELECOMUNICACOES S.A`)
  - leitura: melhor candidato de edge/entrega repetido nesta rodada
- `assets.nflxext.com`
  - IPs resolvidos: `45.57.90.1`, `45.57.91.1`
  - ASN: `AS40027` (`NETFLIX-ASN`)
  - leitura: CDN de assets da Netflix, útil mas não é telemetria
- `ae.nflximg.net`
  - IP resolvido: `104.89.182.40`
  - ASN: `AS16625` (`AKAMAI-AS`)
  - leitura: CDN de imagem/asset associada ao ecossistema Netflix

### Auxiliar / telemetria / backend

- `web.prod.cloud.netflix.com`
  - IPs resolvidos: `3.12.3.40`, `3.137.95.47`, `18.189.65.196`
  - ASN dominante observado: `AS16509` (`AMAZON-02`)
  - leitura: backend/API
- `web.ws.prod.cloud.netflix.com`
  - IPs resolvidos: `3.18.92.247`, `3.129.173.176`, `18.217.83.66`
  - ASN dominante observado: `AS16509` (`AMAZON-02`)
  - leitura: websocket/backend
- `logs.netflix.com`
  - IPs resolvidos: `3.19.205.174`, `3.21.223.19`, `13.59.96.40`
  - ASN dominante observado: `AS16509` (`AMAZON-02`)
  - leitura: logs/telemetria
- `push.prod.netflix.com`
  - IPs resolvidos: `3.137.73.196`, `3.146.200.139`, `3.147.137.216`
  - ASN dominante observado: `AS16509` (`AMAZON-02`)
  - leitura: push/infra auxiliar
- `ichnaea-web.netflix.com`
  - IPs resolvidos: `3.147.179.10`, `3.21.189.253`, `18.119.152.119`
  - ASN dominante observado: `AS16509` (`AMAZON-02`)
  - leitura: serviço auxiliar/telemetria

## Ruído paralelo observado no pcap

O pcap também contém tráfego não-Netflix do ambiente da VM e do próprio host, então não deve ser usado para promover endpoints do grafo Netflix:

- `104.18.32.47`, `104.21.4.50`, `172.67.131.172`
- `198.41.192.7`, `198.41.200.13`, `198.41.200.193`
- `1.1.1.1`, `8.8.8.8`
- `45.57.8.1`, `45.57.9.1`

## Leitura final

- a sessão foi realmente reproduzida no navegador da VM
- o melhor candidato de entrega repetido nesta rodada foi `occ-0-1119-3851.1.nflxso.net`
- o endpoint de entrega já consolidado na rodada anterior continua válido como referência: `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net`
- o material auxiliar foi separado da camada de entrega para não contaminar a leitura operacional

## Limitação

- a reprodução não chegou a um stream de vídeo estável por causa do crash do Widevine no Firefox
- por isso, esta rodada consolidou entrega/CDN e telemetria com base em pcap + DevTools, mas sem playback contínuo
