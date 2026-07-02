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
GUARD = ROOT / "scripts/guard_tau_lensing_score_attempt.py"
PIPELINE = ROOT / "scripts/run_tau_lensing_scoring_pipeline.py"
DEFAULT_SCORE_OUT = ROOT / "payloads/tau_lensing_reduced_score_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_scoring_pipeline_report_v01.json"
DEFAULT_RECEIPT = ROOT / "data/derived/cmb_tau_lensing_score_execution_receipt_v01.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def emit(report: dict[str, Any], write_report: str | None) -> None:
    text = json.dumps(report, indent=2, sort_keys=True)
    if write_report:
        path = Path(write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_receipt(receipt: dict[str, Any], write_receipt_path: str | None) -> None:
    if not write_receipt_path:
        return
    path = Path(write_receipt_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")


def blocked_report(guard: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_id": "tau_lensing_guarded_score_blocked_v01",
        "claim_boundary": "guarded_score_report_only_no_score_when_guard_blocks_no_dark_sector_verdict",
        "guard_decision": guard.get("guard_decision"),
        "score_attempt_allowed": guard.get("score_attempt_allowed") is True,
        "score_gate_passed": guard.get("score_gate_passed") is True,
        "readiness_decision": guard.get("readiness_decision"),
        "blocking_layer": guard.get("blocking_layer"),
        "selected_route_count": guard.get("selected_route_count"),
        "route_submission_audit_decision": guard.get("route_submission_audit_decision"),
        "projection_replay_written": guard.get("projection_replay_written") is True,
        "preflight_ready": guard.get("preflight_ready") is True,
        "pipeline_ready": guard.get("pipeline_ready") is True,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": guard.get("next_required_action"),
        "next_commands": guard.get("next_commands"),
        "source_guard_report_id": guard.get("report_id"),
    }


def receipt_from_blocked_guard(guard: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_id": "tau_lensing_score_execution_receipt_v01",
        "claim_boundary": "score_execution_receipt_only_no_score_when_guard_blocks_no_dark_sector_verdict",
        "receipt_status": "BLOCKED_BEFORE_SCORE_EXECUTION",
        "guard_decision": guard.get("guard_decision"),
        "score_attempt_allowed": guard.get("score_attempt_allowed") is True,
        "score_gate_passed": guard.get("score_gate_passed") is True,
        "readiness_decision": guard.get("readiness_decision"),
        "blocking_layer": guard.get("blocking_layer"),
        "selected_route_count": guard.get("selected_route_count"),
        "score_run": False,
        "score_output_path": None,
        "score_output_sha256": None,
        "score_output_validation_passed": False,
        "dark_sector_verdict": False,
        "source_guard_report_id": guard.get("report_id"),
    }


def receipt_from_completed_score(
    guard: dict[str, Any], pipeline: dict[str, Any], score_out: Path
) -> dict[str, Any]:
    validation = pipeline.get("score_output_validation", {})
    score_payload = json.loads(score_out.read_text()) if score_out.exists() else {}
    return {
        "report_id": "tau_lensing_score_execution_receipt_v01",
        "claim_boundary": "score_execution_receipt_reduced_diagnostic_only_no_likelihood_no_dark_sector_verdict",
        "receipt_status": "REDUCED_SCORE_EXECUTION_COMPLETED",
        "guard_decision": guard.get("guard_decision"),
        "score_attempt_allowed": guard.get("score_attempt_allowed") is True,
        "score_gate_passed": guard.get("score_gate_passed") is True,
        "readiness_decision": guard.get("readiness_decision"),
        "selected_route_count": guard.get("selected_route_count"),
        "score_run": pipeline.get("score_run") is True,
        "score_output_path": str(score_out.relative_to(ROOT)) if score_out.is_relative_to(ROOT) else str(score_out),
        "score_output_sha256": sha256_file(score_out),
        "score_output_validation_passed": validation.get("validated") is True,
        "score_report_id": score_payload.get("report_id"),
        "score_claim_boundary": score_payload.get("claim_boundary"),
        "route_id": score_payload.get("route_id"),
        "grid_sha256": score_payload.get("grid_sha256"),
        "chi2_tau": score_payload.get("chi2_tau"),
        "chi2_per_naive_dof": score_payload.get("chi2_per_naive_dof"),
        "likelihood_run": score_payload.get("likelihood_run"),
        "dark_sector_verdict": False,
        "source_guard_report_id": guard.get("report_id"),
        "source_pipeline_report_id": pipeline.get("report_id"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reduced Tau lensing score only after the guard allows it.")
    parser.add_argument("--score-out", default=str(DEFAULT_SCORE_OUT), help="Output JSON for the reduced score.")
    parser.add_argument(
        "--write-report",
        default=None,
        nargs="?",
        const=str(DEFAULT_REPORT),
        help=f"Optional guarded score report path. Defaults to {DEFAULT_REPORT} when passed without a path.",
    )
    parser.add_argument(
        "--write-receipt",
        default=None,
        nargs="?",
        const=str(DEFAULT_RECEIPT),
        help=f"Optional score execution receipt path. Defaults to {DEFAULT_RECEIPT} when passed without a path.",
    )
    args = parser.parse_args()

    guard = run_json([sys.executable, str(GUARD), "--write-guard"])
    if guard.get("score_attempt_allowed") is not True:
        write_receipt(receipt_from_blocked_guard(guard), args.write_receipt)
        emit(blocked_report(guard), args.write_report)
        return

    score_out = Path(args.score_out)
    pipeline = run_json(
        [
            sys.executable,
            str(PIPELINE),
            "--score-out",
            args.score_out,
            "--write-report",
            args.write_report or str(DEFAULT_REPORT),
        ]
    )
    write_receipt(receipt_from_completed_score(guard, pipeline, score_out), args.write_receipt)
    emit(
        {
            **pipeline,
            "guarded_score_report": True,
            "source_guard_report_id": guard.get("report_id"),
        },
        args.write_report,
    )


if __name__ == "__main__":
    main()
