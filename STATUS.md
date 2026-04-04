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
- `emby-server` está monitorado e atualmente reporta 0 processos

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
- credencial padrão `Admin/zabbix` removida da operação
- evidências objetivas salvas em `artifacts/`
- preparação do git concluída com separação entre fonte versionável, artefatos e segredos locais
- `shellcheck` não está instalado no host, então a validação de shell ficou limitada à execução dos scripts
