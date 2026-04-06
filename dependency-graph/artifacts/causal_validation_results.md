# Causal Validation Results

## Resumo

- Cenário A: PARTIAL
- Cenário B: PARTIAL
- Cenário C: FAIL
- Cenário D: PARTIAL
- Follow-up desta rodada:
  - Apache2 e unbound receberam janela maior e tiveram ida/volta observadas no systemd
  - o Zabbix mostrou a transição de queda, mas o fechamento completo ainda ficou atrasado no último snapshot analisado
  - `wg0` foi fechado como alvo do cluster MikroTik RB3011, não como injeção local neste host

## Cenário A - Apache2 parado

- evento provocado: `systemctl stop apache2`
- timestamp inicial: `2026-04-05T22:07:32-03:00`
- rollback: `systemctl start apache2`
- evidência no runtime do Zabbix:
  - item `69485` (`Service apache2 running`) caiu de `11` para `0`
  - trigger `32506` (`Apache2 parado`) permaneceu em `0` no snapshot consultado
- nó correlacionado: `svc-apache2`
- semântica esperada: `service_failure`
- semântica obtida: `service_failure` parcialmente corroborada
- blast radius esperado: `service-local`
- blast radius obtido: `service-local`
- resultado: `PARTIAL`
- observação curta: a leitura causal bateu no serviço certo, mas o trigger não foi observado como aberto no snapshot consultado
- follow-up de janela maior:
  - stop em `2026-04-05T22:23:52-03:00`
  - snapshot em queda em `2026-04-05T22:25:13-03:00`
  - recovery no systemd em `2026-04-05T22:25:13-03:00`
  - snapshot final em `2026-04-05T22:28:06-03:00`
  - item `69485` voltou para `10`
  - trigger `32506` abriu na queda, mas permaneceu sem fechamento no último snapshot visto

## Cenário B - unbound parado

- evento provocado: `systemctl stop unbound`
- timestamp inicial: `2026-04-05T22:08:43-03:00`
- rollback: `systemctl start unbound`
- evidência no runtime do Zabbix:
  - item `69486` (`Service unbound running`) caiu de `1` para `0`
  - trigger `32537` (`unbound parado`) apareceu com `value=1` no snapshot intermediário
- nó correlacionado: `svc-unbound`
- semântica esperada: `service_failure`
- semântica obtida: `service_failure`
- blast radius esperado: `service-local`
- blast radius obtido: `service-local`
- resultado: `PARTIAL`
- observação curta: o item e o trigger confirmaram a leitura local, mas o retorno para estado saudável não havia sido refletido no banco no momento do último snapshot
- follow-up de janela maior:
  - stop em `2026-04-05T22:25:53-03:00`
  - snapshot em queda em `2026-04-05T22:27:13-03:00`
  - recovery no systemd em `2026-04-05T22:27:14-03:00`
  - snapshot final em `2026-04-05T22:28:06-03:00`
  - item `69486` ainda estava em `0` no snapshot final
  - trigger `32537` abriu na queda, mas também permaneceu sem fechamento no último snapshot visto

## Cenário C - superfície pública do Livecopilot

- evento provocado: `systemctl stop cloudflared`
- timestamp inicial: `2026-04-05T22:10:18-03:00`
- rollback: `systemctl start cloudflared`
- evidência no runtime do Zabbix:
  - itens `69632` a `69634` permaneceram em `1`
  - o snapshot não mostrou indisponibilidade da superfície pública do Livecopilot
- nó correlacionado: `svc-livecopilot-apache-edge`
- semântica esperada: `public_access_failure`
- semântica obtida: não comprovada no runtime desta rodada
- blast radius esperado: `publication-surface`
- blast radius obtido: não comprovado
- resultado: `FAIL`
- observação curta: derrubar `cloudflared` não produziu o evento esperado nesses itens; a hipótese de acoplamento direto com a leitura do Livecopilot público não se sustentou nesta bateria

## Cenário D - wg0

- evento reutilizado: evidência já documentada no grafo e runtime do MikroTik
- timestamp de snapshot: `2026-04-05T22:10:06-03:00`
- rollback: não aplicável neste host; a interface `wg0` não existe localmente
- evidência no runtime do Zabbix:
  - item `69689` (`wg0 operational status`) está presente no binding do grafo
  - o host atual não possui `wg0`, então não houve evento local reversível nesta rodada
- nó correlacionado: `edge-mikrotik-wg0`
- semântica esperada: `overlay_failure`
- semântica obtida: `overlay_failure` apenas documental nesta rodada
- blast radius esperado: `overlay-only`
- blast radius obtido: `overlay-only` documental
- resultado: `PARTIAL`
- observação curta: não houve como provocar com segurança no host atual; a validação fica como confirmação documental do mapeamento, não como prova dinâmica
- follow-up de localização:
  - o `wg0` do grafo pertence ao cluster `MikroTik RB3011`
  - o nó correspondente é `edge-mikrotik-wg0`
  - o host atual não possui interface `wg0`
  - não houve alvo seguro para injeção local nesta máquina
