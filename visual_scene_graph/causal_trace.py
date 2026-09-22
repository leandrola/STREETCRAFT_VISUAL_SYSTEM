"""VSG-1.5: immutable, deterministic traces over supplied structured snapshots."""
from __future__ import annotations

from collections import deque
from copy import deepcopy
import json

from .diagnostic_benchmark.diagnostic_engine import (
    TRACE_STAGES, check_causal_graph_locks, diagnose_causal_snapshots,
    snapshot_sha256 as canonical_sha256,
)

TRACE_VERSION = "1.5.0"
INPUTS = ("expected_graph", "sar2", "reference_reasoning", "vsg",
          "graph_lock_validation", "shadow_contract", "observed_output_graph", "diagnosis")
STAGE_ARTIFACT = dict(zip(TRACE_STAGES, (
    "expected_graph", "sar2", "reference_reasoning", "vsg", "vsg",
    "shadow_contract", "observed_output_graph", "diagnosis")))


def trace_sha256(trace):
    return canonical_sha256({k: v for k, v in trace.items() if k != "trace_sha256"})


def resolve_artifact_ref(ref, artifacts):
    """Resolve artifact-name#JSON-pointer; missing things reference their container."""
    name, sep, pointer = ref.partition("#")
    if not sep or name not in artifacts or artifacts[name] is None:
        raise ValueError(f"Unresolved artifact reference: {ref}")
    value = artifacts[name]
    if pointer:
        if not pointer.startswith("/"):
            raise ValueError(f"Invalid JSON pointer: {ref}")
        for token in pointer[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(value, list):
                if not token.isdigit() or str(int(token)) != token:
                    raise ValueError(f"Invalid array index: {ref}")
                value = value[int(token)]
            else:
                value = value[token]
    return value


def _pointer(artifact, path):
    return artifact + "#" + path


def _item_ref(artifacts, artifact, path, key, target):
    collection = resolve_artifact_ref(_pointer(artifact, path), artifacts)
    for i, item in enumerate(collection):
        if (item.get(key) if key else item) == target:
            return _pointer(artifact, path + f"/{i}"), True
    return _pointer(artifact, path), False


def _location(stage, kind, target, artifacts):
    artifact = STAGE_ARTIFACT[stage]
    if stage == "GRAPH_LOCKS":
        return _item_ref(artifacts, "vsg", "/graph_locks/items", "id", target)
    if stage == "SHADOW_COMPILER":
        path = {"NODE": "/required_nodes", "EDGE": "/required_edges", "LOCK": "/required_locks"}
        if kind == "REFERENCE":
            locks = artifacts["expected_graph"]["graph_locks"]["items"]
            lock = next((l for l in locks if l["type"] == "REFERENCE_ISOLATION_LOCK"
                         and l["expected"]["need_id"] == target), None)
            return _item_ref(artifacts, artifact, "/required_locks", None, lock["id"] if lock else target)
        return _item_ref(artifacts, artifact, path[kind], None, target)
    if stage == "RR2":
        return _item_ref(artifacts, artifact, "/generation_projection", "need_id", target)
    paths = {"NODE": ("/entities", "entity_id") if stage == "SAR2" else ("/nodes", "id"),
             "EDGE": ("/relationships", "relationship_id") if stage == "SAR2" else ("/edges", "id"),
             "REFERENCE": ("/reference_observations", "need_id"),
             "LOCK": ("/graph_locks/items", "id")}
    path, key = paths[kind]
    return _item_ref(artifacts, artifact, path, key, target)


def _input_issues(artifacts):
    required = {
        "expected_graph": {"scene_id": str, "nodes": list, "edges": list,
                           "reference_observations": list, "graph_locks": dict},
        "sar2": {"scene_id": str, "entities": list, "relationships": list},
        "reference_reasoning": {"generation_projection": list, "trace": list},
        "vsg": {"scene_id": str, "nodes": list, "edges": list,
                "reference_observations": list, "graph_locks": dict},
        "shadow_contract": {"required_nodes": list, "required_edges": list,
                            "semantic_text": dict, "required_locks": list},
        "observed_output_graph": {"nodes": list, "edges": list, "reference_observations": list},
        "graph_lock_validation": {"findings": list}, "diagnosis": {"findings": list},
    }
    issues = []
    for name, fields in required.items():
        value = artifacts[name]
        if not isinstance(value, dict):
            issues.append({"artifact": name, "reason": "SNAPSHOT_MISSING"})
            continue
        for key, kind in fields.items():
            if not isinstance(value.get(key), kind):
                issues.append({"artifact": name, "reason": "FIELD_MISSING_OR_INVALID", "field": key})
        if "graph_locks" in fields and isinstance(value.get("graph_locks"), dict):
            if not isinstance(value["graph_locks"].get("items"), list):
                issues.append({"artifact": name, "reason": "LOCK_LEDGER_UNAVAILABLE"})
    for name, value in artifacts.items():
        if not isinstance(value, dict):
            continue
        collections = [(key, value.get(key)) for key in ("nodes", "edges", "entities", "relationships", "reference_observations")]
        if isinstance(value.get("graph_locks"), dict):
            collections.append(("locks", value["graph_locks"].get("items")))
        for key, rows in collections:
            if not isinstance(rows, list):
                continue
            identity_key = {"entities": "entity_id", "relationships": "relationship_id",
                            "reference_observations": "need_id"}.get(key, "id")
            ids = [row.get(identity_key) if isinstance(row, dict) else None for row in rows]
            if any(not isinstance(i, str) or not i for i in ids) or len(ids) != len(set(ids)):
                issues.append({"artifact": name, "reason": "AMBIGUOUS_OR_MISSING_ID", "field": key})
    return issues


def _event_id(scene_id, stage, kind, identity):
    return "EV-" + canonical_sha256([scene_id, stage, kind, identity])[:24]


def _seal(trace):
    trace = deepcopy(trace)
    trace["trace_sha256"] = trace_sha256(trace)
    return trace


def build_causal_trace(*, expected_graph, sar2, reference_reasoning, vsg,
                       graph_lock_validation, shadow_contract, observed_output_graph,
                       diagnosis):
    """Observe supplied snapshots. Never query, generate, repair or mutate inputs.

    expected_graph is structured source evidence, not a pixel interpretation.
    Pass None for any unavailable stage; empty/absent snapshots are not invented.
    """
    artifacts = {name: value for name, value in locals().items() if name in INPUTS}
    issues = _input_issues(artifacts)
    provenance = {name: {"sha256": canonical_sha256(value), "artifact_ref": name + "#"}
                  for name, value in artifacts.items() if value is not None}
    scene_id = (expected_graph or {}).get("scene_id", "UNKNOWN") if isinstance(expected_graph, dict) else "UNKNOWN"
    trace = {"trace_version": TRACE_VERSION, "mode": "TRACE_ONLY", "governs_generation": False,
             "trace_id": "TRACE-" + canonical_sha256(provenance)[:24], "scene_id": scene_id,
             "status": "INCOMPLETE", "root_cause": None, "events": [], "causal_edges": [],
             "symptoms": [], "independent_findings": [], "unresolved_inputs": issues,
             "provenance": provenance}
    if not issues:
        base = {k: artifacts[k] for k in INPUTS if k not in {"diagnosis", "graph_lock_validation"}}
        try:
            computed_locks = check_causal_graph_locks(**base)
            computed_diagnosis = diagnose_causal_snapshots(**base)
            for name, computed in (("graph_lock_validation", computed_locks), ("diagnosis", computed_diagnosis)):
                if canonical_sha256(computed) != canonical_sha256(artifacts[name]):
                    issues.append({"artifact": name, "reason": "SNAPSHOT_DOES_NOT_MATCH_INPUTS"})
            if sar2["scene_id"] != scene_id or vsg["scene_id"] != scene_id:
                issues.append({"artifact": "sar2/vsg", "reason": "SCENE_ID_MISMATCH"})
        except (KeyError, TypeError, ValueError, IndexError, AttributeError) as exc:
            issues.append({"artifact": "pipeline", "reason": "MALFORMED_SNAPSHOT", "detail": str(exc)})
    if issues:
        # Only record snapshots actually present; no absent-stage stand-ins.
        for name, record in provenance.items():
            stage = next((s for s, a in STAGE_ARTIFACT.items() if a == name), "GRAPH_LOCKS")
            trace["events"].append({"event_id": _event_id(scene_id, stage, "SNAPSHOT", name),
                                    "stage": stage, "artifact_kind": "SNAPSHOT", "artifact_id": name,
                                    "artifact_ref": record["artifact_ref"], "operation": "SUPPLIED_SNAPSHOT",
                                    "status": "PRESENT", "input_refs": [], "output_refs": [record["artifact_ref"]],
                                    "evidence_refs": [], "lock_ids": [], "confidence": 1.0})
        return _seal(trace)

    findings = diagnosis["findings"]
    events, by_subject, edges = trace["events"], {}, set()

    def edge(a, b, relation):
        if a and b and a != b:
            edges.add((a["event_id"], b["event_id"], relation))

    def event(stage, kind, identity):
        ref, present = _location(stage, kind, identity, artifacts)
        source_ref, _ = _location("SOURCE_EVIDENCE", kind, identity, artifacts)
        bad = [f for f in findings if (f["stage"], f["target_kind"], f["target"]) == (stage, kind, identity)]
        status = "PRESENT" if present else "MISSING"
        if stage == "RR2":
            status = "ADMITTED" if present else "REJECTED"
        if bad and present:
            status = "ALTERED"
        evidence = [source_ref]
        if kind == "REFERENCE":
            for i, row in enumerate(reference_reasoning["trace"]):
                if row.get("need_id") == identity:
                    evidence.append(f"reference_reasoning#/trace/{i}")
        node = {"event_id": _event_id(scene_id, stage, kind, identity), "stage": stage,
                "artifact_kind": kind, "artifact_id": identity, "artifact_ref": ref,
                "operation": "INSPECT" if present else "ABSENCE_CHECK", "status": status,
                "input_refs": [], "output_refs": [ref] if present else [],
                "evidence_refs": evidence, "confidence": 1.0,
                "lock_ids": sorted({l for f in bad for l in f["lock_ids"]})}
        by_subject[stage, kind, identity] = node
        events.append(node)
        return node

    for kind, field, key in (("NODE", "nodes", "id"), ("EDGE", "edges", "id"),
                             ("REFERENCE", "reference_observations", "need_id")):
        identities = set(row[key] for row in expected_graph[field]) | set(row[key] for row in vsg[field])
        stages = ("SOURCE_EVIDENCE", "RR2" if kind == "REFERENCE" else "SAR2",
                  "VSG", "SHADOW_COMPILER", "OBSERVED_OUTPUT")
        for identity in sorted(identities):
            prev = None
            for stage, relation in zip(stages, ("PRODUCED", "PRODUCED", "PROJECTED_TO", "REQUIRED_BY", "OBSERVED_AS")):
                current = event(stage, kind, identity)
                if prev:
                    current["input_refs"] = [prev["artifact_ref"]]
                edge(prev, current, relation)
                prev = current
    # An edge depends on its endpoint entities, including absent endpoint checks.
    for row in expected_graph["edges"]:
        for stage in ("SAR2", "VSG", "SHADOW_COMPILER", "OBSERVED_OUTPUT"):
            for endpoint in (row["from"], row["to"]):
                edge(by_subject.get((stage, "NODE", endpoint)),
                     by_subject.get((stage, "EDGE", row["id"])), "REQUIRED_BY")
    for lock in sorted(expected_graph["graph_locks"]["items"], key=lambda l: l["id"]):
        kind, target = lock["target"]["kind"], lock["target"]["id"]
        if lock["type"] == "REFERENCE_ISOLATION_LOCK":
            kind, target = "REFERENCE", lock["expected"]["need_id"]
        owner = by_subject.get(("VSG", kind, target))
        locked = event("GRAPH_LOCKS", "LOCK", lock["id"])
        locked["lock_ids"] = [lock["id"]]
        required = event("SHADOW_COMPILER", "LOCK", lock["id"])
        required["lock_ids"] = [lock["id"]]
        edge(owner, locked, "LOCKED_BY")
        edge(locked, required, "REQUIRED_BY")
        edge(required, by_subject.get(("OBSERVED_OUTPUT", kind, target)), "OBSERVED_AS")

    primary = findings[0] if findings else None
    primary_event = by_subject.get((primary["stage"], primary["target_kind"], primary["target"])) if primary else None
    adjacency = {}
    for a, b, _ in edges:
        adjacency.setdefault(a, set()).add(b)
    def reachable(a, b):
        todo, seen = [a], set()
        while todo:
            v = todo.pop()
            if v == b:
                return True
            if v not in seen:
                seen.add(v); todo.extend(adjacency.get(v, ()))
        return False
    for i, f in enumerate(findings):
        cause = by_subject[f["stage"], f["target_kind"], f["target"]]
        ref = cause["artifact_ref"]
        if "SEMANTIC_LOCK_OMISSION" in f["code"]:
            ref = "shadow_contract#/semantic_text"
        diagnostic = {"event_id": _event_id(scene_id, "DIAGNOSTIC", "FINDING", str(i)),
                      "stage": "DIAGNOSTIC", "artifact_kind": "FINDING", "artifact_id": f["code"] + ":" + f["target"],
                      "artifact_ref": f"diagnosis#/findings/{i}", "operation": f["code"], "status": "INVALID",
                      "input_refs": [ref], "output_refs": [], "evidence_refs": cause["evidence_refs"],
                      "confidence": 1.0, "lock_ids": f["lock_ids"]}
        events.append(diagnostic)
        edge(cause, diagnostic, "CAUSED")
        record = {"stage": f["stage"], "code": f["code"], "artifact_id": f["target"],
                  "artifact_ref": ref, "event_id": cause["event_id"],
                  "diagnostic_event": diagnostic["event_id"], "lock_ids": f["lock_ids"], "confidence": 1.0}
        if len(f["lock_ids"]) == 1:
            record["lock_id"] = f["lock_ids"][0]
        if i == 0:
            trace["root_cause"] = record
        elif reachable(primary_event["event_id"], cause["event_id"]):
            record["caused_by"] = primary_event["event_id"]
            trace["symptoms"].append(record)
            edge(primary_event, diagnostic, "CAUSED")
        else:
            trace["independent_findings"].append(record)
    # Store an explicit, inspectable source-to-finding path as well as the DAG.
    sources = sorted(e["event_id"] for e in events if e["stage"] == "SOURCE_EVIDENCE")
    adjacency = {}
    for a, b, _ in sorted(edges):
        adjacency.setdefault(a, []).append(b)
    def path_to(target):
        todo = deque((source, [source]) for source in sources)
        seen = set()
        while todo:
            current, path = todo.popleft()
            if current == target:
                return path
            if current not in seen:
                seen.add(current)
                todo.extend((next_id, path + [next_id]) for next_id in adjacency.get(current, []))
        return []
    for record in ([trace["root_cause"]] if primary else []) + trace["symptoms"] + trace["independent_findings"]:
        record["causal_path"] = path_to(record["event_id"]) + [record["diagnostic_event"]]
    trace["status"] = "FAILURE_LOCALIZED" if primary else "HEALTHY"
    trace["events"] = sorted(events, key=lambda e: (TRACE_STAGES.index(e["stage"]), e["event_id"]))
    trace["causal_edges"] = [{"from_event": a, "to_event": b, "relation": r} for a, b, r in sorted(edges)]
    return _seal(trace)


def validate_causal_trace(trace, artifacts):
    """Validate links/DAG/hash and replay the benchmark to prevent causal forgery."""
    errors = []
    events = trace.get("events", [])
    ids = [e.get("event_id") for e in events]
    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE_EVENT_ID")
    by_id = {e.get("event_id"): e for e in events}
    unresolved = 0
    def inspect(value):
        nonlocal unresolved
        if isinstance(value, dict):
            for key, v in value.items():
                refs = [v] if key == "artifact_ref" else v if key in {"input_refs", "output_refs", "evidence_refs"} else []
                for ref in refs:
                    try: resolve_artifact_ref(ref, artifacts)
                    except (ValueError, KeyError, IndexError, TypeError, AttributeError):
                        unresolved += 1; errors.append("UNRESOLVED_ARTIFACT_REF")
                inspect(v)
        elif isinstance(value, list):
            for v in value: inspect(v)
    inspect(trace)
    for record in ([trace.get("root_cause")] if trace.get("root_cause") else []) + trace.get("symptoms", []) + trace.get("independent_findings", []):
        for ref in [record.get("event_id"), record.get("diagnostic_event"), *record.get("causal_path", [])] + ([record["caused_by"]] if "caused_by" in record else []):
            if ref not in by_id:
                unresolved += 1; errors.append("UNRESOLVED_EVENT_REF")
    adj, indegree = {i: [] for i in by_id}, {i: 0 for i in by_id}
    for edge in trace.get("causal_edges", []):
        a, b = edge.get("from_event"), edge.get("to_event")
        if a not in by_id or b not in by_id:
            unresolved += 1; errors.append("UNRESOLVED_EVENT_REF"); continue
        if by_id[a].get("stage") not in TRACE_STAGES or by_id[b].get("stage") not in TRACE_STAGES:
            errors.append("INVALID_STAGE"); continue
        if TRACE_STAGES.index(by_id[a]["stage"]) > TRACE_STAGES.index(by_id[b]["stage"]):
            errors.append("REVERSED_CAUSAL_ORDER")
        adj[a].append(b); indegree[b] += 1
    queue = deque(i for i, count in indegree.items() if count == 0)
    visited = 0
    while queue:
        a = queue.popleft(); visited += 1
        for b in adj[a]:
            indegree[b] -= 1
            if indegree[b] == 0: queue.append(b)
    cyclic_nodes = len(by_id) - visited
    if cyclic_nodes: errors.append("CAUSAL_CYCLE")
    root = trace.get("root_cause")
    if trace.get("status") == "FAILURE_LOCALIZED" and not isinstance(root, dict):
        errors.append("PRIMARY_ROOT_REQUIRED")
    if trace.get("status") in {"HEALTHY", "INCOMPLETE"} and root is not None:
        errors.append("UNSUPPORTED_ROOT_CAUSE")
    if trace.get("trace_sha256") != trace_sha256(trace): errors.append("HASH_MISMATCH")
    try:
        regenerated = build_causal_trace(**{key: artifacts.get(key) for key in INPUTS})
        if canonical_sha256(regenerated) != canonical_sha256(trace):
            errors.append("TRACE_REPLAY_MISMATCH")
        if regenerated != build_causal_trace(**{key: artifacts.get(key) for key in INPUTS}):
            errors.append("NONDETERMINISTIC_REPLAY")
    except (ValueError, KeyError, TypeError, IndexError):
        errors.append("INVALID_ARTIFACTS")
    return {"status": "FAIL" if errors else "PASS", "errors": sorted(set(errors)),
            "unresolved_references": unresolved, "cycle_count": 1 if cyclic_nodes else 0,
            "trace_status": trace.get("status"), "deterministic": "NONDETERMINISTIC_REPLAY" not in errors}


def render_causal_trace(trace):
    """Readable diagnostic summary; never a generation instruction."""
    lines = [f"{trace['trace_id']} · {trace['status']} · TRACE_ONLY"]
    if trace["unresolved_inputs"]:
        lines.extend(f"Missing/inconsistent input: {i['artifact']} — {i['reason']}"
                     for i in trace["unresolved_inputs"])
    if trace["root_cause"]:
        root = trace["root_cause"]
        lines.append(f"First incorrect transition: {root['stage']} / {root['code']} / {root['artifact_id']}")
        lines.append(f"Artifact: {root['artifact_ref']}")
        if root["lock_ids"]:
            lines.append("Locks: " + ", ".join(root["lock_ids"]))
        lines.extend(f"Symptom: {s['stage']} / {s['code']} / {s['artifact_id']}" for s in trace["symptoms"])
        lines.extend(f"Independent finding: {s['stage']} / {s['code']} / {s['artifact_id']}" for s in trace["independent_findings"])
    return "\n".join(lines)
