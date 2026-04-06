# Netflix Capture Evidence

## Contexto

Captura real executada após a sessão gráfica e o login do Netflix já estarem funcionando.

Janela de coleta:

- início: `2026-04-05 21:16`
- duração alvo: `30-60s`
- método: `tcpdump` no host da observabilidade

## Arquivos gerados

- `captures/20260405-211611-netflix/netflix-session-live.log`
- `captures/20260405-211611-netflix/netflix-session.pcap`

## Evidência operacional observada

### IPs remotos relevantes

- `177.37.221.42`
- `104.18.32.47`
- `104.21.4.50`
- `172.67.131.172`
- `45.57.8.1`
- `45.57.9.1`
- `205.251.193.25`
- `98.85.148.156`
- `54.160.93.182`
- `3.211.157.115`

### Hostnames observados no tráfego

- `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net`
- `nrdp.logs.netflix.com`
- `logs.dradis.netflix.com`
- `logs.us-east-1.internal.dradis.netflix.com`
- `apiproxy-logging-s3-5c4574073964ceac.elb.us-east-1.amazonaws.com`
- `region1.v2.argotunnel.com`
- `livecopilot.escossio.dev.br`

## Leitura operacional

- o tráfego real de Netflix passou por infraestrutura `nflxvideo.net`
- o caminho observável incluiu log endpoints e infra de entrega da Netflix
- o hostname público da observabilidade apareceu no background da VM por atividade paralela do browser/sessão, mas não é o alvo principal desta campanha
- o `websocket` do noVNC permaneceu funcional durante a coleta

## Limite desta rodada

- a evidência principal veio do `network capture`
- não houve instrumentação adicional do DevTools remoto nesta rodada
- para Promover hostnames de entrega a nós do grafo, ainda vale a regra de observação real e repetível
