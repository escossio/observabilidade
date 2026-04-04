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
