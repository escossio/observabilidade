from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from .asn_enrichment import ASNResolver


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


def parse_hops(mtr_json: dict, resolver: ASNResolver) -> list[Hop]:
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
            source = "mtr-no-response"
        elif _is_private_or_local(ip):
            resolver.mark_private()
            asn = "AS private"
            company = "Private / local network"
            category = "private"
            source = "mtr-private"
        else:
            resolution = resolver.lookup(ip, asn_hint=asn_hint)
            asn = resolution.asn
            company = resolution.company
            category = "public"
            source = resolution.source

        label = f"{display_ip}\n{asn}\n{company}"
        hops.append(Hop(order=order, ip=ip, asn=asn, company=company, category=category, label=label, source=source))
    return hops


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


def _looks_like_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
