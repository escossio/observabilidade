# Aplicação no Zabbix

## Cenário 1: Zabbix já existente

1. instalar ou confirmar `zabbix-agent2` no host monitorado
2. importar o inventário de serviços, web e DNS a partir de `config/`
3. criar host ou atualizar host existente sem recriar a stack
4. configurar templates, itens, triggers e web scenarios
5. validar por um serviço, uma URL e um domínio DNS reais
6. se a API central não responder, registrar o bloqueio em `STATUS.md` sem simular aplicação

## Cenário 2: sem API ou credenciais

1. usar `artifacts/zabbix_plan.md`
2. aplicar manualmente os passos no frontend do Zabbix
3. manter a configuração fonte em arquivos do projeto
4. reutilizar os alvos reais já validados neste host:
   - serviço: `apache2`, `unbound`, `emby-server`
   - web: `http://127.0.0.1/` e `http://127.0.0.1:8080/`
   - DNS: `example.com` via `127.0.0.1`

## Livecopilot por camada

Quando o objetivo for distinguir borda, frontend e backend do Livecopilot, usar os alvos abaixo:

- serviço: `livecopilot-semantic-api.service`
- borda Apache: `http://127.0.0.1:8080/`
- frontend público: `http://livecopilot.escossio.dev.br/`
- health público: `http://livecopilot.escossio.dev.br/health`
- health backend: `http://127.0.0.1:8099/health`
- status operacional: `http://127.0.0.1:8099/status`
- API operacional: `http://127.0.0.1:8099/api/panel/summary`

Base mínima de triggers:

- serviço parado
- borda indisponível
- frontend público indisponível
- health backend indisponível
- rota operacional indisponível

## Serviços systemd

Base mínima de triggers:

- serviço parado
- serviço não iniciado após reboot
- serviço em falha repetida, se disponível via item do agente

## Web

Base mínima de triggers:

- página indisponível
- resposta fora do código esperado
- resposta lenta acima do limite definido
- string esperada ausente, quando configurada

## DNS

Base mínima de triggers:

- domínio não resolve
- resolução acima do timeout
- resposta diferente do valor esperado, quando definido

## Revisão

Depois de aplicar, revisar:

- latest data do host
- protótipos de item
- triggers por severidade
- dashboard com os três blocos
