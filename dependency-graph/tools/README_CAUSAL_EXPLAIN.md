# causal_explain

## O que faz

Ferramenta local de leitura causal para sinais do Zabbix.

Ela resolve a entrada contra os bindings reais do `dependency-graph`, encontra o nó do grafo, aplica a semântica causal mínima e imprime uma leitura operacional curta.

## Como rodar

```bash
python3 dependency-graph/tools/causal_explain.py --itemid 69485
python3 dependency-graph/tools/causal_explain.py --triggerid 32506
python3 dependency-graph/tools/causal_explain.py --item-name "wg0 operational status"
python3 dependency-graph/tools/causal_explain.py --json --itemid 69689
```

## Entradas aceitas

- `--itemid <id>`
- `--triggerid <id>`
- `--item-name "<nome>"`
- `--trigger-name "<nome>"`
- `--json`

## Ordem de resolução

1. procura o binding em `dependency-graph/models/zabbix_graph_bindings.yaml`
2. resolve o `graph_node_id`
3. cruza o nó com os modelos de cluster
4. aplica a regra causal mínima em `dependency-graph/models/causal_correlation_rules.yaml`

## Saída esperada

- entrada recebida
- binding encontrado
- nó do grafo
- cluster
- node_role
- semântica de falha
- blast radius provável
- interpretação curta
- próximos checks recomendados
- limites da conclusão

## Exemplos validados

- `69485` -> `svc-apache2`, `service_failure`
- `32506` -> `svc-apache2`, `service_failure`
- `69486` -> `svc-unbound`, `service_failure`
- `69633` -> `svc-livecopilot-apache-edge`, `public_access_failure`
- `69689` -> `edge-mikrotik-wg0`, `overlay_failure`

## Limites

- a ferramenta não faz consulta ao Zabbix em tempo real
- a ferramenta não executa RCA completo
- se não houver binding, ela falha de forma honesta
- se a trigger não existir na base, isso aparece como parte do binding, não como erro mascarado

