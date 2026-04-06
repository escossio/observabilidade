# Causal Tree Grafana Design

## Objetivo

Substituir o bloco textual `Leitura Causal / NOC` por uma visualização de árvore causal mais alinhada ao modelo do `dependency-graph`.

## Problema do bloco textual

- o texto corrido resume bem a rodada validada
- o texto não mostra a estrutura de dependência
- o texto não separa visualmente função, transporte e overlay
- o texto não destaca a relação entre AGT, MikroTik RB3011 e Livecopilot como árvore

## Estratégia escolhida

- usar o painel nativo `text` do Grafana
- rodar o painel em modo `html`
- embutir uma árvore visual em SVG diretamente no conteúdo do painel
- evitar plugin novo
- evitar serviço contínuo novo
- evitar front-end custom separado

## Por que essa estratégia

- é o menor caminho compatível com o ambiente atual
- reaproveita a estrutura já existente do dashboard principal
- permite visual legível em tela menor
- funciona como documentação operacional e como peça de dashboard ao mesmo tempo

## Clusters incluídos na V1

- `AGT`
- `MikroTik RB3011`
- `Livecopilot`

## Estrutura visual da V1

- AGT
  - `agt01`
  - `br0`
  - serviços locais relevantes
- MikroTik RB3011
  - `bridge`
  - `ether1`
  - `pppoe-out1`
  - `wg0` como overlay separado
  - `206.42.12.37`
  - `AS28126 BRISANET`
- Livecopilot
  - `Frontend Público`
  - `cloudflared-livecopilot`
  - `Apache Edge`
  - `Backend FastAPI`

## Convenção visual

- verde: nó saudável
- amarelo: nó em atenção ou degradação
- cinza: nó estrutural, observado de forma auxiliar ou snapshot

## Relações principais desenhadas

- AGT -> `br0` -> MikroTik RB3011
- MikroTik -> `bridge` -> `ether1` -> `pppoe-out1` -> IP público -> AS
- `wg0` fora da cadeia principal
- Livecopilot em cadeia própria com túnel, edge HTTP e backend

## O que a V1 não tenta fazer

- não representa o universo inteiro do `dependency-graph`
- não calcula estado ao vivo no Grafana
- não reclassifica nós automaticamente por evento
- não substitui a camada causal já validada

## Integração no dashboard

- o painel textual anterior foi rebaixado como peça principal
- a nova árvore ocupa o mesmo bloco inferior do dashboard principal
- os painéis de serviço e infraestrutura permanecem intactos

