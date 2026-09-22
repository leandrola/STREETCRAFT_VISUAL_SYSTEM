#!/usr/bin/env python3
"""VSG-1 normalized graph-lock ledger and candidate validation."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
import re

LOCK_VERSION = "1.0.0"
LOCK_TYPES = {
    "SEMANTIC_TEXT_LOCK",
    "GEOMETRY_LOCK",
    "OCCLUSION_LOCK",
    "REFERENCE_ISOLATION_LOCK",
}


def _by_id(items: list[dict]) -> dict[str, dict]:
    return {item["id"]: item for item in items if item.get("id")}


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Z0-9_-]+", "-", str(value).upper()).strip("-")


def _edge_signature(edge: dict) -> dict:
    return {
        "id": edge["id"],
        "type": edge["type"],
        "from": edge["from"],
        "to": edge["to"],
    }


def _lock(lock_id: str, lock_type: str, target_kind: str, target_id: str,
          strength: str, expected: dict, provenance: dict) -> dict:
    return {
        "id": lock_id,
        "type": lock_type,
        "target": {"kind": target_kind, "id": target_id},
        "strength": strength,
        "enforcement": "VALIDATE_ONLY",
        "expected": expected,
        "provenance": provenance,
    }


def build_graph_locks(graph: dict) -> dict:
    """Build one deterministic lock ledger from a VSG graph."""
    nodes = _by_id(graph.get("nodes", []))
    edges = _by_id(graph.get("edges", []))
    items = []
    warnings = []

    for node_id, node in sorted(nodes.items()):
        flags = node.get("locks", {})
        if flags.get("semantic"):
            text = node.get("properties", {}).get("text")
            if text is None:
                warnings.append({"code": "SEMANTIC_LOCK_WITHOUT_TEXT", "target": node_id})
            else:
                items.append(_lock(
                    f"GL-SEM-{_safe_id(node_id)}", "SEMANTIC_TEXT_LOCK", "NODE", node_id,
                    "ABSOLUTE", {"text": text, "node_type": node.get("type")},
                    {"source": "VSG_NODE_LOCK", "evidence": deepcopy(node.get("evidence", {}))},
                ))
        if flags.get("geometry"):
            protected = [
                _edge_signature(edge) for edge in edges.values()
                if node_id in {edge.get("from"), edge.get("to")}
                and edge.get("protection") in {"PR0", "PR1"}
            ]
            protected.sort(key=lambda edge: edge["id"])
            items.append(_lock(
                f"GL-GEO-{_safe_id(node_id)}", "GEOMETRY_LOCK", "NODE", node_id,
                "ABSOLUTE", {
                    "node_type": node.get("type"),
                    "protected_topology": protected,
                },
                {"source": "VSG_NODE_LOCK", "evidence": deepcopy(node.get("evidence", {}))},
            ))

    occlusion_edges = set()
    for edge_id, edge in sorted(edges.items()):
        if edge.get("type") != "OCCLUDES" or edge.get("protection") not in {"PR0", "PR1"}:
            continue
        occlusion_edges.add(edge_id)
        items.append(_lock(
            f"GL-OCC-{_safe_id(edge_id)}", "OCCLUSION_LOCK", "EDGE", edge_id,
            "ABSOLUTE" if edge.get("protection") == "PR0" else "STRONG",
            {"edge": _edge_signature(edge), "protection": edge.get("protection")},
            {"source": "VSG_PROTECTED_RELATION", "evidence": deepcopy(edge.get("evidence", {}))},
        ))

    # Unknown regions can be occlusion-locked without an explicit visible edge.
    for node_id, node in sorted(nodes.items()):
        if not node.get("locks", {}).get("occlusion"):
            continue
        if any(node_id in {edges[eid].get("from"), edges[eid].get("to")} for eid in occlusion_edges):
            continue
        if node.get("type") != "unknown_region":
            continue
        items.append(_lock(
            f"GL-OCC-NODE-{_safe_id(node_id)}", "OCCLUSION_LOCK", "NODE", node_id,
            "ABSOLUTE", {
                "node_type": node.get("type"),
                "epistemic_class": node.get("epistemic_class"),
            },
            {"source": "VSG_UNKNOWN_REGION_LOCK", "evidence": deepcopy(node.get("evidence", {}))},
        ))

    for observation in sorted(graph.get("reference_observations", []), key=lambda item: item.get("need_id", "")):
        target_id = observation.get("target_node_id")
        need_id = observation.get("need_id")
        if observation.get("result") != "ADMITTED" or not target_id or not need_id:
            continue
        items.append(_lock(
            f"GL-REF-{_safe_id(need_id)}-{_safe_id(target_id)}",
            "REFERENCE_ISOLATION_LOCK", "NODE", target_id, "ABSOLUTE",
            {
                "need_id": need_id,
                "permitted_learning": sorted(set(observation.get("permitted_learning", []))),
                "forbidden_transfer": sorted(set(observation.get("forbidden_transfer", []))),
                "evidence_unit_ids": sorted(set(observation.get("evidence_unit_ids", []))),
            },
            {"source": "RR2_ADMISSION", "evidence_bundle_ids": deepcopy(observation.get("evidence_bundle_ids", []))},
        ))

    items.sort(key=lambda item: item["id"])
    counts = Counter(item["type"] for item in items)
    canonical = json.dumps(items, sort_keys=True, separators=(",", ":")).encode()
    return {
        "version": LOCK_VERSION,
        "mode": "VALIDATE_ONLY",
        "governs_generation": False,
        "items": items,
        "summary": {
            "total": len(items),
            "by_type": {lock_type: counts.get(lock_type, 0) for lock_type in sorted(LOCK_TYPES)},
            "warnings": warnings,
        },
        "ledger_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def _violation(lock: dict, code: str, observed=None) -> dict:
    finding = {
        "lock_id": lock.get("id"),
        "lock_type": lock.get("type"),
        "code": code,
        "severity": "S3" if lock.get("strength") == "ABSOLUTE" else "S2",
        "target": deepcopy(lock.get("target")),
    }
    if observed is not None:
        finding["observed"] = observed
    return finding


def validate_graph_locks(expected_graph: dict, candidate_graph: dict | None = None) -> dict:
    """Validate a candidate graph against the immutable ledger of expected_graph."""
    candidate = candidate_graph if candidate_graph is not None else expected_graph
    ledger = expected_graph.get("graph_locks", {})
    items = ledger.get("items", [])
    findings = []

    lock_ids = [item.get("id") for item in items]
    if len(lock_ids) != len(set(lock_ids)):
        findings.append({
            "lock_id": None, "lock_type": "LEDGER", "code": "DUPLICATE_LOCK_ID",
            "severity": "S3", "target": {"kind": "LEDGER", "id": "graph_locks"},
        })

    nodes = _by_id(candidate.get("nodes", []))
    edges = _by_id(candidate.get("edges", []))
    observations = {
        item.get("need_id"): item for item in candidate.get("reference_observations", [])
        if item.get("need_id")
    }

    for lock in items:
        lock_type = lock.get("type")
        target = lock.get("target", {})
        target_id = target.get("id")
        expected = lock.get("expected", {})
        if lock_type not in LOCK_TYPES:
            findings.append(_violation(lock, "UNKNOWN_LOCK_TYPE", lock_type))
            continue

        if lock_type == "SEMANTIC_TEXT_LOCK":
            node = nodes.get(target_id)
            if node is None:
                findings.append(_violation(lock, "SEMANTIC_TARGET_MISSING"))
            elif node.get("properties", {}).get("text") != expected.get("text"):
                findings.append(_violation(lock, "SEMANTIC_TEXT_LOCK_VIOLATION", node.get("properties", {}).get("text")))

        elif lock_type == "GEOMETRY_LOCK":
            node = nodes.get(target_id)
            if node is None:
                findings.append(_violation(lock, "GEOMETRY_NODE_MISSING"))
                continue
            if node.get("type") != expected.get("node_type"):
                findings.append(_violation(lock, "GEOMETRY_TYPE_CHANGED", node.get("type")))
            for signature in expected.get("protected_topology", []):
                observed = edges.get(signature["id"])
                if observed is None:
                    findings.append(_violation(lock, "GEOMETRY_TOPOLOGY_MISSING", signature["id"]))
                elif _edge_signature(observed) != signature:
                    findings.append(_violation(lock, "GEOMETRY_TOPOLOGY_CHANGED", _edge_signature(observed)))

        elif lock_type == "OCCLUSION_LOCK":
            if target.get("kind") == "EDGE":
                observed = edges.get(target_id)
                if observed is None:
                    findings.append(_violation(lock, "OCCLUSION_RELATION_MISSING"))
                elif _edge_signature(observed) != expected.get("edge"):
                    findings.append(_violation(lock, "OCCLUSION_RELATION_CHANGED", _edge_signature(observed)))
            else:
                node = nodes.get(target_id)
                if node is None:
                    findings.append(_violation(lock, "OCCLUSION_UNKNOWN_REGION_MISSING"))
                elif node.get("epistemic_class") != expected.get("epistemic_class"):
                    findings.append(_violation(lock, "OCCLUSION_UNKNOWN_RESOLVED", node.get("epistemic_class")))

        elif lock_type == "REFERENCE_ISOLATION_LOCK":
            observation = observations.get(expected.get("need_id"))
            if observation is None or observation.get("result") != "ADMITTED":
                findings.append(_violation(lock, "REFERENCE_OBSERVATION_MISSING"))
                continue
            applied = set(observation.get("applied_transfers", []))
            forbidden = set(expected.get("forbidden_transfer", []))
            leaked = sorted(applied & forbidden)
            if leaked:
                findings.append(_violation(lock, "REFERENCE_ISOLATION_VIOLATION", leaked))
            if observation.get("target_node_id") != target_id:
                findings.append(_violation(lock, "REFERENCE_TARGET_CHANGED", observation.get("target_node_id")))

    findings.sort(key=lambda item: (item.get("lock_id") or "", item["code"]))
    return {
        "version": LOCK_VERSION,
        "mode": "VALIDATE_ONLY",
        "status": "PASS" if not findings else "FAIL",
        "locks_checked": len(items),
        "findings": findings,
        "s3_count": sum(item["severity"] == "S3" for item in findings),
        "s2_count": sum(item["severity"] == "S2" for item in findings),
    }
