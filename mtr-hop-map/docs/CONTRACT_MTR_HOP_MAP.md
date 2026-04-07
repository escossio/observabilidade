# Contract - MTR Hop Map

## Objetivo

Transformar uma rota observada com `mtr --aslookup` em uma topologia persistente no Zabbix:

- um mapa canônico por destino
- um host global por IP real
- um template ICMP padrão para os hops
- um mapa linear com ícone de nuvem em cada hop
- rótulos mínimos: IP, ASN e empresa
- execução única ou em lote sem duplicar lógica

## Regras

1. Hops com IP real viram host monitorável ou são reutilizados.
2. Hops sem IP real não viram host.
3. A identidade do host é global por IP; destino e ordem pertencem ao mapa e à execução.
4. O mapa é persistente e nomeado por destino.
5. Reexecução não deve gerar duplicação indevida.
6. O destino final aparece como o último nó da cadeia.
7. ASN ausente vira `AS private` e `Private / local network`.
8. Falha no `whois` não derruba a execução; o fallback usa cache local e depois o hint ASN do MTR.
9. O layout é linear horizontal.
10. Falha em um destino não pode derrubar a execução dos demais destinos do lote.
11. O `sysmap` do Zabbix 7.4 não tem tags nativas; a metadata operacional do mapa fica registrada pela automação.
12. `--dry-run` deve bloquear toda escrita no Zabbix e produzir o plano completo de reconciliação.
13. `--json` deve emitir um JSON canônico estável no stdout para automação.

## Política de nome

- host: `hop-ip-{ip_normalizado}`
- mapa: `MTR ASN - <destino>`
- grupo: `Transit / Hop`
- template: `ICMP Ping`

## Metadata operacional do mapa

- `source=mtr-hop-map`
- `target=<destino>`
- `target_slug=<slug>`
- `mode=live|replay`
- `last_trace=<run_id>`
- `dry_run=true|false`

Esses campos ficam em `map_metadata.json` e no relatório agregado do run.

## Dry-run

- lê o estado atual do Zabbix
- calcula host, selement, link e metadata que seriam alterados
- grava `reconciliation_plan.json`
- bloqueia qualquer método de escrita no cliente da API

## Saída JSON

- `--json` ativa a saída canônica em stdout
- o JSON de stdout é o resumo consolidado da execução
- o JSON salvo em `reconciliation_plan.json` continua sendo o plano técnico profundo por destino
- `report.md` continua sendo o resumo humano
- em lote, a saída JSON precisa explicitar sucesso, falha parcial e caminhos dos artifacts por destino
- contrato mínimo do stdout:
  - `run_id`, `mode`, `dry_run`, `started_at`, `finished_at`
  - `summary` agregado com contadores
  - `results[]` com `target`, `status`, `map`, `actions`, `counters`, `artifacts` e `error`

## Persistência

- a evidência local de cada rodada fica em `data/runs/<run_id>/`
- cada destino do lote ganha uma subpasta em `data/runs/<run_id>/targets/<ordem>-<target_slug>/`
- o repositório versiona código, contrato, handoff e evidência textual
- segredos ficam fora do git e são lidos do ambiente provisionado
