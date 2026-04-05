# Dependency Graph

Esta frente documenta o grafo inicial de dependências operacionais do ambiente.

## Objetivo

- representar dependências por cluster, começando por `AGT` e `MikroTik RB3011`
- separar serviços do host, serviços de aplicação, serviços de observabilidade e serviços de publicação
- modelar a cadeia de conectividade acima do host com nós explícitos e legíveis
- explicitar dependências entre clusters quando a borda de um ambiente estiver modelada separadamente
- deixar a base pronta para inferência, impacto e expansão futura sem automatização pesada nesta rodada

## Estrutura

- `clusters/`: leitura humana por cluster
- `models/`: modelo estruturado para automação futura
- `views/`: diagrama versionável do mesmo modelo
- `SEMANTICS.md`: semântica de nós, arestas e estados
- `IMPACT_RULES.md`: regras documentais de impacto direto e propagado

## Modelo inicial

### Cluster inicial

- `AGT`
- `MikroTik RB3011`

### Camadas usadas

1. serviço
2. host
3. acesso / conectividade
4. borda / rede do provedor
5. destino / nuvem

### Leitura operacional

- os serviços apontam para o host
- o host aponta para a cadeia de conectividade que o sustenta ou para um cluster externo já modelado
- a cadeia sobe até o destino percebido como alcançável
- o modelo é explícito, hierárquico e ainda não tenta descobrir tudo automaticamente
- ligações entre clusters são documentais e servem para separar responsabilidade de host versus borda

## Fontes de base usadas nesta rodada

- `STATUS.md`
- `config/services.yaml`
- `/lab/projects/livecopilot/docs/ARCHITECTURE_CURRENT.md`
- `artifacts/monitoring_scope_recommendation.md`
- `artifacts/livecopilot_monitoring_integration.md`

## Uso futuro

- cálculo de impacto por queda de host
- cálculo de impacto entre clusters conectados
- propagação de indisponibilidade por quebra de conectividade
- marcação de nós inferidos versus nós confirmados
- expansão para novos clusters quando houver base suficiente
