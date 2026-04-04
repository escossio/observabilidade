# Zabbix security hardening

## Credencial padrão

- o login padrão `Admin/zabbix` foi removido da operação
- a senha do usuário `Admin` foi alterada via API do Zabbix
- a nova credencial foi validada com autenticação real
- a credencial antiga falha na autenticação após a troca

## Armazenamento local

- a senha nova foi guardada apenas em caminhos locais restritos para uso operacional futuro
- o valor não deve ser exposto em relatórios nem em artefatos públicos
- os caminhos locais de apoio ficam fora do fluxo normal de documentação operacional

## Evidência

- `user.login` com `Admin/zabbix` falha
- `user.login` com a credencial rotacionada funciona
- a API segue acessível no frontend local após a troca de senha
