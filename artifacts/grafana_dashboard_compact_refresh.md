# Grafana dashboard compact refresh

Data: `2026-04-04`

## Estado inicial

- dashboard já estava funcional e com dados reais
- os cards ainda ocupavam mais altura do que o necessário
- o bloco `Emby` ainda aparecia na grade principal

## Ajuste aplicado

- painel `Emby` removido do layout principal
- altura dos cards reduzida de `4` para `3`
- linha de diagnóstico reaproveitada em três blocos mais largos
- `Resumo`, `Problemas`, `Web Público` e `DNS Público` mantidos no topo
- serviços críticos mantidos no miolo do painel

## Efeito visual

- menor peso visual por card
- leitura mais viva e mais compacta
- menos espaço morto entre blocos
- dashboard continua legível sem rolagem na visão padrão

## Hierarquia operacional

- verde para saúde
- amarelo/laranja para atenção ou diagnóstico
- vermelho para falha
- azul/ciano para informação estrutural quando útil

## Evidência técnica

- dashboard uid: `observabilidade-grafana`
- título: `Observabilidade Zabbix - Grafana`
- painel count: `15`
- altura dos cards principais: `3`
- painel `Emby` não consta mais na lista de painéis
- `Grafana Local`, `Zabbix Frontend` e `localhost-a` permanecem como linha de diagnóstico
