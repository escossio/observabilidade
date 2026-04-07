# MTR Hop Map POC

POC para transformar uma rota observada com `mtr --aslookup` em objetos persistentes no Zabbix:

- cada hop com IP vira host monitorável
- cada host usa um template ICMP próprio
- o mapa final é linear e canônico por destino
- o rótulo de cada hop mostra só IP, ASN e empresa

## Decisões fechadas

- destino canônico desta POC: `observabilidade.escossio.dev.br`
- padrão de hostname: `hop-{destino_slug}-{ordem:02d}-{ip_normalizado}`
- grupo de hosts: `Transit / Hop`
- template monitorável: `ICMP Ping`
- template group: `Templates/Network`
- tratamento de hops sem IP real: não criam host
- tratamento de ASN ausente: `AS private` / `Private / local network`
- layout do mapa: linear horizontal

## Estrutura

- `src/`: runner, parser, política, cliente Zabbix e reconciliador
- `scripts/`: invocação prática do POC
- `data/runs/`: evidências de cada execução
- `docs/`: contrato e handoff da frente

## Uso

```bash
cd /srv/observabilidade-zabbix/mtr-hop-map
cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./scripts/run_poc.sh --target observabilidade.escossio.dev.br
```

## O que a execução salva

Cada rodada cria uma pasta em `data/runs/<timestamp>/` com:

- saída bruta do `mtr`
- hops normalizados
- plano de reconciliação
- resultado da API do Zabbix
- relatório Markdown

## Limites da POC

- o template ICMP é próprio desta frente
- a rota é tratada como uma única linha canônica por destino
- a generalização para múltiplos destinos vem depois, sem apagar esta base
