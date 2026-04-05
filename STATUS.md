# Status

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
