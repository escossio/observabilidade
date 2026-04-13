# Handoff - rota individual 57.144.128.34

## Fechamento

- A rota individual oficial de `57.144.128.34` permaneceu no mapa `MTR Route - 57.144.128.34` (`sysmapid 17`).
- A topologia do mapa não foi alterada nesta rodada.
- O problema desta rodada era de monitoramento indevido nos hops externos intermediários, não de mapa.

## O que foi corrigido

- `177.37.221.191`: removida a herança nativa do template `ICMP Ping`.
- `147.75.214.158`: removida a herança nativa do template `ICMP Ping`.
- `129.134.60.178`: removida a herança nativa do template `ICMP Ping`, mantendo a classificação de familia Meta como observacional/sintética.
- `163.77.194.43`: removida a herança nativa do template `ICMP Ping`.
- `57.144.128.34`: monitoramento nativo preservado como destino final.

## Estado final

- intermediários externos: sem triggers nativas/default e sem problemas abertos.
- destino final: com triggers nativas preservadas.
- mapa individual: sem mudança de layout, sem recomputar rota e sem apagar host/mapa.

## Mudança no onboarding

- o onboarding agora classifica a política de monitoramento por classe de hop.
- `local_recurring_backbone` e `destination` seguem recebendo template ICMP nativo.
- `pivot_or_exit_point`, `transit_external`, `service_family_facebook_meta` e `unknown` passam a ser observacionais/sintéticos por padrão.
- a regra foi registrada em código e documentação para não repetir o incidente em novas rotas.

## Evidências

- `facebook_route_trigger_audit.json`
- `facebook_route_trigger_cleanup.json`
- `route_onboarding_policy_fix.json`
- `route_onboarding_diff.json`
- `route_monitoring_policy.json`
- `report.md`

## Limitações restantes

- a seleção entre `pivot_or_exit_point` e `service_family_facebook_meta` ainda depende da evidência do trace e do ASN/empresa observados.
- o próximo refinamento natural é sintetizar alertas por trecho quando houver histórico suficiente.
