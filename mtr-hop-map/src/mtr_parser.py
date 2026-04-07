from __future__ import annotations

import ipaddress
import re
import subprocess
from dataclasses import dataclass
from functools import lru_cache


_PRIVATE_CGNAT = ipaddress.ip_network("100.64.0.0/10")


@dataclass(frozen=True)
class Hop:
    order: int
    ip: str
    asn: str
    company: str
    category: str
    label: str
    source: str


def _is_private_or_local(ip: str) -> bool:
    ip_obj = ipaddress.ip_address(ip)
    return any(
        (
            ip_obj.is_private,
            ip_obj.is_loopback,
            ip_obj.is_link_local,
            ip_obj.is_multicast,
            ip_obj.is_reserved,
            ip_obj in _PRIVATE_CGNAT,
        )
    )


def _normalize_company(text: str) -> str:
    text = text.strip()
    text = re.sub(r",\s*[A-Z]{2}$", "", text)
    return text


@lru_cache(maxsize=512)
def lookup_asn_company(ip: str) -> tuple[str, str]:
    if _is_private_or_local(ip):
        return "AS private", "Private / local network"

    proc = subprocess.run(
        ["whois", "-h", "whois.cymru.com", "-v", ip],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    data_line = next((line for line in lines if re.match(r"^\d+\s+\|", line)), "")
    if not data_line:
        return "AS???", "Unknown ASN"
    fields = [field.strip() for field in data_line.split("|")]
    asn = f"AS{fields[0]}" if fields and fields[0].isdigit() else "AS???"
    as_name = fields[-1] if fields else "Unknown ASN"
    company = "Unknown ASN"
    if " - " in as_name:
        company = as_name.split(" - ", 1)[1].strip()
    else:
        company = as_name.strip()
    return asn, _normalize_company(company)


def parse_hops(mtr_json: dict) -> list[Hop]:
    hubs = mtr_json["report"]["hubs"]
    hops: list[Hop] = []
    for hub in hubs:
        order = int(hub["count"])
        raw_host = str(hub.get("host", "")).strip()
        ip = raw_host if _looks_like_ip(raw_host) else ""
        display_ip = ip or "*"
        asn_hint = str(hub.get("ASN", "AS???")).strip()
        if not ip:
            asn = "AS???"
            company = "No response"
            category = "no-response"
            source = "mtr"
        elif _is_private_or_local(ip):
            asn, company = "AS private", "Private / local network"
            category = "private"
            source = "mtr"
        else:
            asn, company = lookup_asn_company(ip)
            if asn == "AS???" and asn_hint and asn_hint != "AS???":
                asn = asn_hint
            category = "public"
            source = "whois-cymru"
        label = f"{display_ip}\n{asn}\n{company}"
        hops.append(Hop(order=order, ip=ip, asn=asn, company=company, category=category, label=label, source=source))
    return hops


def _looks_like_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
