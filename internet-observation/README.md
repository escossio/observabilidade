# Internet Observation

Esta frente organiza checagens simples de presença pública e a captura controlada de tráfego real durante uso de serviços externos.

## Objetivo desta rodada

- adicionar domínios públicos reais como alvo de checagem simples
- registrar uma validação inicial objetiva de DNS, ping e HTTPS simples
- preparar um playbook de captura real para Netflix
- separar claramente:
  - sinal grosso de reachability
  - observação real de tráfego durante playback

## Estrutura

- `artifacts/`: documentação, validações e playbooks
- `captures/`: arquivos brutos de tcpdump e exportações de evidência durante tráfego real

## Regra operacional

- domínio público conhecido entra como checagem simples
- hostname ou IP só vira evidência operacional relevante quando for observado durante tráfego real
- ping ou GET simples não provam caminho de streaming nem substituem captura real
