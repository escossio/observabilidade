# Blueprint de dashboard

## Bloco de serviços

- status por serviço `systemd`
- contagem de serviços ativos, parados e em manutenção
- destaque para falhas do `apache2`, `unbound` e `emby-server`

## Bloco de páginas

- disponibilidade HTTP/HTTPS por URL
- tempo de resposta
- página lenta versus página indisponível
- foco nos checks reais `http://127.0.0.1/` e `http://127.0.0.1:8080/`

## Bloco de DNS

- resolução por domínio
- tempo de resolução
- divergência entre valor esperado e valor resolvido
- foco no check `example.com` resolvido por `127.0.0.1`

## Resumo geral

- total de checks OK
- total em warning
- total em problema
- total em desconhecido

## Aplicação

Se houver API do Zabbix disponível, este blueprint deve virar dashboard via automação. Caso contrário, use este documento como referência para criação manual controlada, sempre a partir dos arquivos `config/`.

## Estado real desta rodada

- a instância Zabbix central em `10.45.0.6` não respondeu desta frente
- os arquivos canônicos de env/toolbelt esperados em `/srv/aiops/env/` não existem neste host
- o blueprint permanece como referência de aplicação manual até a central ficar acessível a partir desta máquina
