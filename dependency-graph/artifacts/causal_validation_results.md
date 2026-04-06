# Causal Validation Results

## Resumo

- Cenário A: PASS
- Cenário B: PASS
- Cenário C: FAIL
- Cenário D: PARTIAL
- Follow-up desta rodada:
  - Apache2 e unbound receberam calibração temporal seriada com polling a cada 15s
  - o runtime do Zabbix mostrou queda, recuperação e fechamento completos em ambos os serviços
  - a janela curta das rodadas anteriores explicava os `PARTIAL`: o fechamento ainda não tinha sido observado antes do snapshot final
  - `wg0` segue fechado como alvo do cluster MikroTik RB3011, não como injeção local neste host

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
- resultado: `PASS`
- observação curta: a leitura causal bateu no serviço certo e a calibração temporal capturou queda, recuperação e fechamento completos
- follow-up de calibração:
  - stop em `2026-04-05T22:43:03-03:00`
  - primeiro reflexo de queda no item em `2026-04-05T22:43:05-03:00`
  - abertura da trigger em `2026-04-05T22:43:05-03:00`
  - recovery no systemd em `2026-04-05T22:45:04-03:00`
  - primeiro reflexo de recuperação no item em `2026-04-05T22:45:05-03:00`
  - fechamento da trigger em `2026-04-05T22:45:05-03:00`
  - item `69485` voltou ao estado saudável observado no Zabbix

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
- resultado: `PASS`
- observação curta: o item e o trigger confirmaram a leitura local, e a rodada seriada capturou fechamento completo dentro da janela observada
- follow-up de calibração:
  - stop em `2026-04-05T22:46:50-03:00`
  - primeiro reflexo de queda no item em `2026-04-05T22:48:06-03:00`
  - abertura da trigger em `2026-04-05T22:48:06-03:00`
  - recovery no systemd em `2026-04-05T22:48:51-03:00`
  - fechamento da trigger em `2026-04-05T22:49:06-03:00`
  - primeiro reflexo de recuperação no item em `2026-04-05T22:50:06-03:00`
  - o item `69486` voltou ao estado saudável observado no Zabbix

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
