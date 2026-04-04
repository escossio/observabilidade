# Grafana integration

## Estado

- Grafana instalado pela repo oficial: `12.4.2`
- serviço: `grafana-server` ativo
- porta: `3000`
- URL: `http://127.0.0.1:3000/`
- login local validado com `admin/admin` para configuração inicial

## Integração com Zabbix

- plugin instalado: `alexanderzobnin-zabbix-app v6.3.0`
- datasource provisionado: `Zabbix`
- datasource type: `alexanderzobnin-zabbix-datasource`
- datasource URL: `http://127.0.0.1:8081/api_jsonrpc.php`
- autenticação do datasource: usuário `Admin` com a senha rotacionada já existente no backend Zabbix

## Validação objetiva

- `GET /api/health` do Grafana retornou `database: ok`
- `GET /api/datasources` confirmou o datasource `Zabbix`
- consulta Grafana para item numérico real do Zabbix retornou série com dados:
  - item: `Service apache2 running`
  - key: `proc.num[apache2]`
  - valores reais observados no retorno da API do Grafana
- consulta via plugin para item textual de web/DNS precisa de ajuste adicional, porque o plugin atual converte a resposta como métrica numérica e rejeita strings no modo usado

## Observação técnica

- o Grafana já lê dados reais do Zabbix para itens numéricos
- para web/DNS textuais, o backend atual usa `web.page.get` e `net.dns.record`, que retornam texto; o plugin requer uma adaptação extra para exibir isso de forma útil em painel
