# Handoff - MTR Hop Map

## 2026-04-07 - debian2-1 monitorado no Zabbix

- o host `debian2-1` foi criado/reaproveitado no Zabbix
- hostid: `10844`
- grupo: `Remote Sources`
- template: `ICMP Ping`
- monitoramento: `ICMP` via host remoto `10.45.0.2`
- wrapper idempotente: `scripts/ensure_debian2_monitoring.sh`
- config versionada: `sources/debian2-1.json`
- o smoke test remoto segue salvo em `data/runs/20260407-remote-debian2-1-debian2-1-smoke/`

## 2026-04-07 - preparação da origem remota debian2-1

- origem remota registrada: `debian2-1`
- host remoto: `10.45.0.2`
- usuário remoto: `root`
- hostname remoto confirmado: `debian2-1.escossio.dev.br`
- comando remoto padronizado: `/usr/bin/mtr -4 -n -r -c 2 --report-wide --aslookup --json <destino>`
- wrapper local: `scripts/run_remote_source_smoke.sh`
- config local: `sources/debian2-1.json`
- smoke test salvo em `data/runs/20260407-remote-debian2-1-debian2-1-smoke/`

## 2026-04-07 - acabamento visual do mapa canônico

- o mapa canônico único `MTR Unified - Brisanet Observed` continua no `sysmapid 10`
- esta rodada mexeu só em apresentação visual
- o canvas foi ampliado e os ícones ficaram padronizados por classe
- o tronco principal ficou mais limpo e os ramos externos foram separados visualmente
- as ligações corretas foram preservadas

## 2026-04-07 - expansão da frente com Prime Video, Instagram, Microsoft e Akamai

- a frente já validou traces live para:
  - `www.primevideo.com`
  - `www.instagram.com`
  - `www.microsoft.com`
  - `account.microsoft.com`
  - `outlook.live.com`
  - `www.xbox.com`
  - `8.8.8.8`
  - `9.9.9.9`
- a coleta revelou novas famílias externas:
  - Prime Video / Amazon
  - Instagram / Meta
  - Microsoft
  - Akamai
- a pré-seleção Akamai foi baseada em DNS:
  - `www.microsoft.com -> e13678.dscb.akamaiedge.net`
  - `account.microsoft.com -> e9412.b.akamaiedge.net`
  - `www.xbox.com -> e1822.dsca.akamaiedge.net`
- o mapa canônico único continua sendo `MTR Unified - Brisanet Observed` no `sysmapid 10`

## 2026-04-07 - JSON stdout canônico

- A CLI ganhou `--json` para consumo automático.
- O stdout JSON ficou separado do plano profundo em `reconciliation_plan.json`.
- A validação cobriu destino único, lote, replay e dry-run, incluindo falha parcial em lote.

## O que foi construído

Frente nova para transformar MTR com ASN em hosts e mapa Zabbix persistentes.

## O que esta POC entrega

- execução de `mtr --aslookup`
- parser normalizado de hops
- lookup ASN/empresa com cache local e fallback
- criação/reuso de grupo, template, hosts e mapa
- mapa linear por destino
- execução em lote com tolerância a falha por destino
- replay controlado de snapshots MTR
- relatório local agregado por execução e detalhado por destino
- dry-run com plano completo e escrita bloqueada
- validação de idempotência

## Decisões fechadas na prática

- modelo de identidade: host global por IP + mapa específico por destino
- hostname dos hops: `hop-ip-{ip_normalizado}`
- grupo Zabbix: `Transit / Hop`
- template ICMP: `ICMP Ping`
- estratégia do template: reutilizar o template oficial do Zabbix quando existir; fallback local apenas se faltar no ambiente
- nó sem IP real: não vira host
- ASN ausente: `AS private` / `Private / local network`
- falha de `whois`: usar cache local e depois hint ASN do MTR
- layout: horizontal linear, com um nó por hop real
- rótulo de nó: somente IP, ASN e empresa
- entrada de lote:
  - `--target` repetido
  - `--targets-file` com `destino` ou `destino<TAB>replay.json`
- metadata operacional do mapa:
  - `source`, `target`, `target_slug`, `mode`, `last_trace`
  - Zabbix 7.4 sem tags nativas de `sysmap`, então a metadata fica nos artefatos da automação
- falha de destino invalido:
  - retorna erro operacional legível sem interromper os outros destinos do lote
- dry-run:
  - bloqueia escrita no `ZabbixAPI.call()` para `create` e `update`
  - grava `reconciliation_plan.json`
  - mantém `exit code 0` quando o processamento termina sem erro técnico

## Evidência real

- destino validado: `observabilidade.escossio.dev.br`
- mapa canônico: `MTR ASN - observabilidade.escossio.dev.br`
- sysmap final: `5`
- estado final validado: `13` selements e `12` links
- idempotência confirmada:
  - `data/runs/20260406-235600/`
  - `data/runs/20260406-235616/`
  - `data/runs/20260406-235641/`
- endurecimento validado:
  - `data/runs/20260407-001513/`
  - `data/runs/20260407-001546/`
  - `data/runs/20260407-001556/`
  - `data/runs/20260407-001611/`
- generalização live validada:
  - `data/runs/20260407-003427/`
  - mapas:
    - `MTR ASN - observabilidade.escossio.dev.br` -> `sysmapid 5`
    - `MTR ASN - one.one.one.one` -> `sysmapid 8`
  - falha isolada:
    - `invalid.invalid` falhou sem criar mapa
  - hostids compartilhados entre os mapas `5` e `8`:
    - `10780` até `10791`
- replay em lote validado:
  - `data/runs/20260407-003511/`
  - suite:
    - `data/replays/replay-suite-targets.txt`
  - mapa novo:
    - `MTR ASN - one.one.one.one-replay-validation` -> `sysmapid 9`
- dry-run validado:
  - destino único
  - lote com falha parcial
  - replay individual
  - nenhuma escrita observada no Zabbix antes/depois

## Próximo passo

Adicionar suíte mais ampla de churn de rota e, se fizer sentido, uma camada de agenda/orquestração leve acima desta CLI.
