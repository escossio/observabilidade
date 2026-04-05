# Netflix Capture Playbook

## Objetivo

Preparar uma captura real de tráfego durante playback de Netflix para observar hostnames, IPs e conexões efetivas usados pelo cliente.

## Ferramentas validadas nesta VM

- `tcpdump`
- `curl`
- `dig`
- `traceroute`
- navegador com DevTools:
  - `chromium`
  - `firefox`
- `whois`: ausente nesta VM, então o mapeamento de ASN fica opcional e depende de ferramenta externa ou instalação futura

## Antes de começar

- abrir uma sessão de shell no host
- escolher um timestamp para nomear os artefatos
- garantir espaço livre em disco para a captura

## Variáveis sugeridas

```bash
TS=$(date +%Y%m%d-%H%M%S)
OUT_DIR=/srv/observabilidade-zabbix/internet-observation/captures/$TS-netflix
mkdir -p "$OUT_DIR"
```

## Captura de DNS e TLS/TCP

```bash
sudo tcpdump -i any -nn -s 0 -w "$OUT_DIR/netflix-session.pcap" \
  '(port 53) or (tcp port 80) or (tcp port 443) or (udp port 443)'
```

## Captura textual rápida em paralelo

```bash
sudo tcpdump -i any -nn -tttt \
  '(port 53) or (tcp port 443) or (udp port 443)' \
  | tee "$OUT_DIR/netflix-session-live.log"
```

## Roteiro operacional

1. iniciar o `tcpdump` antes de abrir a sessão real
2. abrir `chromium` ou `firefox`
3. abrir DevTools:
   - aba `Network`
   - marcar `Preserve log`
   - opcionalmente filtrar por `media`, `fetch`, `xhr` e `other`
4. acessar `https://www.netflix.com/`
5. autenticar se necessário
6. iniciar playback real de um título
7. manter o playback por pelo menos 2 a 5 minutos
8. registrar no DevTools:
   - hostnames observados
   - requests recorrentes
   - conexões de mídia
   - eventuais redirects
9. encerrar playback
10. parar o `tcpdump`
11. exportar evidências do DevTools:
   - screenshot da aba `Network`
   - HAR se fizer sentido
12. consolidar hostnames, IPs e ASNs observados

## Consolidação pós-captura

### Hostnames via strings no pcap

```bash
strings "$OUT_DIR/netflix-session.pcap" | rg -i 'netflix|nflx|video|edge|cdn' \
  | sort -u > "$OUT_DIR/netflix-hostnames-suspects.txt"
```

### IPs remotos observados

```bash
tcpdump -nn -r "$OUT_DIR/netflix-session.pcap" 2>/dev/null \
  | awk '{print $3, $5}' \
  | sed 's/[>:].*$//' \
  | tr ' ' '\n' \
  | rg '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' \
  | sort -u > "$OUT_DIR/netflix-remote-ips.txt"
```

### ASN dos IPs observados

Use este passo apenas se houver ferramenta de whois disponível.

```bash
while read -r ip; do
  whois "$ip" | rg -i 'origin|originas|aut-num|netname|descr' || true
  echo '---'
done < "$OUT_DIR/netflix-remote-ips.txt" > "$OUT_DIR/netflix-ip-whois.txt"
```

## Limites

- ping em `netflix.com` não prova o caminho real de streaming
- hostname público não equivale ao endpoint efetivo de mídia
- o tráfego pode mudar por CDN, região, horário e catálogo
- sem observação real durante playback, não há base para promover hostnames de CDN ao grafo
