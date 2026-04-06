# explain_recent_events Validation

## Objetivo

Validar a CLI `dependency-graph/tools/explain_recent_events.py` usando o runtime atual do Zabbix.

## Execuções

### Janela ampla, saída textual

```bash
python3 dependency-graph/tools/explain_recent_events.py --minutes 720 --limit 8
```

- total de eventos: `6`
- explicados: `6`
- sem binding: `0`
- abertos: `0`
- resolvidos: `6`
- semântica dominante: `service_failure`

### Janela ampla, filtro por host

```bash
python3 dependency-graph/tools/explain_recent_events.py --minutes 720 --limit 3 --host agt01
```

- total de eventos: `3`
- explicados: `3`
- sem binding: `0`
- host filtrado com sucesso: `agt01`
- leitura causal consistente com Apache2 e unbound

### Saída JSON

```bash
python3 dependency-graph/tools/explain_recent_events.py --minutes 720 --limit 3 --host agt01 --json
```

- JSON gerado com `results` e `summary`
- cada evento trouxe `event`, `binding`, `causal` e `node`
- resumo por semântica: `service_failure`

### Janela aberta recente

```bash
python3 dependency-graph/tools/explain_recent_events.py --minutes 120 --limit 5 --open-only
```

- total de eventos: `0`
- explicados: `0`
- sem binding: `0`
- a consulta funcionou, mesmo sem problemas abertos recentes

## O que a validação confirmou

- a CLI consulta problemas recentes do Zabbix de verdade
- a CLI reaproveita `causal_explain` como motor de leitura
- a consolidação final fica útil para triagem operacional
- a ferramenta não inventa binding

## Limites observados

- `open-only` pode retornar vazio dependendo do estado atual do runtime
- problemas sem binding continuam invisíveis na leitura causal
- a ferramenta é de resumo, não de monitoramento contínuo

