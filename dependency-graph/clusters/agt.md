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
- equipamento de borda validado: `MikroTik RB3011`
- IP de gestão SNMP validado: `10.45.0.1`
- RouterOS / board validados: `7.21.1` / `RB3011UiAS`

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
- bridge `bridge` da `MikroTik RB3011`
- next-hop `10.45.0.1`
- IP público `206.42.12.37`
- sessão WAN `pppoe-out1`
- uplink físico `ether1`
- equipamento de borda `MikroTik RB3011`
- túnel / overlay observado `wg0`
- operadora / AS `AS28126 BRISANET`
- nuvem / destino

## Relações de dependência

- os serviços dependem do host `agt01`
- o host depende da conectividade local via `br0`
- `br0` depende do domínio L2 observado como `bridge` na `MikroTik RB3011`
- o next-hop `10.45.0.1` é servido pela `MikroTik RB3011`, que deixou de ser abstração genérica
- a leitura do grafo é causal, não uma reprodução literal da ordem de encaminhamento de pacotes na RB3011
- `pppoe-out1` foi mantida como sessão WAN principal observada no runtime do Zabbix
- `ether1` foi registrada como uplink físico observado que sustenta a sessão WAN
- `wg0` foi registrada apenas como túnel / overlay observado, fora da cadeia causal principal do AGT
- o IP público observado depende da sessão `pppoe-out1`
- o IP público observado aponta para a operadora `AS28126 BRISANET`
- a operadora / AS sustenta o alcance até a nuvem / destino

## Leitura conceitual de impacto

- se o host `agt01` cair, os serviços do cluster perdem execução local
- se `br0`, a `bridge` da MikroTik ou o next-hop `10.45.0.1` falharem, o host perde a borda imediata de saída
- se `pppoe-out1` ou `ether1` degradarem, a saída principal do AGT para fora do segmento local pode falhar mesmo com o host saudável
- se a `MikroTik RB3011` cair, o AGT perde a borda concreta acima do host e toda a cadeia superior fica comprometida
- se a operadora / AS degradar, o host pode ficar isolado mesmo com serviço local saudável
- se a nuvem / destino tiver problema de rota, os serviços podem parecer indisponíveis para consumo externo

## Observação

- nomes reais foram usados onde havia evidência objetiva local
- a `MikroTik RB3011` entrou como entidade operacional concreta, com `bridge`, `ether1`, `pppoe-out1` e `wg0` derivados da descoberta validada
- `pppoe-out1` foi tratada como WAN principal compatível com a evidência já validada, sem afirmar causalidade além do egress principal
- `wg0` continua apenas como interface de túnel observada, sem ser tratada como requisito da conectividade principal do AGT
- o destino final continua genérico porque a confirmação operacional ainda não existe
- esta versão não faz descoberta automática nem tenta inferir dependências ocultas
