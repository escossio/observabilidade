# Netflix Observed Delivery Model

## Objetivo

Consolidar a captura real da Netflix em uma camada observacional, sem promover endpoint pontual para a cadeia causal principal do grafo.

## Critério de leitura

- `observed_delivery_endpoint`: forte candidato a entrega de vídeo observada
- `observed_auxiliary_endpoint`: endpoint real, mas ligado a log, telemetria ou infraestrutura auxiliar
- `repeated_observation`: ainda `false` para os destinos listados nesta rodada, porque esta foi a primeira captura usada para consolidar o modelo

## Entrega de vídeo observada

### Hostname principal

- `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net`

### IPs associados na captura

- `177.37.221.42`
- `54.160.93.182`
- `3.211.157.115`
- `98.85.148.156`

### Classificação

- `observed_delivery_endpoint: true`
- `observed_auxiliary_endpoint: false`
- `repeated_observation: false`

### Leitura prática

- este é o melhor candidato observado para a camada de entrega de vídeo
- o nome já aponta para infraestrutura de delivery da Netflix e não para telemetria de cliente
- ainda assim, a promoção para dependência principal deve esperar repetição em novas capturas

## Log e telemetria

### Hostnames

- `nrdp.logs.netflix.com`
- `logs.dradis.netflix.com`
- `logs.us-east-1.internal.dradis.netflix.com`
- `apiproxy-logging-s3-5c4574073964ceac.elb.us-east-1.amazonaws.com`

### IPs associados na captura

- `104.18.32.47`
- `104.21.4.50`
- `172.67.131.172`
- `205.251.193.25`

### Classificação

- `observed_delivery_endpoint: false`
- `observed_auxiliary_endpoint: true`
- `repeated_observation: false`

### Leitura prática

- esses destinos são úteis para confirmar que a sessão Netflix gerou telemetria e logs reais
- eles não representam o caminho principal de vídeo
- devem ficar fora da cadeia causal principal

## Infraestrutura auxiliar

### Hostnames

- `region1.v2.argotunnel.com`
- `livecopilot.escossio.dev.br`

### IPs associados na captura

- `45.57.8.1`
- `45.57.9.1`

### Classificação

- `observed_delivery_endpoint: false`
- `observed_auxiliary_endpoint: true`
- `repeated_observation: false`

### Leitura prática

- `region1.v2.argotunnel.com` aparece como infraestrutura auxiliar do ambiente, não como entrega da Netflix
- `livecopilot.escossio.dev.br` apareceu como tráfego paralelo da VM e deve ser tratado como ruído contextual desta captura

## O que não entra no grafo principal ainda

- não promover `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net` para dependência principal do AGT ou da MikroTik sem nova repetição
- não usar endpoints de log como se fossem caminho de vídeo
- não tratar hostnames vistos uma única vez como prova definitiva de causalidade

## Próximo passo recomendado

- repetir a captura em outra sessão real de reprodução
- verificar se o mesmo delivery endpoint ou família de endpoints reaparece
- só então considerar promoção para uma camada mais estrutural do grafo
