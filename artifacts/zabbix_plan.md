# Plano de aplicação Zabbix

## Situação detectada

- Zabbix 7.4.8 foi instalado localmente por pacotes oficiais
- o PostgreSQL 17 local foi reutilizado com sucesso
- o frontend responde em `http://127.0.0.1:8081/`
- a API responde em `http://127.0.0.1:8081/api_jsonrpc.php`

## Passos seguros

1. manter a base local documentada em `artifacts/`
2. revisar os itens e triggers criados a partir dos YAMLs em `config/`
3. ajustar o dashboard com widgets reais, se necessário
4. expandir a cobertura de monitoração apenas se novos alvos reais surgirem

## Evidência esperada

- latest data com um serviço, uma URL e um domínio DNS
- dashboard criado no Zabbix local
- autenticação real com `apiinfo.version`, `user.get` e `host.get`
