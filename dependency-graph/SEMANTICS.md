# Semantics

## Tipos de nó

- `host`: máquina central do cluster
- `service`: serviço executado diretamente no host
- `cluster`: referência explícita a outro cluster já modelado
- `access_device`: interface, bridge, modem ou concentrador local de saída
- `ppp_session`: sessão PPP ou equivalente de acesso
- `public_ip`: IP público ou dedicado observado na saída
- `gateway`: salto de borda, next-hop ou gateway padrão
- `provider`: entidade de operadora, AS ou transporte externo
- `destination`: alvo final percebido como nuvem, serviço externo ou destino remoto
- `inferred`: nó estrutural útil para leitura operacional, mas ainda não confirmado como fato observado

## Camadas

- `service`
- `host`
- `access`
- `edge`
- `provider`
- `destination`

## Metadados por nó

- `id`: identificador estável do nó
- `label`: nome legível do nó
- `type`: tipo operacional do nó
- `layer`: camada do grafo
- `criticality`: impacto esperado em caso de falha
- `depends_on`: referência ao nó imediatamente abaixo na cadeia
- `impact_scope`: porção do ambiente afetada por uma falha
- `impact_targets`: alvos diretos ou categorias afetadas pela falha do nó
- `failure_semantics`: tipo operacional da falha, por exemplo `host_failure`, `edge_failure` ou `overlay_failure`
- `blast_radius`: raio esperado da falha, por exemplo `cluster-local`, `intercluster-edge`, `upstream`
- `severity_if_failed`: severidade operacional esperada se o nó falhar
- `propagation_mode`: como o impacto se propaga, por exemplo `direct`, `transitive`, `contained`, `external`
- `validation_source`: origem da validação do nó
- `confidence`: nível de confiança da classificação
- `notes`: observação curta sobre o porquê da classificação
- `observed_delivery_endpoint`: verdadeiro quando o nó veio de captura real como endpoint de entrega observado
- `observed_auxiliary_endpoint`: verdadeiro quando o nó veio de captura real, mas atua como telemetria, log ou infra auxiliar
- `repeated_observation`: verdadeiro quando o mesmo nó já apareceu em mais de uma captura independente

## Classificação de validação

- `documented`: confirmado por documento, inventário ou fonte explícita
- `observed`: confirmado por evidência local objetiva
- `inferred`: útil para completar a cadeia, mas ainda deduzido
- `pending_confirmation`: existe como hipótese operacional, mas ainda não foi validado

## Relação

- `depends_on`: a disponibilidade do nó de origem depende da disponibilidade do nó de destino
- referências `cluster` usam a mesma relação `depends_on`, mas apontam para uma borda externa já modelada em outro arquivo

## Semântica causal

- `dependência estrutural`: relação estática entre dois nós ou clusters
- `dependência causal principal`: caminho cuja falha afeta a conectividade principal ou a função central do cluster
- `overlay observado`: interface ou túnel validado no ambiente, mas fora da cadeia causal principal
- `impacto direto`: efeito imediato da falha no próprio cluster ou no próximo nó abaixo
- `impacto propagado`: efeito indireto que se espalha para nós dependentes abaixo do ponto de falha
- `blast_radius`: limite operacional do dano esperado quando o nó falha
- `failure_semantics`: classificação curta da natureza da falha para diferenciar host, borda, WAN, overlay, upstream e destino externo

## Regra de propagação

- falha em um nó acima do grafo afeta tudo que está abaixo dele na leitura operacional
- falha no host afeta todos os serviços do cluster
- falha em conectividade afeta o host e, por consequência, todos os serviços que ele sustenta
- falha em gateway, provedor ou destino afeta a percepção externa mesmo com o host saudável
- falha de `overlay observado` não deve derrubar automaticamente a cadeia causal principal
- falha de `cluster` referenciado propaga impacto para o cluster consumidor, mas não reclassifica automaticamente o host consumidor como morto

## Uso futuro

- nós `observed` podem virar fonte para automação e validação
- nós `inferred` podem ser refinados ou substituídos por nomes reais depois
- nós `pending_confirmation` devem continuar explícitos até nova evidência
- arestas manuais podem ser validadas por evidência operacional
- o mesmo modelo pode virar base para cálculo de impacto, caminho causal e correlação de alerta
