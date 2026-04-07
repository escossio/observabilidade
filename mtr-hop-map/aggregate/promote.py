from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


BACKBONE_MIN_RUNS = 8
BACKBONE_MIN_TARGETS = 3
BACKBONE_MIN_RATIO = 0.70
EDGE_MIN_RUNS = 8
EDGE_MIN_TARGETS = 3
EDGE_MIN_RATIO = 0.75


@dataclass(frozen=True)
class PromotedNode:
    ip: str
    role: str
    class_name: str
    label: str
    company: str
    confidence: str
    evidence: list[str]
    observations: int
    target_count: int
    run_count: int
    recurrence_ratio: float
    edge_count: int
    last_internal_count: int


@dataclass(frozen=True)
class PromotedEdge:
    source: str
    target: str
    role: str
    label: str
    confidence: str
    evidence: list[str]
    observations: int
    target_count: int
    run_count: int
    stability_ratio: float


def _recurrence_ratio(row: dict[str, Any]) -> float:
    return float(row.get("recurrence_ratio", 0.0))


def _edge_ratio(row: dict[str, Any]) -> float:
    return float(row.get("edge_stability_ratio", 0.0))


def _confidence_weight(confidence: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(confidence, 0)


def promote_structure(aggregate: dict[str, Any]) -> dict[str, Any]:
    inventory = {row["ip"]: row for row in aggregate["inventory"]}
    path_counter = aggregate["path_counter"]
    dominant_path = []
    if path_counter:
        dominant_path = list(path_counter.most_common(1)[0][0])

    backbone_nodes: list[PromotedNode] = []
    candidate_nodes: list[PromotedNode] = []
    watchlist_nodes: list[PromotedNode] = []

    for row in aggregate["inventory"]:
        class_name = row["classification"]["primary_class"]
        recurrence_ratio = _recurrence_ratio(row)
        edge_ratio = _edge_ratio(row)
        if class_name == "internal_brisanet" and row["run_count"] >= BACKBONE_MIN_RUNS and row["target_count"] >= BACKBONE_MIN_TARGETS and recurrence_ratio >= BACKBONE_MIN_RATIO:
            backbone_nodes.append(
                PromotedNode(
                    ip=row["ip"],
                    role="backbone_observed",
                    class_name=class_name,
                    label=f"{row['ip']}\nbackbone observed\nruns {row['run_count']}/{row['target_count']}",
                    company=row["company"],
                    confidence=row["classification"]["confidence"],
                    evidence=row["classification"]["evidence"],
                    observations=row["observations"],
                    target_count=row["target_count"],
                    run_count=row["run_count"],
                    recurrence_ratio=recurrence_ratio,
                    edge_count=row["edge_count"],
                    last_internal_count=row["last_internal_count"],
                )
            )
        elif class_name == "edge_brisanet_candidate" and row["edge_count"] >= EDGE_MIN_RUNS and row["target_count"] >= EDGE_MIN_TARGETS and edge_ratio >= EDGE_MIN_RATIO:
            candidate_nodes.append(
                PromotedNode(
                    ip=row["ip"],
                    role="edge_brisanet_candidate",
                    class_name=class_name,
                    label=f"{row['ip']}\n[candidate]\nedge {row['edge_count']} conf {row['classification']['confidence']}",
                    company=row["company"],
                    confidence=row["classification"]["confidence"],
                    evidence=row["classification"]["evidence"],
                    observations=row["observations"],
                    target_count=row["target_count"],
                    run_count=row["run_count"],
                    recurrence_ratio=recurrence_ratio,
                    edge_count=row["edge_count"],
                    last_internal_count=row["last_internal_count"],
                )
            )
        elif class_name == "cdn_candidate" and row["run_count"] >= 2:
            candidate_nodes.append(
                PromotedNode(
                    ip=row["ip"],
                    role="cdn_candidate",
                    class_name=class_name,
                    label=f"{row['ip']}\nCDN candidate\n{row['company']}\nconf {row['classification']['confidence']}",
                    company=row["company"],
                    confidence=row["classification"]["confidence"],
                    evidence=row["classification"]["evidence"],
                    observations=row["observations"],
                    target_count=row["target_count"],
                    run_count=row["run_count"],
                    recurrence_ratio=recurrence_ratio,
                    edge_count=row["edge_count"],
                    last_internal_count=row["last_internal_count"],
                )
            )
        elif class_name == "dns_infra_candidate":
            watchlist_nodes.append(
                PromotedNode(
                    ip=row["ip"],
                    role="dns_watchlist",
                    class_name=class_name,
                    label=f"{row['ip']}\nDNS watchlist\nconf {row['classification']['confidence']}",
                    company=row["company"],
                    confidence=row["classification"]["confidence"],
                    evidence=row["classification"]["evidence"],
                    observations=row["observations"],
                    target_count=row["target_count"],
                    run_count=row["run_count"],
                    recurrence_ratio=recurrence_ratio,
                    edge_count=row["edge_count"],
                    last_internal_count=row["last_internal_count"],
                )
            )

    backbone_nodes.sort(key=lambda node: dominant_path.index(node.ip) if node.ip in dominant_path else 999)
    candidate_nodes.sort(key=lambda node: (-node.edge_count, -node.run_count, node.ip))
    watchlist_nodes.sort(key=lambda node: (-node.run_count, node.ip))

    backbone_ips = {node.ip for node in backbone_nodes}
    candidate_edge = next((node for node in candidate_nodes if node.role == "edge_brisanet_candidate"), None)
    cdn_nodes = [node for node in candidate_nodes if node.role == "cdn_candidate"]
    dns_nodes = [node for node in watchlist_nodes if node.role == "dns_watchlist"]

    promoted_edges: list[PromotedEdge] = []
    if dominant_path:
        for left, right in zip(dominant_path, dominant_path[1:]):
            left_row = inventory.get(left)
            right_row = inventory.get(right)
            if not left_row or not right_row:
                continue
            if left in backbone_ips and right in backbone_ips:
                promoted_edges.append(
                    PromotedEdge(
                        source=left,
                        target=right,
                        role="backbone_observed",
                        label=f"{left} -> {right}",
                        confidence="high" if left_row["run_count"] >= BACKBONE_MIN_RUNS and right_row["run_count"] >= BACKBONE_MIN_RUNS else "medium",
                        evidence=["dominant_path", f"pair_runs={min(left_row['run_count'], right_row['run_count'])}"],
                        observations=min(left_row["observations"], right_row["observations"]),
                        target_count=min(left_row["target_count"], right_row["target_count"]),
                        run_count=min(left_row["run_count"], right_row["run_count"]),
                        stability_ratio=min(left_row["recurrence_ratio"], right_row["recurrence_ratio"]),
                    )
                )

    if backbone_nodes and candidate_edge:
        promoted_edges.append(
            PromotedEdge(
                source=backbone_nodes[-1].ip,
                target=candidate_edge.ip,
                role="candidate_edge",
                label=f"{backbone_nodes[-1].ip} -> {candidate_edge.ip}",
                confidence=candidate_edge.confidence,
                evidence=["edge_brisanet_candidate", *candidate_edge.evidence],
                observations=candidate_edge.observations,
                target_count=candidate_edge.target_count,
                run_count=candidate_edge.run_count,
                stability_ratio=candidate_edge.recurrence_ratio,
            )
        )

    if candidate_edge:
        for cdn in cdn_nodes:
            promoted_edges.append(
                PromotedEdge(
                    source=candidate_edge.ip,
                    target=cdn.ip,
                    role="cdn_exit",
                    label=f"{candidate_edge.ip} -> {cdn.ip}",
                    confidence=cdn.confidence,
                    evidence=["cdn_candidate", *cdn.evidence],
                    observations=cdn.observations,
                    target_count=cdn.target_count,
                    run_count=cdn.run_count,
                    stability_ratio=cdn.recurrence_ratio,
                )
            )

    promoted_edges.sort(key=lambda edge: (edge.role, edge.source, edge.target))

    return {
        "meta": {
            "rules": {
                "node": {
                    "min_runs": BACKBONE_MIN_RUNS,
                    "min_targets": BACKBONE_MIN_TARGETS,
                    "min_ratio": BACKBONE_MIN_RATIO,
                },
                "edge": {
                    "min_runs": EDGE_MIN_RUNS,
                    "min_targets": EDGE_MIN_TARGETS,
                    "min_ratio": EDGE_MIN_RATIO,
                },
            },
            "map_name": "MTR Backbone - Brisanet Observed",
        },
        "promoted_nodes": {
            "backbone_observed": [asdict(node) for node in backbone_nodes],
            "candidate_nodes": [asdict(node) for node in candidate_nodes],
            "watchlist_nodes": [asdict(node) for node in watchlist_nodes],
        },
        "promoted_edges": {
            "backbone_observed": [asdict(edge) for edge in promoted_edges if edge.role == "backbone_observed"],
            "candidate_edges": [asdict(edge) for edge in promoted_edges if edge.role != "backbone_observed"],
        },
        "canonical_path": dominant_path,
    }
