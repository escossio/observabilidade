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
- metadata de mapa: `source`, `target`, `target_slug`, `mode`, `last_trace`
- limitação do Zabbix: `sysmap` não tem tags nativas; a metadata fica em `map_metadata.json` e no relatório agregado

## Estrutura

- `src/`: runner, parser, política, cliente Zabbix e reconciliador
- `scripts/`: invocação prática do POC
- `data/replays/`: snapshots controlados para replay de rota
- `data/runs/`: evidências de cada execução
- `docs/`: contrato e handoff da frente
- `data/runs/<run_id>/targets/<ordem>-<target_slug>/`: artefatos por destino dentro do lote

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
./scripts/run_poc.sh --target observabilidade.escossio.dev.br-replay-validation --mtr-json data/replays/observabilidade-route-a.json
./scripts/run_poc.sh --target observabilidade.escossio.dev.br-fallback-validation --mtr-json data/replays/observabilidade-route-b.json --asn-lookup-mode offline
```

## Formato de entrada para lote

- `--target <destino>` pode ser repetido
- `--targets-file <arquivo>` aceita:
  - uma linha com `destino` para modo live
  - uma linha com `destino<TAB>/caminho/replay.json` para replay controlado
- `--replay` e `--mtr-json` valem para um único destino explícito

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
  - `report.md`

## Validado nesta rodada

- idempotência com rota estável
- reconciliação com rota alterada por replay controlado
- fallback ASN em modo `offline`
- reuso global por IP entre mapas diferentes
- execução live com múltiplos destinos e falha parcial sem derrubar o lote
- replay em lote com três destinos

## Limites atuais

- hosts antigos não são apagados automaticamente quando saem de uma rota
- o replay usa snapshots locais, não agenda contínua
- `sysmap` não oferece tags nativas; a correlação operacional do mapa fica nos artefatos do run
