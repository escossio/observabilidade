# Validator

Runner local e autocontido para validar navegacao headless com captura `tcpdump` na propria maquina.

## Estrutura

- `bin/`: launcher e probe do browser
- `runs/`: saida por execucao
- `docs/`: contrato e congelamento do legado
- `archive/`: reservado para consolidacao futura

## Contrato

### Entrada

- `--url`: alvo HTTP/HTTPS
- `--iface`: interface de captura
- `--name`: nome logico da rodada

### Saida

- um diretorio unico em `/srv/validator/runs/<timestamp>-<nome>`
- artefatos minimos:
  - `capture.pcap`
  - `browser-console.json`
  - `browser-network.json`
  - `page.png`
  - `summary.md`

## Execucao

```bash
/srv/validator/bin/run-validator.sh \
  --url https://example.com \
  --iface br0 \
  --name smoke-example
```

## Dependencias

- `tcpdump`
- `chromium`
- `node`
- `jq`
- `playwright-core`

O launcher tenta `sudo -n tcpdump` quando `sudo` existe. Se `sudo` nao existir e o processo ja estiver em `root`, ele executa `tcpdump` diretamente.
