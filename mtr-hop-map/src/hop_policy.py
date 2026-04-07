from __future__ import annotations

import re
from dataclasses import dataclass

from .mtr_parser import Hop


@dataclass(frozen=True)
class HopIdentity:
    hostname: str
    visible_name: str
    tags: list[dict[str, str]]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def normalize_ip(ip: str) -> str:
    return ip.replace(".", "-").replace(":", "-")


def build_hostname(target: str, hop: Hop) -> str:
    return f"hop-{slugify(target)}-{hop.order:02d}-{normalize_ip(hop.ip)}"


def build_identity(target: str, hop: Hop) -> HopIdentity:
    return HopIdentity(
        hostname=build_hostname(target, hop),
        visible_name=f"{hop.ip} / {hop.asn} / {hop.company}",
        tags=[
            {"tag": "role", "value": "transit-hop"},
            {"tag": "target", "value": target},
            {"tag": "hop_index", "value": str(hop.order)},
            {"tag": "source", "value": "mtr-asn-map"},
            {"tag": "hop_category", "value": hop.category},
        ],
    )
