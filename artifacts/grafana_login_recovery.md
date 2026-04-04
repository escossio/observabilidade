# Grafana login recovery

## Resultado

- usuário funcional do Grafana: `admin`
- a credencial insegura `admin/admin` foi desativada por rotação de senha
- a nova credencial foi validada com sucesso na API pública

## Método usado

- rotacionar senha pelo comando nativo `grafana-cli admin reset-admin-password --password-from-stdin`
- validar a resposta pública em `https://observabilidade.escossio.dev.br/api/user`
- comparar o comportamento antes e depois com autenticação básica

## Evidência de sucesso

- `admin/admin` passou a responder `401 Unauthorized`
- a nova credencial respondeu `200 OK`
- a resposta da API confirmou `login=admin` e `isGrafanaAdmin=true`

## Armazenamento restrito

- senha nova armazenada apenas em `/srv/observabilidade-zabbix/backups/20260404-grafana-login/grafana_admin_password.secret`
- permissões aplicadas: `600`
- arquivo fora do git e fora de caminhos versionáveis

## Observação

- o acesso local em `http://127.0.0.1:3000/` continua redirecionando para o domínio público publicado
