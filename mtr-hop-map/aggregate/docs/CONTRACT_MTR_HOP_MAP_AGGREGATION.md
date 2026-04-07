# Contract - MTR Hop Map Aggregation

## Objetivo

Agregação offline dos runs do `mtr-hop-map` para descobrir recorrência, bordas prováveis e classes heurísticas de nós.

Na publicação agregada, a camada passa a consolidar tudo em um único mapa canônico:

- `MTR Unified - Brisanet Observed`

## Fonte principal

- `data/runs/` da frente `mtr-hop-map`
- cada arquivo `mtr_normalized.json` é uma amostra de trace
- `execution.json`, `map_metadata.json` e `report.md` são usados para resolver destino, modo e contexto quando existirem

## Taxonomia mínima

- `internal_brisanet`
- `edge_brisanet_candidate`
- `ix_ptt_candidate`
- `cdn_candidate`
- `dns_infra_candidate`
- `destination`
- `unknown`

## Modelo de confiança

- `high`
- `medium`
- `low`

Cada classificação traz:

- `confidence`
- `evidence`
- `source_type` (`observed`, `inferred`, `external_hint`)

## Heurística de borda Brisanet

- último nó ainda associado à Brisanet/AS28126 antes da saída para ASN externo
- recorrência conta mais que uma ocorrência isolada
- o relatório precisa mostrar contagem de edge e contagem de último hop interno

## Heurística de IX/PTT

- nomes, empresas ou ASN com pistas explícitas de IX/PTT
- quando não houver evidência, o resultado deve aparecer como ausente ou de confiança baixa

## Heurística de CDN

- ASN/empresa conhecidos de CDN
- repetição como final de caminho
- papel recorrente em traces diferentes

## Watchlist DNS

- `177.37.220.17`
- `177.37.220.18`

Se não aparecerem no corpus, o output precisa registrar ausência observada, não inferir presença.

## Saídas

- `aggregate_summary.json`
- `classification_summary.json`
- `hops_inventory.csv`
- `edge_candidates.csv`
- `report.md`
- `unified_nodes.json`
- `unified_edges.json`
- `unified_map_plan.json`
- `zabbix_map_snapshot.json` quando publicado
