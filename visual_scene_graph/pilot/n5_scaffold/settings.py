"""Validate inert proposed configurations; never apply settings or instantiate RNG."""
import hashlib
from dataclasses import dataclass
from types import MappingProxyType

if __package__:
    from .contract import ContractError, canonical, exact_fields, strict_loads, verify_blob
else:
    from contract import ContractError, canonical, exact_fields, strict_loads, verify_blob

PROPOSAL_SHA256 = "aeee1d9d03dfea555f980904556e429e304d788a09b78834e3996927eb6c10e3"
ZERO_CAPS = MappingProxyType({"model_calls": 0, "attempts": 0, "images": 0, "training_steps": 0, "spend": 0})


@dataclass(frozen=True)
class ResolvedSettings:
    configuration_json: str
    configuration_sha256: str
    settings_applied: bool = False
    execution_authorized: bool = False


def proposed_config(name, *, proposal_bytes):
    verify_blob(proposal_bytes, PROPOSAL_SHA256)
    proposal = strict_loads(proposal_bytes)
    if type(name) is not str or name not in ("candidate", "negative_control"):
        raise ContractError("Unknown proposed configuration")
    return {"schema_version": "0.1.0", "scope": "D2_STATIC_ONLY",
            "proposal_id": proposal["proposal_id"], "proposal_version": proposal["version"],
            "proposal_sha256": PROPOSAL_SHA256, "name": name,
            "configuration": proposal["proposed_configurations"][name],
            "execution_caps": dict(ZERO_CAPS)}


def resolve_settings(config, *, proposal_bytes):
    exact_fields(config, {"schema_version", "scope", "proposal_id", "proposal_version",
                          "proposal_sha256", "name", "configuration", "execution_caps"})
    expected = proposed_config(config["name"], proposal_bytes=proposal_bytes)
    exact_fields(config["execution_caps"], ZERO_CAPS)
    if any(type(v) is not int or v != 0 for v in config["execution_caps"].values()):
        raise ContractError("Execution caps must be integer zero")
    # Includes every explicit setting, pins through proposal hash, config identity,
    # RNG design text and the complete relation-active-loop list, with no fallback.
    if canonical(config) != canonical(expected):
        raise ContractError("Proposed configuration identity or content mismatch")
    data = canonical(config)
    return ResolvedSettings(data.decode("utf-8"), hashlib.sha256(data).hexdigest())


def validate_pair(config_a, config_b, *, proposal_bytes):
    a = resolve_settings(config_a, proposal_bytes=proposal_bytes)
    b = resolve_settings(config_b, proposal_bytes=proposal_bytes)
    if a.configuration_json != b.configuration_json:
        raise ContractError("A/B must share the entire proposed configuration")
    return a, b
