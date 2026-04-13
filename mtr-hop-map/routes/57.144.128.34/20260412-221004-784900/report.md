# Rota individual - 57.144.128.34

## Identidade

- route_id: `route-facebook-57-144-128-34`
- target: `57.144.128.34`
- target_family: `facebook-meta`
- map_name: `MTR Route - 57.144.128.34`
- sysmapid: `17`
- run_id: `20260412-221004-784900`
- fonte: `live`

## Caminho observado

- baseline_path: `["10.45.0.1", "100.65.77.1", "172.16.128.221", "172.16.133.150", "172.16.128.113", "172.16.128.181", "177.37.221.191", "147.75.214.158", "129.134.60.178", "163.77.194.43", "57.144.128.34"]`
- first_seen: `2026-04-12T22:10:16.176908`
- baseline salvo em: `route_baseline.json`

## Classificação

- recurring_local_nodes: `10.45.0.1, 100.65.77.1, 172.16.128.221, 172.16.133.150, 172.16.128.113, 172.16.128.181`
- pivot_or_exit_point: `177.37.221.191`
- external_transit_nodes: `147.75.214.158, 163.77.194.43`
- service_family_facebook_meta: `129.134.60.178`
- destination_node: `57.144.128.34`
- unknown_nodes: `-`

## Política de monitoramento

- local_recurring_backbone: validar recorrencia e saude dos trechos adjacentes
- pivot_or_exit_point: usar quorum dos downstreams e continuidade da sequencia
- transit_external: preferir trigger sintetico por trecho
- service_family_facebook_meta: monitorar a familia Meta como bloco de caminho
- destination: monitorar reachability e comportamento final de 57.144.128.34
- unknown: preservar como gap de observacao, nao como host gerenciavel

## Validação

- rota validada como unidade: `true`
- destino alcançado: `true`
- baseline registrado: `true`
- mapa criado: `true`
- mapa global alterado: `false`
- mapa global canônico: `MTR Unified - Brisanet Observed` / `sysmapid 10`
- mapa individual: `MTR Route - 57.144.128.34` / `sysmapid 17`

## Evidências salvas

- `route_definition.json`
- `route_baseline.json`
- `route_classification.json`
- `route_monitoring_policy.json`
- `route_validation_report.json`
- `mtr_raw.json`
- `mtr_parsed.json`
- `mtr_normalized.json`
- `reconcile_phase1.json`
- `reconcile_phase2.json`
- `execution.json`
- `asn_summary.json`
- `map_metadata.json`
- `zabbix_map_snapshot.json`
- `report.md`
- `handoff.md`

