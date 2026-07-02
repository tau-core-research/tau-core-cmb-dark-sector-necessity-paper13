#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "scripts/intake_tau_lensing_route_evidence.py"
ENVIRONMENT = ROOT / "scripts/check_tau_lensing_scoring_environment.py"
MATERIALIZER = ROOT / "scripts/materialize_tau_lensing_projection_replay.py"
PREFLIGHT = ROOT / "scripts/preflight_tau_lensing_reduced_score.py"
RUNNER = ROOT / "scripts/run_tau_lensing_reduced_score.py"
VALIDATOR = ROOT / "scripts/validate_tau_lensing_reduced_score_output.py"
REPLAY = ROOT / "payloads/tau_lensing_pp_grid_projection_replay_v01.json"
DEFAULT_SCORE_OUT = ROOT / "payloads/tau_lensing_reduced_score_v01.json"
DEFAULT_PIPELINE_REPORT = ROOT / "data/derived/cmb_tau_lensing_scoring_pipeline_report_v01.json"


def run_json(cmd: list[str]) -> dict[str, Any]:
    completed = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def run_checked(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)


def emit_report(report: dict[str, Any], write_report: str | None) -> None:
    text = json.dumps(report, indent=2, sort_keys=True)
    if write_report:
        path = Path(write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


def blocked_report(
    preflight: dict[str, Any],
    intake: dict[str, Any],
    environment: dict[str, Any],
    materializer: dict[str, Any],
) -> dict[str, Any]:
    next_required_action = preflight.get("next_required_action")
    if intake.get("selected_route_count", 0) != 1:
        next_required_action = "fill_exactly_one_staging_route_evidence_set_then_run_guarded_staging_promotion"
    return {
        "report_id": "tau_lensing_scoring_pipeline_blocked_v01",
        "claim_boundary": "scoring_pipeline_orchestrator_only_no_score_run_no_dark_sector_verdict",
        "pipeline_ready": False,
        "score_run": False,
        "dark_sector_verdict": False,
        "blocking_intake": intake,
        "scoring_environment": environment,
        "blocking_materializer": materializer,
        "blocking_preflight": preflight,
        "next_required_action": next_required_action,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight, run, and validate the reduced Tau lensing score.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check score readiness without executing the reduced score runner.",
    )
    parser.add_argument("--score-out", default=str(DEFAULT_SCORE_OUT), help="Output JSON for validated reduced score.")
    parser.add_argument(
        "--write-report",
        default=None,
        nargs="?",
        const=str(DEFAULT_PIPELINE_REPORT),
        help=f"Optional pipeline JSON report path. Defaults to {DEFAULT_PIPELINE_REPORT} when passed without a path.",
    )
    args = parser.parse_args()

    intake = run_json([sys.executable, str(INTAKE)])
    environment = run_json([sys.executable, str(ENVIRONMENT)])
    materializer = run_json([sys.executable, str(MATERIALIZER)])
    preflight = run_json([sys.executable, str(PREFLIGHT)])
    if preflight.get("ready_for_reduced_score_execution") is not True:
        emit_report(blocked_report(preflight, intake, environment, materializer), args.write_report)
        return

    if args.dry_run:
        result = {
            "report_id": "tau_lensing_scoring_pipeline_ready_dry_run_v01",
            "claim_boundary": "scoring_pipeline_readiness_dry_run_only_no_score_run_no_dark_sector_verdict",
            "pipeline_ready": True,
            "scoring_environment": environment,
            "blocking_intake": intake,
            "blocking_materializer": materializer,
            "blocking_preflight": preflight,
            "score_run": False,
            "physical_tau_score_run": False,
            "score_output": None,
            "dark_sector_verdict": False,
            "next_required_action": "run_score_attempt_guard_then_make_score_report",
        }
        emit_report(result, args.write_report)
        return

    score_out = Path(args.score_out)
    run_checked([sys.executable, str(RUNNER), str(REPLAY), "--write-score", str(score_out)])
    validation = run_json([sys.executable, str(VALIDATOR), str(score_out)])
    result = {
        "report_id": "tau_lensing_scoring_pipeline_completed_v01",
        "claim_boundary": "scoring_pipeline_orchestrator_reduced_score_only_no_likelihood_no_dark_sector_verdict",
        "pipeline_ready": True,
        "scoring_environment": environment,
        "score_run": True,
        "score_output": str(score_out),
        "score_output_validation": validation,
        "dark_sector_verdict": False,
    }
    emit_report(result, args.write_report)


if __name__ == "__main__":
    main()
