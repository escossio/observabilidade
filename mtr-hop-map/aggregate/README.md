# MTR Hop Map Aggregation

Camada de correlação offline sobre os runs já gerados pela frente `mtr-hop-map`.

## O que ela lê

- `data/runs/<run_id>/...`
- `mtr_normalized.json` como fonte principal
- `execution.json`, `map_metadata.json` e `report.md` quando existirem

## O que ela gera

- `aggregate_summary.json`
- `classification_summary.json`
- `hops_inventory.csv`
- `edge_candidates.csv`
- `report.md`

## Uso

```bash
cd /srv/observabilidade-zabbix/mtr-hop-map
python3 -m aggregate.main
python3 -m aggregate.main --runs-root data/runs
python3 -m aggregate.main --output-dir aggregate/data/runs/demo
```

## Interpretação

- `fato observado`: aparece diretamente em `mtr_normalized.json`
- `inferência heurística`: vem da classificação e dos rankings
- `hipótese fraca`: qualquer classe com confiança `low`

