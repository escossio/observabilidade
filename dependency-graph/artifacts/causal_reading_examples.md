# Causal Reading Examples

## Objetivo

Exemplos concretos de como ler sinais reais do Zabbix usando o binding já fechado e a camada mínima de correlação causal.

## Exemplo 1: Apache2 parado

- evento observado: `Apache2 parado`
- nó correlacionado: `svc-apache2`
- tipo do nó: `service`
- semântica: `service_failure`
- blast radius provável: `service-local`
- hipótese principal: o serviço `apache2` falhou no host `agt01`
- hipótese alternativa: a publicação local está degradada por dependência direta do host, mas o serviço ainda pode subir depois
- o que verificar em seguida: processo `apache2`, porta local, log do serviço e dependências imediatas
- o que não implica automaticamente: falha da MikroTik, falha da WAN ou falha geral do AGT

## Exemplo 2: Web 127.0.0.1 indisponível

- evento observado: `Web 127.0.0.1 indisponivel`
- nó correlacionado: `svc-apache2`
- tipo do nó: `service`
- semântica: `service_failure`
- blast radius provável: `service-local`
- hipótese principal: a camada HTTP local deixou de responder no próprio host
- hipótese alternativa: o processo existe, mas a rota local, o socket ou a resposta do web check falhou
- o que verificar em seguida: `apache2`, `127.0.0.1:80`, configuração do site e resposta local
- o que não implica automaticamente: borda externa caída ou problema de WAN

## Exemplo 3: unbound parado

- evento observado: `unbound parado`
- nó correlacionado: `svc-unbound`
- tipo do nó: `service`
- semântica: `service_failure`
- blast radius provável: `service-local`
- hipótese principal: o resolvedor local parou ou deixou de responder
- hipótese alternativa: o serviço está vivo, mas a checagem de processo não conseguiu refletir a saúde funcional
- o que verificar em seguida: processo `unbound`, porta local, resolução DNS e dependências de rede local
- o que não implica automaticamente: falha da RB3011 ou perda da WAN principal

## Exemplo 4: PPPoE tunnel status down

- evento observado: `PPPoE tunnel status down`
- nó correlacionado: `edge-mikrotik-pppoe-out1`
- tipo do nó: `ppp_session`
- semântica: `wan_primary_failure`
- blast radius provável: `wan-primary`
- hipótese principal: a sessão WAN principal caiu
- hipótese alternativa: o enlace físico ainda existe, mas a sessão autenticada caiu antes do IP público se manter estável
- o que verificar em seguida: sessão PPPoE, autenticação, rota default, IP público e operadora
- o que não implica automaticamente: falha do host `agt01`

## Exemplo 5: wg0 down

- evento observado: `wg0 down`
- nó correlacionado: `edge-mikrotik-wg0`
- tipo do nó: `access_device`
- semântica: `overlay_failure`
- blast radius provável: `overlay-only`
- hipótese principal: o overlay WireGuard foi perdido
- hipótese alternativa: o túnel caiu, mas a WAN principal e a cadeia funcional seguem estáveis
- o que verificar em seguida: handshake, peers, política de roteamento e dependentes do overlay
- o que não implica automaticamente: perda da internet principal

## Exemplo 6: Bridge down

- evento observado: `bridge down`
- nó correlacionado: `access-mikrotik-bridge`
- tipo do nó: `access_device`
- semântica: `local_edge_failure`
- blast radius provável: `intercluster-edge`
- hipótese principal: o domínio L2 local de saída foi perdido
- hipótese alternativa: a RB3011 está viva, mas a borda local não sustenta mais o tráfego do AGT
- o que verificar em seguida: bridge, portas membros, estado de enlace local e next-hop
- o que não implica automaticamente: queda total do host `agt01`

## Exemplo 7: Livecopilot Frontend Público indisponível

- evento observado: `Livecopilot Frontend Público indisponível`
- nó correlacionado: `svc-livecopilot-apache-edge`
- tipo do nó: `functional_node`
- semântica: `public_access_failure`
- blast radius provável: `publication-surface`
- hipótese principal: o túnel dedicado `cloudflared-livecopilot.service` ou a borda pública deixou de publicar o site
- hipótese alternativa: o backend pode seguir saudável enquanto a publicação pública cai
- o que verificar em seguida: túnel dedicado, edge HTTP, frontend público, health público e publicação externa
- o que não implica automaticamente: falha do backend, falha da RB3011 ou falha total do host

## Leitura comparativa

- falha local: restringe-se ao serviço ou host observado
- falha de borda: afeta a saída local e pode derrubar a percepção externa sem matar o host
- falha de WAN: compromete a conectividade principal externa e pode existir mesmo com host e borda vivos
- falha de overlay: afeta apenas o túnel sobreposto e não deve ser promovida à cadeia principal
