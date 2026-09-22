#!/usr/bin/env python3
"""Unified Streetcraft orchestration: CIL -> SAR2 -> CGC -> RR2/Archive -> hardening gate.

This module is the executable glue that was previously documented but not wired
end-to-end. It does not call an image vendor. Its terminal READY state means the
Compact Generation Contract is safe to hand to a model adapter.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
for rel in ("command_invocation", "scene_intelligence", "visual_scene_graph", "hardening", "reference_runtime", "patch"):
    p = str(ROOT / rel)
    if p not in sys.path:
        sys.path.insert(0, p)

from resolve_commands import resolve as resolve_commands
from scene_intelligence import build_scene_analysis_record, project_scene_to_cgc
from vsg_observer import build_visual_scene_graph
from operational_hardening import build_contract, material_delta_allowed
from reference_reasoning import resolve_reference, enrich_cgc
from svs_1_9_1_patch import classify_text_token, low_confidence_render_hint, patch_pre_generation_gate

DOMAIN_FEATURE_TYPE = {
    "SIGNAGE": "signage_style",
    "CAMERA": "camera",
    "REGIONAL_CHARACTER": "geography",
    "LIGHT_ATMOSPHERE": "atmosphere",
    "RAIN_SNOW_ASPHALT": "atmosphere",
    "ARCHITECTURE": "geometry",
    "STOREFRONT": "geometry",
    "STREET_FURNITURE": "prop",
    "TRANSIT_INFRASTRUCTURE": "geometry",
    "INDUSTRIAL": "geometry",
    "VEHICLES": "prop",
    "PEOPLE_ACTIVITY": "prop",
}


def _uniq(values):
    return list(dict.fromkeys(values))


def _resolved_config(request: dict) -> tuple[dict, dict]:
    command = resolve_commands(request.get("command_text", ""))
    if command["status"] == "ERROR":
        return command, {}
    cfg = deepcopy(command.get("config", {}))
    scene = request.get("scene", {})
    for key in ("profile", "mode", "camera"):
        if cfg.get(key) is None:
            cfg[key] = request.get(key) or scene.get(key)
    if not cfg.get("profile") or not cfg.get("mode") or not cfg.get("camera"):
        raise ValueError("Orchestration requires resolved profile, mode and camera")
    return command, cfg


def _scene_with_runtime_config(scene: dict, cfg: dict) -> dict:
    out = deepcopy(scene)
    out["mode"] = cfg["mode"]
    out["profile"] = cfg["profile"]
    return out


def _entity_map(sar2: dict) -> dict[str, dict]:
    return {e["entity_id"]: e for e in sar2.get("entities", [])}


def _need_from_hint(hint: dict, sar2: dict) -> dict:
    entity = _entity_map(sar2).get(hint["entity_id"], {})
    state = hint["state"]
    return {
        "need_id": f"SAR2-{hint['entity_id']}",
        "state": state,
        "target_domains": deepcopy(hint.get("target_domains", [])),
        "specific_problem": entity.get("reference_problem") or hint.get("reason") or f"Reference need for {hint['entity_id']}",
        "task_context": entity.get("reference_task_context", f"SAR2 {sar2['scene_id']}"),
        "source_context": entity.get("reference_source_context", entity.get("label", hint["entity_id"])),
        "min_provenance": entity.get("min_provenance", "P2"),
        "max_transfer_risk": entity.get("max_transfer_risk", "MEDIUM"),
        "max_results": entity.get("max_results", 3),
        "source_invariants": deepcopy(entity.get("source_invariants", [])),
        "forbidden_transfers": deepcopy(entity.get("forbidden_transfers", [])),
        "region": entity.get("region"),
        "period": entity.get("period"),
        "target_entity_id": hint["entity_id"],
    }


def _reference_needs(request: dict, sar2: dict) -> list[dict]:
    needs = [_need_from_hint(h, sar2) for h in sar2.get("reference_need_hints", [])]
    explicit = deepcopy(request.get("reference_needs", []))
    by_id = {n["need_id"]: n for n in needs}
    for n in explicit:
        by_id[n["need_id"]] = n
    return list(by_id.values())


def _draft_cgc(request: dict, cfg: dict, sar2: dict) -> dict:
    source_identity = request.get("source_identity") or sar2["source_identity"]
    delta = int(request.get("material_intensity_delta", 0))
    occ = list(sar2.get("unknown_locks", []))
    if cfg.get("occlusion_lock") == "LOCKED_UNKNOWN":
        occ = _uniq(occ + ["GLOBAL_LOCKED_UNKNOWN"])
    cgc = build_contract(
        source_identity, cfg["mode"], cfg["profile"], cfg["camera"],
        preserve=request.get("preserve", []), transform=request.get("transform", []),
        remove=request.get("remove", []), infer=request.get("infer", []),
        unknown=request.get("unknown", []), forbid=request.get("forbid", []),
        semantic_text_lock=request.get("semantic_text_lock", "STRICT"),
        material_intensity_delta=delta, occlusion_locks=occ,
    )
    cgc = project_scene_to_cgc(cgc, sar2)
    cgc["cil"] = {"commands": request.get("command_text", ""), "resolved": deepcopy(cfg)}
    hard_forbid = []
    if cfg.get("identity_lock") == "STRICT":
        hard_forbid += ["change_source_identity", "replace_P0_geometry"]
    if cfg.get("frontalization") == "STRICT":
        hard_forbid += ["camera_non_frontal", "oblique_camera_drift"]
    if cfg.get("preservation") == "STRICT_OBSERVED_EVIDENCE":
        hard_forbid += ["replace_observed_evidence"]
    if cfg.get("uncertainty") == "STRICT_UNKNOWN_PRESERVATION":
        hard_forbid += ["resolve_locked_unknown_without_evidence"]
    cgc["forbid"] = _uniq(cgc.get("forbid", []) + hard_forbid)
    if cfg.get("aspect_ratio"):
        cgc["aspect_ratio"] = cfg["aspect_ratio"]
    if cfg.get("street_presence"):
        cgc["street_presence"] = cfg["street_presence"]
    return cgc


def _reference_features(rr: dict, needs: list[dict]) -> list[dict]:
    need_by_id = {n["need_id"]: n for n in needs}
    out = []
    for p in rr.get("generation_projection", []):
        need = need_by_id.get(p["need_id"], {})
        domain = p.get("domain")
        f = {
            "evidence_unit_id": p.get("evidence_unit_id"),
            "domain": domain,
            "feature_type": DOMAIN_FEATURE_TYPE.get(domain, "documentary"),
            "value": p.get("visible_fact"),
            "permitted_learning": deepcopy(p.get("permitted_learning", [])),
            "forbidden_transfer": deepcopy(p.get("forbidden_transfer", [])),
        }
        target = need.get("target_entity_id")
        if target:
            f["target_entity_id"] = target
        if domain == "SIGNAGE":
            f["semantic_specificity"] = 0
        if domain == "RAIN_SNOW_ASPHALT":
            f["property"] = "surface_wetness"
        out.append(f)
    return out


def _text_plan(request: dict) -> tuple[list[dict], dict]:
    tokens = []
    for raw in request.get("text_tokens", []):
        if raw.get("state") in {"FROZEN_EXACT", "MASK_PARTIAL", "MASK_GRAPHIC_ONLY"}:
            token = deepcopy(raw)
        else:
            token = classify_text_token(
                raw.get("literal"), raw.get("confidence"),
                preservation_level=raw.get("preservation_level", "P2"),
                identity_bearing=bool(raw.get("identity_bearing", False)),
                numeral=bool(raw.get("numeral", False)),
            )
            if raw.get("token_id"):
                token["token_id"] = raw["token_id"]
        tokens.append(token)
    proposed = deepcopy(request.get("proposed_text", {}))
    if not proposed:
        for t in tokens:
            key = t.get("token_id") or t.get("literal")
            hint = low_confidence_render_hint(t)
            if hint["semantic_mode"] == "EXACT":
                proposed[key] = hint["literal"]
            elif hint["semantic_mode"] == "PARTIAL_ONLY":
                proposed[key] = hint.get("known_fragment") or None
            else:
                proposed[key] = None
    return tokens, proposed


def orchestrate(request: dict, *, archive_retriever=None) -> dict:
    """Resolve one Streetcraft request through the pre-generation boundary."""
    request = deepcopy(request)
    command, cfg = _resolved_config(request)
    if command.get("status") == "ERROR":
        return {"version": "SC-ORCH-1.0", "status": "COMMAND_ERROR", "command": command, "generation_ready": False}

    scene = _scene_with_runtime_config(request["scene"], cfg)
    sar2 = build_scene_analysis_record(**scene)
    vsg_config = request.get("vsg", {})
    cgc_draft = _draft_cgc(request, cfg, sar2)
    needs = _reference_needs(request, sar2)

    fear_city_confirmed = bool(request.get("fear_city_confirmed", False))
    occlusion_locked = bool(sar2.get("unknown_locks")) or cfg.get("occlusion_lock") == "LOCKED_UNKNOWN"
    rr = resolve_reference(
        needs=needs, profile=cfg["profile"], mode=cfg["mode"], camera=cfg["camera"],
        archive_retriever=archive_retriever,
        query_budget=request.get("query_budget", 4),
        allow_support=request.get("allow_support", True),
        semantic_text_lock=cgc_draft["semantic_text_lock"],
        occlusion_locked=occlusion_locked,
        fear_city_confirmed=fear_city_confirmed,
    )
    vsg = None
    if str(vsg_config.get("mode", "OFF")).upper() == "OBSERVER":
        vsg = build_visual_scene_graph(
            sar2,
            reference_id=vsg_config.get("reference_id"),
            reference_sha256=vsg_config.get("reference_sha256"),
            reference_reasoning=rr,
            reference_needs=needs,
        )

    base = {
        "version": "SC-ORCH-1.0", "command": command, "resolved_config": cfg,
        "sar2": sar2, "reference_needs": needs, "reference_reasoning": rr,
        "cgc_draft": cgc_draft, "generation_ready": False,
    }
    if vsg is not None:
        base["visual_scene_graph"] = vsg
    if rr["status"] != "READY":
        base["status"] = "BLOCKED_REFERENCE"
        base["block_reason"] = rr["status"]
        return base

    cgc_rr = enrich_cgc(cgc_draft, rr)
    ref_features = _reference_features(rr, needs) + deepcopy(request.get("reference_features", []))
    text_tokens, proposed_text = _text_plan(request)
    allowed_domains = {d for n in needs for d in n.get("target_domains", [])}
    source_entity_ids = {e["entity_id"] for e in sar2.get("entities", [])}
    camera_lock = cfg["camera"] if cfg["camera"] in {"CG-S", "CG-FC"} else None
    pre = patch_pre_generation_gate(
        text_tokens=text_tokens, proposed_text=proposed_text,
        fear_city_confirmed=fear_city_confirmed,
        proposed_geo_tokens=request.get("proposed_geo_tokens", []),
        source_authored_geo_tokens=request.get("source_authored_geo_tokens", []),
        reference_features=ref_features, allowed_domains=allowed_domains,
        source_entity_ids=source_entity_ids, camera_lock=camera_lock,
        source_states=request.get("source_states", {}),
    )

    material_ok = material_delta_allowed(
        cfg["mode"], cgc_rr["material_intensity_delta"],
        evidence_support=bool(request.get("material_delta_evidence_support", False)),
    )
    if not material_ok:
        finding = {"status": "FAIL", "severity": "S3", "code": "MATERIAL_INTENSITY_DELTA_BLOCK",
                   "mode": cfg["mode"], "requested": cgc_rr["material_intensity_delta"]}
        pre = deepcopy(pre)
        pre["findings"] = pre.get("findings", []) + [finding]
        pre["status"] = "BLOCK_GENERATION"

    cgc_final = deepcopy(cgc_rr)
    cgc_final["pre_generation_gate"] = deepcopy(pre)
    cgc_final["reference_features"] = deepcopy(ref_features)
    cgc_final["text_render_plan"] = {"tokens": text_tokens, "proposed_text": proposed_text}

    base["cgc_final"] = cgc_final
    base["pre_generation_gate"] = pre
    if pre["status"] == "PASS":
        base["status"] = "GENERATION_READY"
        base["generation_ready"] = True
    elif pre["status"] == "REVIEW_REQUIRED":
        base["status"] = "REVIEW_REQUIRED"
    else:
        base["status"] = "BLOCKED_PREFLIGHT"
    return base
