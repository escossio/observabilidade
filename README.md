# Observabilidade Zabbix

Repositório da frente de observabilidade que usa **Zabbix como backend de coleta, itens, triggers e alertas** e **Grafana como camada principal de visualização**.

O objetivo é manter a operação reproduzível por arquivos, scripts e documentação, sem depender de ajuste manual solto na interface.

## Visão geral

Esta frente monitora:

- serviços `systemd`
- páginas HTTP/HTTPS
- resolução DNS

A arquitetura está separada em duas camadas:

- **Zabbix** coleta dados, mantém itens, dispara triggers e concentra alertas
- **Grafana** consome os dados do Zabbix para exibição operacional e painéis de uso diário

## Arquitetura operacional

O fluxo do projeto é:

1. os inventários em `config/` definem o que deve ser monitorado
2. os scripts em `scripts/` validam os arquivos e geram plano ou evidência
3. o Zabbix recebe os itens, triggers e alertas
4. o Grafana lê o backend do Zabbix para o painel principal
5. os artefatos em `artifacts/` registram diagnóstico, validação e decisões

O repositório versiona a parte **estrutural e documental** da frente.

Não entram no versionamento por padrão:

- segredos e credenciais locais
- runtime do ambiente
- backups
- artefatos descartáveis ou sensíveis
- inventários brutos de coleta

## Estrutura do repositório

### `config/`

Inventários editáveis da frente.

- `services.yaml`: serviços `systemd` monitorados
- `web_checks.yaml`: URLs e verificações HTTP
- `dns_checks.yaml`: domínios e registros DNS

### `docs/`

Documentação operacional da frente.

- `aplicacao_zabbix.md`: referência de aplicação da frente no Zabbix
- `dashboard_blueprint.md`: blueprint do painel operacional

### `examples/`

Exemplos de referência para manter o formato esperado dos inventários.

### `scripts/`

Automação pequena e reproduzível para:

- coletar inventário do host
- validar os YAMLs
- gerar plano de aplicação
- renderizar exemplos

### `artifacts/`

Saídas geradas durante diagnóstico, validação e integração.

- relatórios de ambiente
- evidências de Zabbix
- evidências de Grafana
- relatório de preparação do git

### `README.md`

Visão geral da frente e ponto de entrada do repositório.

### `STATUS.md`

Estado operacional atual, decisões tomadas, riscos e pendências.

## Como o projeto está organizado

O repositório foi montado para separar claramente:

- **fonte versionável**: documentação, configurações sanitizadas, scripts e exemplos
- **artefatos operacionais**: relatórios e evidências geradas
- **segredos locais**: credenciais, arquivos de runtime e backups

Isso permite evoluir a frente sem misturar:

- configuração limpa
- documentação de uso
- evidência operacional
- segredos

## Fluxo operacional

### 1. Definir o que monitorar

Atualize os arquivos em `config/`.

### 2. Validar a estrutura

Execute:

```bash
./scripts/validate_configs.sh
```

### 3. Gerar ou aplicar o plano

Execute:

```bash
./scripts/apply_or_generate_zabbix_plan.sh
```

### 4. Manter documentação e evidência

Os resultados ficam em `artifacts/` e o estado consolidado em `STATUS.md`.

## Estado atual

- Zabbix local instalado e funcional
- Grafana instalado e integrado ao Zabbix
- host monitorado: `agt01`
- itens criados para serviços, web e DNS
- triggers criadas para serviço, web e DNS
- dashboard do Zabbix preenchido
- dashboard principal do Grafana criado
- credencial padrão do Zabbix removida da operação

Consulte `STATUS.md` para o fechamento mais recente.

## Segurança

- não versionar credenciais
- não versionar backups
- não versionar runtime local
- não versionar artefatos brutos descartáveis

## Próximos passos

- refinar a visualização dos checks textuais no Grafana
- manter `config/` como fonte única dos checks
- preservar a separação entre documentação, artefatos e segredos

