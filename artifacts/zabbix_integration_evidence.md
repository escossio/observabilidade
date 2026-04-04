# Evidências de integração Zabbix

## Central Zabbix

- `http://127.0.0.1/zabbix/api_jsonrpc.php` respondeu `404 Not Found`, então não existe Zabbix local funcional nesta máquina
- `http://10.45.0.6/zabbix/api_jsonrpc.php` falhou com conexão recusada em `10.45.0.6:80`
- `10.45.0.6` roteia via `br0` a partir de `10.45.0.3`, mas não responde a `ping`
- os arquivos canônicos esperados de toolbelt/env não existem neste host:
  - `/srv/aiops/env/zbx.env`
  - `/srv/aiops/env/zbx.base.env`
  - `/srv/aiops/env/zbx.local.env`
- por bloqueio de rede e ausência do toolbelt local, não foi possível validar `apiinfo.version`, autenticação ou aplicar mudanças na API central

## Validações reais do host

- serviço `apache2`: ativo e habilitado
- serviço `unbound`: ativo e habilitado
- serviço `emby-server`: ativo e habilitado
- URL `http://127.0.0.1/`: `HTTP/1.1 200 OK`
- URL `http://127.0.0.1:8080/`: `HTTP/1.1 200 OK`
- DNS `example.com` consultado em `127.0.0.1`: `104.18.27.120` e `104.18.26.120`
- DNS `localhost` consultado em `127.0.0.1`: resolvido localmente conforme `/etc/hosts`
- validação de arquivos YAML concluída com sucesso via `./scripts/validate_configs.sh`
- inventário do ambiente salvo em `artifacts/environment_inventory.txt`

## Observação

- a integração automática com o Zabbix central ficou bloqueada por falta de endpoint acessível e credenciais/toolbelt disponíveis neste host
