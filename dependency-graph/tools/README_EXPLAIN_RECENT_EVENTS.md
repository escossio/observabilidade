# explain_recent_events

## O que faz

Consulta problemas/eventos recentes no Zabbix e transforma cada trigger relevante em uma leitura causal curta usando `causal_explain`.

## Como rodar

```bash
python3 dependency-graph/tools/explain_recent_events.py --minutes 60 --limit 8
python3 dependency-graph/tools/explain_recent_events.py --minutes 120 --limit 8 --open-only
python3 dependency-graph/tools/explain_recent_events.py --minutes 720 --limit 8 --json
```

## Entradas aceitas

- `--minutes <N>`
- `--limit <N>`
- `--host "<nome>"`
- `--severity <nível>`
- `--open-only`
- `--json`

## Como funciona

1. consulta a tabela de problemas recentes do Zabbix
2. extrai `triggerid` do problema
3. chama `causal_explain` para resolver o binding
4. consolida por evento e no resumo final

## Saída esperada

- timestamp do evento
- host
- trigger/evento
- nó correlacionado
- cluster
- semântica
- blast radius
- leitura curta
- status open/resolved quando disponível
- resumo consolidado no final

## Exemplo validado

Rodada real com `--minutes 720 --limit 8` retornou 6 eventos resolvidos, todos mapeados para `service_failure`:

- `Apache2 parado`
- `unbound parado`
- `Apache2 parado`
- `unbound parado`
- `Apache2 parado`
- `unbound parado`

## Limites

- a consulta depende do conteúdo recente do runtime do Zabbix
- problemas sem binding não são explicados
- a ferramenta não substitui RCA completo
- `--host` e `--severity` são filtros opcionais simples, úteis para triagem rápida

## Relação com `causal_explain`

- `causal_explain` resolve um sinal individual
- `explain_recent_events` agrega sinais recentes e reutiliza `causal_explain` como motor de leitura
- a lógica de semântica continua centralizada na CLI já validada

