# Correlation Layer

## Objetivo

Esta camada traduz sinais reais do Zabbix em leitura operacional causal mínima, usando os bindings já fechados no `dependency-graph`.

Ela não substitui o binding. Ela lê por cima dele.

## Princípio central

- evento Zabbix é gatilho observacional, não verdade completa
- binding localiza o nó do grafo
- o nó carrega a semântica de falha
- a semântica define escopo, blast radius e leitura esperada
- a árvore de transporte separa falha local, serviço, borda, WAN, overlay e upstream
- a saída é uma hipótese operacional legível, não prova absoluta

## Saída canônica

- `evento_observado`
- `nó_correlacionado`
- `tipo_do_nó`
- `semântica`
- `escopo_probável`
- `blast_radius_probável`
- `cadeia_causal_principal`
- `hipótese_alternativa`
- `próximos_testes`

## O que esta camada consegue dizer

- o que falhou
- em que camada falhou
- qual semântica de falha representa
- qual é o escopo provável
- qual é o blast radius provável
- qual cadeia causal é mais plausível
- o que não deve ser inferido automaticamente

## O que esta camada não faz

- não faz RCA completo
- não cruza múltiplos eventos simultâneos de forma avançada
- não usa histórico temporal profundo
- não automatiza resposta
- não cria sinais novos
- não transforma hipótese em certeza

## Regra de leitura por camada

### Falha local de host

Quando o nó é `host` e a semântica é `host_failure`:

- o host base falhou ou degradou
- os serviços abaixo podem ser efeito secundário
- a borda não deve ser culpada por padrão

### Falha de serviço

Quando o nó é `service` e a semântica é `service_failure`:

- o serviço específico falhou
- a função local associada pode ficar indisponível
- o restante do host não está automaticamente comprometido

### Falha de acesso público

Quando a semântica é `public_access_failure`:

- a borda pública ou o frontend exposto falhou
- o serviço interno pode continuar saudável
- a indisponibilidade externa não prova falha do host nem da WAN inteira

### Falha de borda local

Quando a semântica é `local_edge_failure`:

- o domínio local de saída foi perdido ou degradado
- o host atrás da borda pode continuar vivo
- a falha está no salto local de acesso, não no serviço final

### Falha de uplink WAN

Quando a semântica é `wan_uplink_failure`:

- o enlace físico ou o caminho de uplink degradou
- a WAN principal pode ser afetada antes da sessão PPPoE cair
- isso ainda não prova falha do host consumidor

### Falha de WAN principal

Quando a semântica é `wan_primary_failure`:

- a sessão principal de internet caiu
- a conectividade externa principal está comprometida
- o host local e o equipamento de borda podem continuar vivos

### Falha de overlay

Quando a semântica é `overlay_failure`:

- o túnel sobreposto caiu
- a cadeia principal não deve ser marcada como caída por isso sozinho
- o impacto é restrito aos dependentes do overlay

### Falha de upstream

Quando a semântica é `external_edge_failure` ou `upstream_provider_failure`:

- o problema está acima da borda local
- a saída externa ou o provedor estão afetados
- o host local não deve ser reclassificado como morto sem outro sinal

## Regra de prudência

- se a semântica é local, não culpar borda ou WAN
- se a semântica é de borda, não culpar automaticamente o host
- se a semântica é de overlay, não promover à cadeia principal
- se o evento é de frontend público, não concluir falha total do backend sem evidência adicional

## Status da camada

Esta camada é mínima, determinística e legível. Ela serve como base para correlação posterior, não como motor definitivo de RCA.
