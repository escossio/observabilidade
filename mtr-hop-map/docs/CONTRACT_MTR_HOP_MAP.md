# Contract - MTR Hop Map POC

## Objetivo

Transformar uma rota observada com `mtr --aslookup` em uma topologia persistente no Zabbix:

- um mapa canônico por destino
- um host global por IP real
- um template ICMP padrão para os hops
- um mapa linear com ícone de nuvem em cada hop
- rótulos mínimos: IP, ASN e empresa

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

## Política de nome

- host: `hop-ip-{ip_normalizado}`
- mapa: `MTR ASN - <destino>`
- grupo: `Transit / Hop`
- template: `ICMP Ping`

## Persistência

- a evidência local de cada rodada fica em `data/runs/<timestamp>/`
- o repositório versiona código, contrato, handoff e evidência textual
- segredos ficam fora do git e são lidos do ambiente provisionado
