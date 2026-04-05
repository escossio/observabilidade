# Impact Rules

## Objetivo

Este arquivo registra regras documentais de impacto para o `dependency-graph`.

Nesta rodada, o foco é explicitar como a falha se propaga entre:

- cluster `AGT`
- cluster `MikroTik RB3011`
- upstream `AS28126 BRISANET`
- `nuvem / destino`

## Regras do cluster AGT

### Falha em `agt01`

- impacto direto: serviços do cluster AGT perdem execução local
- impacto propagado: publicação, observabilidade local e aplicações do AGT podem deixar de responder
- não implica falha da MikroTik
- não implica falha da operadora
- blast radius: `cluster-local`

### Falha em `br0`

- impacto direto: o host perde a ligação local com a borda
- impacto propagado: o AGT pode parecer indisponível externamente mesmo com processos ainda vivos
- não implica falha da MikroTik
- blast radius: `intercluster-edge`

### Falha no cluster `MikroTik RB3011`

- impacto direto: o AGT perde a borda concreta acima do host
- impacto propagado: publicação e egress do AGT podem falhar
- não implica morte do host `agt01`
- blast radius: `edge-shared`

## Regras do cluster MikroTik

### Falha em `MikroTik RB3011`

- impacto direto: perde-se a borda local e o next-hop do AGT
- impacto propagado: `bridge`, `ether1`, `pppoe-out1` e caminho público deixam de sustentar o AGT
- não implica falha do host `agt01`
- blast radius: `edge-shared`

### Falha em `bridge`

- impacto direto: AGT perde o domínio L2 local de saída
- impacto propagado: o AGT pode perder acesso à borda mesmo com a RB3011 viva
- blast radius: `intercluster-edge`

### Falha em `ether1`

- impacto direto: degrada o uplink físico da WAN principal
- impacto propagado: pode derrubar `pppoe-out1` e o caminho público
- blast radius: `wan-uplink`

### Falha em `pppoe-out1`

- impacto direto: derruba a WAN principal observada
- impacto propagado: pode afetar acesso público e egress do AGT sem derrubar host nem RB3011
- blast radius: `wan-primary`

### Falha em `wg0`

- impacto direto: afeta apenas overlays dependentes
- impacto propagado: não deve derrubar automaticamente a cadeia principal do AGT
- blast radius: `overlay-only`

### Falha em `AS28126 BRISANET`

- impacto direto: afeta o caminho acima da MikroTik
- impacto propagado: acesso público e egress podem falhar
- não implica falha do host AGT
- não implica falha da RB3011
- blast radius: `upstream`

### Falha em `nuvem / destino`

- impacto direto: falha externa acima do provedor
- impacto propagado: percepção de indisponibilidade remota sem evidência de falha local
- blast radius: `external-destination`

## Regras intercluster

- `AGT` depende do cluster `MikroTik RB3011` pela ligação `br0 -> borda`
- falha no AGT não implica falha na MikroTik
- falha na MikroTik pode impactar o AGT
- falha em `pppoe-out1` pode fazer o AGT parecer indisponível para clientes externos mesmo com `agt01` saudável
- falha em `wg0` não deve ser interpretada como perda da WAN principal

## Exemplos de leitura operacional

- se `agt01` cair, os serviços do AGT param, mas a `MikroTik RB3011` pode continuar saudável
- se a `MikroTik RB3011` cair, o AGT perde borda, mas isso não prova falha do host
- se `pppoe-out1` cair, o AGT pode perder egress e publicação pública com host e MikroTik ainda ativos
- se `wg0` cair, o impacto deve ficar restrito ao overlay observado
- se `AS28126 BRISANET` falhar, a quebra é de upstream, não de host nem de borda local

## Limites atuais

- as regras ainda são documentais
- ainda não existe engine automática de RCA
- `nuvem / destino` continua inferido
