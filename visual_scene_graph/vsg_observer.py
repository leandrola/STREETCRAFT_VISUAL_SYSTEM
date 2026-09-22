#!/usr/bin/env python3
"""VSG-0 Observer: deterministic, non-governing projection of SAR2.

The observer makes Streetcraft's current scene understanding inspectable.  It
does not modify SAR2, RR2, the Compact Generation Contract, preflight, or the
generation decision.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json

try:
    from .graph_locks import build_graph_locks
except ImportError:  # direct module execution used by portable validators
    from graph_locks import build_graph_locks

VSG_VERSION = "1.0.0"

NODE_TYPES = {
    "building", "facade", "storefront", "sign", "window", "door", "cornice",
    "roof", "parapet", "chimney", "hvac", "skylight", "water_tank",
    "access_bulkhead", "unknown_region", "unclassified",
}

ROOFTOP_TYPES = {
    "roof", "parapet", "chimney", "hvac", "skylight", "water_tank",
    "access_bulkhead",
}
GEOMETRY_TYPES = {
    "building", "facade", "storefront", "window", "door", "cornice",
    *ROOFTOP_TYPES,
}
RELATION_TYPES = {
    "ABOVE", "BELOW", "LEFT_OF", "RIGHT_OF", "ATTACHED_TO", "INSIDE",
    "BEHIND", "IN_FRONT_OF", "OCCLUDES", "CONTAINS", "PART_OF",
}

KIND_TO_TYPE = {
    "ARCHITECTURE": "building",
    "FACADE": "facade",
    "STOREFRONT": "storefront",
    "SIGNAGE": "sign",
    "SIGN": "sign",
    "WINDOW": "window",
    "DOOR": "door",
    "CORNICE": "cornice",
    "ROOF": "roof",
    "PARAPET": "parapet",
    "CHIMNEY": "chimney",
    "HVAC": "hvac",
    "SKYLIGHT": "skylight",
    "WATER_TANK": "water_tank",
    "ACCESS_BULKHEAD": "access_bulkhead",
    "OCCLUDED_REGION": "unknown_region",
}

CONFIDENCE = {"UNKNOWN": 0.0, "LOW": 0.35, "MEDIUM": 0.65, "HIGH": 0.9}


def _confidence(value) -> float:
    if isinstance(value, (int, float)):
        return round(max(0.0, min(1.0, float(value))), 4)
    return CONFIDENCE.get(str(value or "UNKNOWN").upper(), 0.0)


def _node_type(entity: dict) -> str:
    explicit = str(entity.get("vsg_type", "")).lower()
    if explicit in NODE_TYPES:
        return explicit
    return KIND_TO_TYPE.get(str(entity.get("kind", "")).upper(), "unclassified")


def _locks(entity: dict, relationships: list[dict]) -> dict:
    roles = set(entity.get("roles", []))
    preservation = entity.get("preservation_level")
    node_type = _node_type(entity)
    eid = entity["entity_id"]
    protected_occlusion = any(
        r.get("predicate") == "OCCLUDES"
        and eid in {r.get("subject"), r.get("object")}
        and r.get("protection") in {"PR0", "PR1"}
        for r in relationships
    )
    return {
        "identity": "IDENTITY_ANCHOR" in roles,
        "semantic": bool(entity.get("semantic_lock", False)) or (
            node_type == "sign" and preservation in {"P0", "P1"}
        ),
        "geometry": bool(entity.get("geometry_lock", False)) or (
            node_type in GEOMETRY_TYPES and preservation == "P0"
        ),
        "occlusion": protected_occlusion or "UNKNOWN_REGION" in roles,
    }


def _evidence(source: dict, fallback_reference_id: str | None = None) -> dict:
    evidence = {}
    reference_id = source.get("reference_id") or fallback_reference_id
    if reference_id:
        evidence["reference_id"] = reference_id
    if source.get("region") is not None:
        evidence["region"] = deepcopy(source["region"])
    if source.get("evidence_id"):
        evidence["evidence_id"] = source["evidence_id"]
    return evidence


def _circuit(name: str, node_ids: set[str], edges: list[dict]) -> dict:
    circuit_edges = [
        edge["id"] for edge in edges
        if edge["from"] in node_ids and edge["to"] in node_ids
    ]
    return {"name": name, "nodes": sorted(node_ids), "edges": sorted(circuit_edges)}


def _reference_observations(reference_reasoning: dict | None, reference_needs: list[dict] | None) -> list[dict]:
    """Retain RR2 routing/provenance without letting it govern the graph."""
    rr = reference_reasoning or {}
    needs = {need.get("need_id"): need for need in (reference_needs or [])}
    traces = {trace.get("need_id"): trace for trace in rr.get("trace", [])}
    projected: dict[str, list[dict]] = {}
    for item in rr.get("generation_projection", []):
        projected.setdefault(item.get("need_id"), []).append(item)
    observations = []
    for need_id in sorted(set(needs) | set(traces) | set(projected)):
        need = needs.get(need_id, {})
        trace = traces.get(need_id, {})
        items = projected.get(need_id, [])
        observations.append({
            "need_id": need_id,
            "target_node_id": need.get("target_entity_id"),
            "result": "ADMITTED" if items else trace.get("reason", "NO_PROJECTION"),
            "evidence_unit_ids": sorted(
                item["evidence_unit_id"] for item in items if item.get("evidence_unit_id")
            ),
            "evidence_bundle_ids": sorted(trace.get("evidence_bundle_ids", [])),
            "permitted_learning": sorted({
                value for item in items for value in item.get("permitted_learning", [])
            }),
            "forbidden_transfer": sorted({
                value for item in items for value in item.get("forbidden_transfer", [])
            }),
            "applied_transfers": [],
        })
    return observations


def build_visual_scene_graph(
    sar2: dict,
    *,
    reference_id: str | None = None,
    reference_sha256: str | None = None,
    reference_reasoning: dict | None = None,
    reference_needs: list[dict] | None = None,
) -> dict:
    """Project a SAR2 record into a passive, traceable VSG artifact."""
    relationships = sar2.get("relationships", [])
    nodes = []
    unclassified = []
    for entity in sar2.get("entities", []):
        node_type = _node_type(entity)
        if node_type == "unclassified":
            unclassified.append(entity["entity_id"])
        node = {
            "id": entity["entity_id"],
            "type": node_type,
            "source_kind": entity.get("kind", "UNKNOWN"),
            "label": entity.get("label", entity["entity_id"]),
            "confidence": _confidence(entity.get("confidence")),
            "epistemic_class": entity.get("epistemic_class", "UNKNOWN"),
            "observed": bool(entity.get("observed", False)),
            "locks": _locks(entity, relationships),
            "evidence": _evidence(entity, reference_id),
        }
        properties = deepcopy(entity.get("vsg_properties", {}))
        if entity.get("text") is not None:
            properties["text"] = entity["text"]
        if properties:
            node["properties"] = properties
        nodes.append(node)

    node_ids = {node["id"] for node in nodes}
    edges = []
    unsupported_relations = []
    dangling_relations = []
    for relation in relationships:
        predicate = str(relation.get("predicate", "")).upper()
        rid = relation.get("relationship_id", "UNIDENTIFIED")
        if relation.get("subject") not in node_ids or relation.get("object") not in node_ids:
            dangling_relations.append(rid)
            continue
        if predicate not in RELATION_TYPES:
            unsupported_relations.append(rid)
            continue
        edges.append({
            "id": rid,
            "type": predicate,
            "from": relation["subject"],
            "to": relation["object"],
            "confidence": _confidence(relation.get("confidence")),
            "protection": relation.get("protection", "PRX"),
            "epistemic_class": relation.get("epistemic_class", "UNKNOWN"),
            "evidence": _evidence(relation, reference_id),
        })

    nodes.sort(key=lambda item: item["id"])
    edges.sort(key=lambda item: item["id"])
    type_by_id = {node["id"]: node["type"] for node in nodes}
    semantic_ids = {node["id"] for node in nodes if node["locks"]["semantic"]}
    rooftop_ids = {nid for nid, kind in type_by_id.items() if kind in ROOFTOP_TYPES}
    geometry_ids = {nid for nid, kind in type_by_id.items() if kind in GEOMETRY_TYPES}
    occlusion_ids = {
        endpoint for edge in edges if edge["type"] == "OCCLUDES"
        for endpoint in (edge["from"], edge["to"])
    } | {node["id"] for node in nodes if node["locks"]["occlusion"]}

    canonical_input = {
        "scene_id": sar2.get("scene_id"),
        "source_identity": sar2.get("source_identity"),
        "entities": sar2.get("entities", []),
        "relationships": relationships,
    }
    input_sha256 = hashlib.sha256(
        json.dumps(canonical_input, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    provenance = {
        "producer": "Streetcraft VSG-0 Observer",
        "sar_version": "SAR2",
        "rr_version": "RR2",
        "rr_status": (reference_reasoning or {}).get("status", "NOT_SUPPLIED"),
        "input_sha256": input_sha256,
        "node_count": len(nodes),
        "edge_count": len(edges),
    }
    if reference_sha256:
        provenance["reference_sha256"] = reference_sha256

    graph = {
        "schema_version": VSG_VERSION,
        "mode": "OBSERVER",
        "governs_generation": False,
        "scene_id": sar2.get("scene_id"),
        "source_identity": sar2.get("source_identity"),
        "nodes": nodes,
        "edges": edges,
        "reference_observations": _reference_observations(reference_reasoning, reference_needs),
        "functional_subgraphs": [
            _circuit("semantic_text", semantic_ids, edges),
            _circuit("rooftop", rooftop_ids, edges),
            _circuit("geometry", geometry_ids, edges),
            _circuit("occlusion", occlusion_ids, edges),
        ],
        "diagnostics": {
            "unclassified_nodes": sorted(unclassified),
            "unsupported_relations": sorted(unsupported_relations),
            "dangling_relations": sorted(dangling_relations),
        },
        "provenance": provenance,
    }
    graph["graph_locks"] = build_graph_locks(graph)
    return graph
