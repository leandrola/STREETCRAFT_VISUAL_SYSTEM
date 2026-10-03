"""Exactly sixteen D2 stdlib acceptance checks; run this file directly with -B."""
import argparse
import ast
import copy
import datetime
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

if __package__:
    from . import contract, ledger, settings
else:
    import contract
    import ledger
    import settings

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BASELINE = "8ca0422dfb5bfceb524652fbc4560c7ef79f5de0"
RESULT = "validation/vsg_2b/n5_scaffold/STATIC_RESULT.json"
NEW_FILES = ["visual_scene_graph/pilot/n5_scaffold/" + name for name in
             ("README.md", "__init__.py", "contract.py", "settings.py", "ledger.py", "fixtures.json", "static_checks.py")] + [RESULT]
EDIT_FILES = {"development/coordination/CHECKPOINT.json", "development/coordination/README.md"}


def insist(condition, reason):
    if not condition:
        raise AssertionError(reason)


def rejected(operation, error=contract.ContractError):
    try:
        operation()
    except error:
        return
    raise AssertionError("Invalid input was accepted")


def git(*args):
    """The only subprocess boundary is a bounded read-only git query."""
    if not args or args[0] not in {"ls-tree", "ls-files", "diff"}:
        raise AssertionError("Non-read-only git operation forbidden")
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=30)


class Checks:
    def __init__(self):
        self.fixture = contract.strict_loads((HERE / "fixtures.json").read_bytes())
        self.payload = (ROOT / self.fixture["inputs"]["payload"]["path"]).read_bytes()
        self.source = (ROOT / self.fixture["inputs"]["source"]["path"]).read_bytes()
        self.proposal = (ROOT / self.fixture["proposal"]["path"]).read_bytes()
        self.preservation = {}

    def envelope(self, branch="B"):
        return contract.make_envelope(branch, payload_bytes=self.payload, source_bytes=self.source)

    def validate(self, envelope, payload=None, source=None):
        return contract.validate_envelope(envelope, payload_bytes=self.payload if payload is None else payload,
                                          source_bytes=self.source if source is None else source)

    def config(self, name="candidate"):
        return settings.proposed_config(name, proposal_bytes=self.proposal)

    def resolve(self, config):
        return settings.resolve_settings(config, proposal_bytes=self.proposal)

    def valid_envelope(self):
        for branch in ("A", "B"):
            e = self.envelope(branch)
            before = contract.canonical(e)
            validated = self.validate(e)
            insist(contract.canonical(validated) == before and validated is not e, "Fresh valid envelope required")
            validated["prompt"] = "changed returned copy"
            insist(contract.canonical(e) == before, "Validation altered caller input")

    def missing_field(self):
        for branch in ("A", "B"):
            for field in contract.FIELDS:
                e = self.envelope(branch)
                del e[field]
                rejected(lambda: self.validate(e))

    def unknown_field(self):
        e = self.envelope()
        e["dispatch"] = True
        rejected(lambda: self.validate(e))
        rejected(lambda: contract.strict_loads('{"branch":"A","branch":"B"}'))
        rejected(lambda: contract.strict_loads('{"nested":{"x":0,"x":1}}'))
        rejected(lambda: contract.strict_loads('{"x":NaN}'))

    def supported_predicate(self):
        for predicate in ("LEFT_OF", "RIGHT_OF", "ABOVE", "BELOW"):
            records = self.envelope()["relational_records"]
            records[0]["value"]["type"] = predicate
            contract.validate_records(records)
        self.validate(self.envelope())

    def unsupported_predicate(self):
        for predicate in ("OCCLUDES", "UNKNOWN", "", None, True, [], {}):
            e = self.envelope()
            e["relational_records"][0]["value"]["type"] = predicate
            rejected(lambda: self.validate(e))

    def exact_input_hash(self):
        for blob, name in ((self.payload, "payload"), (self.source, "source")):
            damaged = blob[:-1] + bytes([blob[-1] ^ 1])
            rejected(lambda: self.validate(self.envelope(), **{name: damaged}))
        for field in ("source_sha256", "payload_sha256"):
            e = self.envelope()
            e[field] = "0" * 64
            rejected(lambda: self.validate(e))
        for name, expected in (("payload", contract.PAYLOAD_SHA256), ("source", contract.SOURCE_SHA256)):
            insist(self.fixture["inputs"][name]["sha256"] == expected, "Fixture pin mismatch")
        insist(self.fixture["proposal"]["sha256"] == settings.PROPOSAL_SHA256, "Proposal fixture pin mismatch")

    def mutated_d_rejection(self):
        e = self.envelope()
        e["relational_records"][0]["value"]["type"] = "RIGHT_OF"
        contract.validate_records(e["relational_records"])
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["relational_records"][0]["value"]["from"] = "sign_01"
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["prompt"] += "\nnew design"
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["case"] = "R2B-191-E"
        rejected(lambda: self.validate(e))

    def protected_lock_completeness(self):
        for index in (2, 3, 4):
            e = self.envelope()
            del e["relational_records"][index]
            rejected(lambda: self.validate(e))
        e = self.envelope()
        e["relational_records"][4]["value"]["expected"]["text"] = "TERMINAL D1NER"
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["relational_records"][2]["value"]["enforcement"] = "EDIT_ALLOWED"
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["relational_records"][0]["lock_ids"] = []
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["relational_records"][2] = copy.deepcopy(e["relational_records"][3])
        rejected(lambda: self.validate(e))

    def a_r_absence(self):
        e = self.envelope("A")
        e["relational_records"] = self.envelope()["relational_records"]
        rejected(lambda: self.validate(e))
        for change in (lambda text: text[:-1], lambda text: text + "\n"):
            e = self.envelope("A")
            e["prompt"] = change(e["prompt"])
            rejected(lambda: self.validate(e))
        payload = contract.strict_loads(self.payload)
        exact = contract.canonical(payload["A"]["common"]).decode() + "\n" + payload["A"]["relations_and_locks"]
        insist(self.envelope("A")["prompt"] == exact, "A exact JSONL text changed")

    def b_typed_records(self):
        for changed in (json.dumps(self.envelope()["relational_records"]), [], {}, None):
            e = self.envelope()
            e["relational_records"] = changed
            rejected(lambda: self.validate(e))
        e = self.envelope()
        e["relational_records"][1] = copy.deepcopy(e["relational_records"][0])
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["prompt"] += "\n" + json.dumps(e["relational_records"])
        rejected(lambda: self.validate(e))
        e = self.envelope()
        e["relational_records"][0]["value"]["confidence"] = True
        rejected(lambda: self.validate(e))

    def explicit_config_identity(self):
        for name in ("candidate", "negative_control"):
            self.resolve(self.config(name))
        for field in ("scope", "proposal_id", "proposal_version", "proposal_sha256"):
            c = self.config()
            c[field] = "wrong"
            rejected(lambda: self.resolve(c))
        for field in ("id", "version", "kind"):
            c = self.config()
            c["configuration"][field] = "wrong"
            rejected(lambda: self.resolve(c))
        for field in self.config()["configuration"]["settings"]:
            c = self.config()
            del c["configuration"]["settings"][field]
            rejected(lambda: self.resolve(c))
        c = self.config()
        c["configuration"]["settings"]["root_seed"] += 1
        rejected(lambda: self.resolve(c))
        c = self.config()
        c["configuration"]["relation_active_loop_indices"].pop()
        rejected(lambda: self.resolve(c))
        c = self.config()
        c["configuration"]["settings"]["extra"] = 0
        rejected(lambda: self.resolve(c))
        rejected(lambda: settings.resolve_settings(self.config(), proposal_bytes=self.proposal + b"\n"))

    def ab_shared_settings(self):
        a, b = settings.validate_pair(self.config(), self.config(), proposal_bytes=self.proposal)
        insist(a.configuration_sha256 == b.configuration_sha256, "Matched settings digests differ")
        rejected(lambda: settings.validate_pair(self.config(), self.config("negative_control"), proposal_bytes=self.proposal))
        c = self.config()
        c["configuration"]["settings"]["RNG"]["initial"] += 1
        rejected(lambda: settings.validate_pair(self.config(), c, proposal_bytes=self.proposal))

    def zero_execution_caps(self):
        c = self.config()
        resolved = self.resolve(c)
        insist(resolved.settings_applied is False and resolved.execution_authorized is False, "Runtime authority implied")
        insist(all(type(v) is int and v == 0 for v in c["execution_caps"].values()), "Nonzero approved cap")
        for field in c["execution_caps"]:
            for value in (1, -1, True, 0.0):
                changed = copy.deepcopy(c)
                changed["execution_caps"][field] = value
                rejected(lambda: self.resolve(changed))
        log = ledger.Ledger()
        rejected(lambda: log.caps.__setitem__("attempts", 1), AttributeError)
        rejected(lambda: setattr(log, "caps", {"attempts": 1}), AttributeError)
        rejected(lambda: setattr(resolved, "execution_authorized", True), AttributeError)

    def reservation_cap_rejection(self):
        log = ledger.Ledger()
        for field in log.caps:
            for value in (1, -1, True, 0.0, "0"):
                units = dict(log.caps)
                units[field] = value
                rejected(lambda: log.reserve("bad", units), ledger.LedgerError)
        for units in ({}, {**dict(log.caps), "extra": 0}, None):
            rejected(lambda: log.reserve("bad", units), ledger.LedgerError)
        insist(log.events == (), "Rejected real work created reservation")

    def failed_reservation_no_retry(self):
        log = ledger.Ledger()
        units = dict(log.caps)
        first = log.reserve("static-validation-only", units)
        units["attempts"] = 1
        second = log.fail("static-validation-only", "simulated validation failure")
        insist(log.events == (first, second) and second.units == first.units, "Failed reservation not retained")
        insist(all(v == 0 for _, v in second.units) and second.static_only, "Simulation consumed execution units")
        rejected(lambda: log.reserve("static-validation-only", dict(log.caps)), ledger.LedgerError)
        rejected(lambda: log.fail("static-validation-only", "retry"), ledger.LedgerError)
        rejected(lambda: log.fail("unknown", "not reserved"), ledger.LedgerError)
        rejected(lambda: setattr(first, "status", "deleted"), AttributeError)
        insist(log.events == (first, second), "Rejected retry rewrote history")

    def isolation_and_preservation(self):
        insist(sys.dont_write_bytecode, "Run with -B to keep scaffold free of generated cache files")
        f = self.fixture
        insist(f["baseline"] == BASELINE and f["version"] == "0.1.0" and f["scope"] == "D2_STATIC_ONLY", "Fixture identity mismatch")
        insist(f["allowed_new_files"] == NEW_FILES and set(f["allowed_existing_edits"]) == EDIT_FILES, "Approved file scope changed")
        insist(f["limits"] == {"new_files": 8, "static_acceptance_checks": 16, "engineering_hours": 40,
                              "model_calls": 0, "attempts": 0, "images": 0}, "Approved limits changed")
        insist([c["id"] for c in f["checks"]] == [i for i, _ in TESTS], "Sixteen acceptance definitions changed")
        allowed_imports = {"argparse", "ast", "copy", "datetime", "hashlib", "json", "math", "subprocess", "sys",
                           "time", "pathlib", "dataclasses", "types", "contract", "settings", "ledger"}
        forbidden_calls = {"eval", "exec", "compile", "__import__", "generate", "predict", "dispatch",
                           "from_pretrained", "load_model", "tokenize", "train", "system", "popen", "urlopen"}
        for path in sorted(HERE.glob("*.py")):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Import):
                    insist(all(a.name in allowed_imports for a in node.names), "Import outside stdlib/scaffold")
                if isinstance(node, ast.ImportFrom):
                    insist(node.module in allowed_imports or (node.module is None and node.level == 1
                            and all(a.name in {"contract", "settings", "ledger"} for a in node.names)), "Import outside stdlib/scaffold")
                if isinstance(node, ast.Call):
                    name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                    insist(name not in forbidden_calls, "Forbidden runtime/dispatch call")
                    if name in {"run", "check_output", "Popen"}:
                        insist(path.name == "static_checks.py" and name == "check_output", "Subprocess outside static git queries")
        baseline_paths = set(git("ls-tree", "-r", "--name-only", BASELINE).splitlines())
        current_paths = set(git("ls-files", "--cached", "--others", "--exclude-standard").splitlines())
        added = current_paths - baseline_paths
        insist(added == set(NEW_FILES) and all((ROOT / p).is_file() for p in NEW_FILES), "Exactly eight approved new files required")
        changed = set(git("diff", "--name-only", BASELINE, "--", *sorted(baseline_paths)).splitlines())
        insist(changed.issubset(EDIT_FILES), "Operational or historical file changed")
        cp = contract.strict_loads((ROOT / "development/coordination/CHECKPOINT.json").read_bytes())
        insist(cp["decisions"]["D1"] == "APPROVED_DESIGN_BASIS_ONLY"
                and cp["decisions"]["D2"] == "APPROVED_ISOLATED_SCAFFOLD_ONLY"
                and cp["decisions"]["D3"] == cp["decisions"]["D4"] == "PENDING", "Approval scope mismatch")
        insist(cp["authorization"]["proposal_sha256"] == settings.PROPOSAL_SHA256
                and cp["authorization"]["D2_limits"] == f["limits"], "Approval identity/limits mismatch")
        insist(not cp["settings_applied"] and not cp["execution_authorized"] and cp["model_tests"] == "NOT_RUN"
                and cp["generated_images"] == 0 and cp["milestones"]["VSG-2B"]["status"] == "BLOCKED / PENDING_VISUAL", "Execution gate changed")
        self.preservation = {"baseline": BASELINE, "prior_files": len(baseline_paths),
                             "unchanged_previous_files": len(baseline_paths - EDIT_FILES),
                             "allowed_existing_changes": sorted(changed), "new_files": sorted(added),
                             "imports": "STDLIB_AND_SIBLING_SCAFFOLD_ONLY", "dispatch": "ABSENT"}


TESTS = [
    ("VALID_ENVELOPE", "valid_envelope"), ("MISSING_FIELD", "missing_field"),
    ("UNKNOWN_FIELD", "unknown_field"), ("SUPPORTED_PREDICATE", "supported_predicate"),
    ("UNSUPPORTED_PREDICATE", "unsupported_predicate"), ("EXACT_INPUT_HASH", "exact_input_hash"),
    ("MUTATED_D_REJECTION", "mutated_d_rejection"), ("PROTECTED_LOCK_COMPLETENESS", "protected_lock_completeness"),
    ("A_R_ABSENCE", "a_r_absence"), ("B_TYPED_RECORDS", "b_typed_records"),
    ("EXPLICIT_CONFIG_IDENTITY", "explicit_config_identity"), ("AB_SHARED_SETTINGS", "ab_shared_settings"),
    ("ZERO_EXECUTION_CAPS", "zero_execution_caps"), ("RESERVATION_CAP_REJECTION", "reservation_cap_rejection"),
    ("FAILED_RESERVATION_NO_RETRY", "failed_reservation_no_retry"), ("ISOLATION_AND_PRESERVATION", "isolation_and_preservation")
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--verify-only", action="store_true")
    mode.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.resolve() != (ROOT / RESULT).resolve():
        parser.error("Only the approved STATIC_RESULT.json output path is permitted")
    started = time.perf_counter()
    context = Checks()
    results = []
    for ident, method in TESTS:
        try:
            getattr(context, method)()
            results.append({"id": ident, "status": "PASS"})
        except Exception as exc:
            results.append({"id": ident, "status": "FAIL", "error": type(exc).__name__ + ": " + str(exc)})
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in NEW_FILES if p != RESULT and (ROOT / p).is_file()}
    inputs = {v["path"]: hashlib.sha256((ROOT / v["path"]).read_bytes()).hexdigest()
              for v in [*context.fixture["inputs"].values(), context.fixture["proposal"]]}
    report = {"milestone": "M3", "status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
              "scope": "D2_STATIC_ONLY", "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "baseline": BASELINE, "checks": results, "checks_count": len(results),
              "elapsed_seconds": round(time.perf_counter() - started, 4), "artifact_sha256": hashes,
              "input_sha256": inputs, "preservation": context.preservation,
              "independent_review": "PENDING", "model_tests": "NOT_RUN", "generated_images": 0,
              "model_calls": 0, "attempts": 0, "settings_applied": False, "execution_authorized": False,
              "production_authorized": False, "provider_READY": False, "VSG-2B": "BLOCKED / PENDING_VISUAL"}
    if args.output is not None:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
