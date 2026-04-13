# MTR Hop Map

Frente para transformar uma rota observada com `mtr --aslookup` em objetos persistentes no Zabbix:

- cada hop com IP vira host monitorável
- cada mapa continua específico por destino
- cada host de hop passa a ser canônico por IP
- o mapa final é linear e canônico por destino
- o rótulo de cada hop mostra só IP, ASN e empresa

## Decisões fechadas

- destino canônico desta POC: `observabilidade.escossio.dev.br`
- identidade de host: `global por IP`
- padrão de hostname: `hop-ip-{ip_normalizado}`
- grupo de hosts: `Transit / Hop`
- template monitorável padrão: `ICMP Ping`
- estratégia do template: reutilizar o template oficial do Zabbix quando ele existir; criar fallback local só se ele não existir
- template group esperado: `Templates/Network devices`
- tratamento de hops sem IP real: não criam host
- tratamento de ASN ausente: `AS private` / `Private / local network`
- fallback ASN público: `ASN do MTR + Unknown ASN` quando o `whois` não puder ser usado
- cache ASN/empresa: `data/cache/asn_company_cache.json`
- layout do mapa: linear horizontal
- execução em lote: tolerante a falha por destino
- `--dry-run`: calcula o plano completo sem escrever no Zabbix
- `--json`: emite contrato canônico de stdout para automação
- metadata de mapa: `source`, `target`, `target_slug`, `mode`, `last_trace`
- limitação do Zabbix: `sysmap` não tem tags nativas; a metadata fica em `map_metadata.json` e no relatório agregado

## Estrutura

- `src/`: runner, parser, política, cliente Zabbix e reconciliador
- `scripts/`: invocação prática do POC
- `data/replays/`: snapshots controlados para replay de rota
- `data/runs/`: evidências de cada execução
- `docs/`: contrato e handoff da frente
- `data/runs/<run_id>/targets/<ordem>-<target_slug>/`: artefatos por destino dentro do lote
- `aggregate/`: camada de correlação e classificação sobre os runs já coletados

## Uso

```bash
cd /srv/observabilidade-zabbix/mtr-hop-map
cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./scripts/run_poc.sh
./scripts/run_poc.sh --target observabilidade.escossio.dev.br
./scripts/run_poc.sh --target observabilidade.escossio.dev.br --target one.one.one.one
./scripts/run_poc.sh --targets-file data/replays/replay-suite-targets.txt --asn-lookup-mode offline
./scripts/run_poc.sh --dry-run --target observabilidade.escossio.dev.br
./scripts/run_poc.sh --dry-run --targets-file data/replays/replay-suite-targets.txt
./scripts/run_poc.sh --json --target observabilidade.escossio.dev.br
./scripts/run_poc.sh --json --dry-run --targets-file data/replays/replay-suite-targets.txt
./scripts/run_poc.sh --target observabilidade.escossio.dev.br-replay-validation --mtr-json data/replays/observabilidade-route-a.json
./scripts/run_poc.sh --target observabilidade.escossio.dev.br-fallback-validation --mtr-json data/replays/observabilidade-route-b.json --asn-lookup-mode offline
python3 -m aggregate.main
python3 -m aggregate.main --runs-root data/runs
python3 -m aggregate.main --output-dir aggregate/data/runs/demo
```

## Formato de entrada para lote

- `--target <destino>` pode ser repetido
- `--targets-file <arquivo>` aceita:
  - uma linha com `destino` para modo live
  - uma linha com `destino<TAB>/caminho/replay.json` para replay controlado
- `--replay` e `--mtr-json` valem para um único destino explícito
- `--dry-run` bloqueia toda escrita no Zabbix e grava `reconciliation_plan.json`
- `--json` imprime no stdout um JSON canônico com resumo agregado, resultados por destino e caminhos dos artifacts

## Convenção final do mapa

- nome canônico: `MTR ASN - <destino>`
- mapa específico por destino
- hosts globais por IP reaproveitados entre mapas
- metadata operacional por destino:
  - `source=mtr-hop-map`
  - `target=<destino>`
  - `target_slug=<slug>`
  - `mode=live|replay`
  - `last_trace=<run_id>`
- política de template por classe:
  - `local_recurring_backbone` e `destination`: template ICMP nativo
  - `pivot_or_exit_point`, `transit_external`, `service_family_facebook_meta` e `unknown`: sem herdar template ICMP padrão

## O que a execução salva

Cada rodada cria uma pasta em `data/runs/<run_id>/` com:

- `batch_execution.json`
- `batch_summary.json`
- `report.md`
- uma subpasta por destino em `targets/`
- dentro de cada destino:
  - `mtr_raw.json`
  - `mtr_parsed.json`
  - `mtr_normalized.json`
  - `reconcile_phase1.json`
  - `reconcile_phase2.json`
  - `execution.json`
  - `asn_summary.json`
  - `map_metadata.json`
  - `reconciliation_plan.json` quando `--dry-run` estiver ativo
  - `report.md`

## Agregação de traces

A camada de agregação em `aggregate/` lê os runs já produzidos pela CLI para montar:

- inventário de hops por IP
- recorrência de caminhos
- candidatos a borda Brisanet
- candidatos a IX/PTT
- candidatos a CDN
- leitura dedicada para `177.37.220.17` e `177.37.220.18`

## Validado nesta rodada

- idempotência com rota estável
- reconciliação com rota alterada por replay controlado
- fallback ASN em modo `offline`
- reuso global por IP entre mapas diferentes
- execução live com múltiplos destinos e falha parcial sem derrubar o lote
- replay em lote com três destinos
- dry-run com destino único, replay e lote com falha parcial
- stdout JSON canônico com single, replay, dry-run e lote com falha parcial

## Limites atuais

- hosts antigos não são apagados automaticamente quando saem de uma rota
- o replay usa snapshots locais, não agenda contínua
- `sysmap` não oferece tags nativas; a correlação operacional do mapa fica nos artefatos do run
- a classificação da camada agregada é heurística e traz confiança explícita
- o corpus atual não mostra os IPs `177.37.220.17` e `177.37.220.18`; eles ficam como watchlist ausente até aparecerem em novas coletas
- `IX/PTT` e `CDN` ficam como candidatos, não como verdade final
