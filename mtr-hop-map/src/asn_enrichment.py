from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ASNResolution:
    asn: str
    company: str
    source: str
    used_fallback: bool


class ASNResolver:
    def __init__(self, cache_path: Path, lookup_mode: str = "online", timeout_seconds: int = 5) -> None:
        self.cache_path = cache_path
        self.lookup_mode = lookup_mode
        self.timeout_seconds = timeout_seconds
        self.cache = self._load_cache()
        self.stats = {
            "whois_success": 0,
            "cache_ip_hit": 0,
            "cache_asn_hit": 0,
            "hint_fallback": 0,
            "unknown_fallback": 0,
            "private_shortcut": 0,
        }
        self.events: list[str] = []

    def lookup(self, ip: str, asn_hint: str = "AS???") -> ASNResolution:
        cached_ip = self.cache["ip"].get(ip)
        if cached_ip:
            self.stats["cache_ip_hit"] += 1
            return ASNResolution(
                asn=cached_ip["asn"],
                company=cached_ip["company"],
                source="cache-ip",
                used_fallback=False,
            )

        if self.lookup_mode == "online":
            result = self._lookup_online(ip)
            if result is not None:
                return result

        if asn_hint and asn_hint != "AS???" and asn_hint in self.cache["asn"]:
            self.stats["cache_asn_hit"] += 1
            company = self.cache["asn"][asn_hint]["company"]
            return ASNResolution(asn=asn_hint, company=company, source="cache-asn-fallback", used_fallback=True)

        if asn_hint and asn_hint != "AS???":
            self.stats["hint_fallback"] += 1
            self.events.append(f"fallback ASN hint usado para {ip}: {asn_hint}")
            return ASNResolution(asn=asn_hint, company="Unknown ASN", source="mtr-as-hint-fallback", used_fallback=True)

        self.stats["unknown_fallback"] += 1
        self.events.append(f"fallback sem ASN para {ip}")
        return ASNResolution(asn="AS???", company="Unknown ASN", source="fallback-unknown", used_fallback=True)

    def mark_private(self) -> None:
        self.stats["private_shortcut"] += 1

    def summary(self) -> dict:
        return {
            "lookup_mode": self.lookup_mode,
            "timeout_seconds": self.timeout_seconds,
            "cache_path": str(self.cache_path),
            "stats": self.stats,
            "events": self.events,
        }

    def _lookup_online(self, ip: str) -> ASNResolution | None:
        try:
            proc = subprocess.run(
                ["whois", "-h", "whois.cymru.com", "-v", ip],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=True,
            )
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError) as exc:
            self.events.append(f"whois falhou para {ip}: {exc}")
            return None

        lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        data_line = next((line for line in lines if re.match(r"^\d+\s+\|", line)), "")
        if not data_line:
            self.events.append(f"whois sem linha util para {ip}")
            return None

        fields = [field.strip() for field in data_line.split("|")]
        asn = f"AS{fields[0]}" if fields and fields[0].isdigit() else "AS???"
        as_name = fields[-1] if fields else "Unknown ASN"
        company = as_name.split(" - ", 1)[1].strip() if " - " in as_name else as_name.strip()
        company = re.sub(r",\s*[A-Z]{2}$", "", company)

        self.stats["whois_success"] += 1
        self._write_cache(ip, asn, company)
        return ASNResolution(asn=asn, company=company, source="whois-cymru", used_fallback=False)

    def _load_cache(self) -> dict:
        if not self.cache_path.exists():
            return {"ip": {}, "asn": {}}
        try:
            data = json.loads(self.cache_path.read_text())
        except json.JSONDecodeError:
            return {"ip": {}, "asn": {}}
        return {
            "ip": data.get("ip", {}),
            "asn": data.get("asn", {}),
        }

    def _write_cache(self, ip: str, asn: str, company: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        self.cache["ip"][ip] = {"asn": asn, "company": company, "updated_at": now}
        if asn and asn != "AS???":
            self.cache["asn"][asn] = {"company": company, "updated_at": now}
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self.cache, indent=2, ensure_ascii=False) + "\n")
