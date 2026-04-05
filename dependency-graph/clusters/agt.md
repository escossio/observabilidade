# Cluster AGT

## Escopo

Cluster inicial do grafo de dependências operacionais do host `AGT`.

O cluster está organizado da borda de serviço para cima, com o host no centro da leitura.

## Host principal

- `agt01`
- interface de saída observada: `br0`
- gateway padrão observado: `10.45.0.1`
- IP público de saída observado: `206.42.12.37`
- operadora observada pelo egress: `AS28126 BRISANET SERVICOS DE TELECOMUNICACOES S.A`

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

- bridge `br0`
- sessão PPP
- IP público `206.42.12.37`
- gateway `10.45.0.1`
- operadora / AS `AS28126 BRISANET`
- nuvem / destino

## Relações de dependência

- os serviços dependem do host `agt01`
- o host depende da conectividade local via `br0`
- a conectividade local observada depende da rota padrão até `10.45.0.1`
- a cadeia acima do host ainda mantém a sessão PPP como hipótese pendente
- o IP público observado depende do caminho de saída via `br0`
- o gateway observado aponta para a operadora `AS28126 BRISANET`
- a operadora / AS sustenta o alcance até a nuvem / destino

## Leitura conceitual de impacto

- se o host `agt01` cair, os serviços do cluster perdem execução local
- se `br0` ou a rota padrão caírem, o host perde saída e a cadeia superior deixa de sustentar o tráfego
- se a sessão PPP existir de fato e cair, a leitura operacional deve tratar isso como quebra da camada de acesso até confirmação adicional
- se a operadora / AS degradar, o host pode ficar isolado mesmo com serviço local saudável
- se a nuvem / destino tiver problema de rota, os serviços podem parecer indisponíveis para consumo externo

## Observação

- nomes reais foram usados onde havia evidência objetiva local
- a sessão PPP permanece genérica porque não houve processo PPP ativo nem evidência local suficiente para nomeação final
- o destino final continua genérico porque a confirmação operacional ainda não existe
- esta versão não faz descoberta automática nem tenta inferir dependências ocultas
