# noc_shift_summary

## O que faz

Gera um resumo operacional de turno/NOC a partir dos problemas recentes do Zabbix já explicados pela camada causal.

Ele reaproveita `explain_recent_events`, agrupa por semântica, cluster, host e trigger e fecha com uma leitura final curta.

## Como rodar

```bash
python3 dependency-graph/tools/noc_shift_summary.py --minutes 720 --limit 8
python3 dependency-graph/tools/noc_shift_summary.py --minutes 720 --limit 3 --host agt01
python3 dependency-graph/tools/noc_shift_summary.py --minutes 120 --limit 5 --open-only
python3 dependency-graph/tools/noc_shift_summary.py --minutes 720 --limit 8 --json
```

## Entradas aceitas

- `--minutes <N>`
- `--limit <N>`
- `--host "<nome>"`
- `--severity <nível>`
- `--open-only`
- `--json`

## O que mostra

- totais do período
- agrupamento por semântica
- agrupamento por cluster
- agrupamento por host
- top triggers/eventos
- leitura final resumida

## Relação com `explain_recent_events`

- `explain_recent_events` resolve evento por evento
- `noc_shift_summary` consolida o mesmo conjunto em leitura de turno/NOC
- a semântica continua centralizada em `causal_explain`

## Limites

- a ferramenta depende do runtime recente do Zabbix
- eventos sem binding não são explicados
- `--open-only` pode retornar vazio dependendo do período consultado
- não é daemon nem substitui RCA completo

