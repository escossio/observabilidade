from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from .mtr_parser import Hop


@dataclass(frozen=True)
class HopIdentity:
    hostname: str
    visible_name: str
    tags: list[dict[str, str]]


MonitoringTemplateMode = Literal["link", "clear", "ignore"]


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


def classify_hop_role(hop: Hop, destination_ip: str | None = None) -> str:
    company = hop.company.upper()
    if destination_ip and hop.ip == destination_ip:
        return "destination"
    if hop.category == "private":
        return "local_recurring_backbone"
    if hop.asn == "AS28126" or "BRISANET" in company:
        return "pivot_or_exit_point"
    if hop.asn == "AS32934" or "FACEBOOK" in company or "META" in company:
        return "service_family_facebook_meta"
    return "transit_external"


def monitoring_mode_for_role(role: str) -> MonitoringTemplateMode:
    if role in {"local_recurring_backbone", "destination"}:
        return "link"
    if role in {"pivot_or_exit_point", "transit_external", "service_family_facebook_meta", "unknown"}:
        return "clear"
    return "ignore"
