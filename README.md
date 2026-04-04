# Observabilidade Zabbix

Frente de trabalho para monitoramento com Zabbix cobrindo:

- status de serviços `systemd`
- disponibilidade de páginas HTTP/HTTPS
- resolução DNS

Este diretório é a base isolada da frente. A ideia é manter tudo reproduzível por arquivos, scripts e artefatos, evitando dependência de ajuste manual solto na UI.

## Diagnóstico resumido

- Apache `2.4.66` está instalado e ativo no host
- Não há serviços `zabbix*` ativos no ambiente no momento do diagnóstico
- Não foram encontrados arquivos usuais de configuração do Zabbix em `/etc`, `/opt` ou `/usr/local`
- Pacotes `zabbix-server-pgsql`, `zabbix-server-mysql`, `zabbix-frontend-php` e `zabbix-agent2` não estão instalados
- O host já expõe DNS local via `unbound` em `127.0.0.1:53` e `10.45.0.3:53`

Conclusão inicial:

- não existe stack Zabbix funcional local para reaproveitar
- a frente segue com plano de implantação e artefatos editáveis
- a aplicação segura depende de informar credenciais/API do Zabbix ou de instalar a stack mínima fora desta rodada

## Estrutura

- `config/`: inventários editáveis de serviços, URLs e checagens DNS
- `scripts/`: coleta de ambiente, validação e geração de plano
- `docs/`: blueprint do dashboard e guia de aplicação
- `examples/`: exemplos de referência
- `artifacts/`: saídas geradas pelo diagnóstico e validação

## Versionamento

- a fonte versionável deve ficar em `README.md`, `STATUS.md`, `config/`, `scripts/`, `docs/` e `examples/`
- artefatos operacionais e evidências sensíveis ficam em `artifacts/` e não devem ser publicados por padrão
- segredos locais, backups e arquivos de runtime devem ser mantidos fora do git

## Como preencher os inventários

### `config/services.yaml`

Liste os serviços `systemd` que devem ser monitorados. O arquivo já vem com exemplos e o script de coleta marca quais existem de fato no host.

Campos esperados:

- `name`: nome legível do serviço
- `unit`: unidade `systemd`
- `enabled`: se o serviço deve entrar no escopo
- `severity`: severidade base

### `config/web_checks.yaml`

Liste URLs HTTP/HTTPS para checagem de disponibilidade.

Campos esperados:

- `name`
- `url`
- `expected_status`
- `timeout`
- `follow_redirects`
- `expected_string` opcional

### `config/dns_checks.yaml`

Liste domínios e registros para validação de resolução.

Campos esperados:

- `name`
- `domain`
- `server` opcional
- `record_type`
- `expected_value` opcional
- `timeout`

## Como validar

Execute:

```bash
./scripts/validate_configs.sh
```

O script valida a sintaxe dos YAMLs, checa se `shellcheck` existe e valida os inventários gerados em `artifacts/`.

## Como aplicar

Se existir Zabbix funcional e credenciais/API disponíveis:

```bash
./scripts/apply_or_generate_zabbix_plan.sh
```

Sem API/credenciais, o script gera um plano objetivo em `artifacts/zabbix_plan.md` com os passos para aplicar no Zabbix existente.

## Serviços systemd

O monitoramento de serviços deve priorizar Zabbix Agent 2 com checagens baseadas em `systemd`.

Exemplos já previstos:

- `apache2`
- `nginx`
- `postfix`
- `dovecot`
- `zabbix-agent2`

Se o serviço não existir no host, ele permanece como exemplo e não deve ser forçado.

## Web checks

Os checks web devem ser transformados em web scenarios no Zabbix.

Fluxo previsto:

1. preencher `config/web_checks.yaml`
2. validar com `scripts/validate_configs.sh`
3. gerar ou aplicar o plano com `scripts/apply_or_generate_zabbix_plan.sh`

## DNS checks

Os checks DNS devem usar a capacidade do Zabbix Agent 2 ou items nativos equivalentes do Zabbix, sem gambiarra desnecessária.

Critérios previstos:

- resolução bem-sucedida
- tempo de resposta
- divergência de valor esperado, quando configurado

## Dashboard e alertas

Veja:

- `docs/dashboard_blueprint.md`
- `docs/aplicacao_zabbix.md`

## Estado atual

Consulte `STATUS.md` para diagnóstico, decisões, pendências e riscos.
