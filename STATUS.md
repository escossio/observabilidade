# Status

## 2026-04-07 - mapa unificado expandido com 4 novos destinos

- fonte de verdade desta rodada:
  - `replay` controlado para os 4 alvos
  - os runs consolidados já estavam salvos em `mtr-hop-map/data/runs/20260407-030220-957449/`
- a camada `mtr-hop-map/aggregate` incorporou os destinos `8.8.8.8`, `9.9.9.9`, `dell.com` e `wiki.mikrotik.com`
- o mapa canônico único continua sendo:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- o mapa final publicado no Zabbix está com:
  - `39` nós
  - `38` links
- o tronco comum permaneceu intacto e os novos ramos foram anexados ao mesmo grafo:
  - Google para `8.8.8.8`
  - Quad9 para `9.9.9.9`
  - Dell para `dell.com`
  - Mikrotik para `wiki.mikrotik.com`
- a borda candidata `187.19.161.199` permaneceu no mesmo mapa como candidato forte, sem promoção indevida
- os mapas por destino continuam intactos
- os IPs `177.37.220.17` e `177.37.220.18` continuam sem evidência observada no corpus atual


## 2026-04-07 - mapa agregado unificado do MTR publicado

- a camada `mtr-hop-map/aggregate` consolidou a topologia observada em um único mapa canônico no Zabbix:
  - `MTR Unified - Brisanet Observed`
  - `sysmapid 10`
- o mapa unificado mantém no mesmo grafo:
  - tronco comum recorrente
  - borda Brisanet candidata
  - saídas externas/CDN
  - watchlist DNS
- artefatos da rodada:
  - `unified_nodes.json`
  - `unified_edges.json`
  - `unified_map_plan.json`
  - `report.md`
  - `zabbix_map_snapshot.json`
- validação real:
  - `15` nós e `13` links no mapa final
  - `187.19.161.199` segue como candidato fortíssimo de borda Brisanet
  - `177.37.220.17` e `177.37.220.18` não foram promovidos por ausência de evidência no corpus

## 2026-04-07 - camada de agregacao de traces adicionada

- foi criada a frente `mtr-hop-map/aggregate` para correlacionar varios runs já coletados
- o inventário agregado já distingue:
  - hops recorrentes
  - candidatos a borda Brisanet
  - candidatos a CDN
  - candidatos a IX/PTT
  - watchlist explícita para `177.37.220.17` e `177.37.220.18`
- saídas geradas na rodada:
  - `aggregate_summary.json`
  - `classification_summary.json`
  - `hops_inventory.csv`
  - `edge_candidates.csv`
  - `report.md`
- validação real:
- corpus lido com `19` runs e `22` targets
  - `15` hops únicos
  - `3` paths únicos
  - borda Brisanet mais forte: `187.19.161.199`
  - não houve candidato forte de IX/PTT no corpus atual
  - os IPs `177.37.220.17` e `177.37.220.18` não apareceram nos traces e ficaram como watchlist ausente

## 2026-04-07 - JSON stdout canônico da frente MTR hop map

- `--json` passou a emitir um contrato estável de stdout para automação.
- O JSON de stdout foi separado do `reconciliation_plan.json` e do `report.md`.
- A validação cobriu destino único, dry-run, lote com falha parcial e replay.
- O dry-run continuou sem escrita no Zabbix durante a validação desta rodada.

## 2026-04-07 - dry-run da frente MTR hop map implementado

- `--dry-run` agora planeja a reconciliação completa sem escrever no Zabbix
- o bloqueio de escrita ficou centralizado no cliente da API e vale para `create` e `update`
- o plano é gravado em `reconciliation_plan.json`
- a validação cobriu:
  - destino único
  - lote com falha parcial
  - replay
- o estado do Zabbix permaneceu inalterado nos dry-runs

## 2026-04-07 - frente MTR hop map generalizada para multiplos destinos

- generalizacao implementada:
  - a CLI agora aceita `--target` repetido para lote simples
  - a CLI agora aceita `--targets-file` com um destino por linha ou `destino<TAB>replay.json`
  - a frente agora processa multiplos destinos dentro do mesmo `run_id`
  - cada destino grava artefatos em `mtr-hop-map/data/runs/<run_id>/targets/<ordem>-<target_slug>/`
- convencao de mapa consolidada:
  - nome canonico continua `MTR ASN - <destino>`
  - metadata operacional do mapa foi padronizada em `source`, `target`, `target_slug`, `mode` e `last_trace`
  - o `sysmap` do Zabbix 7.4 nao expõe tags nativas de mapa; essa metadata ficou formalizada em `map_metadata.json` e no relatorio agregado
- validacao real desta rodada:
  - lote live executado com `observabilidade.escossio.dev.br`, `one.one.one.one` e `invalid.invalid`
  - `observabilidade.escossio.dev.br` reutilizou o mapa canonico `sysmapid 5`
  - `one.one.one.one` criou/atualizou o mapa `sysmapid 8`
  - `invalid.invalid` falhou sem interromper os demais destinos e sem criar mapa
  - reuso global por IP entre mapas foi confirmado com intersecao real dos hostids `10780..10791`
- cobertura de replay ampliada:
  - fixture nova: `mtr-hop-map/data/replays/one-one-one-one-route-a.json`
  - suite nova: `mtr-hop-map/data/replays/replay-suite-targets.txt`
  - replay em lote validado no run `mtr-hop-map/data/runs/20260407-003511/`
  - mapa de replay novo: `MTR ASN - one.one.one.one-replay-validation` / `sysmapid 9`

## 2026-04-07 - endurecimento da frente MTR hop map

- decisao de arquitetura fechada:
  - host de hop agora e `global por IP`
  - mapas continuam especificos por destino
- endurecimento implementado:
  - reuso de host por IP no grupo `Transit / Hop`
  - replay controlado de MTR por `--mtr-json`
  - cache persistente de ASN em `mtr-hop-map/data/cache/`
  - modo `offline` para fallback de enrichment
- validacao real:
  - mapa canonico `sysmapid 5` preservado com `13` selements e `12` links
  - mapa de replay `sysmapid 6` confirmou troca de rota sem apagar host antigo
  - mapa de fallback `sysmapid 7` confirmou execucao sem `whois`
- template ICMP:
  - a frente passou a reutilizar o template oficial `ICMP Ping` (`templateid 10564`) quando ele existe no ambiente

## 2026-04-06 - frente MTR hop map estabilizada no Zabbix

- POC executada contra `observabilidade.escossio.dev.br`
- mapa canônico criado:
  - `MTR ASN - observabilidade.escossio.dev.br`
  - `sysmapid 5`
- estado final validado:
  - `13` nós com IP real
  - `12` links em cadeia
  - labels com `IP / ASN / empresa`
- política aplicada:
  - hostname `hop-{destino_slug}-{ordem:02d}-{ip_normalizado}`
  - grupo `Transit / Hop`
  - template `ICMP Ping`
  - ícone `Cloud_(96)`
- idempotência provada:
  - primeira execução criou o mapa
  - segunda e terceira execuções reaproveitaram o mesmo mapa sem crescer a cardinalidade
- artefatos da frente:
  - `mtr-hop-map/data/runs/20260406-235600/`
  - `mtr-hop-map/data/runs/20260406-235616/`
  - `mtr-hop-map/data/runs/20260406-235641/`

## 2026-04-06 - nova captura Netflix com tcpdump e DevTools na VM

- Sessão gráfica validada:
  - o Firefox da VM já estava autenticado no Netflix
  - o browse abriu sem pedir credencial novamente
- Captura desta rodada:
  - diretório: `internet-observation/captures/20260406-230119-netflix-session/`
  - pcap: `netflix-session.pcap`
  - evidência visual do DevTools: `devtools-network-home.png` e `devtools-network-watch.png`
- Leituras confirmadas na página:
  - `web.prod.cloud.netflix.com`
  - `web.ws.prod.cloud.netflix.com`
  - `logs.netflix.com`
  - `assets.nflxext.com`
  - `help.nflxext.com`
  - `occ-0-1119-3851.1.nflxso.net`
  - `ae.nflximg.net`
  - `push.prod.netflix.com`
  - `ichnaea-web.netflix.com`
- Classificação operacional:
  - `occ-0-1119-3851.1.nflxso.net` continua sendo o melhor candidato de entrega/edge na sessão repetida
  - `assets.nflxext.com` entrou como CDN de assets da Netflix
  - `logs.netflix.com`, `push.prod.netflix.com` e `ichnaea-web.netflix.com` ficaram na camada auxiliar/telemetria
- ASN associado quando aplicável:
  - `AS28126` para `177.37.221.41` ligado ao `occ-0-1119-3851.1.nflxso.net`
  - `AS40027` para `45.57.90.1` ligado a `assets.nflxext.com`
- Limitação:
  - o plugin Widevine do Firefox crashou durante a navegação, então a reprodução não chegou a um stream de vídeo estável nesta rodada
  - a classificação foi fechada com tcpdump + DevTools + repetição da família de hosts de entrega
- Artefato novo:
  - `internet-observation/artifacts/netflix_session_ip_classification.md`

## 2026-04-06 - notebook note-leo ligado ao RB3011 no mapa visual do Zabbix

- Mapa alterado:
  - `sysmapid`: `2`
  - nome: `AGT - Visão Visual`
- Novo elemento no mapa:
  - host Zabbix: `note-leo`
  - `hostid`: `10779`
  - visible name: `note-leo / 10.45.0.10`
  - ícone: `Notebook_(96)`
  - `imageid`: `70`
  - `selementid`: `6`
  - posição visual: `x=100`, `y=20`, com porte `170x170`
- Novo link:
  - `linkid`: `4`
  - direção visual: `note-leo / 10.45.0.10` -> `MikroTik RB3011`
  - linha: `DRAWTYPE_BOLD_LINE` (`drawtype=2`)
  - cor OK: `00AA00`
  - label final:
    - `Down {?last(/note-leo/net.if.in["wlp42s0"])}`
    - `Up {?last(/note-leo/net.if.out["wlp42s0"])}`
  - label multilinha: funcionou
  - `show_label`: `always`
- Gatilhos associados ao novo link:
  - `32621` - `Linux: Interface wlp42s0: Link down`
  - `32566` - `RB3011 bridge down`
  - `32567` - `RB3011 ether1 down`
  - `32568` - `RB3011 pppoe-out1 down`
- Itens usados para tráfego:
  - download: `69831` - `Interface wlp42s0: Bits received` (`net.if.in["wlp42s0"]`)
  - upload: `69846` - `Interface wlp42s0: Bits sent` (`net.if.out["wlp42s0"]`)
- Validação:
  - `map.update` respondeu com sucesso para o novo elemento
  - `map.update` respondeu com sucesso para o novo link
  - `map.get` confirmou o `selementid 6` do notebook e o `linkid 4`
  - o frontend autenticado do Zabbix, carregado em Chromium com sessão real, exibiu o mapa com `note-leo / 10.45.0.10`, `MikroTik RB3011` e `AGT / 10.45.0.3`
  - o padrão visual do link anterior foi replicado para o notebook
  - o AGT e o RB3011 permaneceram intactos
  - não houve alteração no Grafana
- Limitação:
  - o notebook ainda não tem triggers próprios de discovery de interface materializados além do `wlp42s0 Link down`, então o link reutiliza os gatilhos reais disponíveis no host e na borda
- Artefato atualizado:
  - `artifacts/zabbix_agt_visual_map.md`

## 2026-04-06 - notebook note-leo onboardado no Zabbix

- Identidade real validada no notebook:
  - hostname: `note-leo`
  - FQDN: `note-leo.escossio.dev.br`
  - sistema: `Linux note-leo 6.12.74+deb12-amd64`
- Acesso e agent:
  - acesso SSH como `root` funcionou com a senha informada
  - `zabbix-agent2` estava `active` e `enabled`
  - a porta `10050/tcp` estava bloqueada pelo `firewalld` e foi liberada apenas para `10.45.0.3`
- Validação do agent:
  - `agent.ping` retornou `1`
  - `system.hostname` retornou `note-leo`
  - `system.uname` retornou a string do Debian 12 / kernel 6.12
- Cadastro no Zabbix:
  - host: `note-leo`
  - visible name: `note-leo / 10.45.0.10`
  - `hostid`: `10779`
  - grupo: `Linux servers` (`groupid 2`)
  - template vinculado: `Linux by Zabbix agent` (`templateid 10001`)
  - interface agent: `10.45.0.10:10050`
- Estado da coleta:
  - o host já aparece como `available=1` na interface agent
  - métricas base do template já começaram a preencher `latest data`
  - a regra `net.if.discovery` existe no template e está em `1h`
  - os prototypes de tráfego `net.if.in["{#IFNAME}"]` e `net.if.out["{#IFNAME}"]` estão presentes
  - no agent, `net.if.discovery` retornou `wlp42s0` entre as interfaces
  - no agent, `net.if.in["wlp42s0"]` e `net.if.out["wlp42s0"]` retornaram valores reais
  - a materialização dos itens de rede no Zabbix depende do próximo ciclo de discovery
- Limitação registrada:
  - a coleta de rede ficou habilitada e validada no agent, mas ainda depende da janela de descoberta de `1h` do template para aparecer como itens derivados no Zabbix
- Artefato criado:
  - `artifacts/notebook_10.45.0.10_zabbix_onboarding.md`

## 2026-04-06 - RB3011 reduzida um pouco no mapa AGT do Zabbix

- Ajuste aplicado:
  - o ícone da `MikroTik RB3011` foi reduzido de `200x200` para `170x170`
  - o `imageid` continua `189`
- Efeito visual:
  - a RB3011 ficou um pouco menor sem perder a foto oficial
  - o link e o AGT permaneceram intactos
  - a leitura do mapa ficou mais equilibrada
- Estado validado no runtime:
  - `sysmapid`: `2`
  - AGT: `selementid` `5`
  - RB3011: `selementid` `3`
  - link: `linkid` `3`
- Validação:
  - `map.update` respondeu com sucesso
  - `map.get` confirmou o novo tamanho do elemento
  - o frontend autenticado exibiu a RB3011 menor e legível
  - não houve alteração no Grafana
- Artefatos tocados:
  - `artifacts/zabbix_agt_visual_map.md`
  - `artifacts/rb3011_icon_research.md`

## 2026-04-06 - ícone da RB3011 ajustado no mapa AGT do Zabbix

- Alteração aplicada:
  - o elemento `MikroTik RB3011` passou a usar o novo ícone `RB3011 official mapfit`
  - `imageid`: `189`
- Motivo técnico:
  - a versão quadrada grande gerava renderização fora de escala no frontend
  - a versão `mapfit` preserva a foto oficial, mas entra no mapa com tamanho legível
- Estado validado no runtime:
  - `sysmapid`: `2`
  - AGT atual: `selementid` `5`
  - RB3011 atual: `selementid` `3`
  - link atual: `linkid` `3`
  - os dois elementos continuaram ligados
  - o link manteve triggers e label de tráfego
- Validação visual:
  - o frontend autenticado exibiu o RB3011 com o novo ícone pequeno e legível
  - o AGT permaneceu intacto
  - não houve alteração no Grafana
- Artefatos tocados:
  - `artifacts/zabbix_agt_visual_map.md`
  - `artifacts/rb3011_icon_research.md`

## 2026-04-06 - pesquisa e shortlist de ícones para RB3011 no mapa do Zabbix

- Objetivo desta rodada:
  - pesquisar e preparar ativos visuais próximos da MikroTik RB3011 para uso interno no mapa `AGT - Visão Visual`
  - não aplicar nada no mapa ainda
- Resultado da pesquisa:
  - 5 opções relevantes foram consolidadas
  - melhor opção principal: `01b_official_rb3011_photo_iconfit.png`
  - reserva prática: `03_mikrotik_logo.svg`
  - fallback genérico: `04_generic_router_flat_label_colour.svg`
- Candidatos salvos em:
  - `artifacts/rb3011_icon_candidates/`
- Artefato novo:
  - `artifacts/rb3011_icon_research.md`
- Observação:
  - a imagem oficial do RB3011 segue como a opção mais fiel ao equipamento
  - a versão `iconfit` é a mais equilibrada para uso em mapa pequeno no Zabbix
  - não houve alteração no Grafana nem no mapa nesta rodada

## 2026-04-06 - acabamento visual do link AGT -> RB3011 no mapa visual do Zabbix

- Mapa alterado:
  - `sysmapid`: `2`
  - nome: `AGT - Visão Visual`
- Elementos usados:
  - AGT: `selementid` `2`
  - MikroTik RB3011: `selementid` `3`
- Link criado:
  - `linkid`: `1`
  - direção visual: `AGT / 10.45.0.3` -> `MikroTik RB3011`
  - tipo: `trigger`
  - cor OK: `00AA00`
  - label final:
    - `Down {?last(/agt01/net.if.in["br0"])}`
    - `Up {?last(/agt01/net.if.out["br0"])}`
  - label multilinha: funcionou
  - `show_label`: `always`
  - `drawtype`: `2` (`DRAWTYPE_BOLD_LINE`)
- Gatilhos associados ao link:
  - `32532` - `Linux: Interface br0: Link down`
  - `32566` - `RB3011 bridge down`
  - `32567` - `RB3011 ether1 down`
  - `32568` - `RB3011 pppoe-out1 down`
- Itens usados para download/upload:
  - download: `69515` - `Interface br0: Bits received` (`net.if.in["br0"]`)
  - upload: `69527` - `Interface br0: Bits sent` (`net.if.out["br0"]`)
  - unidade dos itens: `bps`
- Validação:
  - `map.update` respondeu com sucesso
  - `map.get` confirmou o link entre os dois elementos
  - `trigger.get` confirmou os quatro gatilhos associados
  - o frontend autenticado em `zabbix.php?action=map.view&sysmapid=2` exibiu o link com o label resolvido em duas linhas
  - a linha apareceu mais grossa com `DRAWTYPE_BOLD_LINE`
  - o label ficou acima da linha de forma aproximada, que é o melhor equivalente nativo suportado nesta versão do Zabbix
  - os dois elementos anteriores permaneceram intactos
  - não houve alteração no Grafana
- Limitação documentada:
  - o Zabbix não expõe posicionamento nativo separado para o rótulo de link; a aproximação ficou por label multilinha + linha bold
  - esta combinação passa a ser o padrão visual para os próximos links do mapa
- Artefato atualizado:
  - `artifacts/zabbix_agt_visual_map.md`

## 2026-04-06 - RB3011 adicionada como segundo elemento solto no mapa AGT

- Mapa alterado:
  - `sysmapid`: `2`
  - nome: `AGT - Visão Visual`
- Novo elemento adicionado:
  - host Zabbix: `MikroTik RB3011`
  - `hostid`: `10778`
  - label: `MikroTik RB3011`
  - ícone: `Router_(96)` (`imageid` `126`)
  - posição: elemento solto, sem ligação com o AGT
  - o elemento ficou com porte visual equivalente ao do AGT pela mesma família/tamanho de ícone
- Navegação:
  - manteve-se o comportamento de host element com o mesmo destino operacional do mapa
  - o link do mapa continua apontando para `zabbix.php?action=host.dashboard.view&hostid={HOST.ID}`
- Validação:
  - `map.update` respondeu com sucesso
  - `map.get` confirmou os dois elementos no mapa
  - o elemento do AGT permaneceu intacto
  - não houve alteração no Grafana
- Artefatos:
  - `artifacts/zabbix_agt_visual_map.md`

## 2026-04-06 - mapa visual do host AGT criado no Zabbix

- Mapa criado no runtime do Zabbix:
  - `sysmapid`: `2`
  - nome: `AGT - Visão Visual`
  - dimensão: `860x420`
- Host ligado ao mapa:
  - host: `agt01`
  - `hostid`: `10776`
  - IP/interface observada: `10.45.0.3` / `127.0.0.1:10050`
  - grupo: `Linux servers`
  - template vinculado: `Linux by Zabbix agent`
- Elemento visual:
  - tipo: host element
  - label: `AGT / 10.45.0.3`
  - ícone: `Server_(96)` (`imageid` `151`)
  - o elemento ficou ligado ao host real do Zabbix
- Navegação escolhida:
  - URL do elemento: `zabbix.php?action=host.dashboard.view&hostid={HOST.ID}`
  - decisão: usar o dashboard nativo do host como entrada operacional mais útil
  - motivo: a consulta ao host mostrou dashboards disponíveis (`System performance`, `Network interfaces`, `Filesystems`)
- Validação:
  - `map.create` respondeu com sucesso
  - `map.get` confirmou o elemento do host e a URL associada
  - não houve alteração no Grafana
- Artefato novo:
  - `artifacts/zabbix_agt_visual_map_created.md`

## 2026-04-06 - árvore causal do Grafana saiu de SVG inline para embed estático

- Causa raiz confirmada:
  - o painel 26 guardava o XML/SVG inteiro em `options.content`
  - no acesso real/mobile o Grafana passou a expor esse XML cru como texto
  - o SVG em si estava válido; a falha era de entrega/renderização no `Text panel`
- Correção aplicada:
  - helper `dependency-graph/tools/render_grafana_causal_tree.py` passou a publicar a árvore em arquivo estático
  - caminho local publicado: `/usr/share/grafana/public/img/observabilidade-zabbix/causal-tree-state.svg`
  - URL estável usada pelo painel: `/public/img/observabilidade-zabbix/causal-tree-state.svg`
  - painel 26 trocado de SVG inline para wrapper HTML com `<img ...>`
- Dashboard alterado:
  - uid `observabilidade-grafana`
  - painel `26`
  - versão `28 -> 29`
- Validação:
  - `py_compile` do helper passou sem erro
  - `HEAD` autenticado do asset público respondeu `200` com `content-type: image/svg+xml`
  - `GET /api/dashboards/uid/observabilidade-grafana` confirmou o painel 26 com `<img src='/public/img/observabilidade-zabbix/causal-tree-state.svg?...'>`
  - sessão Chromium autenticada confirmou no DOM real:
    - `imageFound: true`
    - `rawSvgTextVisible: false`
  - `d-solo` mobile autenticado confirmou:
    - `imageFound: true`
    - `complete: true`
    - `rawSvgTextVisible: false`
  - screenshot mobile salvo em `/tmp/grafana-causal-tree-mobile-devtools.png`
- Artefatos novos:
  - `dependency-graph/artifacts/grafana_causal_tree_svg_embed_fix.md`
- Limitações:
  - o SVG publicado fica dentro do estático do Grafana e pode precisar ser regravado após upgrade de pacote
  - a imagem continua snapshot-driven
- Próximo passo natural:
  - se a operação quiser mais legibilidade no celular, aumentar a altura do painel 26 sem mexer no restante da grade

## 2026-04-06 - árvore causal do Grafana passou a refletir estado real por nó

- O dashboard principal `Observabilidade Zabbix - Grafana` manteve a árvore causal SVG no painel 26, mas saiu de uma V1 estrutural para uma V1 com estado real por cor.
- Dashboard alterado:
  - uid `observabilidade-grafana`
  - painel `26`
  - versão `27 -> 28`
- Estratégia adotada:
  - helper local `dependency-graph/tools/render_grafana_causal_tree.py`
  - leitura do runtime atual do Zabbix via API local
  - classificação local em `up`, `down`, `warn` e `unknown`
  - regravação do SVG já colorido no painel Grafana
  - sem plugin novo
  - sem serviço contínuo novo
  - sem mexer no restante do dashboard
- Convenção visual desta rodada:
  - verde = saudável
  - vermelho = falha
  - amarelo = atenção / parcial
  - cinza = sem leitura / sem binding
- Nós verdes no snapshot validado:
  - `apache2`
  - `cloudflared`
  - `unbound`
  - `grafana-server`
  - `zabbix-server`
  - `zabbix-agent2`
  - `postgresql`
  - `ssh`
  - `MikroTik RB3011`
  - `bridge`
  - `ether1`
  - `pppoe-out1`
  - `wg0`
  - `Frontend Público`
  - `Apache Edge`
  - `Backend FastAPI`
- Nós amarelos no snapshot validado:
  - `Livecopilot`
- Nós cinzas no snapshot validado:
  - `agt01`
  - `br0`
  - `cloudflared-livecopilot`
  - `206.42.12.37`
  - `AS28126 BRISANET`
- Nós vermelhos no snapshot validado:
  - nenhum nesta rodada
- Leitura operacional relevante:
  - `agt01` ficou cinza porque o binding atual do host aponta para `69621` e o item veio sem `lastclock` útil
  - `Livecopilot` ficou amarelo porque frontend, edge e backend estão verdes, mas o nó causal do túnel dedicado ainda não tem binding direto fechado
  - `wg0` continua separado como overlay, mas agora reflete o estado operacional real do item SNMP
- Artefatos novos:
  - `dependency-graph/tools/render_grafana_causal_tree.py`
  - `dependency-graph/artifacts/causal_tree_state_mapping.md`
  - `dependency-graph/artifacts/grafana_causal_tree_state_validation.md`
- Validação:
  - regravação do dashboard confirmada via API do Grafana
  - painel 26 confirmado com classes `state-up`, `state-down`, `state-warn` e `state-unknown`
  - screenshot headless confirmou a árvore colorida
  - validação no ambiente gráfico da VM confirmou o dashboard real aberto no Chromium em `DISPLAY=:20`
- Limitações:
  - a cor ainda é snapshot-driven
  - o helper precisa ser executado de novo para refletir nova rodada
  - nós sem binding direto continuam cinza por honestidade estrutural
- Próximo passo natural:
  - fechar binding direto do `cloudflared-livecopilot`
  - trocar o sinal de host de `agt01` por um binding mais confiável para saúde do host

## 2026-04-06 - árvore causal substituiu o bloco textual no Grafana

- O dashboard principal `Observabilidade Zabbix - Grafana` deixou de usar o bloco textual como peça principal da leitura causal/NOC.
- O painel 26 foi regravado como uma árvore causal visual em SVG embutido.
- Dashboard alterado:
  - uid `observabilidade-grafana`
  - versão `25 -> 27`
- Estratégia adotada:
  - painel nativo `text`
  - modo `html`
  - SVG embutido direto no conteúdo do painel
  - sem plugin novo
  - sem serviço contínuo novo
  - sem tocar nos painéis atuais de serviço/infra
- Clusters/árvores incluídos na V1:
  - `AGT`
  - `MikroTik RB3011`
  - `Livecopilot`
- A árvore mostra:
  - `agt01`
  - `br0`
  - `apache2`
  - `cloudflared`
  - `unbound`
  - `grafana-server`
  - `zabbix-server`
  - `zabbix-agent2`
  - `postgresql`
  - `ssh`
  - `bridge`
  - `ether1`
  - `pppoe-out1`
  - `wg0`
  - `206.42.12.37`
  - `AS28126 BRISANET`
  - `Livecopilot Frontend Público`
  - `cloudflared-livecopilot`
  - `Apache Edge`
  - `Backend FastAPI`
- Convenção visual usada:
  - verde = saudável
  - amarelo = atenção / degradação
  - cinza = estrutural ou snapshot
- O que ficou estrutural nesta V1:
  - a posição dos nós e as relações principais entre clusters
  - `wg0` como overlay separado da cadeia principal
- O que ficou refletindo estado real já validado:
  - os nós e bindings já conhecidos no `dependency-graph`
  - os serviços e saltos reais documentados para AGT, MikroTik e Livecopilot
- Artefatos novos:
  - `dependency-graph/artifacts/causal_tree_grafana_design.md`
  - `dependency-graph/artifacts/grafana_causal_tree_validation.md`
- Validação:
  - dashboard regravado com sucesso via API do Grafana
  - painel 26 confirmado como `text/html` com SVG embutido
  - dashboard antigo permaneceu íntegro
  - render local do SVG confirmou a árvore visual
  - validação reforçada no ambiente gráfico da VM:
    - sessão XFCE em `DISPLAY=:20`
    - janela Chromium aberta no dashboard principal
    - título da janela confirmando `Observabilidade Zabbix - Grafana`
    - painel `Árvore Causal / Dependência` presente no DOM da página renderizada
- Limitações:
  - a árvore V1 ainda é majoritariamente estrutural e não calcula estado em tempo real dentro do Grafana
  - a leitura fina de falha por nó ainda depende da camada causal já validada fora do painel
- Próximo passo natural:
  - evoluir a V1 para um mapa dinâmico por estado dos nós, se a operação quiser calcular cores e destaques a partir dos bindings em cada rodada

## 2026-04-06 - resumo operacional de turno/NOC adicionado

- Foi criada a CLI `dependency-graph/tools/noc_shift_summary.py`.
- Artefatos novos:
  - `dependency-graph/tools/README_NOC_SHIFT_SUMMARY.md`
  - `dependency-graph/artifacts/noc_shift_summary_validation.md`
- Entradas aceitas:
  - `--minutes`
  - `--limit`
  - `--host`
  - `--severity`
  - `--open-only`
  - `--json`
- Como a ferramenta funciona:
  - reaproveita `explain_recent_events`
  - consolida por semântica, cluster, host e top triggers
  - produz leitura final resumida para turno/NOC
- Validação real executada:
  - janela ampla `--minutes 720 --limit 8` -> 6 eventos explicados
  - janela filtrada por host `--minutes 720 --limit 3 --host agt01` -> 3 eventos explicados
  - `--open-only` em 120 minutos -> retorno vazio válido
- Leitura operacional obtida:
  - semântica dominante: `service_failure`
  - cluster dominante: `AGT`
  - host dominante: `agt01`
  - sem evidência de problema público ou WAN principal nessa janela
- Limitações assumidas:
  - depende do runtime recente do Zabbix
  - problemas sem binding não entram na leitura causal
  - não substitui RCA completo nem operação contínua
- Próximo passo natural:
  - usar o resumo de turno como visão de entrada para triagem diária e correlação rápida

## 2026-04-06 - utilitário de resumo causal para eventos recentes do Zabbix

- Foi criada a CLI `dependency-graph/tools/explain_recent_events.py`.
- Artefatos novos:
  - `dependency-graph/tools/README_EXPLAIN_RECENT_EVENTS.md`
  - `dependency-graph/artifacts/explain_recent_events_validation.md`
- Entradas aceitas:
  - `--minutes`
  - `--limit`
  - `--host`
  - `--severity`
  - `--open-only`
  - `--json`
- Como a ferramenta funciona:
  - consulta problemas recentes do Zabbix via PostgreSQL
  - extrai `triggerid` de cada problema
  - reaproveita `causal_explain` para resolver o binding e a semântica
  - consolida leitura por evento e resumo final
- Validação real executada:
  - `--minutes 720 --limit 8` -> 6 eventos explicados, todos `service_failure`
  - `--minutes 720 --limit 3 --host agt01` -> 3 eventos explicados
  - `--minutes 120 --limit 5 --open-only` -> consulta válida, sem eventos abertos recentes
- Limitações assumidas:
  - a consulta depende do conteúdo recente do runtime do Zabbix
  - eventos sem binding não são explicados
  - a ferramenta é de triagem e resumo, não de RCA completo
- Próximo passo natural:
  - usar o utilitário para leitura rápida de problemas recentes, mantendo `causal_explain` como motor central

## 2026-04-05 - ferramenta executável de explicação causal adicionada

- Foi criada a CLI local `dependency-graph/tools/causal_explain.py`.
- Artefatos novos:
  - `dependency-graph/tools/README_CAUSAL_EXPLAIN.md`
  - `dependency-graph/artifacts/causal_explain_validation.md`
- Entradas aceitas na primeira versão:
  - `--itemid`
  - `--triggerid`
  - `--item-name`
  - `--trigger-name`
  - `--json`
- O que a ferramenta faz:
  - resolve o binding real do Zabbix
  - localiza o nó do grafo
  - aplica a semântica mínima da camada causal
  - imprime leitura operacional curta com próximos checks e limites
- Casos testados com sucesso:
  - Apache2 `69485` e `32506`
  - unbound `69486`
  - Livecopilot público `69633`
  - wg0 `69689`
- Ajuste importante feito na base:
  - o binding de `wg0` foi alinhado para `69689` no YAML consolidado
- Limitações assumidas:
  - ferramenta offline
  - não faz RCA completo
  - não substitui a leitura humana da camada causal
- Próximo passo natural:
  - usar a CLI como utilitário de apoio para leitura rápida e triagem de sinais do Zabbix

## 2026-04-05 - validação final do wg0 no alvo MikroTik bloqueada

- Foi confirmada a identificação correta do cenário `wg0`:
  - nó `edge-mikrotik-wg0`
  - host Zabbix `MikroTik RB3011`
  - itemid `69689`
  - key `mikrotik.ifOperStatus[16]`
- A rota até `10.45.0.1` existe, mas a execução dinâmica ficou bloqueada:
  - `22/tcp` recusou conexão
  - não havia caminho administrativo seguro para provocar a mudança em `wg0`
- Artefato novo:
  - `dependency-graph/artifacts/wg0_overlay_validation.md`
- Resultado final desta frente:
  - `wg0` -> `BLOCKED`
- Leitura causal mantida:
  - `overlay_failure`
  - impacto restrito ao overlay
  - sem promoção para `pppoe-out1`, `ether1`, `bridge` ou host
- Conclusão prática:
  - Apache2, unbound e a superfície pública do Livecopilot já estão fechados
  - a bateria causal fica fechada operacionalmente para os cenários validáveis nesta máquina
  - `wg0` permanece bloqueado por falta de acesso administrativo seguro ao alvo MikroTik

## 2026-04-05 - calibração temporal do Zabbix para Apache2 e unbound

- Foi executada uma rodada de calibração temporal com polling seriado de 15s para medir a janela real de convergência do Zabbix.
- Artefato novo:
  - `dependency-graph/artifacts/zabbix_timing_calibration.md`
- O que foi medido:
  - Apache2 (`69485` / `32506`)
  - unbound (`69486` / `32537`)
- Tempos observados:
  - Apache2: queda em `2s`, abertura da trigger em `2s`, recuperação do item em `2m02s`, fechamento da trigger em `2m02s`
  - unbound: queda em `1m16s`, abertura da trigger em `1m16s`, fechamento da trigger em `15s`, recuperação do item em `1m15s`
- Janela recomendada para futuras validações:
  - pelo menos `2m30s` após o start
  - idealmente `3m00s` para evitar falso `PARTIAL`
- Reclassificação honesta desta rodada:
  - Apache2 -> `PASS`
  - unbound -> `PASS`
- A conclusão desta frente é que o gargalo anterior era de janela/latência de observação, não de semântica causal.

## 2026-04-05 - follow-up dos PARTIAL da validação causal

- Foi executado follow-up com janela maior para os cenários que ainda estavam `PARTIAL`.
- Artefatos novos:
  - `dependency-graph/artifacts/causal_validation_followup.md`
- Cenários revisitados:
  - `Apache2 parado`
  - `unbound parado`
  - `wg0`
- Resultado honesto após o follow-up:
  - `Apache2 parado` permaneceu `PARTIAL`
  - `unbound parado` permaneceu `PARTIAL`
  - `wg0` permaneceu `PARTIAL`
- O que melhorou:
  - Apache2 e unbound tiveram ida/volta confirmadas no systemd
  - o Zabbix registrou a queda corretamente
  - o `wg0` foi finalmente fechado como alvo do cluster `MikroTik RB3011`, não como algo testável neste host local
- O que ainda impede `PASS` completo:
  - a recuperação no Zabbix ainda não fechou de forma limpa no último snapshot consultado
  - `wg0` exige o host/edge correto para injeção segura
- Conclusão desta rodada:
  - a camada causal continua correta
  - o gargalo restante é de janela/latência de observação, não de modelagem


## 2026-04-05 - superfície pública do Livecopilot alinhada ao runtime real

- A hipótese anterior do cenário público falhou porque o fault injection usou `cloudflared.service`, que publica outros domínios.
- A investigação mostrou o caminho real da superfície pública do Livecopilot:
  - `livecopilot.escossio.dev.br`
  - `cloudflared-livecopilot.service`
  - `http://127.0.0.1:8080`
  - `livecopilot-semantic-api.service`
  - `http://127.0.0.1:8099`
- Checks Zabbix que representam a superfície pública real:
  - `69624` `Livecopilot Apache Edge`
  - `69625` `Livecopilot Frontend Publico`
  - `69630` `Livecopilot Public Health`
  - derivados `69632`, `69633`, `69634`
- Checks Zabbix de backend que ficaram preservados no teste:
  - `69626` `Livecopilot Backend Health`
  - `69627` `Livecopilot Backend Status`
  - `69628` `Livecopilot Backend API`
  - derivados `69635`, `69636`, `69637`
- Fault injection realista validado nesta rodada:
  - `systemctl stop cloudflared-livecopilot`
- Efeito observado:
  - `frontend público` e `public health` caíram
  - `apache edge` ficou estável
  - `backend health`, `backend status` e `backend API` ficaram estáveis
- Conclusão operacional:
  - `public_access_failure` continua válida
  - o ponto real de falha observável é o túnel dedicado `cloudflared-livecopilot.service`
  - derrubar `cloudflared.service` genérico era hipótese errada para este cenário
- Resultado da nova validação pública:
  - `PASS`


## 2026-04-05 - validação curta da correlação causal executada

- Foi executada uma bateria curta de validação reversível para a camada mínima de correlação causal.
- Artefatos novos:
  - `dependency-graph/artifacts/causal_validation_plan.md`
  - `dependency-graph/artifacts/causal_validation_results.md`
- Cenários executados nesta rodada:
  - `Apache2 parado`
  - `unbound parado`
  - `Livecopilot superfície pública` via `cloudflared`
- Cenário apenas documental nesta rodada:
  - `wg0`
- Resultados registrados com honestidade:
  - `Apache2 parado` -> `PARTIAL`
  - `unbound parado` -> `PARTIAL`
  - `Livecopilot superfície pública` -> `FAIL`
  - `wg0` -> `PARTIAL`
- O que a bateria confirmou:
  - a leitura de `service_failure` bateu no serviço certo para Apache2 e unbound
  - o blast radius local ficou contido como esperado
  - a hipótese de `public_access_failure` para Livecopilot não ficou comprovada nesta rodada
  - `wg0` não pôde ser provocado com segurança no host atual
- O que ainda falta validar:
  - confirmar o acoplamento exato entre superfície pública do Livecopilot e os itens derivados corretos
  - validar um evento dinâmico real de `wg0` no host/edge correto
  - acompanhar a latência de atualização do Zabbix após rollback para fechar `PASS` em cenários de serviço


## 2026-04-05 - camada mínima de correlação causal criada

- Foi criada a primeira camada explícita de correlação causal por cima dos bindings reais do Zabbix.
- Artefatos novos:
  - `dependency-graph/CORRELATION.md`
  - `dependency-graph/models/causal_correlation_rules.yaml`
  - `dependency-graph/artifacts/causal_reading_examples.md`
- O que essa camada faz:
  - correlaciona evento Zabbix com nó do grafo
  - lê semântica de falha já existente
  - traduz a falha em escopo provável, blast radius e próximos testes
  - separa leitura de host, serviço, borda, WAN, overlay e upstream
- Semânticas cobertas nesta rodada:
  - `host_failure`
  - `service_failure`
  - `public_access_failure`
  - `local_edge_failure`
  - `wan_uplink_failure`
  - `wan_primary_failure`
  - `overlay_failure`
  - `external_edge_failure`
  - `upstream_provider_failure`
- Exemplos concretos materializados:
  - `Apache2 parado`
  - `Web 127.0.0.1 indisponivel`
  - `unbound parado`
  - `PPPoE tunnel status down`
  - `wg0 down`
  - `bridge down`
  - `Livecopilot Frontend Público indisponível`
- Limites explícitos desta rodada:
  - ainda não é engine automática online
  - ainda não é RCA completo
  - ainda não cruza múltiplos eventos simultâneos de forma avançada
  - ainda depende da qualidade do binding e da semântica já documentada
  - ainda não usa histórico temporal profundo
- Próximo passo natural:
  - usar essa camada como base para correlação incremental de múltiplos sinais e priorização operacional

## 2026-04-05 - bindings fechados no runtime do Zabbix

- A consulta ao banco do Zabbix fechou os `itemid` exatos pendentes dos serviços base e da MikroTik.
- Artefatos atualizados:
  - `dependency-graph/ZABBIX_BINDINGS.md`
  - `dependency-graph/ZABBIX_BINDING_README.md`
  - `dependency-graph/models/zabbix_graph_bindings.yaml`
- Serviços base agora com itemid exato:
  - `zabbix-server` -> `69615`
  - `zabbix-agent2` -> `69616`
  - `grafana-server` -> `69617`
  - `cloudflared` -> `69618`
  - `postgresql@17-main` -> `69619`
  - `ssh` -> `69620`
- MikroTik agora com itemids exatos para:
  - `SNMP system name` -> `69656`
  - `SNMP uptime` -> `69657`
  - `Memory size` -> `69659`
  - `Board name` -> `69661`
  - `RouterOS version` -> `69662`
  - `Temperature` -> `69663`
  - `Voltage` -> `69664`
  - `PPPoE tunnel status` -> `69665`
  - `WireGuard tunnel status` -> `69666`
  - `bridge operational status` -> `69690`
  - `ether1 operational status` -> `69692`
  - `pppoe-out1 operational status` -> `69701`
  - `wg0 operational status` -> `69689`
  - `ether1 inbound traffic` -> `69707`
  - `ether1 outbound traffic` -> `69722`
- Cobertura mínima obrigatória ficou praticamente inteira:
  - AGT base
  - Livecopilot por camada
  - MikroTik RB3011 e trilha principal de transporte
- O que continua pendente por falta de sinal real dedicado:
  - binding Zabbix do upstream `AS28126 BRISANET`
  - binding Zabbix recorrente do endpoint Netflix observado
- O que ficou para revisão futura:
  - triggers dedicadas para alguns serviços base não existem na base consultada

## 2026-04-05 - bindings pendentes reduzidos e cobertura mínima consolidada

- A camada de binding foi refinada para distinguir `complete`, `partial` e `pending`.
- Artefatos atualizados:
  - `dependency-graph/ZABBIX_BINDINGS.md`
  - `dependency-graph/ZABBIX_BINDING_README.md`
  - `dependency-graph/models/zabbix_graph_bindings.yaml`
- Cobertura mínima obrigatória já consolidada:
  - `agt01`
  - `apache2`
  - `unbound`
  - Livecopilot por camada
  - MikroTik RB3011
  - `bridge`, `ether1`, `pppoe-out1` e `wg0`
- Bindings com IDs exatos já fechados:
  - `CPU temperature` / `cpu.temp` / `69621`
  - `Service apache2 running` / `69485`
  - `Web apache 127.0.0.1` / `69488`
  - `Service unbound running` / `69486`
  - `Livecopilot Serviço estado` / `69631`
  - `Livecopilot Apache Edge estado` / `69632`
  - `Livecopilot Frontend Público estado` / `69633`
  - `Livecopilot Public Health estado` / `69634`
  - `Livecopilot Backend Health estado` / `69635`
  - `Livecopilot Backend Status estado` / `69636`
  - `Livecopilot Backend API estado` / `69637`
  - triggers `32506`, `32507`, `32537`
- Ainda parcialmente pendente:
  - `zabbix-server`
  - `zabbix-agent2`
  - `cloudflared`
  - `postgresql@17-main`
  - `ssh`
  - IDs SNMP exatos da MikroTik
  - upstream `AS28126 BRISANET`
- Regra de fechamento:
  - manter o binding útil e legível mesmo quando alguns `itemid` ainda não puderem ser extraídos

## 2026-04-05 - binding Zabbix -> dependency-graph iniciado

- Foi criada a camada explícita de binding entre itens/triggers do Zabbix e nós do `dependency-graph`.
- Artefatos novos:
  - `dependency-graph/ZABBIX_BINDINGS.md`
  - `dependency-graph/ZABBIX_BINDING_README.md`
  - `dependency-graph/models/zabbix_graph_bindings.yaml`
- O binding inicial cobre:
  - `agt01`
  - serviços centrais do AGT
  - Livecopilot por camada
  - MikroTik RB3011
  - bridge, ether1, pppoe-out1 e wg0
- Mapeamentos reais já ligados a IDs conhecidos:
  - `CPU temperature` / `cpu.temp` / `69621`
  - itens derivados do Livecopilot `69631` a `69637`
  - `Service apache2 running` / `69485`
  - `Web apache 127.0.0.1` / `69488`
  - `Service unbound running` / `69486`
  - triggers `32506`, `32507` e `32537`
- A semântica de falha agora conversa com o binding:
  - `host_failure`
  - `service_failure`
  - `public_access_failure`
  - `wan_primary_failure`
  - `wan_uplink_failure`
  - `overlay_failure`
- O que ficou pendente nesta rodada:
  - `itemid`/`triggerid` exatos dos serviços base ainda não extraídos
  - IDs SNMP do MikroTik ainda não coletados
  - binding do upstream `AS28126 BRISANET`
  - binding de endpoints observados da Netflix como sinal recorrente
- Próximo passo natural:
  - completar itemids/triggers pendentes sem inflar o escopo

## 2026-04-05 - árvore de transporte por salto formalizada

- O `dependency-graph` passou a distinguir explicitamente:
  - `functional_node`
  - `transport_node`
  - `observed_delivery_node`
  - `observed_auxiliary_node`
- Foi criado o artefato:
  - `dependency-graph/TRANSPORT_TREE.md`
- Os modelos do `AGT` e da `MikroTik RB3011` foram enriquecidos com `role` por nó para deixar clara a leitura por salto.
- A cadeia de transporte ficou explícita como leitura separada da função:
  - `agt01` como função operacional
  - `br0` como transporte
  - `MikroTik RB3011` como função de borda
  - `bridge`, `ether1`, `pppoe-out1`, `206.42.12.37` e `AS28126 BRISANET` como transporte
- A folha observacional da Netflix foi mantida separada:
  - `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net`
- O que continua fora da cadeia principal:
  - endpoints de log e telemetria
  - endpoints auxiliares de edge
  - a folha Netflix sem repetição observada suficiente
- Regra futura:
  - só promover observação pontual depois de repetição em novas capturas

## 2026-04-05 - modelagem observacional da entrega Netflix consolidada

- Foi criada uma camada observacional para separar os destinos capturados na reprodução real da Netflix.
- Artefato novo:
  - `internet-observation/artifacts/netflix_observed_delivery_model.md`
- Classificação aplicada:
  - entrega de vídeo observada
  - log/telemetria
  - infraestrutura auxiliar
- Endpoint classificado como melhor candidato à entrega de vídeo observada:
  - `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net`
- Endpoints classificados como log/telemetria:
  - `nrdp.logs.netflix.com`
  - `logs.dradis.netflix.com`
  - `logs.us-east-1.internal.dradis.netflix.com`
  - `apiproxy-logging-s3-5c4574073964ceac.elb.us-east-1.amazonaws.com`
- Endpoints classificados como infra auxiliar:
  - `region1.v2.argotunnel.com`
  - `livecopilot.escossio.dev.br`
- Regra de promoção futura:
  - nenhum hostname observado uma única vez entrou na cadeia causal principal
  - a promoção depende de repetição em novas capturas
- Ajuste mínimo de semântica também foi registrado para suportar:
  - `observed_delivery_endpoint`
  - `observed_auxiliary_endpoint`
  - `repeated_observation`

## 2026-04-05 - captura real de Netflix iniciada e consolidada

- A fase de captura real foi iniciada sem mexer na sessão gráfica nem na publicação do noVNC.
- A coleta foi feita com `tcpdump` no host da observabilidade.
- Artefatos gerados na captura:
  - `internet-observation/captures/20260405-211611-netflix/netflix-session-live.log`
  - `internet-observation/captures/20260405-211611-netflix/netflix-session.pcap`
- Endpoints/hosts relevantes observados no tráfego:
  - `ipv4-c010-jdo001-brisanet-isp.1.oca.nflxvideo.net`
  - `nrdp.logs.netflix.com`
  - `logs.dradis.netflix.com`
  - `logs.us-east-1.internal.dradis.netflix.com`
  - `apiproxy-logging-s3-5c4574073964ceac.elb.us-east-1.amazonaws.com`
  - `region1.v2.argotunnel.com`
- IPs remotos relevantes observados:
  - `177.37.221.42`
  - `104.18.32.47`
  - `104.21.4.50`
  - `172.67.131.172`
  - `45.57.8.1`
  - `45.57.9.1`
  - `205.251.193.25`
  - `98.85.148.156`
  - `54.160.93.182`
  - `3.211.157.115`
- Leitura prática:
  - a entrega observável passou por infraestrutura `nflxvideo.net`
  - a observação veio do tráfego real, não de inferência de catálogo
- Observação sobre DevTools:
  - não havia canal remoto de DevTools exposto nesta rodada sem mexer na sessão
  - a evidência principal ficou no `network capture`

## 2026-04-05 - sessão XFCE do noVNC restaurada

- A camada de publicação do noVNC permaneceu intacta.
- A correção foi feita apenas na sessão gráfica da VM.
- Causa raiz identificada:
  - sessão `liveui` iniciando com `DBUS_SESSION_BUS_ADDRESS` e `XDG_RUNTIME_DIR` herdados do root
  - ownership incorreto em `~/.config` e `~/.vnc`
  - `light-locker` entrando na sessão sem contexto de LightDM
- Correções aplicadas:
  - criado `/home/liveui/.vnc/xstartup`
  - sessão sobe com `dbus-run-session -- startxfce4`
  - ownership de `~/.config` e `~/.vnc` corrigido para `liveui`
  - `light-locker` desabilitado para a sessão VNC
- Resultado local:
  - `xfce4-session` sobe
  - `xfsettingsd` sobe
  - `xfce4-panel` sobe
  - `Thunar --daemon` sobe
  - `xfdesktop` sobe
- Resultado visual:
  - o noVNC passou a exibir a área de trabalho XFCE da VM
- Observação:
  - ainda existem warnings menores de `at-spi`, mas eles não impedem a sessão gráfica de funcionar

## 2026-04-05 - raiz do noVNC finalizada sem directory listing

- Causa do `Directory listing for /`:
  - a raiz `/` do vhost `novnc` estava sendo proxied diretamente para a raiz do `websockify`
  - o listing vinha do servidor embutido do noVNC, não de `DocumentRoot` local do Apache
- Ajuste aplicado no vhost `novnc`:
  - rewrite interna de `/` para `/vnc.html?autoconnect=true&path=websockify`
  - sem redirect externo e sem depender de `http` atrás do Cloudflare
- Resultado de UX:
  - `/` deixou de mostrar listagem de diretório
  - `/` passou a abrir a interface do noVNC
  - `/vnc.html?autoconnect=true&path=websockify` continua funcional
- Validação do websocket mantida:
  - `wss://novnc.escossio.dev.br/websockify` conectou
  - retorno `RFB 003.008`
- Evidência visual:
  - navegador headless conseguiu carregar a raiz pública do `novnc` e gerar screenshot
- Pronto para a etapa seguinte:
  - login manual no Netflix
  - playback real
  - captura de tráfego

## 2026-04-05 - noVNC movido para hostname dedicado

- O noVNC saiu do path misturado na observabilidade e passou para hostname próprio:
  - `novnc.escossio.dev.br`
- O vhost antigo por path foi removido do default Apache:
  - `/novnc/`
  - `/novnc/websockify`
- Foi criado vhost dedicado no Apache:
  - `/etc/apache2/sites-available/novnc.conf`
  - `ServerName novnc.escossio.dev.br`
  - proxy HTTP para `10.45.0.3:6081`
  - proxy WebSocket para `10.45.0.3:6081/websockify`
- Proteção simples aplicada:
  - `Basic Auth` no Apache
  - arquivo secreto fora do repositório em `/etc/apache2/.htpasswd-novnc`
- O `cloudflared` foi ajustado com ingress dedicada para o hostname:
  - arquivo `/etc/cloudflared/config.yml`
  - rota DNS criada para o tunnel `6394a032-08e8-4bc7-a957-44c77e743c49`
- Validação local concluída:
  - UI direta do noVNC respondeu `200`
  - UI via Apache local com `Host: novnc.escossio.dev.br` respondeu `200`
  - WebSocket local via Apache conectou e respondeu `RFB 003.008`
- Validação pública concluída:
  - `https://novnc.escossio.dev.br/vnc.html` respondeu `401` sem credencial e `200` com credencial
  - `wss://novnc.escossio.dev.br/websockify` conectou e respondeu `RFB 003.008`
  - navegador headless conseguiu carregar o noVNC em `autoconnect` e gerar screenshot da sessão
- A sessão remota ficou pronta para a próxima etapa:
  - login manual no Netflix
  - playback real
  - captura com `tcpdump`
  - observação com DevTools

## 2026-04-05 - noVNC publicado por proxy reverso no Apache

- A sessão gráfica compartilhada da VM já existia via `x11vnc` + `websockify`.
- Causa do acesso falhar para uso remoto:
  - o noVNC estava exposto apenas no IP privado `10.45.0.3:6081`
- Ajuste operacional aplicado:
  - proxy reverso público no Apache para `/novnc/`
  - proxy de websocket para `/novnc/websockify`
- Arquivo de sistema alterado com backup prévio:
  - `/etc/apache2/sites-available/000-default.conf`
  - backup: `/etc/apache2/sites-available/000-default.conf.bak-20260405-202635`
- Validação local:
  - `http://127.0.0.1/novnc/vnc.html` respondeu `200`
- Observação:
  - o hostname público `observabilidade.escossio.dev.br` redireciona para tela de login antes do noVNC
  - a sessão do navegador dentro da VM continua pronta em `https://www.netflix.com/`

## 2026-04-05 - domínios reais adicionados e playbook de captura preparado

- Foi criada a frente `internet-observation/` para separar checagem pública simples de observação real de tráfego.
- Estrutura criada:
  - `internet-observation/README.md`
  - `internet-observation/artifacts/domain_targets.md`
  - `internet-observation/artifacts/netflix_capture_playbook.md`
  - `internet-observation/artifacts/initial_domain_validation.md`
  - `internet-observation/captures/`
- Domínios adicionados ao escopo DNS:
  - `netflix.com`
  - `www.netflix.com`
  - `primevideo.com`
  - `www.primevideo.com`
  - `google.com`
  - `www.google.com`
  - `youtube.com`
  - `www.youtube.com`
- Endpoints HTTPS públicos adicionados ao escopo web:
  - `https://www.netflix.com/`
  - `https://www.primevideo.com/`
  - `https://www.google.com/`
  - `https://www.youtube.com/`
- Validação simples executada com:
  - `dig`
  - `ping`
  - `curl -L` com `GET`
- Resultado objetivo desta coleta:
  - Netflix respondeu em HTTPS simples, mas ICMP falhou
  - Prime Video, Google e YouTube responderam em DNS, ICMP e HTTPS simples
  - `HEAD` simples devolveu `405` em Netflix e Prime Video, então a referência documental desta rodada ficou em `GET`
- Ferramentas presentes na VM:
  - `tcpdump`
  - `curl`
  - `dig`
  - `traceroute`
  - `chromium`
  - `firefox`
- Ferramenta ausente:
  - `mtr`
- Observação importante:
  - ping e domínio público não substituem observação do tráfego real de streaming
- A metodologia de captura real para Netflix ficou preparada com `tcpdump` + DevTools + consolidação posterior de hostnames, IPs e ASN.

## 2026-04-05 - regras de impacto adicionadas ao dependency-graph

- O `dependency-graph` passou a carregar semântica explícita de impacto além de dependência estrutural.
- Foi criado o artefato:
  - `dependency-graph/IMPACT_RULES.md`
- A semântica do projeto foi estendida para suportar:
  - `impact_targets`
  - `failure_semantics`
  - `blast_radius`
  - `severity_if_failed`
  - `propagation_mode`
- O cluster `AGT` agora distingue explicitamente:
  - falha do host `agt01`
  - falha de `br0`
  - falha da borda `MikroTik RB3011`
- O cluster `MikroTik RB3011` agora distingue explicitamente:
  - falha da borda local
  - falha de uplink físico
  - falha da WAN principal
  - falha de overlay
  - falha de upstream
  - falha externa acima do provedor
- `wg0` permaneceu separado da cadeia causal principal e continua tratado como `overlay observed`.
- `nuvem / destino` continua inferido.
- Limite atual:
  - as regras ainda são documentais e sem engine automática de RCA
- Próximo passo provável:
  - decidir se essas regras viram uma camada agregadora de correlação ou consulta operacional sobre os clusters já modelados

## 2026-04-05 - MikroTik separada em cluster próprio no dependency-graph

- Foi criado o cluster dedicado `MikroTik RB3011` no `dependency-graph`.
- Novos artefatos desta rodada:
  - `dependency-graph/clusters/mikrotik-rb3011.md`
  - `dependency-graph/models/mikrotik_rb3011_dependency_model.yaml`
  - `dependency-graph/views/mikrotik_rb3011_dependency_graph.mmd`
- O cluster `AGT` foi simplificado para manter apenas:
  - serviços do host
  - host `agt01`
  - `br0`
  - dependência explícita do cluster `MikroTik RB3011`
- A cadeia estrutural da borda deixou de ficar repetida dentro do AGT.
- A ligação intercluster ficou explícita como `br0 -> cluster MikroTik RB3011`.
- O cluster dedicado da MikroTik passou a carregar:
  - `MikroTik RB3011`
  - `bridge`
  - `next-hop 10.45.0.1`
  - `ether1`
  - `pppoe-out1`
  - IP público `206.42.12.37`
  - `AS28126 BRISANET`
  - `wg0` como overlay observado
- O que continua inferido:
  - `nuvem / destino`
  - a leitura causal/documental do caminho acima da RB3011
- O `README` e a `SEMANTICS.md` foram ajustados para admitir múltiplos clusters e referência intercluster explícita.
- Próximo passo natural:
  - decidir se haverá um modelo agregador acima dos clusters para mapear todo o ambiente sem duplicação
  - expandir a mesma separação para outras bordas ou outros hosts, quando houver base confirmada

## 2026-04-05 - MikroTik RB3011 integrada ao dependency-graph do AGT

- O cluster `AGT` deixou de depender de uma abstração genérica de concentrador e passou a apontar para a borda concreta `MikroTik RB3011`.
- A cadeia superior do AGT foi reescrita com evidência já validada no runtime e no inventário local:
  - `br0`
  - `bridge` da MikroTik
  - `next-hop 10.45.0.1`
  - IP público `206.42.12.37`
  - `pppoe-out1`
  - `ether1`
  - `MikroTik RB3011`
  - `AS28126 BRISANET`
- Nós concretizados nesta rodada:
  - `MikroTik RB3011` como equipamento real de borda do AGT
  - `bridge` como domínio L2 local observado
  - `ether1` como uplink físico observado
  - `pppoe-out1` como sessão WAN principal compatível com a evidência validada
  - `wg0` como túnel / overlay observado fora da cadeia causal principal
- O nó genérico do concentrador do link deixou de existir no modelo do AGT.
- O que continua inferido:
  - `nuvem / destino`, porque ainda não há um alvo único confirmado
  - a leitura do caminho na RB3011 continua causal e documental, não uma reprodução literal do forwarding interno do equipamento
- Os três formatos do grafo foram atualizados:
  - `dependency-graph/clusters/agt.md`
  - `dependency-graph/models/agt_dependency_model.yaml`
  - `dependency-graph/views/agt_dependency_graph.mmd`
- O arquivo `STATUS.md` foi atualizado nesta mesma rodada.
- Não houve mudança no runtime do Grafana.

## 2026-04-04 - integração do Livecopilot por camada

- O Livecopilot foi integrado ao escopo de observabilidade por camada sem alterar a arquitetura do serviço.
- Checks propostos nesta rodada:
  - serviço `livecopilot-semantic-api.service`
  - borda Apache em `http://127.0.0.1:8080/`
  - frontend público em `http://livecopilot.escossio.dev.br/`
  - health backend local em `http://127.0.0.1:8099/health`
  - status operacional em `http://127.0.0.1:8099/status`
  - endpoint operacional de API em `http://127.0.0.1:8099/api/panel/summary`
- O bloco do Livecopilot foi descrito para o Grafana como leitura separada de serviço, borda, frontend e backend.
- Não houve inclusão de DNS novo porque o objetivo operacional foi cobrir publicação e aplicação, não resolução específica.
- A escrita automática no Zabbix central ficou acessível por API local nesta máquina e os itens/triggers da camada Livecopilot foram aplicados no runtime.

## 2026-04-04 - correção de visibilidade do bloco Livecopilot no Grafana

- O dashboard principal do Grafana foi regravado com um bloco Livecopilot explícito logo abaixo do topo principal.
- Causa raiz: o bloco não existia no JSON do dashboard servindo a UI, apesar de os itens/triggers já existirem no Zabbix.
- A posição final ficou visível no layout real, com a seção Livecopilot aparecendo entre o bloco principal e os painéis inferiores.
- A validação foi feita por API do Grafana e por captura visual do dashboard autenticado.
- O recorte visual mostrou os painéis `Livecopilot Serviço`, `Livecopilot Apache Edge` e `Livecopilot Frontend Público` já no corpo da página.

## 2026-04-05 - correção de renderização dos cards Livecopilot no Grafana

- Os cards Livecopilot estavam visíveis, mas renderizando `N/A` porque os itens base eram strings HTTP/systemd e o datasource do Grafana não entregava frames úteis para a query anterior.
- A correção mínima foi criar itens numéricos derivados no Zabbix para cada camada do Livecopilot, preservando os itens originais como fonte operacional.
- Itens derivados criados:
  - `Livecopilot Serviço estado` (`69631`)
  - `Livecopilot Apache Edge estado` (`69632`)
  - `Livecopilot Frontend Público estado` (`69633`)
  - `Livecopilot Public Health estado` (`69634`)
  - `Livecopilot Backend Health estado` (`69635`)
  - `Livecopilot Backend Status estado` (`69636`)
  - `Livecopilot Backend API estado` (`69637`)
- O dashboard principal do Grafana foi regravado para ancorar os cards nesses `itemids` numéricos.
- A validação por `api/ds/query` passou a retornar `frames: 1` para todos os cards do bloco Livecopilot.
- A validação visual autenticada mostrou os cards em estado operacional real, com leitura verde e sem `N/A`.
- O card `Livecopilot Backend Status` foi tratado como diagnóstico complementar e passou a exibir `OK` quando saudável.
- O layout macro não foi alterado.

## 2026-04-05 - reorganização em duas colunas do dashboard Grafana

- O dashboard principal foi reorganizado em duas faixas visuais claras abaixo do topo aprovado.
- Coluna esquerda:
  - serviços críticos do host
  - serviços de telemetria operacional tratados como status de aplicativo/infra
  - bloco Livecopilot inteiro, preservando leitura `UP / DOWN / OK`
- Coluna direita:
  - `CPU`
  - `Memória Livre`
  - `Temperatura CPU`
- O topo permaneceu intacto:
  - `Resumo`
  - `Problemas`
  - `Web Público`
  - `DNS Público`
- A reorganização foi feita somente com `gridPos`, sem mexer em coleta, itens, triggers ou thresholds.
- A captura autenticada mostrou a divisão visual clara entre serviços à esquerda e telemetria à direita.

## 2026-04-05 - simplificação visual dos cards de serviço

- Os cards de serviço passaram a mostrar o nome do serviço como conteúdo principal dentro da caixa.
- A cor do card continua indicando estado operacional:
  - verde para saudável / `UP`
  - vermelho para indisponível / `DOWN`
  - cinza para diagnóstico complementar
- A telemetria permaneceu separada na coluna da direita, sem mudança de coleta nem de thresholds.
- O card `DNS Local` foi mantido como diagnóstico complementar.
- A mudança foi puramente de apresentação no Grafana, sem tocar na baseline do Zabbix.
- O refinamento final reduziu a tipografia dos cards de serviço para deixar a leitura mais compacta.

## 2026-04-05 - proveniência visual do host `agt01`

- Os cards estatísticos passaram a exibir um badge visual `agt01` no cabeçalho para deixar explícito que as informações vêm do host monitorado.
- O badge foi aplicado sem alterar a coluna de telemetria.
- O conteúdo principal do card continua sendo o serviço ou a métrica, e a origem passou a ficar marcada visualmente no topo do card.

## Diagnóstico inicial

- Diretório do projeto criado e organizado
- Apache instalado e em execução
- PostgreSQL 17 já estava instalado e ouvindo em `127.0.0.1:5432`
- DNS local ativo via `unbound`; `dnsmasq` não está ativo

## Decisão

- Instalar Zabbix localmente por pacotes oficiais 7.4
- Reutilizar o PostgreSQL já existente, sem criar nova instância
- Publicar o frontend em Apache de forma isolada e limpa

## O que foi criado

- estrutura base do projeto
- inventários YAML para serviços, web e DNS
- scripts para coleta, validação e geração de plano
- documentação de aplicação e blueprint de dashboard
- repositório oficial Zabbix adicionado no host
- stack local instalada com `zabbix-server-pgsql`, `zabbix-frontend-php`, `zabbix-apache-conf`, `zabbix-agent2` e `zabbix-sql-scripts`

## Pendências

- nenhuma pendência bloqueante para o escopo desta rodada

## Riscos

- checks DNS e web precisam refletir o comportamento real do host
- `emby-server` já apareceu com leitura inconsistente em validação anterior, mas o inventário desta rodada encontrou o serviço ativo e expondo `8096`

## Resultado desta rodada

- versão instalada do Zabbix: `7.4.8`
- frontend acessível em `http://127.0.0.1:8081/`
- `zabbix-server` e `zabbix-agent2` ativos
- PostgreSQL 17 reutilizado com sucesso
- database `zabbix` e role `zabbix` criados na instância existente
- schema oficial importado com sucesso
- host `agt01` criado com `hostid 10776`
- itens criados para serviços, web e DNS
- triggers criadas para serviço, web e DNS, com complementos para `unbound` e `web 8080`
- dashboard `Observabilidade Zabbix - resumo` preenchido com widgets reais
- Grafana instalado e integrado ao Zabbix como camada principal de visualização
- dashboard principal do Grafana criado em `observabilidade-grafana`
- hostname público `observabilidade.escossio.dev.br` publicado para o Grafana via Cloudflare Tunnel
- login operacional do Grafana validado com o usuário `admin`
- credencial padrão `Admin/zabbix` removida da operação
- evidências objetivas salvas em `artifacts/`
- preparação do git concluída com separação entre fonte versionável, artefatos e segredos locais
- README reorganizado para explicitar a arquitetura Zabbix → Grafana e a estrutura do repositório
- `shellcheck` não está instalado no host, então a validação de shell ficou limitada à execução dos scripts
- hardening imediato do Grafana realizado com rotação da credencial `admin` via `grafana-cli`
- login antigo `admin/admin` deixou de autenticar
- nova credencial validada pela API pública do Grafana
- segredo armazenado apenas em caminho local restrito fora do git: `/srv/observabilidade-zabbix/backups/20260404-grafana-login/grafana_admin_password.secret` (permissões `600`)
- troubleshooting do dashboard Grafana iniciado e causa raiz identificada: os painéis numéricos estavam filtrando pelo `key_` do Zabbix, mas o plugin do Grafana respondeu corretamente apenas quando o filtro passou a usar o **nome do item**
- painéis de web/DNS em item textual exigiram adaptação para painéis de problema/status, porque o plugin não renderizou os retornos textuais como `stat`
- inventário operacional do host Debian iniciado com cruzamento de `systemd` ativo/habilitado/falho e `ss`/processos para escopo de monitoramento
- classificação preliminar fechada entre serviços críticos, úteis e ruído operacional sem mexer em configuração
- artefatos novos previstos nesta rodada:
  - `artifacts/debian_services_inventory.md`
  - `artifacts/monitoring_scope_recommendation.md`
- achado operacional relevante:
  - `snmpd.service` está em estado `failed`
  - `emby-server.service` segue ativo e exposto em `8096`, então é candidato a monitoramento útil, não crítico

## Fechamento da rodada atual

- inventário confirmado com base em `systemd` (`running`, `enabled`, `failed`), `ss -tulpn` e `ps`
- base mínima atualizada em `config/services.yaml`: `zabbix-server`, `zabbix-agent2`, `apache2`, `grafana-server`, `cloudflared`, `unbound`, `postgresql@17-main`, `ssh`
- segunda linha documentada no YAML: `emby-server`, `livecopilot-semantic-api`, `cloudflared-livecopilot`, `smbd`, `nmbd`, `winbind`, `libvirtd`
- serviços dispensáveis para item dedicado agora: `dbus`, `polkit`, `systemd-journald`, `systemd-logind`, `systemd-machined`, `systemd-udevd`, `udisks2`, `avahi-daemon`, `cron`, `virtlockd`, `virtlogd`, `liveui-xfce`, `liveui-xvfb`, `getty@tty1`, `user@0`, `dnsmasq` da libvirt
- falha operacional registrada sem correção nesta rodada: `snmpd.service`
- documentação atualizada com os artefatos:
  - `artifacts/debian_services_inventory.md`
  - `artifacts/monitoring_scope_recommendation.md`
- `config/services.yaml` foi alinhado à base mínima real do host, sem mexer em runtime do Zabbix/Grafana
- ajuste mínimo pendente: incluir `dnsmasq` apenas se a rede da libvirt virar alvo explícito de monitoramento
- inventário de web/DNS também foi alinhado à baseline operacional, com foco no domínio público publicado e no resolvedor local real
- `observabilidade.escossio.dev.br` virou base mínima de web e DNS; checks herdados e genéricos ficaram fora
- runtime do Zabbix sincronizado com a baseline final:
  - itens de serviço criados para `zabbix-server`, `zabbix-agent2`, `grafana-server`, `cloudflared`, `postgresql` e `ssh`
  - item DNS legado de `example.com` foi reaproveitado para `observabilidade.escossio.dev.br`
  - item web legado de `127.0.0.1` foi reaproveitado para o domínio público `observabilidade.escossio.dev.br`
  - dashboard do Grafana foi rebatizado para a baseline atual e já não exibe `example.com` como painel principal

## Fechamento da rodada visual

- dashboard principal do Grafana reorganizado em grade 4x4 para reduzir área morta e eliminar rolagem na visualização padrão
- linha 1 reservada para `Resumo`, `Problemas`, `Web Público` e `DNS Público`
- linhas centrais reservadas para os serviços críticos da baseline operacional
- linha inferior reservada para diagnósticos e segunda linha: `Grafana Local`, `Zabbix Frontend`, `localhost-a` e `Emby`
- cores e hierarquia visual ajustadas para leitura operacional rápida em monitor grande ou TV
- validação técnica confirmada por API do Grafana após o save do dashboard
- artefato novo previsto nesta rodada:
  - `artifacts/grafana_dashboard_visual_refresh.md`

## Fechamento da rodada compacta

- dashboard principal compactado para reduzir a altura dos cards e deixar a leitura mais viva
- painel `Emby` removido do layout principal sem impacto na baseline de coleta
- cards centrais reduzidos para altura `3` e linha de diagnóstico reaproveitada em três blocos mais largos
- `Resumo` e demais cards principais seguem acima da dobra com leitura operacional preservada
- validação técnica confirmada por API após o save compacto do dashboard
- artefato novo desta rodada:
  - `artifacts/grafana_dashboard_compact_refresh.md`

## Fechamento da rodada semântica

- dashboard principal do Grafana teve a semântica operacional ajustada sem mexer no layout base
- `RAM` foi rebatizada para `Memória disponível` e recebeu threshold compatível com `vm.memory.size[pavailable]`
- painéis de serviço que ainda exibiam número cru passaram a usar mapeamento operacional `Up/Down`
- `localhost-a` foi rebaixado para leitura diagnóstica com cor neutra/atenção leve
- `CPU Temp` foi mantido como painel operacional de temperatura com unidade e thresholds coerentes, sem alterar a baseline de coleta
- documentação desta rodada foi registrada nos artefatos do projeto
- dashboard principal permaneceu sem scroll e com a hierarquia visual intacta

## Fechamento da rodada de query do CPU Temp

- o painel `CPU Temp` foi ajustado para o modo `Item ID` do datasource Zabbix
- a query passou a ancorar explicitamente o item `cpu.temp` pelo `itemid 69621`
- o datasource do Grafana voltou a responder com série real para o painel
- o valor validado para temperatura no Grafana foi `38.5 C`
- a correção foi aplicada sem mexer no layout geral nem nos demais cards
- documentação desta rodada foi registrada nos artefatos do projeto

## Fechamento da rodada de refinamento visual

- títulos dos cards foram encurtados para nomes operacionais mais diretos
- a compactação anterior foi revertida parcialmente para recuperar legibilidade
- cards principais voltaram para altura 2 para mostrar melhor o valor
- painel `localhost-a` foi renomeado para `DNS Local`
- `Zabbix Server` foi encurtado para `Zabbix`
- `Apache2` foi encurtado para `Apache`
- `Memória disponível` passou a aparecer como `Memória Livre`
- `CPU Temp` passou a aparecer como `Temperatura CPU`
- a grade principal permaneceu sem scroll e com as queries intactas
- documentação desta rodada foi registrada nos artefatos do projeto

## Fechamento da rodada de densidade

## 2026-04-05 - frente inicial do dependency graph por cluster

- Foi criada uma frente documental própria para o grafo de dependências operacionais em `dependency-graph/`.
- O primeiro cluster modelado foi o host `AGT`, representado pelo host real `agt01`.
- Serviços incluídos no cluster AGT nesta rodada:
  - `zabbix-server`
  - `zabbix-agent2`
  - `grafana-server`
  - `apache2`
  - `cloudflared`
  - `cloudflared-livecopilot`
  - `postgresql@17-main`
  - `unbound`
  - `ssh`
  - `livecopilot-semantic-api`
  - `emby-server`
  - `smbd`
  - `nmbd`
  - `winbind`
  - `libvirtd`
- A cadeia de conectividade acima do host foi modelada de forma explícita com:
  - concentrador do link do host
  - sessão PPP
  - IP dedicado
  - gateway / next-hop
  - operadora / AS
  - nuvem / destino
- Foram criadas três representações do mesmo modelo:
  - `dependency-graph/clusters/agt.md`
  - `dependency-graph/models/agt_dependency_model.yaml`
  - `dependency-graph/views/agt_dependency_graph.mmd`
- A semântica dos nós e das relações foi documentada em `dependency-graph/SEMANTICS.md`.
- O modelo ainda é manual e hierárquico, sem descoberta automática e sem mexer no runtime do Zabbix/Grafana.
- Limitação atual: os nós de conectividade acima do host ainda usam nomes operacionais genéricos onde a documentação não confirmou o nome final.
- Próximo passo provável: refinar a cadeia de conectividade com nomes reais e expandir o grafo para novos clusters quando houver base confirmada.

## 2026-04-05 - refinamento operacional da cadeia AGT

- A cadeia acima do host `agt01` foi refinada com evidência local objetiva.
- Fatos confirmados nesta rodada:
  - interface de saída principal: `br0`
  - default route: `default via 10.45.0.1 dev br0 onlink`
  - gateway / next-hop: `10.45.0.1`
  - IP público de saída: `206.42.12.37`
  - operadora / AS: `AS28126 BRISANET SERVICOS DE TELECOMUNICACOES S.A`
- A consulta de conectividade não encontrou processo PPP ativo, então a sessão PPP permaneceu como hipótese pendente e foi marcada explicitamente como `pending_confirmation`.
- O nó genérico de IP foi substituído por um IP real observado.
- O nó genérico de gateway foi substituído por um gateway real observado.
- O nó de operadora / AS passou a carregar identidade real confirmada pelo egress público.
- O destino final continua genérico porque não houve confirmação operacional de um alvo único.
- O modelo agora carrega metadados úteis por nó:
  - `id`
  - `label`
  - `type`
  - `layer`
  - `criticality`
  - `depends_on`
  - `impact_scope`
  - `validation_source`
  - `confidence`
  - `notes`
- A documentação foi atualizada em:
  - `dependency-graph/SEMANTICS.md`
  - `dependency-graph/clusters/agt.md`
  - `dependency-graph/models/agt_dependency_model.yaml`
  - `dependency-graph/views/agt_dependency_graph.mmd`
- O grafo ficou mais útil para responder impacto de rota, quebra de acesso e distinção entre fato observado, inferência e pendência.
- Próximo passo natural:
  - confirmar se a sessão PPP existe de fato ou remover a hipótese
  - identificar um destino operacional real, se houver um alvo único
  - expandir a mesma semântica para outros clusters quando houver base local suficiente

## 2026-04-05 - rodada parcial de validação SNMP da MikroTik

- A frente `mikrotik-snmp/` foi iniciada para validar SNMP e levantar inventário bruto de OIDs úteis.
- O IP alvo usado na validação foi `10.45.0.6`, alinhado com os artefatos de integração do ambiente.
- A instalação do pacote `snmp` foi concluída no host para viabilizar `snmpwalk` e `snmpget`.
- A tentativa de reachability por `ping` para `10.45.0.6` falhou com perda total de pacotes.
- A tentativa de leitura SNMP v2c com community `public` em `sysDescr` retornou `Timeout: No Response`.
- Os primeiros walks dos blocos `1.3.6.1.2.1.1` e `1.3.6.1.2.1.2` também retornaram timeout.
- A rodada foi interrompida a pedido do usuário antes da varredura dos blocos `1.3.6.1.2.1.25` e `1.3.6.1.4.1.14988`.
- A validação ainda não confirmou SNMP operacional a partir do host do Zabbix; neste ponto o problema parece ser reachability ou community de leitura incorreta.
- Os artefatos brutos já gerados foram salvos em `mikrotik-snmp/discovery/`.

## 2026-04-05 - validação SNMP da MikroTik corrigindo o IP alvo

- O IP correto da MikroTik foi ajustado para `10.45.0.1`.
- A validação por `ping` para `10.45.0.1` respondeu com sucesso.
- A leitura SNMP v2c com community `public` respondeu com sucesso em `sysDescr.0`.
- `snmpwalk` dos blocos principais respondeu com dados reais e foi salvo nos arquivos de descoberta.
- O bloco `system` confirmou:
  - `sysDescr.0 = RouterOS RB3011UiAS`
  - `sysName.0 = MikroTik`
  - `sysObjectID.0 = .1.3.6.1.4.1.14988.1`
- O bloco `interfaces` confirmou a presença de:
  - `bridge`
  - `pppoe-out1`
  - `wg0`
  - `ether1` a `ether10`
- O bloco `host/resources` trouxe memória e armazenamento lógico.
- O bloco `enterprise MikroTik` trouxe:
  - versão de RouterOS
  - modelo da board
  - sensores de temperatura e voltagem
  - contadores e nomes de interfaces
- Foi criado o inventário inicial em:
  - `mikrotik-snmp/discovery/mikrotik_oid_inventory.md`
- Foi criada a nota de validação em:
  - `mikrotik-snmp/artifacts/snmp_validation.md`
- O próximo passo natural é transformar essa base em template Zabbix, mas isso ainda não foi feito nesta rodada.

## 2026-04-05 - template inicial SNMP da MikroTik criado

- Foi criado o template inicial em `mikrotik-snmp/template/mikrotik_snmp_template.yaml`.
- O template ficou baseado apenas em OIDs validados na rodada anterior.
- Escopo incluído no template:
  - identificação do equipamento
  - uptime
  - inventário de interfaces
  - estado operacional das interfaces
  - tráfego por interface
  - memória
  - board
  - versão do RouterOS
  - temperatura
  - voltagem
  - interfaces `pppoe-out1` e `wg0` como sinais úteis já observados
- A community padrão ficou parametrizada como `{$SNMP_COMMUNITY}` com default `public`.
- A frente continua sem importação para runtime do Zabbix nesta rodada.
- Próximo passo natural:
  - revisar os detalhes do template para importação manual ou automação posterior
  - ajustar itens/prototypes se você quiser separar interface discovery e sinais fixos

## 2026-04-05 - template Zabbix importável da MikroTik gerado

- Foi gerado o export XML importável em `mikrotik-snmp/template/mikrotik_snmp_template.zabbix.xml`.
- O XML ficou enxuto e focado no que foi validado:
  - `sysDescr`
  - `sysName`
  - `sysUpTime`
  - `ifNumber`
  - descoberta de interfaces
  - `ifDescr`
  - `ifOperStatus`
  - `ifInOctets`
  - `ifOutOctets`
  - memória
  - uptime de host resources
  - board
  - versão do RouterOS
  - temperatura
  - voltagem
  - `pppoe-out1`
  - `wg0`
- A exportação ainda não foi importada no runtime do Zabbix; ficou apenas versionada como artefato pronto para importação manual.
- O XML passou por validação estrutural local e o volume final ficou em `12` itens fixos e `4` protótipos de item de descoberta.

## 2026-04-05 - importação do template MikroTik no runtime do Zabbix

- O template `MikroTik SNMP` foi importado com sucesso no Zabbix local.
- O host `MikroTik RB3011` foi criado com hostid `10778`.
- O host recebeu a interface SNMP `10.45.0.1:161` com `SNMP v2c` e community `public`.
- O host foi associado ao template `MikroTik SNMP` com templateid `10777`.
- Itens principais com `latest data` real confirmado:
  - `SNMP system description` -> `RouterOS RB3011UiAS`
  - `SNMP system name` -> `MikroTik`
  - `SNMP uptime` -> `28918200`
  - `Interface count` -> `15`
  - `Memory size` -> `1048576`
  - `Host resources uptime` -> `28918200`
  - `Board name` -> `RB3011UiAS`
  - `RouterOS version` -> `7.21.1`
  - `Temperature` -> `31`
  - `Voltage` -> `240`
  - `PPPoE tunnel status` -> `1`
  - `WireGuard tunnel status` -> `1`
- A descoberta de interfaces não fechou nesta rodada: o item `mikrotik.if.discovery` ficou `unsupported` com erro de OID SNMP inválido no formato esperado pelo Zabbix.
- A validação foi registrada em `mikrotik-snmp/artifacts/zabbix_template_import_validation.md`.
- A base principal já está coletando; a correção fina da LLD fica como próxima rodada separada para não inflar o escopo.

## 2026-04-05 - ajuste tentado na descoberta de interfaces da MikroTik

- A regra `mikrotik.if.discovery` foi revisada para tentar gerar LLD de interfaces no Zabbix.
- O host e os itens fixos continuaram válidos com `latest data` real.
- A descoberta de interfaces permaneceu `unsupported` com o mesmo erro de parsing de OID SNMP.
- O Zabbix continuou exigindo `pairs of macro and OID are expected` na regra de descoberta, então a LLD segue como pendência técnica isolada.
- A decisão desta rodada foi manter a coleta principal em produção e não expandir mais a estrutura da LLD até uma correção específica do formato suportado pela versão local do Zabbix.

- cards `stat` do dashboard principal voltaram para altura `2`
- o valor voltou a ter mais protagonismo do que o título
- a organização visual anterior foi preservada
- queries, thresholds, cores e itens permaneceram inalterados
- documentação desta rodada foi registrada nos artefatos do projeto

## Rodada de saúde do host

- descoberta local concluída para CPU e memória nativas do template Linux by Zabbix agent
- `system.cpu.util` segue coletando como CPU usage
- `vm.memory.size[pavailable]` segue coletando como base operacional de RAM no host
- a fonte local de temperatura foi validada via `lm-sensors` em `nct6776-isa-0290` / `temp2`
- a key final do item passou a ser `cpu.temp`
- o agent2 recebeu `UserParameter=cpu.temp` apontando para `/sys/class/hwmon/hwmon1/temp2_input`
- o item `CPU temperature` foi convertido para coleta operacional no Zabbix e recebeu `lastvalue` real
- o painel `CPU Temp` do Grafana foi validado como apontando para o item final `CPU temperature` / `cpu.temp`
- dashboard principal do Grafana permaneceu sem alterações nesta rodada

## 2026-04-05 - análise do template oficial MikroTik

- foi criada a análise de lacuna do template oficial `Mikrotik by SNMP` contra a nossa base validada
- o template oficial cobre `ICMP Ping`, `ICMP Packet Loss`, `ICMP Latency`, `SNMP Availability`, `Identity`, `Model`, `Firmware`, `Temperature`, `Voltage`, `Memory` e LLD de `CPU` e `Interfaces`
- a nossa base já valida `sysDescr`, `sysName`, `sysUpTime`, `ifNumber`, memória, board, versão do RouterOS, temperatura, voltagem e túneis observados
- a principal pendência técnica identificada foi alinhar a LLD de interfaces ao formato oficial aceito pelo Zabbix local
- o próximo passo útil é fechar apenas o gap funcional, sem inflar o template com descoberta desnecessária

## 2026-04-05 - ajuste tentado na LLD de interfaces MikroTik

- a regra `mikrotik.if.discovery` foi simplificada para um único par macro/OID: `discovery[{#SNMPINDEX},1.3.6.1.2.1.2.2.1.1]`
- o template foi reimportado com sucesso no Zabbix local
- mesmo após `config_cache_reload`, o host `MikroTik RB3011` continua com a regra em estado `unsupported`
- o erro atual permanece `Invalid SNMP OID: pairs of macro and OID are expected`
- a coleta fixa principal continua funcionando; a LLD de interfaces segue como bloqueio isolado para a próxima correção

## 2026-04-05 - LLD de interfaces MikroTik corrigida

- a descoberta de interfaces foi migrada de `SNMP LLD` direta para o padrão compatível com a instância local: item mestre `walk[]` + descoberta `DEPENDENT` com `SNMP_WALK_TO_JSON`
- os protótipos de item também passaram a ser `DEPENDENT`, usando `SNMP_WALK_VALUE` sobre o mesmo walk bruto
- o host `MikroTik RB3011` saiu do estado `unsupported` na regra `mikrotik.if.discovery`
- a LLD gerou itens reais para interfaces como `bridge`, `ether1`, `pppoe-out1` e `wg0`
- latest data validado após a correção:
  - `pppoe-out1 operational status` = `1`
  - `wg0 operational status` = `1`
  - `ether1 inbound traffic` = `1490222658`
  - `ether1 outbound traffic` = `540053278`
- o `delay` do item mestre foi devolvido para `1m` após a validação inicial
