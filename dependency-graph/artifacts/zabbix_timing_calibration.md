# Zabbix Timing Calibration

## Objetivo

Medir a janela real de convergência do Zabbix para itens e triggers de serviço locais, usando polling seriado após queda e recuperação reais.

## Método

- alvo em cada ciclo: parar o serviço via `systemctl`, consultar `history_uint`, `triggers` e `problem` em série, religar o serviço e continuar consultando até estabilização
- intervalo de observação: 15s
- critérios observados: primeiro instante em que o item refletiu queda, primeiro instante em que a trigger abriu, primeiro instante em que o item refletiu recuperação, primeiro instante em que a trigger fechou
- observação importante: a leitura foi feita no runtime do Zabbix via PostgreSQL, não por snapshot único

## Apache2

- alvo: `svc-apache2`
- itemid: `69485`
- triggerid: `32506`
- trigger relacionada web: `32507`
- stop do systemd: `2026-04-05T22:43:03-03:00`
- primeiro instante em que o item refletiu queda: `2026-04-05T22:43:05-03:00`
- primeiro instante em que a trigger abriu: `2026-04-05T22:43:05-03:00`
- start/recovery do systemd: `2026-04-05T22:45:04-03:00`
- primeiro instante em que o item refletiu recuperação: `2026-04-05T22:45:05-03:00`
- primeiro instante em que a trigger fechou: `2026-04-05T22:45:05-03:00`
- tempo até queda do item: `2s`
- tempo até abertura da trigger: `2s`
- tempo até recuperação do item: `2m02s`
- tempo até fechamento da trigger: `2m02s`
- atraso entre recovery do systemd e recovery observado no Zabbix: `1s`
- tempo total de convergência observado: `2m02s`

## unbound

- alvo: `svc-unbound`
- itemid: `69486`
- triggerid: `32537`
- stop do systemd: `2026-04-05T22:46:50-03:00`
- primeiro instante em que o item refletiu queda: `2026-04-05T22:48:06-03:00`
- primeiro instante em que a trigger abriu: `2026-04-05T22:48:06-03:00`
- start/recovery do systemd: `2026-04-05T22:48:51-03:00`
- primeiro instante em que o item refletiu recuperação: `2026-04-05T22:50:06-03:00`
- primeiro instante em que a trigger fechou: `2026-04-05T22:49:06-03:00`
- tempo até queda do item: `1m16s`
- tempo até abertura da trigger: `1m16s`
- tempo até recuperação do item: `1m15s`
- tempo até fechamento da trigger: `15s`
- atraso entre recovery do systemd e recovery observado no Zabbix: `1m15s`
- tempo total de convergência observado: `1m15s`

## Leitura operacional

- Apache2 convergiu rápido no runtime observado, com item e trigger fechando no primeiro minuto útil após o start
- unbound mostrou fechamento da trigger antes da consolidação do item, então a recuperação observável no item ficou mais lenta do que o fechamento do alerta
- a janela que faltava nos ciclos anteriores era curta demais para capturar o fechamento completo sem ambiguidade

## Janela recomendada

- janela segura mínima para futuras baterias de serviço: `2m30s` após o start, com polling a cada `15s`
- janela prática para reduzir falso PARTIAL: `3m00s` após o start, quando a intenção for provar fechamento completo sem depender de um único snapshot
- para a fase de queda, manter pelo menos `60s` de observação após o stop
