# Contract - MTR Hop Map POC

## Objetivo

Transformar uma rota observada com `mtr --aslookup` em uma topologia persistente no Zabbix:

- um mapa canônico por destino
- um host por hop com IP real
- um template ICMP por host
- um mapa linear com ícone de nuvem em cada hop
- rótulos mínimos: IP, ASN e empresa

## Regras

1. Hops com IP real viram host monitorável ou são reutilizados.
2. Hops sem IP real não viram host.
3. O mapa é persistente e nomeado por destino.
4. Reexecução não deve gerar duplicação indevida.
5. O destino final aparece como o último nó da cadeia.
6. ASN ausente vira `AS private` e `Private / local network`.
7. O layout é linear horizontal.

## Política de nome

- host: `hop-{destino_slug}-{ordem:02d}-{ip_normalizado}`
- mapa: `MTR ASN - <destino>`
- grupo: `Transit / Hop`
- template: `ICMP Ping`

## Persistência

- a evidência local de cada rodada fica em `data/runs/<timestamp>/`
- o repositório versiona código, contrato, handoff e evidência textual
- segredos ficam fora do git e são lidos do ambiente provisionado

