# Zabbix installation evidence

## Packages installed

- zabbix-release 1:7.4-1+debian13
- zabbix-server-pgsql 1:7.4.8-1+debian13
- zabbix-frontend-php 1:7.4.8-1+debian13
- zabbix-apache-conf 1:7.4.8-1+debian13
- zabbix-agent2 1:7.4.8-1+debian13
- zabbix-sql-scripts 1:7.4.8-1+debian13
- php8.4-pgsql / php-pgsql

## Repository

- official Zabbix repository added from `repo.zabbix.com` for Debian trixie
- candidate version for the Zabbix stack was 7.4.8

## Database

- database: `zabbix`
- role: `zabbix`
- PostgreSQL connection: `127.0.0.1:5432`
- schema import source: `/usr/share/zabbix/sql-scripts/postgresql/server.sql.gz`
- import completed successfully

## Frontend

- Apache vhost: `127.0.0.1:8081`
- frontend URL: `http://127.0.0.1:8081/`
- API URL: `http://127.0.0.1:8081/api_jsonrpc.php`
