# Status

# Status

## 2026-04-13 - rota Facebook/Meta 57.144.128.34 corrigida e onboarding endurecido

- a rota individual `route-facebook-57-144-128-34` foi limpa sem mexer no mapa `MTR Route - 57.144.128.34`
- `177.37.221.191`, `147.75.214.158`, `129.134.60.178` e `163.77.194.43` perderam a heranca nativa do template `ICMP Ping`
- os problemas ativos nessas ocorrencias foram resolvidos apos a limpeza de template
- `57.144.128.34` continuou com monitoramento nativo como destino final
- o onboarding agora classifica a politica por classe e impede template ICMP padrao em:
  - `pivot_or_exit_point`
  - `transit_external`
  - `service_family_facebook_meta`
  - `unknown`
- os arquivos de evidencia e politica foram gravados em:
  - `routes/57.144.128.34/20260412-221004-784900/`
- a documentacao geral da frente passou a explicitar a politica de template por classe

## 2026-04-12 - rota individual oficial de 57.144.128.34 inaugurada

- destino inaugural da familia Facebook/Meta:
  - `57.144.128.34`
- rota individual oficial criada com:
  - `route_id route-facebook-57-144-128-34`
  - `map_name MTR Route - 57.144.128.34`
  - `sysmapid 17`
- o baseline inicial da rota foi salvo em:
  - `routes/57.144.128.34/20260412-221004-784900/route_baseline.json`
- os artefatos formais da rota individual ficaram em:
  - `routes/57.144.128.34/20260412-221004-784900/`
- a classificação separou a rota em:
  - `local_recurring_backbone`
  - `pivot_or_exit_point`
  - `transit_external`
  - `service_family_facebook_meta`
  - `destination`
- a malha local reutilizou o edge Brisanet candidato `177.37.221.191`
- o mapa global canônico permaneceu intacto em:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- o reconciliador continuou a criar o sysmap vazio primeiro e a renderizar somente hops com IP no Zabbix

## 2026-04-12 - rota individual oficial de dell.com inaugurada

- destino inaugural do novo fluxo:
  - `dell.com`
- rota individual oficial criada com:
  - `route_id route-dell-com`
  - `map_name MTR ASN - dell.com`
  - `sysmapid 16`
- o baseline inicial da rota foi salvo em:
  - `routes/dell.com/20260412-220216-226816/route_baseline.json`
- os artefatos formais da rota individual ficaram em:
  - `routes/dell.com/20260412-220216-226816/`
- a classificação separou a rota em:
  - `local_recurring_backbone`
  - `pivot_or_exit_point`
  - `transit_external`
  - `service_family_dell_att`
  - `destination`
  - `unknown`
- o mapa global canônico permaneceu intacto em:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- o reconciliador foi ajustado para:
  - criar o sysmap vazio primeiro
  - renderizar apenas hops com IP no Zabbix
  - manter os `no-response` só como evidência e não como elementos vazios

## 2026-04-07 - debian2 espelhado no baseline do AGT

- baseline de referência:
  - host `agt01`
- host final no Zabbix:
  - `debian2`
- baseline aplicado:
  - grupo `Linux servers`
  - template `Linux by Zabbix agent`
  - interface `10.45.0.2:10050`
  - inventário `-1`
  - sem tags e sem macros específicas
- agent remoto preparado com override explícito:
  - `/etc/zabbix/zabbix_agentd.conf.d/90-debian2-baseline.conf`
- validação real:
  - SSH sem senha ok
  - `zabbix_get` respondeu `agent.ping`, `agent.version`, `system.uptime` e `system.cpu.load[all,avg1]`
- artefatos da rodada salvos em:
  - `data/runs/20260407-debian2-baseline/`
- o mapa do MTR/Zabbix não foi alterado

## 2026-04-07 - mapa unificado expandido com novos ramos

- fonte de verdade desta rodada:
  - `replay` controlado para os 4 alvos
  - run consolidado em `data/runs/20260407-030220-957449/`
- o mapa canônico único `MTR Unified - Brisanet Observed` foi expandido in-place no `sysmapid 10`
- os alvos desta rodada trouxeram novos ramos para o mesmo grafo:
  - `8.8.8.8` -> Google
  - `9.9.9.9` -> Quad9
  - `dell.com` -> Dell
  - `wiki.mikrotik.com` -> Mikrotik
- o grafo final manteve:
  - tronco comum recorrente
  - borda candidata `187.19.161.199`
  - saídas externas/CDN relevantes
  - watchlist DNS sem promoção indevida
- estado final publicado:
  - `39` elementos
  - `38` links
- artefatos novos relevantes:
  - `data/runs/20260407-030220-957449/target_branch_analysis.json`
  - `aggregate/data/runs/20260407-030253-324917/unified_nodes.json`
  - `aggregate/data/runs/20260407-030253-324917/unified_edges.json`
  - `aggregate/data/runs/20260407-030253-324917/unified_map_plan.json`
  - `aggregate/data/runs/20260407-030253-324917/zabbix_map_snapshot.json`
- validação final cruzada manteve o mapa canônico `sysmapid 10` intacto e sem duplicação de IPs equivalentes


## 2026-04-07 - mapa agregado unificado publicado

- a camada de agregação passou a consolidar o corpus em um único mapa canônico:
  - `MTR Unified - Brisanet Observed`
- a publicação foi feita in-place no `sysmapid 10`
- o mapa único preserva:
  - backbone observado
  - borda candidata
  - saídas externas/CDN
  - watchlist DNS
- artefatos novos da rodada:
  - `aggregate/unified_nodes.json`
  - `aggregate/unified_edges.json`
  - `aggregate/unified_map_plan.json`
  - `aggregate/zabbix_map_snapshot.json`

## 2026-04-07 - camada de agregacao de traces criada

- nova camada `aggregate/` para ler os runs já gerados e montar uma visão agregada de recorrência e fronteira
- heurísticas iniciais implementadas:
  - `internal_brisanet`
  - `edge_brisanet_candidate`
  - `ix_ptt_candidate`
  - `cdn_candidate`
  - `dns_infra_candidate`
  - `destination`
  - `unknown`
- leitura explícita para:
  - `177.37.220.17`
  - `177.37.220.18`
- saídas estruturadas:
  - `aggregate_summary.json`
  - `classification_summary.json`
  - `hops_inventory.csv`
  - `edge_candidates.csv`
  - `report.md`
- corpus agregado nesta rodada:
  - `19` runs
  - `22` targets
  - `15` hops únicos
  - `3` paths únicos
- principal candidato a borda Brisanet:
  - `187.19.161.199`
- IX/PTT:
  - nenhum candidato forte no corpus atual
- DNS watchlist:
  - os IPs `177.37.220.17` e `177.37.220.18` não apareceram nos traces analisados

## 2026-04-07 - JSON stdout canônico implementado

- A CLI ganhou `--json` para emissão de um contrato estável de stdout.
- O JSON de stdout ficou separado do `reconciliation_plan.json` e do `report.md`.
- A validação cobriu destino único, dry-run, lote com falha parcial e replay.
- A execução dry-run seguiu sem escrita no Zabbix.

## 2026-04-07 - dry-run de reconciliação implementado

- comportamento fechado:
  - `--dry-run` executa a pipeline inteira de `mtr`, parsing, enrichment, matching e diff
  - a escrita no Zabbix fica bloqueada no ponto único `ZabbixAPI.call()` para métodos de create/update
  - o plano completo é salvo em `reconciliation_plan.json`
  - o resumo humano fica em `report.md`
- validação real desta rodada:
  - destino único dry-run: `observabilidade.escossio.dev.br`
  - lote dry-run: `observabilidade.escossio.dev.br`, `one.one.one.one`, `invalid.invalid`
  - replay dry-run: `observabilidade.escossio.dev.br` com `observabilidade-route-b.json`
  - nenhum dos dry-runs alterou o estado do Zabbix; leitura antes/depois permaneceu igual
- evidências principais:
  - run dry-run de destino único: `data/runs/20260407-011601-018210/`
  - run dry-run de lote: `data/runs/20260407-011617-903048/`
  - run dry-run de replay: `data/runs/20260407-011601-018210/`
- decisão de saída:
  - exit code continua `0` quando a execução técnica termina sem erro, mesmo com mudanças previstas
  - falhas reais continuam retornando código não zero

## 2026-04-07 - generalizacao controlada para multiplos destinos

- decisao de execucao fechada:
  - destino unico: `--target <destino>`
  - lote simples: repetir `--target`
  - lote por arquivo: `--targets-file <arquivo>`
  - replay/teste: `--target <destino> --replay <json>` ou linha `destino<TAB>replay.json` no arquivo
- convencao final de mapa:
  - nome canonico: `MTR ASN - <destino>`
  - metadata operacional: `source`, `target`, `target_slug`, `mode`, `last_trace`
  - Zabbix 7.4 nao expõe tags nativas em `sysmap`; por isso a metadata do mapa fica versionada em `map_metadata.json` e no resumo agregado do run
- estrutura de artefatos atual:
  - run agregado: `data/runs/<run_id>/`
  - por destino: `data/runs/<run_id>/targets/<ordem>-<target_slug>/`
  - relatorio agregado: `data/runs/<run_id>/report.md`
- validacao live desta rodada:
  - run: `data/runs/20260407-003427/`
  - destinos: `observabilidade.escossio.dev.br`, `one.one.one.one`, `invalid.invalid`
  - mapas confirmados:
    - `MTR ASN - observabilidade.escossio.dev.br` -> `sysmapid 5`
    - `MTR ASN - one.one.one.one` -> `sysmapid 8`
    - `invalid.invalid` nao criou mapa
  - lote tolerante a falha: um destino falhou sem derrubar os outros dois
  - reuso global por IP confirmado entre os mapas `5` e `8` com hostids compartilhados `10780..10791`
- replay automatizado ampliado:
  - fixture nova: `data/replays/one-one-one-one-route-a.json`
  - suite nova: `data/replays/replay-suite-targets.txt`
  - run: `data/runs/20260407-003511/`
  - mapa novo de replay: `MTR ASN - one.one.one.one-replay-validation` -> `sysmapid 9`
- endurecimento adicional:
  - `mtr_runner` agora devolve erro operacional legivel quando o destino e invalido ou o JSON do `mtr` vem quebrado

## 2026-04-07 - identidade global por IP, replay de rota e fallback ASN validados

- decisao de arquitetura fechada:
  - host de hop agora e `global por IP`
  - mapa continua `especifico por destino`
  - ordem de hop fica na execucao e no mapa, nao na identidade do host
- mudancas de codigo aplicadas:
  - hostname canônico mudou para `hop-ip-{ip_normalizado}`
  - reuso de host passou a procurar pelo IP no grupo `Transit / Hop`
  - hosts antigos da POC foram migrados in-place para a identidade canônica global
  - enrichment ASN ganhou cache persistente em `data/cache/asn_company_cache.json`
  - enrichment ASN ganhou modo `offline` e fallback por hint do MTR
  - a frente passou a aceitar replay com `--mtr-json`
- validacao real executada:
  - rota estavel no mapa canonico:
    - run: `data/runs/20260407-001513/`
    - mapa: `sysmapid 5`
    - resultado: hosts migrados para `global-ip` e segunda fase toda em `reused`
  - rota alterada por replay controlado:
    - snapshot A: `data/replays/observabilidade-route-a.json`
    - snapshot B: `data/replays/observabilidade-route-b.json`
    - runs: `data/runs/20260407-001546/` e `data/runs/20260407-001556/`
    - mapa de validacao: `sysmapid 6`
    - resultado: o mapa trocou o ultimo hop de `104.21.4.50` para `172.67.131.172`, sem apagar o host antigo `10793`
  - fallback ASN:
    - run: `data/runs/20260407-001611/`
    - modo: `offline`
    - resultado: execucao seguiu com `AS28126` e `AS13335` vindos do hint do MTR e empresa `Unknown ASN`
- estado final no runtime:
  - grupo `Transit / Hop`: `14` hosts
  - todos os hosts do grupo com tags `identity_scope=global-ip` e `canonical_ip=<ip>`
  - mapa canonico `sysmapid 5`: `13` selements e `12` links
  - mapa replay `sysmapid 6`: `13` selements e `12` links
  - mapa fallback `sysmapid 7`: `13` selements e `12` links
- template ICMP:
  - o ambiente tem `ICMP Ping` oficial da Zabbix (`templateid 10564`)
  - a frente agora reutiliza esse template como padrao
  - criacao de template local so acontece se o ambiente nao tiver o template oficial

## 2026-04-07 - hipótese de endurecimento da frente

- risco principal identificado:
  - a identidade do host ainda está acoplada a `destino + ordem + ip`, o que não é canônico para reuso global por IP
- risco de reconciliação:
  - a frente já reconcilia o mapa atual, mas ainda não tem replay controlado para provar rota mutável de forma reproduzível
- risco de enrichment ASN:
  - o lookup em `whois.cymru.com` ainda pode falhar de forma abrupta porque não há cache persistente nem modo degradado explícito
- risco de template:
  - o template `ICMP Ping` existe e funciona, mas ainda não está documentado como padrão local reutilizável da solução

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
# Status

## 2026-04-07 - debian2-1 registrado no Zabbix como origem monitorada

- source remota canônica: `debian2-1`
- host remoto: `10.45.0.2`
- usuário remoto efetivo: `root`
- hostname remoto confirmado: `debian2-1.escossio.dev.br`
- o host Zabbix foi criado/reaproveitado com:
  - grupo `Remote Sources`
  - template `ICMP Ping`
  - `hostid 10844`
- a source remota versionada está em:
  - `sources/debian2-1.json`
- o wrapper idempotente de monitoramento está em:
  - `scripts/ensure_debian2_monitoring.sh`
- o smoke test remoto anterior permanece como evidência em:
  - `data/runs/20260407-remote-debian2-1-debian2-1-smoke/`
- o mapa canônico `sysmapid 10` não sofreu alteração

## 2026-04-07 - source remota debian2-1 preparada

- source remota canônica: `debian2-1`
- host remoto: `10.45.0.2`
- usuário remoto efetivo: `root`
- hostname remoto confirmado: `debian2-1.escossio.dev.br`
- comando padronizado de coleta:
  - `/usr/bin/mtr -4 -n -r -c 2 --report-wide --aslookup --json <destino>`
- wrapper local versionado:
  - `scripts/run_remote_source_smoke.sh`
- configuração local versionada:
  - `sources/debian2-1.json`
- smoke test executado com sucesso para `8.8.8.8`
- nenhum mapa do Zabbix foi alterado
