#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts/guard_tau_lensing_score_attempt.py"
OUTPUT_AUDIT = ROOT / "scripts/audit_tau_lensing_score_output_status.py"
DEFAULT_STATUS = ROOT / "data/derived/cmb_tau_lensing_scoring_status_summary_v01.json"
DEFAULT_RECEIPT = ROOT / "data/derived/cmb_tau_lensing_score_execution_receipt_v01.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def load_receipt() -> dict[str, Any]:
    if not DEFAULT_RECEIPT.exists():
        return {
            "receipt_exists": False,
            "receipt_status": "NO_RECEIPT_PRESENT",
            "receipt_claim_boundary": None,
            "receipt_score_output_sha256": None,
            "receipt_score_output_validation_passed": False,
        }
    receipt = json.loads(DEFAULT_RECEIPT.read_text())
    return {
        "receipt_exists": True,
        "receipt_status": receipt.get("receipt_status"),
        "receipt_claim_boundary": receipt.get("claim_boundary"),
        "receipt_score_output_sha256": receipt.get("score_output_sha256"),
        "receipt_score_output_validation_passed": receipt.get("score_output_validation_passed") is True,
    }


def build_status() -> dict[str, Any]:
    guard = run_json([sys.executable, str(GUARD), "--write-guard"])
    output_audit = run_json([sys.executable, str(OUTPUT_AUDIT), "--write-audit"])
    receipt = load_receipt()
    score_attempt_allowed = guard.get("score_attempt_allowed") is True
    physical_score_accepted = output_audit.get("physical_tau_score_output_accepted") is True
    control_score_accepted = output_audit.get("control_score_output_accepted") is True
    diagnostic_probe_score_accepted = output_audit.get("diagnostic_probe_score_output_accepted") is True
    if diagnostic_probe_score_accepted:
        scoring_status = "DIAGNOSTIC_PROBE_SCORE_ACCEPTED"
        plain_language_status = "A reduced diagnostic probe score exists; it is not a physical Tau response claim."
    elif control_score_accepted:
        scoring_status = "CONTROL_SCORE_ACCEPTED"
        plain_language_status = "A reduced control score exists; it is not a physical Tau response claim."
    elif physical_score_accepted:
        scoring_status = "PHYSICAL_TAU_SCORE_ACCEPTED"
        plain_language_status = "A score output exists and the current gate accepts it as a physical Tau score."
    elif score_attempt_allowed:
        scoring_status = "READY_TO_RUN_PHYSICAL_TAU_SCORE"
        plain_language_status = "The gates allow a score attempt, but no accepted physical Tau score is recorded yet."
    else:
        scoring_status = "BLOCKED_BEFORE_PHYSICAL_TAU_SCORE"
        plain_language_status = (
            "The scoring machinery is tested, but a physical Tau score is still blocked before execution."
        )

    return {
        "report_id": "tau_lensing_scoring_status_summary_v01",
        "claim_boundary": "scoring_status_summary_only_no_new_score_no_dark_sector_verdict",
        "scoring_status": scoring_status,
        "plain_language_status": plain_language_status,
        "score_attempt_allowed": score_attempt_allowed,
        "score_gate_passed": guard.get("score_gate_passed") is True,
        "readiness_decision": guard.get("readiness_decision"),
        "blocking_layer": guard.get("blocking_layer"),
        "selected_route_count": guard.get("selected_route_count"),
        "route_submission_audit_decision": guard.get("route_submission_audit_decision"),
        "route_submission_ready_for_materializer": guard.get("route_submission_ready_for_materializer") is True,
        "projection_replay_written": guard.get("projection_replay_written") is True,
        "preflight_ready": guard.get("preflight_ready") is True,
        "pipeline_ready": guard.get("pipeline_ready") is True,
        "physical_tau_score_output_accepted": physical_score_accepted,
        "control_score_output_accepted": control_score_accepted,
        "diagnostic_probe_score_output_accepted": diagnostic_probe_score_accepted,
        "route_is_control": output_audit.get("route_is_control") is True,
        "route_is_diagnostic_probe": output_audit.get("route_is_diagnostic_probe") is True,
        "route_classification": output_audit.get("route_classification"),
        "score_output_audit_decision": output_audit.get("audit_decision"),
        "score_output_exists": output_audit.get("score_output_exists") is True,
        "score_output_path": output_audit.get("score_output_path"),
        **receipt,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": guard.get("next_required_action"),
        "next_commands": guard.get("next_commands"),
        "source_guard_report_id": guard.get("report_id"),
        "source_output_audit_report_id": output_audit.get("report_id"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a compact Tau lensing scoring status summary.")
    parser.add_argument(
        "--write-status",
        default=None,
        nargs="?",
        const=str(DEFAULT_STATUS),
        help=f"Optional JSON status path. Defaults to {DEFAULT_STATUS} when passed without a path.",
    )
    args = parser.parse_args()

    status = build_status()
    text = json.dumps(status, indent=2, sort_keys=True)
    if args.write_status:
        path = Path(args.write_status)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
