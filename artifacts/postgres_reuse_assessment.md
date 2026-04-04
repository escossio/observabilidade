# PostgreSQL reuse assessment

## Existing PostgreSQL

- service: active
- cluster: 17/main
- version: PostgreSQL 17.9 (Debian 17.9-0+deb13u1)
- listen_addresses: localhost
- port: 5432
- local auth: peer for unix socket, scram-sha-256 for 127.0.0.1/32

## Existing databases and roles before Zabbix

- databases: livecopilot, postgres, template0, template1
- roles: livecopilot_app, pg_checkpoint, pg_create_subscription, pg_database_owner, pg_execute_server_program, pg_maintain, pg_monitor, pg_read_all_data, pg_read_all_settings, pg_read_all_stats, pg_read_server_files, pg_signal_backend, pg_stat_scan_tables, pg_use_reserved_connections, pg_write_all_data, pg_write_server_files, postgres

## Reuse decision

- no new PostgreSQL instance was installed
- role `zabbix` was created in the existing cluster
- database `zabbix` was created in the existing cluster
- schema was imported into the existing cluster
- privileges were granted on the public schema objects so the server could validate the database as a Zabbix database
