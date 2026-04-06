# Transport Tree

## Objetivo

Este documento descreve a leitura por salto do `dependency-graph` sem confundir função, transporte e observação.

## Papéis

- `functional_node`: nó que representa serviço, host ou função operacional direta
- `transport_node`: nó que existe para carregar a travessia até o próximo salto
- `observed_delivery_node`: folha observacional vinda de captura real de tráfego
- `observed_auxiliary_node`: folha observacional que apareceu na captura, mas não representa a cadeia principal

## Regra prática

- nó funcional responde à pergunta "o que o ambiente faz?"
- nó de transporte responde à pergunta "por onde a função passa?"
- nó observado responde à pergunta "o que apareceu de fato no tráfego real?"

## Cadeia inicial usada como referência

### AGT

- `agt01` como `functional_node`
- `br0` como `transport_node`

### MikroTik RB3011

- `MikroTik RB3011` como `functional_node`
- `bridge` como `transport_node`
- `ether1` como `transport_node`
- `pppoe-out1` como `transport_node`
- `206.42.12.37` como `transport_node`
- `AS28126 BRISANET` como `transport_node`

### Observação Netflix

- `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net` como `observed_delivery_node`
- `nrdp.logs.netflix.com` como `observed_auxiliary_node`
- `logs.dradis.netflix.com` como `observed_auxiliary_node`
- `logs.us-east-1.internal.dradis.netflix.com` como `observed_auxiliary_node`
- `apiproxy-logging-s3-5c4574073964ceac.elb.us-east-1.amazonaws.com` como `observed_auxiliary_node`
- `region1.v2.argotunnel.com` como `observed_auxiliary_node`

## Leitura esperada

Uma leitura útil da árvore fica próxima de:

- sessão de playback observada
- endpoint de entrega observado
- upstream / AS
- IP público
- PPPoE WAN principal
- uplink físico
- MikroTik RB3011
- bridge / br0
- host AGT
- serviço ou sessão local

## O que entra e o que fica fora

- nós funcionais entram porque sustentam a função principal do ambiente
- nós de transporte entram porque são saltos obrigatórios para a travessia
- nós observados entram porque foram vistos em tráfego real
- log e telemetria ficam como observação auxiliar
- nenhum endpoint observado uma única vez deve virar dependência estrutural definitiva sem repetição

## Critério de promoção futura

- repetir a captura em novas sessões
- confirmar que o mesmo endpoint ou a mesma família reaparece
- só então considerar promoção de uma folha observacional para dependência mais estrutural
