# Semantics

## Tipos de nó

- `host`: máquina central do cluster
- `service`: serviço executado diretamente no host
- `access`: nó de acesso ou conectividade local
- `edge`: nó de borda, salto de rede ou next-hop
- `provider`: entidade de operadora, AS ou transporte externo
- `destination`: alvo final percebido como nuvem, serviço externo ou destino remoto

## Classificação de origem

- `direct`: nó confirmado por documentação ou inventário local
- `inferred`: nó necessário para completar a cadeia, mas ainda sem nome final confirmado

## Relação

- `depends_on`: a disponibilidade do nó de origem depende da disponibilidade do nó de destino

## Regra de propagação

- falha em um nó acima do grafo afeta tudo que está abaixo dele na leitura operacional
- falha no host afeta todos os serviços do cluster
- falha em conectividade afeta o host e, por consequência, todos os serviços que ele sustenta
- falha em borda ou provedor afeta a percepção externa mesmo com o host saudável

## Uso futuro

- nós `direct` podem virar fonte para automação e validação
- nós `inferred` podem ser refinados ou substituídos por nomes reais depois
- arestas manuais podem ser validadas por evidência operacional
- o mesmo modelo pode virar base para cálculo de impacto, caminho causal e correlação de alerta
