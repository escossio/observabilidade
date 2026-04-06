# causal_explain Validation

## Objetivo

Validar a CLI `dependency-graph/tools/causal_explain.py` com sinais reais já consolidados na bateria causal.

## Execuções

### Apache2

```bash
python3 dependency-graph/tools/causal_explain.py --itemid 69485
python3 dependency-graph/tools/causal_explain.py --triggerid 32506
```

- binding encontrado: `svc-apache2`
- semântica: `service_failure`
- blast radius: `service-local`
- leitura operacional: serviço específico falhou; host pode seguir saudável

### unbound

```bash
python3 dependency-graph/tools/causal_explain.py --itemid 69486
```

- binding encontrado: `svc-unbound`
- semântica: `service_failure`
- blast radius: `service-local`
- leitura operacional: serviço específico falhou; borda não deve ser implicada automaticamente

### Livecopilot público

```bash
python3 dependency-graph/tools/causal_explain.py --itemid 69633
```

- binding encontrado: `svc-livecopilot-apache-edge`
- semântica: `public_access_failure`
- blast radius: `publication-surface`
- leitura operacional: a superfície pública falhou; o backend interno pode continuar ativo

### wg0

```bash
python3 dependency-graph/tools/causal_explain.py --itemid 69689
```

- binding encontrado: `edge-mikrotik-wg0`
- semântica: `overlay_failure`
- blast radius: `overlay-only`
- leitura operacional: o túnel sobreposto caiu; a cadeia principal não deve ser marcada como caída por isso sozinho

## O que a validação confirmou

- a CLI aceita `--itemid` e `--triggerid`
- a CLI resolve bindings reais sem inventar correspondência
- a semântica retornada bate com os cenários já validados
- a leitura causal fica curta e operacional, sem RCA exagerado

## Limites observados

- a saída é documental, não tempo-real
- entradas sem binding retornam erro honesto
- a ferramenta não consulta o Zabbix no momento da execução
- a ferramenta não substitui a camada de correlação humana

