# Congelamento do legado

## Escopo congelado

- `/home/codex/validation-runner` foi preservado intacto.
- `/home/codex/artifacts` foi preservado intacto.
- a nova implementacao desta rodada fica isolada em `/srv/validator`.

## Estado encontrado em `/home/codex/validation-runner`

- a arvore contem codigo executavel e artefatos historicos.
- arquivos principais encontrados no topo:
  - `package.json`
  - `run_validation_round.js`
  - `run_validation_round.js.bak.20260324T010930Z`
  - `questions.json`
  - `questions-multiturn.json`
  - `questions-hardening.json`
- artefatos existentes em `artifacts/` incluem, entre outros:
  - `browser-console.json`
  - `browser-network.json`
  - `capture.pcap`
  - `correlation.json`
  - `network_stats.txt`
  - `response-quality.json`
  - `round_meta.json`
  - `summary.md`
  - `ui-results.json`

## Pontos de acoplamento antigo identificados

### Dependencia de `/srv/liveui`

- arquivo: `/home/codex/validation-runner/run_validation_round.js`
- ponto:
  - linha 8: `require("/srv/liveui/automation/node_modules/playwright")`

### Dependencia explicita do host `10.45.0.3`

- arquivo: `/home/codex/validation-runner/run_validation_round.js`
- pontos:
  - linha 15: `DEFAULT_APP_URL = ... "http://10.45.0.3:8099"`
  - linha 16: `HOST_IP = ... "10.45.0.3"`

### Captura remota via SSH no host `10.45.0.3`

- arquivo: `/home/codex/validation-runner/run_validation_round.js`
- pontos:
  - linha 104: base SSH para `${HOST_USER}@${HOST_IP}`
  - linhas 195-219: instala script remoto, faz `start/status/stop/fetch` de tcpdump e copia o pcap por `scp`

## Conclusao operacional

- o runner legado da VM depende do host `10.45.0.3` tanto para abrir a aplicacao quanto para capturar `tcpdump`.
- ele tambem carrega dependencia de Playwright a partir de `/srv/liveui`.
- a nova rodada substitui esse desenho por um runner 100% local em `/srv/validator`, com browser local, `tcpdump` local e artefatos locais.
