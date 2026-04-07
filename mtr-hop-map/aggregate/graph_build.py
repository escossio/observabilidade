from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from .classify import classify_node
from .loader import TraceSample


@dataclass
class AggregatedNode:
    ip: str
    asns: Counter[str]
    companies: Counter[str]
    hostnames: Counter[str]
    classes: Counter[str]
    observations: int
    sample_targets: set[str]
    sample_runs: set[str]
    path_count: int
    last_hop_count: int
    last_internal_count: int
    edge_count: int
    transitions_from: Counter[str]
    transitions_to: Counter[str]
    evidence: list[str]
    classification: dict[str, Any]


def build_aggregate(samples: list[TraceSample]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "ip": "",
        "asns": Counter(),
        "companies": Counter(),
        "hostnames": Counter(),
        "observations": 0,
        "sample_targets": set(),
        "sample_runs": set(),
        "sample_count": 0,
        "run_count": 0,
        "path_count": 0,
        "last_hop_count": 0,
        "last_internal_count": 0,
        "edge_count": 0,
        "transitions_from": Counter(),
        "transitions_to": Counter(),
    })
    path_counter: Counter[tuple[str, ...]] = Counter()
    target_counter: Counter[str] = Counter()
    run_counter: Counter[str] = Counter()
    last_internal_counter: Counter[str] = Counter()
    edge_counter: Counter[str] = Counter()
    class_counter: Counter[str] = Counter()
    unique_targets: set[str] = set()

    for sample in samples:
        run_counter[sample.run_id] += 1
        target_counter[sample.target] += 1
        unique_targets.add(sample.target)
        hops = [hop for hop in sample.hops if hop.get("ip")]
        path = tuple(hop["ip"] for hop in hops)
        path_counter[path] += 1
        last_internal_ip = None
        for idx, hop in enumerate(hops):
            ip = str(hop.get("ip", ""))
            node = nodes[ip]
            node["ip"] = ip
            node["observations"] += 1
            node["sample_targets"].add(sample.target)
            node["sample_runs"].add(sample.run_id)
            node["sample_count"] += 1
            node["run_count"] = len(node["sample_runs"])
            node["asns"][str(hop.get("asn", ""))] += 1
            node["companies"][str(hop.get("company", ""))] += 1
            node["hostnames"][str(hop.get("hostname", ""))] += 1
            if idx == len(hops) - 1:
                node["last_hop_count"] += 1
                node["evidence_last"] = hop
            if str(hop.get("asn", "")) == "AS28126" or "BRISANET" in str(hop.get("company", "")).upper():
                last_internal_ip = ip
            if idx > 0:
                prev_ip = str(hops[idx - 1]["ip"])
                node["transitions_from"][prev_ip] += 1
                nodes[prev_ip]["transitions_to"][ip] += 1
        if last_internal_ip:
            nodes[last_internal_ip]["last_internal_count"] += 1
            last_internal_counter[last_internal_ip] += 1
        if len(hops) >= 2:
            penultimate = hops[-2]
            if str(penultimate.get("asn", "")) == "AS28126" or "BRISANET" in str(penultimate.get("company", "")).upper():
                nodes[str(penultimate["ip"])]["edge_count"] += 1
                edge_counter[str(penultimate["ip"])] += 1

    inventory: list[dict[str, Any]] = []
    total_runs = len({sample.run_id for sample in samples}) or 1
    for ip, node in nodes.items():
        asn = node["asns"].most_common(1)[0][0] if node["asns"] else "AS???"
        company = node["companies"].most_common(1)[0][0] if node["companies"] else "Unknown"
        hostname = node["hostnames"].most_common(1)[0][0] if node["hostnames"] else ""
        run_count = len(node["sample_runs"])
        target_count = len(node["sample_targets"])
        recurrence_ratio = run_count / total_runs
        edge_stability_ratio = node["edge_count"] / run_count if run_count else 0.0
        record = {
            "ip": ip,
            "asn": asn,
            "company": company,
            "hostname": hostname,
            "observations": node["observations"],
            "sample_count": target_count,
            "target_count": target_count,
            "run_count": run_count,
            "path_count": len({sample.target for sample in samples if ip in [hop.get("ip") for hop in sample.hops]}),
            "last_hop_count": node["last_hop_count"],
            "last_internal_count": node["last_internal_count"],
            "edge_count": node["edge_count"],
            "recurrence_ratio": recurrence_ratio,
            "edge_stability_ratio": edge_stability_ratio,
            "transitions_from": dict(node["transitions_from"]),
            "transitions_to": dict(node["transitions_to"]),
        }
        classification = classify_node(record)
        class_counter[classification.primary_class] += 1
        record["classification"] = {
            "primary_class": classification.primary_class,
            "confidence": classification.confidence,
            "evidence": classification.evidence,
            "source_type": classification.source_type,
            "subclasses": classification.subclasses,
        }
        inventory.append(record)

    inventory.sort(key=lambda item: (-item["observations"], item["ip"]))
    edge_rankings = sorted(
        (item for item in inventory if item["edge_count"] > 0 or item["last_internal_count"] > 0),
        key=lambda item: (-item["edge_count"], -item["last_internal_count"], -item["observations"], item["ip"]),
    )
    internal_rankings = sorted(
        (item for item in inventory if item["classification"]["primary_class"] in {"internal_brisanet", "edge_brisanet_candidate"}),
        key=lambda item: (-item["observations"], item["ip"]),
    )
    cdn_rankings = sorted(
        (item for item in inventory if item["classification"]["primary_class"] == "cdn_candidate"),
        key=lambda item: (-item["observations"], item["ip"]),
    )
    ix_rankings = sorted(
        (item for item in inventory if item["classification"]["primary_class"] == "ix_ptt_candidate"),
        key=lambda item: (-item["observations"], item["ip"]),
    )
    dns_rankings = sorted(
        (item for item in inventory if item["classification"]["primary_class"] == "dns_infra_candidate"),
        key=lambda item: (-item["observations"], item["ip"]),
    )

    sample_pairs = Counter()
    for sample in samples:
        ips = [hop["ip"] for hop in sample.hops if hop.get("ip")]
        for left, right in zip(ips, ips[1:]):
            sample_pairs[(left, right)] += 1

    return {
        "samples": samples,
        "inventory": inventory,
        "path_counter": path_counter,
        "sample_pairs": sample_pairs,
        "target_counter": target_counter,
        "run_counter": run_counter,
        "last_internal_counter": last_internal_counter,
        "edge_counter": edge_counter,
        "class_counter": class_counter,
        "unique_targets": sorted(unique_targets),
        "edge_rankings": edge_rankings,
        "internal_rankings": internal_rankings,
        "cdn_rankings": cdn_rankings,
        "ix_rankings": ix_rankings,
        "dns_rankings": dns_rankings,
    }
