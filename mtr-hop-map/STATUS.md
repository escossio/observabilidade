# Status

## 2026-04-06 - POC MTR hop map executada e estabilizada

- destino validado na POC:
  - `observabilidade.escossio.dev.br`
- mapa canônico criado no Zabbix:
  - `MTR ASN - observabilidade.escossio.dev.br`
  - `sysmapid`: `5`
- base de persistência definida:
  - grupo: `Transit / Hop` (`groupid 25`)
  - template ICMP: `ICMP Ping` (`templateid 10564`)
  - ícone: `Cloud_(96)` (`imageid 5`)
- cadência validada:
  - primeira execução criou o mapa
  - segunda execução reaproveitou o mesmo mapa sem duplicar hosts
  - terceira execução confirmou estado estável com `13` selements e `12` links
- rota consolidada:
  - `13` hops reais com IP
  - labels no mapa com apenas IP, ASN e empresa
  - ASN privado ficou como `AS private` / `Private / local network`
  - AS público resolvido via `whois.cymru.com`
- evidências principais:
  - `data/runs/20260406-235600/report.md`
  - `data/runs/20260406-235616/report.md`
  - `data/runs/20260406-235641/report.md`
- próxima etapa recomendada:
  - generalizar a frente para múltiplos destinos mantendo esta política de naming e reconciliação

## 2026-04-06 - frente MTR hop map iniciada

- destino canônico fechado para a POC:
  - `observabilidade.escossio.dev.br`
- decisões já travadas:
  - hostname: `hop-{destino_slug}-{ordem:02d}-{ip_normalizado}`
  - grupo de hosts: `Transit / Hop`
  - template: `ICMP Ping`
  - layout: linear horizontal
  - ASN ausente: `AS private` / `Private / local network`
  - hops sem IP real: não viram host
- base reaproveitada:
  - credenciais locais do Zabbix lidas do datasource provisionado em Grafana
  - ícone de nuvem do Zabbix já identificado: `Cloud_(96)` / `imageid 5`
  - API local já confirmada em `http://127.0.0.1:8081/api_jsonrpc.php`
- pendências imediatas:
  - implementar runner/parser/reconciliador
  - executar MTR real
  - reconciliar hosts, template e mapa
  - validar idempotência em segunda execução
