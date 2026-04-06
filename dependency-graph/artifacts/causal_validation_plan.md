# Causal Validation Plan

## Objetivo

Validar a camada mínima de correlação causal com cenários curtos, reversíveis e de baixo risco.

## Cenários escolhidos

### Cenário A - Apache2 parado

- pré-condição: Apache2 ativo e monitorado pelo Zabbix
- risco: baixo
- rollback: `systemctl start apache2`
- expectativa causal: `service_failure` em `svc-apache2`

### Cenário B - unbound parado

- pré-condição: unbound ativo e monitorado pelo Zabbix
- risco: baixo
- rollback: `systemctl start unbound`
- expectativa causal: `service_failure` em `svc-unbound`

### Cenário C - superfície pública do Livecopilot

- pré-condição: binding existente para Livecopilot e edge público
- risco: médio
- rollback: `systemctl start cloudflared`
- expectativa causal: `public_access_failure` sem inferir backend down automaticamente

### Cenário D - wg0

- pré-condição: evidência de runtime disponível no grafo/Zabbix
- risco: baixo se realizado no host correto, alto se for forçado no lugar errado
- rollback: reversão da interface ou validação documental
- expectativa causal: `overlay_failure` restrito ao overlay

## Critério de execução

- executar somente o que for reversível e claramente localizado
- se não houver acesso seguro ao nó alvo, registrar como validação histórica/documental
- registrar PASS, PARTIAL ou FAIL com honestidade
