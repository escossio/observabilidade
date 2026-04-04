# GitHub repository presentation

## Descrição curta recomendada

Observabilidade com Zabbix como backend de coleta e Grafana como painel principal.

## Descrição expandida recomendada

Repositório da frente de observabilidade que organiza inventários, scripts, documentação e evidências para monitoramento com Zabbix no backend e Grafana na camada de visualização.

## Estrutura resumida

- `config/`: inventários editáveis de serviços, web e DNS
- `docs/`: blueprint e instruções operacionais
- `examples/`: exemplos de referência
- `scripts/`: validação e automação pequena
- `artifacts/`: relatórios e evidências geradas
- `README.md`: visão geral
- `STATUS.md`: estado atual

## Tags sugeridas

- `observability`
- `zabbix`
- `grafana`
- `monitoring`
- `postgresql`
- `automation`
- `infrastructure`

## Fora do versionamento

- credenciais e segredos locais
- runtime do ambiente
- backups
- artefatos descartáveis ou sensíveis
- inventários brutos de coleta

## Nota operacional

- o repositório está estruturado para ser publicado sem expor senha, token ou arquivo local de credencial
