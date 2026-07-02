#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "payloads/tau_lensing_reduced_score_v01.json"
PROVENANCE = ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json"
GUARD = ROOT / "scripts/guard_tau_lensing_score_attempt.py"
VALIDATOR = ROOT / "scripts/validate_tau_lensing_reduced_score_output.py"
RECEIPT = ROOT / "data/derived/cmb_tau_lensing_score_execution_receipt_v01.json"
DEFAULT_AUDIT = ROOT / "data/derived/cmb_tau_lensing_score_output_status_audit_v01.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_receipt() -> dict[str, Any]:
    if not RECEIPT.exists():
        return {
            "score_execution_receipt_exists": False,
            "score_execution_receipt_status": "NO_RECEIPT_PRESENT",
            "score_execution_receipt_output_sha256": None,
            "score_execution_receipt_validation_passed": False,
        }
    receipt = json.loads(RECEIPT.read_text())
    return {
        "score_execution_receipt_exists": True,
        "score_execution_receipt_status": receipt.get("receipt_status"),
        "score_execution_receipt_output_sha256": receipt.get("score_output_sha256"),
        "score_execution_receipt_validation_passed": receipt.get("score_output_validation_passed") is True,
        "score_execution_receipt_claim_boundary": receipt.get("claim_boundary"),
    }


def validate_existing_score() -> dict[str, Any]:
    if not SCORE.exists():
        return {
            "score_output_exists": False,
            "score_schema_valid": False,
            "score_claim_boundary": None,
            "score_route_id": None,
        }
    try:
        validation = run_json([sys.executable, str(VALIDATOR), str(SCORE)])
        payload = json.loads(SCORE.read_text())
        return {
            "score_output_exists": True,
            "score_schema_valid": validation.get("validated") is True,
            "score_output_sha256": sha256_file(SCORE),
            "score_claim_boundary": payload.get("claim_boundary"),
            "score_route_id": payload.get("route_id"),
            "score_likelihood_run": payload.get("likelihood_run"),
            "score_dark_sector_verdict": payload.get("dark_sector_verdict"),
        }
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return {
            "score_output_exists": True,
            "score_schema_valid": False,
            "score_output_sha256": sha256_file(SCORE),
            "score_validation_error": str(exc),
            "score_claim_boundary": None,
            "score_route_id": None,
        }


def route_classification() -> str:
    if not PROVENANCE.exists():
        return "unknown"
    try:
        provenance = json.loads(PROVENANCE.read_text())
    except json.JSONDecodeError:
        return "unknown"
    haystack = " ".join(
        str(provenance.get(key, ""))
        for key in [
            "derivation_script_or_formula",
            "no_endpoint_fit_statement",
            "notes",
            "probe_status",
        ]
    ).lower()
    if "probe" in haystack or "diagnostic" in haystack or "not a tau-derived physical response" in haystack:
        return "diagnostic_probe"
    if "control" in haystack or "identically zero" in haystack or "null-control" in haystack:
        return "control"
    return "physical_candidate"


def build_audit() -> dict[str, Any]:
    guard = run_json([sys.executable, str(GUARD), "--write-guard"])
    score_status = validate_existing_score()
    receipt_status = load_receipt()
    receipt_matches_score = (
        score_status.get("score_output_sha256") is not None
        and score_status.get("score_output_sha256") == receipt_status.get("score_execution_receipt_output_sha256")
    )
    score_output_accepted = (
        score_status.get("score_output_exists") is True
        and score_status.get("score_schema_valid") is True
        and guard.get("score_attempt_allowed") is True
        and guard.get("score_gate_passed") is True
        and receipt_status.get("score_execution_receipt_status") == "REDUCED_SCORE_EXECUTION_COMPLETED"
        and receipt_status.get("score_execution_receipt_validation_passed") is True
        and receipt_matches_score
    )
    route_class = route_classification()
    control_score = score_output_accepted and route_class == "control"
    diagnostic_probe_score = score_output_accepted and route_class == "diagnostic_probe"
    physical_score_accepted = score_output_accepted and route_class == "physical_candidate"
    if diagnostic_probe_score:
        audit_decision = "DIAGNOSTIC_PROBE_SCORE_OUTPUT_ACCEPTED"
        next_required_action = "interpret_as_pipeline_probe_not_physical_tau_response"
    elif control_score:
        audit_decision = "CONTROL_SCORE_OUTPUT_ACCEPTED"
        next_required_action = "interpret_as_control_baseline_not_physical_tau_response"
    elif physical_score_accepted:
        audit_decision = "PHYSICAL_TAU_SCORE_OUTPUT_ACCEPTED"
        next_required_action = "interpret_score_under_claim_boundary"
    elif score_status.get("score_output_exists") is True:
        audit_decision = "SCORE_OUTPUT_PRESENT_BUT_NOT_PHYSICAL_TAU_SCORE"
        next_required_action = "do_not_interpret_score_until_score_attempt_guard_allows"
    else:
        audit_decision = "NO_SCORE_OUTPUT_PRESENT"
        next_required_action = "submit_route_evidence_before_score_attempt"

    return {
        "report_id": "tau_lensing_score_output_status_audit_v01",
        "claim_boundary": "score_output_status_audit_only_no_new_score_no_dark_sector_verdict",
        "audit_decision": audit_decision,
        "physical_tau_score_output_accepted": physical_score_accepted,
        "control_score_output_accepted": control_score,
        "diagnostic_probe_score_output_accepted": diagnostic_probe_score,
        "route_is_control": route_class == "control",
        "route_is_diagnostic_probe": route_class == "diagnostic_probe",
        "route_classification": route_class,
        "score_output_path": str(SCORE.relative_to(ROOT)),
        **score_status,
        **receipt_status,
        "score_execution_receipt_matches_score_output": receipt_matches_score,
        "score_attempt_allowed": guard.get("score_attempt_allowed") is True,
        "score_gate_passed": guard.get("score_gate_passed") is True,
        "readiness_decision": guard.get("readiness_decision"),
        "selected_route_count": guard.get("selected_route_count"),
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": next_required_action,
        "source_guard_report_id": guard.get("report_id"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit whether an existing reduced score output is physical Tau score.")
    parser.add_argument(
        "--write-audit",
        default=None,
        nargs="?",
        const=str(DEFAULT_AUDIT),
        help=f"Optional JSON audit path. Defaults to {DEFAULT_AUDIT} when passed without a path.",
    )
    args = parser.parse_args()
    audit = build_audit()
    text = json.dumps(audit, indent=2, sort_keys=True)
    if args.write_audit:
        path = Path(args.write_audit)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
