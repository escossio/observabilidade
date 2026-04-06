# noc_shift_summary Validation

## Objetivo

Validar a CLI `dependency-graph/tools/noc_shift_summary.py` como resumo operacional de turno/NOC.

## Execuções

### Janela ampla

```bash
python3 dependency-graph/tools/noc_shift_summary.py --minutes 720 --limit 8
```

- total de eventos: `6`
- explicados: `6`
- sem binding: `0`
- semântica dominante: `service_failure`
- cluster dominante: `AGT`
- host dominante: `agt01`
- problemas públicos: `não`
- problemas WAN principal: `não`

### Janela filtrada por host

```bash
python3 dependency-graph/tools/noc_shift_summary.py --minutes 720 --limit 3 --host agt01
```

- total de eventos: `3`
- explicados: `3`
- sem binding: `0`
- leitura final coerente com AGT
- top triggers: `Apache2 parado` e `unbound parado`

### Janela aberta recente

```bash
python3 dependency-graph/tools/noc_shift_summary.py --minutes 120 --limit 5 --open-only
```

- total de eventos: `0`
- consulta válida
- nenhum evento aberto recente no runtime atual

### JSON

```bash
python3 dependency-graph/tools/noc_shift_summary.py --minutes 720 --limit 8 --json
```

- JSON gerado com `period`, `summary` e `results`
- campos úteis retornados:
  - `dominant_semantics`
  - `most_affected_cluster`
  - `most_affected_host`
  - `public_surface_issues_present`
  - `wan_primary_issues_present`
  - `unbound_events_present`
  - `apache_events_present`
  - `unexplained_events`

## O que a validação confirmou

- a ferramenta roda localmente
- a ferramenta reaproveita `explain_recent_events` e, por consequência, `causal_explain`
- a agregação por semântica, cluster e host ficou útil para leitura de turno
- o resumo final separa corretamente superfície pública, WAN principal e serviços locais

## Limites observados

- a consulta depende do runtime recente do Zabbix
- `open-only` pode retornar vazio
- problemas sem binding não entram na leitura causal
- não substitui RCA completo nem operação em tempo real contínuo

