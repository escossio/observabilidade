# Handoff - MTR Hop Map POC

## O que foi construído

Frente nova para transformar MTR com ASN em hosts e mapa Zabbix persistentes.

## O que esta POC entrega

- execução de `mtr --aslookup`
- parser normalizado de hops
- lookup ASN/empresa
- criação/reuso de grupo, template, hosts e mapa
- mapa linear por destino
- relatório local por execução
- validação de idempotência

## Decisões fechadas na prática

- hostname dos hops: `hop-{destino_slug}-{ordem:02d}-{ip_normalizado}`
- grupo Zabbix: `Transit / Hop`
- template ICMP: `ICMP Ping`
- nó sem IP real: não vira host
- ASN ausente: `AS private` / `Private / local network`
- layout: horizontal linear, com um nó por hop real
- rótulo de nó: somente IP, ASN e empresa

## Evidência real

- destino validado: `observabilidade.escossio.dev.br`
- mapa canônico: `MTR ASN - observabilidade.escossio.dev.br`
- sysmap final: `5`
- estado final validado: `13` selements e `12` links
- idempotência confirmada:
  - `data/runs/20260406-235600/`
  - `data/runs/20260406-235616/`
  - `data/runs/20260406-235641/`

## Próximo passo

Generalizar a frente para múltiplos destinos depois de fechar a POC de um único alvo.
