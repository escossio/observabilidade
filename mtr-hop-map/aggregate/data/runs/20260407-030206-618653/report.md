# MTR Hop Map - Mapa Unificado

## Critérios

- nó backbone observado: runs >= 8, targets >= 3, recurrence >= 0.7
- aresta canônica: runs >= 8, targets >= 3, estabilidade >= 0.75

## Backbone observado

- `10.45.0.1` - runs `22` - targets `15` - confidence `medium`
- `100.65.77.1` - runs `22` - targets `15` - confidence `medium`
- `172.16.128.221` - runs `22` - targets `15` - confidence `medium`
- `172.16.133.150` - runs `22` - targets `15` - confidence `medium`
- `172.16.128.113` - runs `22` - targets `15` - confidence `medium`
- `172.16.128.181` - runs `22` - targets `15` - confidence `medium`
- `172.16.128.182` - runs `21` - targets `12` - confidence `medium`
- `172.16.130.122` - runs `19` - targets `11` - confidence `medium`
- `172.16.134.242` - runs `19` - targets `11` - confidence `medium`
- `172.16.135.209` - runs `19` - targets `11` - confidence `medium`
- `172.16.128.42` - runs `19` - targets `11` - confidence `medium`

## Borda candidata

- `187.19.161.199` - edge `22` - runs `19` - confidence `high`

## Saídas CDN

- `104.21.4.50` - `Cloudflare, Inc.` - confidence `high`
- `172.67.131.172` - `Cloudflare, Inc.` - confidence `high`
- `108.170.226.233` - `Google LLC` - confidence `medium`
- `142.250.166.72` - `Google LLC` - confidence `medium`
- `192.178.110.171` - `Google LLC` - confidence `medium`

## Watchlist DNS

- `1.0.0.1` - confidence `high`
- `8.8.8.8` - confidence `high`

## Arestas promovidas

- `10.45.0.1 -> 100.65.77.1` - backbone observado - confidence `high`
- `100.65.77.1 -> 172.16.128.221` - backbone observado - confidence `high`
- `172.16.128.113 -> 172.16.128.181` - backbone observado - confidence `high`
- `172.16.128.181 -> 172.16.128.182` - backbone observado - confidence `high`
- `172.16.128.182 -> 172.16.130.122` - backbone observado - confidence `high`
- `172.16.128.221 -> 172.16.133.150` - backbone observado - confidence `high`
- `172.16.130.122 -> 172.16.134.242` - backbone observado - confidence `high`
- `172.16.133.150 -> 172.16.128.113` - backbone observado - confidence `high`
- `172.16.134.242 -> 172.16.135.209` - backbone observado - confidence `high`
- `172.16.135.209 -> 172.16.128.42` - backbone observado - confidence `high`
- `172.16.128.42 -> 187.19.161.199` - `candidate_edge` - confidence `high`
- `187.19.161.199 -> 104.21.4.50` - `cdn_exit` - confidence `high`
- `187.19.161.199 -> 108.170.226.233` - `cdn_exit` - confidence `medium`
- `187.19.161.199 -> 142.250.166.72` - `cdn_exit` - confidence `medium`
- `187.19.161.199 -> 172.67.131.172` - `cdn_exit` - confidence `high`
- `187.19.161.199 -> 192.178.110.171` - `cdn_exit` - confidence `medium`

## Zabbix

- sysmapid: `10`
- elementos: `39`
- links: `16`
- mapa: `MTR Unified - Brisanet Observed`

## Watchlist ausente do corpus

- `177.37.220.17`
- `177.37.220.18`

## Distinção de camadas

- backbone observado: nós e arestas com recorrência alta e estável
- candidatos: nós/arestas com evidência forte mas ainda heurística
- watchlist: itens observáveis ou ausentes que precisam de monitoramento separado

## Artefatos

- `unified_nodes.json`
- `unified_edges.json`
- `unified_map_plan.json`
