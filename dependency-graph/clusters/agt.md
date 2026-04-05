# Cluster AGT

## Escopo

Cluster inicial do grafo de dependências operacionais do host `AGT`.

O cluster está organizado da borda de serviço para cima, com o host no centro da leitura.

## Host principal

- `agt01`

## Serviços ligados ao host

### Serviços de observabilidade

- `zabbix-server`
- `zabbix-agent2`
- `grafana-server`

### Serviços de publicação

- `apache2`
- `cloudflared`
- `cloudflared-livecopilot`

### Serviços de infraestrutura local

- `postgresql@17-main`
- `unbound`
- `ssh`

### Serviços de aplicação

- `livecopilot-semantic-api`
- `emby-server`
- `smbd`
- `nmbd`
- `winbind`
- `libvirtd`

## Cadeia de conectividade acima do host

- concentrador do link do host
- sessão PPP
- IP dedicado
- gateway / next-hop
- operadora / AS
- nuvem / destino

## Relações de dependência

- os serviços dependem do host `agt01`
- o host depende da conectividade local e da rota até o provedor
- a conectividade local depende da sessão PPP
- a sessão PPP depende do IP dedicado e do gateway / next-hop
- o IP dedicado e o gateway dependem da operadora / AS
- a operadora / AS suporta o alcance até a nuvem / destino

## Leitura conceitual de impacto

- se o host `agt01` cair, os serviços do cluster perdem execução local
- se a sessão PPP cair, a rota de saída do host deixa de existir
- se a operadora / AS degradar, o host pode ficar isolado mesmo com serviço local saudável
- se a nuvem / destino tiver problema de rota, os serviços podem parecer indisponíveis para consumo externo

## Observação

- nomes genéricos foram mantidos onde a documentação atual ainda não confirmou o nome operacional final
- esta versão não faz descoberta automática nem tenta inferir dependências ocultas
