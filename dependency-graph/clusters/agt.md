# Cluster AGT

## Escopo

Cluster inicial do grafo de dependências operacionais do host `AGT`.

O cluster está organizado da borda de serviço para cima, com o host no centro da leitura.

## Host principal

- `agt01`
- interface de saída observada: `br0`
- borda externa dependente: cluster `MikroTik RB3011`
- ligação intercluster principal: `br0 -> cluster MikroTik RB3011`

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
- dependência explícita do cluster `MikroTik RB3011`
- cadeia superior delegada ao cluster dedicado da MikroTik:
  - `bridge`
  - `next-hop 10.45.0.1`
  - `ether1`
  - `pppoe-out1`
  - `206.42.12.37`
  - `AS28126 BRISANET`
  - `nuvem / destino`

## Relações de dependência

- os serviços dependem do host `agt01`
- o host depende da conectividade local via `br0`
- `br0` depende do cluster dedicado `MikroTik RB3011`
- a cadeia externa do AGT deixou de ficar embutida neste cluster e passou a ser mantida no cluster da borda
- a leitura intercluster continua causal e documental, sem tentar reproduzir forwarding interno

## Leitura conceitual de impacto

- se o host `agt01` cair, os serviços do cluster perdem execução local
- se `br0` falhar, o host perde a ligação local com a borda
- se o cluster `MikroTik RB3011` falhar, o AGT perde a borda concreta acima do host mesmo com o host ainda saudável
- falhas de operadora, IP público ou WAN principal agora são lidas no cluster dedicado da MikroTik, não mais dentro do AGT

## Observação

- nomes reais foram usados onde havia evidência objetiva local
- a borda MikroTik foi separada para um cluster próprio para evitar duplicação estrutural
- o cluster AGT mantém apenas o que pertence ao host e a sua ligação imediata com a borda
- o destino final continua genérico porque a confirmação operacional ainda não existe e agora fica documentado no cluster da MikroTik
- esta versão não faz descoberta automática nem tenta inferir dependências ocultas
