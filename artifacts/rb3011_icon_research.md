# RB3011 Icon Research

## Objetivo

Selecionar o ativo visual mais próximo possível da MikroTik RB3011 para uso interno no mapa do Zabbix `AGT - Visão Visual`, com foco em legibilidade pequena, aderência ao equipamento e baixo risco operacional.

## Metodologia

- Partir do estado atual documentado em `STATUS.md` e `artifacts/zabbix_agt_visual_map.md`
- Pesquisar primeiro fontes oficiais e comunitárias com maior chance de representar o equipamento ou a marca com fidelidade
- Priorizar fontes em esta ordem:
  - imagem do equipamento RB3011
  - ícone comunitário MikroTik
  - ícone genérico de roteador com boa leitura em tamanho pequeno
- Baixar apenas os candidatos mais promissores para `artifacts/rb3011_icon_candidates/`
- Preparar um derivado simples do asset oficial para uso como ícone quadrado no Zabbix

## Fontes consultadas

- MikroTik product page e assets públicos do RB3011
- Repositório comunitário `loganmarchione/homelab-svg-assets`
- Repositório comunitário `bwks/network-icons-svg`

## Candidatos baixados

- `01_official_rb3011_photo.png`
  - Origem: `https://cdn.mikrotik.com/web-assets/rb_images/1407_hi_res.png`
  - Tipo: PNG
  - Tamanho: `1920x558`
  - Observação: imagem oficial do RB3011, transparente, semanticamente a mais precisa

- `01b_official_rb3011_photo_iconfit.png`
  - Origem: derivada local do asset oficial acima
  - Tipo: PNG
  - Tamanho: `1024x1024`
  - Observação: versão preparada para iconografia, mantendo o equipamento centralizado em canvas quadrado

- `03_mikrotik_logo.svg`
  - Origem: `loganmarchione/homelab-svg-assets`
  - Tipo: SVG
  - Tamanho/viewBox: SVG vetorial
  - Observação: representa a marca MikroTik, não o modelo RB3011; boa leitura, mas menos fiel ao equipamento

- `04_generic_router_flat_label_colour.svg`
  - Origem: `bwks/network-icons-svg`
  - Tipo: SVG
  - Tamanho/viewBox: `477.15662 x 123.40902`
  - Observação: roteador genérico limpo, bom para leitura pequena, mas sem identidade MikroTik

- `05_generic_router_square_colour_3d.svg`
  - Origem: `bwks/network-icons-svg`
  - Tipo: SVG
  - Tamanho/viewBox: `258.25999 x 104.5435`
  - Observação: roteador genérico mais pictórico; visualmente mais pesado que o flat label

## Shortlist final

1. `01b_official_rb3011_photo_iconfit.png`
   - Aderência visual: 10/10
   - Legibilidade pequena: 8/10
   - Recomendação: melhor opção principal para o Zabbix
   - Licença/uso: asset público do fabricante; uso interno é pragmático, mas a redistribuição não deve ser presumida como livre

2. `01_official_rb3011_photo.png`
   - Aderência visual: 10/10
   - Legibilidade pequena: 6/10
   - Recomendação: boa referência fiel, mas menos amigável para o slot quadrado de mapa
   - Licença/uso: mesma observação do asset oficial

3. `03_mikrotik_logo.svg`
   - Aderência visual: 6/10
   - Legibilidade pequena: 9/10
   - Recomendação: reserva segura se a prioridade for clareza visual, não fidelidade ao modelo
   - Licença/uso: MIT no repositório; ainda assim é marca registrada e deve ser tratada com cuidado de branding

4. `04_generic_router_flat_label_colour.svg`
   - Aderência visual: 5/10
   - Legibilidade pequena: 9/10
   - Recomendação: melhor fallback genérico se a marca não for prioridade
   - Licença/uso: GPL-3.0 no repositório

5. `05_generic_router_square_colour_3d.svg`
   - Aderência visual: 4/10
   - Legibilidade pequena: 7/10
   - Recomendação: reserva final; visual aceitável, mas menos limpa que a opção flat
   - Licença/uso: GPL-3.0 no repositório

## Recomendação final

Escolher `01b_official_rb3011_photo_iconfit.png` como ícone principal da RB3011 no mapa do Zabbix.

Motivo: é o único candidato que combina fidelidade ao modelo, transparência, preparo em canvas quadrado e leitura aceitável em tamanho pequeno.

## Reserva

Se a imagem oficial ficar visualmente pesada no slot do mapa, a segunda opção prática é `03_mikrotik_logo.svg` por legibilidade. Se a prioridade mudar para iconografia neutra, a melhor opção genérica é `04_generic_router_flat_label_colour.svg`.

## Próximos passos sugeridos

- Aplicar a opção principal no elemento RB3011 do mapa
- Validar o comportamento visual no frontend do Zabbix
- Se a leitura ficar ruim, trocar para a reserva e manter o modelo de seleção documentado para os próximos links e hosts
