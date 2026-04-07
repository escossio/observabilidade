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


def build_hostname(hop: Hop) -> str:
    return f"hop-ip-{normalize_ip(hop.ip)}"


def build_identity(hop: Hop) -> HopIdentity:
    return HopIdentity(
        hostname=build_hostname(hop),
        visible_name=f"Transit Hop {hop.ip}",
        tags=[
            {"tag": "role", "value": "transit-hop"},
            {"tag": "source", "value": "mtr-asn-map"},
            {"tag": "identity_scope", "value": "global-ip"},
            {"tag": "canonical_ip", "value": hop.ip},
            {"tag": "hop_category", "value": hop.category},
        ],
    )
