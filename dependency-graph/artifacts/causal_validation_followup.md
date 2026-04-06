# Causal Validation Follow-up

## Objetivo

Fechar os cenários que ficaram `PARTIAL` na bateria anterior, sem inventar PASS quando a recuperação não aparece completa no runtime do Zabbix.

## Cenários revisitados

### Apache2 parado

- motivo do `PARTIAL` anterior: janela curta demais para o retorno do estado saudável aparecer no Zabbix
- nova estratégia: ampliar a janela após stop e após start
- resultado final: `PARTIAL`
- motivo: o item voltou a refletir recuperação, mas o trigger não fechou no último snapshot observado

### unbound parado

- motivo do `PARTIAL` anterior: janela curta demais para o retorno do estado saudável aparecer no Zabbix
- nova estratégia: ampliar a janela após stop e após start
- resultado final: `PARTIAL`
- motivo: o item abriu corretamente e o serviço voltou no systemd, mas o último snapshot do Zabbix ainda não mostrou o fechamento completo do ciclo

### wg0

- motivo do `PARTIAL` anterior: o host atual não é o host certo para provocar `wg0`
- nova estratégia: localizar o host/edge correto no grafo e no cluster da MikroTik RB3011
- resultado final: `PARTIAL`
- motivo: o `wg0` pertence ao cluster `MikroTik RB3011` e é `edge-mikrotik-wg0`; neste host local não existe interface `wg0` para injeção segura

## Conclusão do follow-up

- a semântica da correlação permaneceu correta
- o gargalo principal foi de observação/recuperação do runtime, não de modelagem
- `wg0` foi fechado como alvo do cluster MikroTik, não como teste local deste host
