# MTR Hop Map POC

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

## Estrutura

- `src/`: runner, parser, política, cliente Zabbix e reconciliador
- `scripts/`: invocação prática do POC
- `data/replays/`: snapshots controlados para replay de rota
- `data/runs/`: evidências de cada execução
- `docs/`: contrato e handoff da frente

## Uso

```bash
cd /srv/observabilidade-zabbix/mtr-hop-map
cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./scripts/run_poc.sh
./scripts/run_poc.sh --target observabilidade.escossio.dev.br
./scripts/run_poc.sh --target observabilidade.escossio.dev.br-replay-validation --mtr-json data/replays/observabilidade-route-a.json
./scripts/run_poc.sh --target observabilidade.escossio.dev.br-fallback-validation --mtr-json data/replays/observabilidade-route-b.json --asn-lookup-mode offline
```

## O que a execução salva

Cada rodada cria uma pasta em `data/runs/<timestamp>/` com:

- saída bruta do `mtr`
- hops normalizados
- plano de reconciliação
- resultado da API do Zabbix
- sumário do enrichment ASN/cache
- relatório Markdown

## Validado nesta rodada

- idempotência com rota estável
- reconciliação com rota alterada por replay controlado
- fallback ASN em modo `offline`
- reuso global por IP entre mapas diferentes

## Limites atuais

- hosts antigos não são apagados automaticamente quando saem de uma rota
- o replay usa snapshots locais, não agenda contínua
- a generalização para múltiplos destinos vem depois, sobre esta base
