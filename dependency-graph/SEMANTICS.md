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
- `validation_source`: origem da validação do nó
- `confidence`: nível de confiança da classificação
- `notes`: observação curta sobre o porquê da classificação

## Classificação de validação

- `documented`: confirmado por documento, inventário ou fonte explícita
- `observed`: confirmado por evidência local objetiva
- `inferred`: útil para completar a cadeia, mas ainda deduzido
- `pending_confirmation`: existe como hipótese operacional, mas ainda não foi validado

## Relação

- `depends_on`: a disponibilidade do nó de origem depende da disponibilidade do nó de destino
- referências `cluster` usam a mesma relação `depends_on`, mas apontam para uma borda externa já modelada em outro arquivo

## Regra de propagação

- falha em um nó acima do grafo afeta tudo que está abaixo dele na leitura operacional
- falha no host afeta todos os serviços do cluster
- falha em conectividade afeta o host e, por consequência, todos os serviços que ele sustenta
- falha em gateway, provedor ou destino afeta a percepção externa mesmo com o host saudável

## Uso futuro

- nós `observed` podem virar fonte para automação e validação
- nós `inferred` podem ser refinados ou substituídos por nomes reais depois
- nós `pending_confirmation` devem continuar explícitos até nova evidência
- arestas manuais podem ser validadas por evidência operacional
- o mesmo modelo pode virar base para cálculo de impacto, caminho causal e correlação de alerta
