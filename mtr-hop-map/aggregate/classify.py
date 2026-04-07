from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


BRISANET_ASNS = {"AS28126"}
BRISANET_COMPANY_HINTS = {"BRISANET", "BRISANET SERVICOS DE TELECOMUNICACOES S.A"}
CDN_ASNS = {"AS13335", "AS15169", "AS16509", "AS8075"}
CDN_COMPANY_HINTS = {"CLOUDFLARE", "AKAMAI", "GOOGLE", "AMAZON", "FASTLY", "MICROSOFT"}
IX_HINTS = {"IX", "PTT", "PEERING", "INTERCONEX", "EXCHANGE"}
DNS_HINTS = {"DNS", "RESOLVER", "NAMESERVER"}
KNOWN_DNS_IPS = {"1.0.0.1", "1.1.1.1", "8.8.8.8", "8.8.4.4"}


@dataclass
class NodeClassification:
    primary_class: str
    confidence: str
    evidence: list[str] = field(default_factory=list)
    source_type: str = "observed"
    subclasses: list[str] = field(default_factory=list)


def _upper(value: str) -> str:
    return value.upper()


def classify_node(node: dict[str, Any]) -> NodeClassification:
    ip = str(node.get("ip", ""))
    asn = str(node.get("asn", ""))
    company = str(node.get("company", ""))
    target = str(node.get("target", ""))
    observations = int(node.get("observations", 0))
    last_internal_count = int(node.get("last_internal_count", 0))
    edge_count = int(node.get("edge_count", 0))
    sample_count = int(node.get("sample_count", 0))
    path_count = int(node.get("path_count", 0))
    last_hop_count = int(node.get("last_hop_count", 0))

    evidence: list[str] = []
    subclasses: list[str] = []

    if ip in {"177.37.220.17", "177.37.220.18"}:
        return NodeClassification(
            primary_class="dns_infra_candidate",
            confidence="low",
            evidence=["absent_from_current_corpus", "watchlist_ip"],
            source_type="external_hint",
        )

    if ip in KNOWN_DNS_IPS:
        return NodeClassification(
            primary_class="dns_infra_candidate",
            confidence="high",
            evidence=[f"known_dns_ip={ip}", f"asn={asn}", f"company={company}"],
            source_type="observed",
        )

    upper_company = _upper(company)
    if asn in BRISANET_ASNS or any(hint in upper_company for hint in BRISANET_COMPANY_HINTS):
        evidence.append(f"asn={asn}")
        evidence.append(f"company={company}")
        subclasses.append("brisanet")
        if edge_count > 0 or last_internal_count > 0:
            primary = "edge_brisanet_candidate"
            if edge_count > 0:
                evidence.append(f"edge_count={edge_count}")
            if last_internal_count > 0:
                evidence.append(f"last_internal_count={last_internal_count}")
            confidence = "high" if edge_count >= 2 or last_internal_count >= 2 else "medium"
            return NodeClassification(primary, confidence, evidence, "observed", subclasses)
        confidence = "high" if observations >= 3 else "medium"
        return NodeClassification("internal_brisanet", confidence, evidence, "observed", subclasses)

    if any(hint in upper_company for hint in CDN_COMPANY_HINTS) or asn in CDN_ASNS:
        evidence.append(f"asn={asn}")
        evidence.append(f"company={company}")
        subclasses.append("cdn")
        confidence = "high" if observations >= 3 or last_hop_count > 0 else "medium"
        return NodeClassification("cdn_candidate", confidence, evidence, "observed", subclasses)

    if any(hint in _upper(target) for hint in IX_HINTS) or any(hint in upper_company for hint in IX_HINTS):
        evidence.append(f"target={target}")
        evidence.append(f"company={company}")
        return NodeClassification("ix_ptt_candidate", "low", evidence, "inferred")

    if any(hint in _upper(str(node.get("hostname", ""))) for hint in DNS_HINTS) or any(hint in upper_company for hint in DNS_HINTS):
        evidence.append(f"hostname={node.get('hostname', '')}")
        evidence.append(f"company={company}")
        return NodeClassification("dns_infra_candidate", "low", evidence, "inferred")

    if last_hop_count > 0 and asn not in {"AS???", "AS private"}:
        return NodeClassification(
            "destination",
            "medium" if last_hop_count >= 2 else "low",
            [f"last_hop_count={last_hop_count}", f"asn={asn}"],
            "observed",
        )

    if observations > 0 and (asn == "AS private" or "Private / local network" in company or ip.startswith("10.") or ip.startswith("172.16.") or ip.startswith("100.64.") or ip.startswith("100.65.")):
        evidence.append(f"asn={asn}")
        evidence.append(f"company={company}")
        if observations >= 3:
            confidence = "medium"
        else:
            confidence = "low"
        return NodeClassification("internal_brisanet", confidence, evidence, "observed", subclasses)

    if edge_count > 0 or last_internal_count > 0:
        evidence.append(f"edge_count={edge_count}")
        evidence.append(f"last_internal_count={last_internal_count}")
        return NodeClassification("edge_brisanet_candidate", "low", evidence, "inferred")

    return NodeClassification("unknown", "low", evidence or [f"asn={asn}", f"company={company}"], "inferred")
