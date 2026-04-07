# MTR Hop Map - Agregação

## Escopo

- agregação de múltiplos runs, replays e batches já coletados pela frente `mtr-hop-map`
- foco em recorrência de hops, candidatos de borda Brisanet, IX/PTT, CDN e DNS infra
- distinção explícita entre fato observado, inferência heurística e hipótese fraca

## Resumo

- runs lidos: `22`
- targets lidos: `30`
- hops únicos: `39`
- paths únicos: `7`

## Hops mais recorrentes

- `10.45.0.1` - `30` ocorrências - `internal_brisanet` - confiança `medium`
- `100.65.77.1` - `30` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.128.113` - `30` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.128.181` - `30` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.128.221` - `30` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.133.150` - `30` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.128.182` - `24` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.128.42` - `22` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.130.122` - `22` ocorrências - `internal_brisanet` - confiança `medium`
- `172.16.134.242` - `22` ocorrências - `internal_brisanet` - confiança `medium`

## Candidatos a borda Brisanet

- `187.19.161.199` - edge `22` - last-internal `22` - confiança `high`

## Candidatos IX/PTT

- nenhum candidato forte observado no corpus atual

## Candidatos CDN

- `104.21.4.50` - `Cloudflare, Inc.` - confiança `high`
- `172.67.131.172` - `Cloudflare, Inc.` - confiança `high`
- `108.170.226.233` - `Google LLC` - confiança `medium`
- `142.250.166.72` - `Google LLC` - confiança `medium`
- `192.178.110.171` - `Google LLC` - confiança `medium`

## DNS infra 177.37.220.17 / 177.37.220.18

- 177.37.220.17: absent_from_current_corpus - confiança `low`
- 177.37.220.18: absent_from_current_corpus - confiança `low`

## Distinção de evidência

- fatos observados vêm diretamente dos hops agregados dos runs
- inferências heurísticas vêm das regras de recorrência, posição no caminho e ASN/empresa
- hipóteses fracas ficam marcadas com confiança baixa e evidência limitada

## Arquivos

- `aggregate_summary.json`
- `classification_summary.json`
- `hops_inventory.csv`
- `edge_candidates.csv`
