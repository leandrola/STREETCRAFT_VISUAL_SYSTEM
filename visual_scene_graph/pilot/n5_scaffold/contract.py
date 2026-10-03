"""Strict, inert envelopes for the byte-frozen D comparison; no tokenizer or model."""
import hashlib
import json
import math

PAYLOAD_SHA256 = "7b995c02541b831524236cf36c9e8e834a8ddbcaea43da6a1f6669918f8a586d"
SOURCE_SHA256 = "282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc"
PREDICATES = frozenset({"LEFT_OF", "RIGHT_OF", "ABOVE", "BELOW"})
LOCK_IDS = frozenset({"GL-GEO-DINER_01", "GL-GEO-FACADE_01", "GL-SEM-SIGN_01"})
FIELDS = frozenset({"schema_version", "case", "branch", "source_sha256",
                    "payload_sha256", "prompt", "relational_records"})


class ContractError(ValueError):
    """A static input violates the frozen contract."""


def canonical(value):
    """JSON bytes with strict finite JSON types; no boolean/number equivalence."""
    def valid(v):
        if type(v) is dict:
            if not all(type(k) is str for k in v):
                raise ContractError("JSON keys must be strings")
            for item in v.values():
                valid(item)
        elif type(v) is list:
            for item in v:
                valid(item)
        elif type(v) is float:
            if not math.isfinite(v):
                raise ContractError("Non-finite JSON number")
        elif v is not None and type(v) not in (str, int, bool):
            raise ContractError("Unsupported JSON type")
    valid(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def strict_loads(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError("Duplicate JSON field")
            result[key] = value
        return result
    def invalid_constant(_):
        raise ContractError("Non-finite JSON number")
    try:
        value = json.loads(data, object_pairs_hook=unique, parse_constant=invalid_constant)
        canonical(value)
        return value
    except (ValueError, TypeError, UnicodeError) as exc:
        raise ContractError("Invalid strict JSON") from exc


def exact_fields(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise ContractError("Missing or unknown fields")


def verify_blob(data, expected):
    if type(data) is not bytes or hashlib.sha256(data).hexdigest() != expected:
        raise ContractError("Frozen input SHA-256 mismatch")


def validate_records(records):
    """Validate the typed D port; inverse predicates are valid syntax, not D truth."""
    if type(records) is not list or len(records) != 10:
        raise ContractError("D requires ten typed records")
    ids = set()
    locks = set()
    for row in records:
        exact_fields(row, {"id", "priority", "value", "lock_ids"})
        if type(row["id"]) is not str or row["id"] in ids:
            raise ContractError("Invalid or duplicate record ID")
        ids.add(row["id"])
        if type(row["lock_ids"]) is not list or any(type(v) is not str for v in row["lock_ids"]):
            raise ContractError("Invalid lock references")
        if row["id"].startswith("edge:"):
            exact_fields(row["value"], {"confidence", "epistemic_class", "evidence", "from", "protection", "to", "type"})
            if type(row["value"]["type"]) is not str or row["value"]["type"] not in PREDICATES:
                raise ContractError("Unsupported predicate")
            if type(row["value"]["confidence"]) not in (int, float) or not 0 <= row["value"]["confidence"] <= 1:
                raise ContractError("Invalid confidence")
            if type(row["priority"]) is not str or row["priority"] not in ("PR0", "PR1"):
                raise ContractError("Invalid edge priority")
        elif row["id"].startswith("lock:"):
            exact_fields(row["value"], {"enforcement", "expected", "provenance", "strength", "target", "type"})
            if row["priority"] != "LOCK" or row["value"]["enforcement"] != "VALIDATE_ONLY":
                raise ContractError("Invalid protected lock")
            locks.add(row["id"][5:])
        elif row["id"].startswith("topology:"):
            if type(row["value"]) is not list or any(type(v) is not str for v in row["value"]):
                raise ContractError("Invalid topology")
            if type(row["priority"]) is not str or row["priority"] not in ("P0", "P2"):
                raise ContractError("Invalid topology priority")
        else:
            raise ContractError("Unsupported record kind")
    if locks != LOCK_IDS:
        raise ContractError("Protected lock completeness mismatch")
    canonical(records)


def frozen_payload(payload_bytes, source_bytes):
    verify_blob(payload_bytes, PAYLOAD_SHA256)
    verify_blob(source_bytes, SOURCE_SHA256)
    payload = strict_loads(payload_bytes)
    exact_fields(payload, {"A", "B"})
    for branch in ("A", "B"):
        exact_fields(payload[branch], {"common", "relations_and_locks"})
    if canonical(payload["A"]["common"]) != canonical(payload["B"]["common"]):
        raise ContractError("Shared common mismatch")
    if type(payload["A"]["relations_and_locks"]) is not str:
        raise ContractError("A requires opaque exact JSONL text")
    # A JSONL is never parsed to feed R. The typed source is exclusively frozen B.
    validate_records(payload["B"]["relations_and_locks"])
    return payload


def make_envelope(branch, *, payload_bytes, source_bytes):
    if type(branch) is not str or branch not in ("A", "B"):
        raise ContractError("Unsupported branch")
    payload = frozen_payload(payload_bytes, source_bytes)
    common_text = canonical(payload[branch]["common"]).decode("utf-8")
    return {"schema_version": "0.1.0", "case": "R2B-191-D", "branch": branch,
            "source_sha256": SOURCE_SHA256, "payload_sha256": PAYLOAD_SHA256,
            "prompt": common_text + ("\n" + payload["A"]["relations_and_locks"] if branch == "A" else ""),
            "relational_records": [] if branch == "A" else payload["B"]["relations_and_locks"]}


def validate_envelope(envelope, *, payload_bytes, source_bytes):
    exact_fields(envelope, FIELDS)
    if envelope["schema_version"] != "0.1.0" or envelope["case"] != "R2B-191-D":
        raise ContractError("Unsupported envelope identity")
    if type(envelope["prompt"]) is not str:
        raise ContractError("Prompt must be text")
    branch = envelope["branch"]
    expected = make_envelope(branch, payload_bytes=payload_bytes, source_bytes=source_bytes)
    if branch == "A":
        if type(envelope["relational_records"]) is not list or envelope["relational_records"]:
            raise ContractError("A must not carry R")
    else:
        validate_records(envelope["relational_records"])
    if canonical(envelope) != canonical(expected):
        raise ContractError("Envelope differs from frozen D truth or exact text")
    return strict_loads(canonical(envelope))
