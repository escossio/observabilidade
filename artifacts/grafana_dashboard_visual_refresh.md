# Grafana dashboard visual refresh

Data: `2026-04-04`

## Estado inicial

- dashboard principal existia e já consumia dados reais do Zabbix
- a distribuição anterior deixava espaços mortos e leitura pouco hierarquizada
- a visualização padrão ainda dependia de melhor aproveitamento da largura da tela

## Ajuste aplicado

- dashboard reorganizado em grade `4x4`
- linha superior reservada para `Resumo`, `Problemas`, `Web Público` e `DNS Público`
- linhas centrais reservadas para os serviços críticos da baseline operacional
- linha inferior reservada para segunda linha e diagnóstico local
- títulos encurtados para leitura mais rápida em monitor grande ou TV

## Hierarquia visual

- verde para estado saudável
- amarelo/laranja para atenção, diagnóstico ou segunda linha
- vermelho para falha
- azul/ciano para informação estrutural quando útil

## Resultado validado

- o dashboard principal abre sem exigir rolagem na visualização padrão
- os painéis principais ficaram acima da dobra
- a largura da tela passou a ser usada de forma equilibrada
- `example.com` não aparece mais como painel principal
- o painel de serviço principal destaca `grafana-server`

## Evidência técnica

- dashboard uid: `observabilidade-grafana`
- título: `Observabilidade Zabbix - Grafana`
- painel count: `16`
- painel principal de linha de serviços: `Service grafana-server running`
- painéis de diagnóstico preservados: `Grafana Local`, `Zabbix Frontend`, `localhost-a`, `Emby`
