#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "scripts/run_tau_lensing_scoring_pipeline.py"
DEFAULT_DECISION = ROOT / "data/derived/cmb_tau_lensing_score_readiness_decision_v01.json"


def run_pipeline() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(PIPELINE), "--dry-run", "--write-report"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def decide(report: dict[str, Any]) -> dict[str, Any]:
    env_ready = report.get("scoring_environment", {}).get(
        "environment_ready_for_reduced_score_once_tau_replay_exists"
    ) is True
    intake = report.get("blocking_intake", {})
    preflight = report.get("blocking_preflight", {})
    materializer = report.get("blocking_materializer", {})
    route_count = intake.get("selected_route_count", 0)
    firewall = preflight.get("firewall_status", {})
    route_status = preflight.get("route_status", {})
    failure_route_complete = route_status.get("failure_route_complete") is True
    firewall_passed = firewall.get("firewall_passed") is True
    replay_written = materializer.get("projection_replay_written") is True
    preflight_ready = preflight.get("ready_for_reduced_score_execution") is True
    pipeline_ready = report.get("pipeline_ready") is True

    if pipeline_ready and preflight_ready and firewall_passed:
        readiness_decision = "READY_TO_SCORE"
        blocking_layer = "none"
        next_action = "run_make_score_attempt_guard_then_make_score_report_if_allowed"
    elif not env_ready:
        readiness_decision = "BLOCKED_ON_ACT_SCORING_ENVIRONMENT"
        blocking_layer = "act_environment"
        next_action = "repair_act_scoring_environment"
    elif route_count != 1:
        readiness_decision = "BLOCKED_ON_TAU_ROUTE_EVIDENCE"
        blocking_layer = "tau_route_evidence"
        next_action = "fill_exactly_one_staging_route_evidence_set_then_run_guarded_staging_promotion"
    elif not firewall_passed:
        readiness_decision = "BLOCKED_ON_ROUTE_EVIDENCE_FIREWALL"
        blocking_layer = "route_evidence_firewall"
        next_action = firewall.get("next_required_action") or "run_make_evidence_check"
    elif failure_route_complete:
        readiness_decision = "FAILURE_ROUTE_RECORDED_SCORE_BLOCKED"
        blocking_layer = "tau_route_failure_recorded"
        next_action = "preserve_failure_route_no_score_run"
    elif not replay_written:
        readiness_decision = "BLOCKED_ON_PROJECTION_REPLAY"
        blocking_layer = "projection_replay"
        next_action = "run_make_materialize_replay"
    else:
        readiness_decision = "BLOCKED_ON_PREFLIGHT"
        blocking_layer = "score_preflight"
        next_action = report.get("next_required_action")

    return {
        "report_id": "tau_lensing_score_readiness_decision_v01",
        "claim_boundary": "score_readiness_decision_only_no_score_run_no_dark_sector_verdict",
        "readiness_decision": readiness_decision,
        "blocking_layer": blocking_layer,
        "act_environment_ready": env_ready,
        "selected_route_count": route_count,
        "route_evidence_firewall_passed": firewall_passed,
        "route_evidence_firewall_selected_route": firewall.get("selected_route"),
        "projection_replay_written": replay_written,
        "preflight_ready": preflight_ready,
        "pipeline_ready": pipeline_ready,
        "score_run": report.get("score_run") is True,
        "dark_sector_verdict": False,
        "next_required_action": next_action,
        "source_pipeline_report_id": report.get("report_id"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Decide reduced Tau lensing score readiness from pipeline state.")
    parser.add_argument(
        "--write-decision",
        default=None,
        nargs="?",
        const=str(DEFAULT_DECISION),
        help=f"Optional JSON decision path. Defaults to {DEFAULT_DECISION} when passed without a path.",
    )
    args = parser.parse_args()

    decision = decide(run_pipeline())
    text = json.dumps(decision, indent=2, sort_keys=True)
    if args.write_decision:
        path = Path(args.write_decision)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
