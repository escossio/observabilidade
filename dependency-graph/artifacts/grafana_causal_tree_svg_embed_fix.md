# Grafana Causal Tree Static SVG Embed Fix

## Objetivo

Corrigir a entrega da árvore causal no Grafana para o acesso real/mobile sem redesenhar a árvore nem adicionar plugin novo.

## Causa raiz

- o painel 26 usava `Text` em modo `html` com o XML/SVG inteiro inline em `options.content`
- no ambiente gráfico da VM isso chegou a aparecer corretamente, mas no acesso real/mobile a UI do Grafana passou a exibir o XML cru como texto
- o problema estava na forma de renderização do painel, não no SVG nem no conteúdo causal

## Estratégia adotada

- manter o helper `dependency-graph/tools/render_grafana_causal_tree.py` como gerador do SVG
- publicar o SVG gerado em arquivo estático do próprio Grafana
- trocar o painel 26 para embutir a árvore por `<img>`
- manter o painel como `text/html` só como container simples da imagem
- manter o dashboard principal e o painel 26 sem plugin novo nem serviço novo

## Caminho publicado

- arquivo local: `/usr/share/grafana/public/img/observabilidade-zabbix/causal-tree-state.svg`
- URL estável consumida pelo painel: `https://observabilidade.escossio.dev.br/public/img/observabilidade-zabbix/causal-tree-state.svg`
- URL efetiva no painel: `/public/img/observabilidade-zabbix/causal-tree-state.svg?v=<epoch>`

## Painel alterado

- dashboard: `Observabilidade Zabbix - Grafana`
- uid: `observabilidade-grafana`
- painel: `26`
- título: `Árvore Causal / Dependência`
- versão do dashboard: `28 -> 29`

## Forma final de embed

- o helper continua renderizando o SVG completo
- antes de publicar o dashboard, o helper grava o SVG em `/usr/share/grafana/public/img/observabilidade-zabbix/causal-tree-state.svg`
- o conteúdo do painel virou um wrapper HTML curto com:
  - `<img src="/public/img/observabilidade-zabbix/causal-tree-state.svg?v=...">`

## Validação técnica

- `python3 -m py_compile dependency-graph/tools/render_grafana_causal_tree.py` passou sem erro
- `python3 dependency-graph/tools/render_grafana_causal_tree.py --apply-grafana` regravou o dashboard com sucesso
- `GET /api/dashboards/uid/observabilidade-grafana` confirmou:
  - versão `29`
  - painel 26 com `options.content` baseado em `<img ...>`
  - sem SVG inline no conteúdo do painel
- `HEAD https://observabilidade.escossio.dev.br/public/img/observabilidade-zabbix/causal-tree-state.svg` com autenticação respondeu `200`
- `content-type: image/svg+xml`

## Validação real/mobile

- no Chromium autenticado da sessão gráfica (`remote-debugging-port=9223`), o dashboard real carregado confirmou:
  - `panelTitleFound: true`
  - `imageFound: true`
  - `imageSrc: /public/img/observabilidade-zabbix/causal-tree-state.svg?v=1775513595`
  - `rawSvgTextVisible: false`
- no `d-solo` do painel 26 com emulação mobile:
  - `imageFound: true`
  - `complete: true`
  - `rawSvgTextVisible: false`
- evidência visual gerada:
  - screenshot mobile do painel: `/tmp/grafana-causal-tree-mobile-devtools.png`

## Evidência objetiva

- o XML cru deixou de ser a carga do painel
- o painel passou a apontar para um arquivo SVG estático real
- o dashboard autenticado passou a expor a árvore por `img`
- a renderização mobile deixou de depender do parser do `Text panel` para interpretar SVG inline

## Limitações

- o asset estático fica dentro de `/usr/share/grafana/public`, então atualização de pacote do Grafana pode sobrescrever a árvore publicada
- a imagem continua snapshot-driven; para refletir nova rodada ainda é preciso rodar o helper
- o painel continua com altura fixa do dashboard atual
