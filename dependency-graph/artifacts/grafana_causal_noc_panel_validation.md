# Grafana causal/NOC panel validation

## Objetivo

Adicionar ao dashboard principal do Grafana um bloco compacto com a leitura causal/NOC já validada pela CLI `noc_shift_summary`.

## Estratégia escolhida

- caminho mínimo: painel nativo `text` em Markdown
- reaproveitamento do datasource existente: `alexanderzobnin-zabbix-datasource` continua intacto para os painéis atuais
- sem plugin novo
- sem serviço contínuo novo
- sem reestruturação do dashboard

## Por que esse caminho

- o `noc_shift_summary` já estava validado localmente com dados reais do runtime do Zabbix
- a leitura causal é agregada e curta, então um painel textual compacto é suficiente nesta rodada
- isso evita criar uma nova camada de ingestão só para expor sete campos estáveis

## Dashboard alterado

- título: `Observabilidade Zabbix - Grafana`
- uid: `observabilidade-grafana`
- versão antes: `24`
- versão depois: `25`
- URL: `https://observabilidade.escossio.dev.br/d/observabilidade-grafana/observabilidade-zabbix-grafana`

## Bloco adicionado

- título do painel: `Leitura Causal / NOC`
- tipo: `text`
- posição: `x=0, y=20, w=24, h=4`
- foco: leitura operacional rápida sem mexer nos cards existentes

## Campos exibidos

- Eventos no período: `6`
- Explicados: `6`
- Sem binding: `0`
- Eventos abertos: `0`
- Semântica dominante: `service_failure`
- Cluster dominante: `AGT`
- Host dominante: `agt01`
- leitura operacional complementar: sem evidência de problema público ou WAN principal nesta rodada validada

## Evidência técnica

- dashboard regravado com sucesso via `POST /api/dashboards/db`
- resposta da API do Grafana confirmou `status=success`
- versão do dashboard incrementada para `25`
- o JSON do dashboard passou a conter o novo painel sem alterar os anteriores

## O que foi evitado

- não foi criado plugin novo
- não foi criado exporter contínuo
- não foi alterado o datasource principal dos painéis existentes
- não foi mexido no layout superior já estável

## Limitações

- a leitura exibida é um snapshot da rodada validada do `noc_shift_summary`
- os valores não são calculados ao vivo pelo Grafana nesta primeira versão
- se o runtime do Zabbix mudar, o painel precisa ser regravado para refletir a nova rodada

## Próximo passo natural

- automatizar a atualização desse bloco a partir de uma nova execução validada do `noc_shift_summary`, se a operação quiser o valor sempre sincronizado
