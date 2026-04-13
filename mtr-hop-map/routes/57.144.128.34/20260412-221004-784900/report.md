# Rota individual - 57.144.128.34

## Fechamento desta rodada

- rota_id: `route-facebook-57-144-128-34`
- destino final: `57.144.128.34`
- mapa individual: `MTR Route - 57.144.128.34` / `sysmapid 17`
- mapa global canônico: `MTR Unified - Brisanet Observed` / `sysmapid 10`
- objetivo cumprido: limpar incidentes indevidos nos hops externos intermediários e preservar o monitoramento nativo do destino final

## Evidência da auditoria

- `177.37.221.191` carregava 4 triggers herdadas do template `ICMP Ping` e abriu 2 problemas ativos
- `147.75.214.158` carregava 4 triggers herdadas do template `ICMP Ping` e abriu 2 problemas ativos
- `129.134.60.178` carregava 4 triggers herdadas do template `ICMP Ping`, mas não tinha problema aberto no momento da auditoria
- `163.77.194.43` carregava 4 triggers herdadas do template `ICMP Ping` e abriu 2 problemas ativos
- `57.144.128.34` manteve 4 triggers nativas válidas para o destino e não tinha problema aberto

## Correção aplicada

- `177.37.221.191`: template `ICMP Ping` removido; problemas resolvidos automaticamente
- `147.75.214.158`: template `ICMP Ping` removido; problemas resolvidos automaticamente
- `129.134.60.178`: template `ICMP Ping` removido; host passou a operar como observacional/sintético
- `163.77.194.43`: template `ICMP Ping` removido; problemas resolvidos automaticamente
- `57.144.128.34`: template `ICMP Ping` preservado; política nativa de destino mantida

## Estado final da rota

- intermediários externos: sem triggers nativas/default de ICMP e sem problemas abertos
- 129.134.60.178: classificado como `service_family_facebook_meta`, sem herança nativa
- destino final: monitoramento nativo preservado
- mapa: sem alteração de topologia, sem recomputar a rota e sem apagar o mapa individual

## Mudança de onboarding

- hops `local_recurring_backbone` e `destination` continuam recebendo template ICMP nativo
- hops `pivot_or_exit_point`, `transit_external`, `service_family_facebook_meta` e `unknown` não herdam template ICMP padrão
- a regra ficou codificada em `src/hop_policy.py`, `src/zabbix_api.py` e `src/zabbix_reconcile.py`

## Artefatos desta rodada

- `facebook_route_trigger_audit.json`
- `facebook_route_trigger_cleanup.json`
- `route_onboarding_policy_fix.json`
- `route_onboarding_diff.json`
- `route_monitoring_policy.json`
- `report.md`
- `handoff.md`

## Limitações restantes

- a distinção entre `pivot_or_exit_point` e `service_family_facebook_meta` continua dependente da evidência observada no MTR e na empresa/ASN
- a política sintética ainda pode ser refinada com triggers por trecho quando houver série histórica suficiente

## Próximo passo natural

- reexecutar novas janelas da mesma rota para confirmar se a sequência permanece estável após a correção de policy
