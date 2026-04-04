# Status

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
