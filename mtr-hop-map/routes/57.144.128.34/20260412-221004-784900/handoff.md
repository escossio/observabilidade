# Handoff - rota individual 57.144.128.34

## Fechamento

- A rota individual oficial de `57.144.128.34` foi criada com `route_id` `route-facebook-57-144-128-34`.
- O mapa individual foi publicado no Zabbix como `MTR Route - 57.144.128.34` (`sysmapid 17`).
- O baseline inicial ficou ancorado na coleta live de `20260412-221004-784900`.
- O mapa canônico global permaneceu em `sysmapid 10`.

## O que a rodada consolidou

- `177.37.221.191` foi registrado como pivot de saída e reaproveitamento de edge Brisanet candidato.
- `147.75.214.158` e `163.77.194.43` ficaram como trânsito externo.
- `129.134.60.178` ficou como familia Facebook/Meta antes do destino final.
- `57.144.128.34` ficou como destino final da rota individual.

## O que mudou no código

- O reconciliador já vinha criando o sysmap vazio primeiro e renderizando só hops com IP.
- Nesta rodada, nenhuma mudança estrutural adicional foi necessária para o Zabbix aceitar a rota.

## Limitações restantes

- A classificação de `service_family_facebook_meta` continua heurística e depende da topologia observada nesta primeira rota.
- Ainda não existe um gerador automático dedicado para criar a pasta da rota individual a partir de qualquer novo run sem script auxiliar.

## Próximo passo natural

- Reexecutar `57.144.128.34` em novas janelas para validar se a sequência se mantém ou se uma variante persistente aparece.

