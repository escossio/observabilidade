# Relatório visual da rodada

## Resumo
- mapa canônico único mantido: `MTR Unified - Brisanet Observed`
- `sysmapid`: `10`
- tamanho antigo do canvas: `1900x560`
- tamanho novo do canvas: `2440x1846`
- `selement_count`: `63`
- `link_count`: `65`
- as ligações foram preservadas; a mudança foi só de apresentação visual

## Política visual
- backbone observado: `Server_(96)`
- borda candidata: `Router_(96)`
- CDN e demais externos: `Cloud_(96)`
- watchlist DNS: `Notebook_(96)`
- labels do tronco foram reduzidos para `IP + core runs/targets`
- labels de borda e CDN foram encurtados para reduzir poluição

## Layout
- tronco alinhado horizontalmente no topo/centro superior
- famílias externas distribuídas em bandas separadas
- Google, Quad9, Akamai, Microsoft, Meta, Amazon, ATT, Twelve99, Dell e Mikrotik ficaram em faixas distintas quando possível

## Validação
- `sysmapid 10` permaneceu o mesmo
- `link_count` permaneceu em `65`
- não houve recálculo da topologia lógica
- o snapshot final do Zabbix está em `zabbix_map_snapshot.json`
