# Grafana dashboard created

- dashboard uid: `observabilidade-grafana`
- title: `Observabilidade Zabbix - Grafana`
- URL: `http://127.0.0.1:3000/d/observabilidade-grafana/observabilidade-zabbix-grafana`
- panel count: `18`

## Painéis

- `Resumo` - `stat`
- `Problemas` - `table` (`Zabbix Problems`)
- `Web Público` - `table` (`Zabbix Problems`)
- `DNS Público` - `table` (`Zabbix Problems`)
- `Zabbix Server` - `stat`
- `Agent2` - `stat`
- `Apache2` - `stat`
- `Grafana` - `stat`
- `Cloudflared` - `stat`
- `Unbound` - `stat`
- `PostgreSQL` - `stat`
- `SSH` - `stat`
- `Grafana Local` - `URL`
- `Zabbix Frontend` - `URL`
- `localhost-a` - `stat`
- `CPU` - `stat`
- `RAM` - `stat`
- `CPU Temp` - `stat`

## Validação

- o dashboard foi salvo com sucesso no Grafana
- o datasource Zabbix está associado ao dashboard
- os painéis de serviço usam itens reais do Zabbix com filtro pelo nome do item
- os painéis principais ficaram acima da dobra na grade 4x4
- os cards foram compactados para altura menor e linha de diagnóstico reaproveitada
- os painéis de web e DNS foram rebatizados para a baseline atual
- `example.com` deixou de aparecer como painel principal
- a rodada de saúde do host adicionou uma nova linha com `CPU`, `RAM` e `CPU Temp`
- a visualização padrão não exige rolagem para ver o conjunto principal
- `Emby` foi removido do layout principal
- a semântica operacional foi refinada nesta rodada sem alterar a grade principal
- `RAM` passou a representar `Memória disponível`
- painéis de serviço remanescentes passaram a exibir `Up/Down` em vez de valor cru
- `localhost-a` foi rebaixado para leitura diagnóstica
- `CPU Temp` recebeu threshold e unidade de temperatura coerentes
- `CPU Temp` passou a usar `itemid 69621` no modo `Item ID` do datasource

## Rodada de saúde do host

- o dashboard principal do Grafana foi expandido com `CPU`, `RAM` e `CPU Temp`
- o painel `CPU Temp` referencia o item `CPU temperature` do Zabbix
- o painel usa a key final `cpu.temp` no backend
- a validação final de consistência entre Zabbix e Grafana foi concluída nesta rodada

## Rodada semântica

- `RAM` foi rebatizada para `Memória disponível` para refletir corretamente a métrica `vm.memory.size[pavailable]`
- os cards `Apache2`, `PostgreSQL` e `Zabbix Frontend` passaram a usar leitura operacional `Up/Down`
- `localhost-a` deixou de competir visualmente com os painéis críticos
- `CPU Temp` permaneceu ligado ao item `CPU temperature` / `cpu.temp` e teve sua apresentação mantida como dado operacional de temperatura

## Rodada de query do CPU Temp

- o painel `CPU Temp` deixou o modo `Metrics` e passou a usar o modo `Item ID`
- a query foi ancorada no `itemid 69621` para evitar o `frames: 0` observado no filtro por nome
- o valor retornado pelo datasource voltou a ser exposto no dashboard

## Rodada de refinamento visual

- `Zabbix Server` foi encurtado para `Zabbix`
- `Apache2` foi encurtado para `Apache`
- `Memória disponível` foi encurtada para `Memória Livre`
- `localhost-a` foi rebatizado para `DNS Local`
- `CPU Temp` foi rebatizado para `Temperatura CPU`
- a altura dos cards stat foi reduzida para `1`
- o topo com `Resumo`, `Problemas`, `Web Público` e `DNS Público` foi preservado
- as queries e thresholds permaneceram intactos
