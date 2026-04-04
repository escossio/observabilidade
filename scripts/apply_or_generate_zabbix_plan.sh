#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARTIFACTS_DIR="$ROOT_DIR/artifacts"
mkdir -p "$ARTIFACTS_DIR"

plan="$ARTIFACTS_DIR/zabbix_plan.md"
cat > "$plan" <<'EOF'
# Plano de aplicação Zabbix

## Situação detectada

- Zabbix não foi encontrado como stack funcional instalada neste host
- não há credencial/API disponível nesta frente para automação direta
- a aplicação deve seguir como passo controlado em uma stack Zabbix existente ou em instalação futura

## Passos seguros

1. confirmar host/instância Zabbix de destino
2. instalar `zabbix-agent2` apenas no host monitorado, se aplicável
3. importar inventários de `config/services.yaml`, `config/web_checks.yaml` e `config/dns_checks.yaml`
4. criar ou ajustar templates/items/triggers para:
   - serviços `systemd`
   - web scenarios
   - checagens DNS
5. criar dashboard com os blocos definidos em `docs/dashboard_blueprint.md`
6. validar um item real de cada classe antes de considerar a frente pronta

## Evidência esperada

- latest data com um serviço `systemd`
- latest data com uma URL
- latest data com um domínio DNS
- dashboard com resumo por estado
EOF

echo "generated $plan"
