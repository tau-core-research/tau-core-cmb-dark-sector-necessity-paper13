#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCORE_GATE = ROOT / "scripts/run_tau_lensing_score_gate.py"
DEFAULT_GUARD = ROOT / "data/derived/cmb_tau_lensing_score_attempt_guard_v01.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def build_guard() -> dict[str, Any]:
    gate = run_json([sys.executable, str(SCORE_GATE), "--write-gate"])
    allowed = gate.get("score_gate_passed") is True
    if allowed:
        guard_decision = "ALLOW_SCORE_ATTEMPT"
        next_required_action = "run_make_score_report"
    else:
        guard_decision = "BLOCK_SCORE_ATTEMPT"
        next_required_action = gate.get("unblock_next_required_action") or "inspect_score_gate"

    return {
        "report_id": "tau_lensing_score_attempt_guard_v01",
        "claim_boundary": "score_attempt_guard_only_no_score_run_no_dark_sector_verdict",
        "guard_decision": guard_decision,
        "score_attempt_allowed": allowed,
        "score_gate_passed": gate.get("score_gate_passed") is True,
        "readiness_decision": gate.get("readiness_decision"),
        "blocking_layer": gate.get("blocking_layer"),
        "selected_route_count": gate.get("selected_route_count"),
        "route_submission_audit_decision": gate.get("route_submission_audit_decision"),
        "route_submission_ready_for_materializer": gate.get("route_submission_ready_for_materializer") is True,
        "projection_replay_written": gate.get("projection_replay_written") is True,
        "preflight_ready": gate.get("preflight_ready") is True,
        "pipeline_ready": gate.get("pipeline_ready") is True,
        "act_environment_ready": gate.get("act_environment_ready") is True,
        "smoke_passed": gate.get("smoke_passed") is True,
        "positive_score_path_smoke_passed": gate.get("positive_score_path_smoke_passed") is True,
        "firewall_blocker_smoke_passed": gate.get("firewall_blocker_smoke_passed") is True,
        "good_route_submission_smoke_passed": gate.get("good_route_submission_smoke_passed") is True,
        "next_commands": gate.get("next_commands"),
        "next_required_action": next_required_action,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "source_score_gate_report_id": gate.get("report_id"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Guard the reduced Tau lensing score attempt without running score.")
    parser.add_argument(
        "--write-guard",
        default=None,
        nargs="?",
        const=str(DEFAULT_GUARD),
        help=f"Optional JSON guard path. Defaults to {DEFAULT_GUARD} when passed without a path.",
    )
    args = parser.parse_args()

    guard = build_guard()
    text = json.dumps(guard, indent=2, sort_keys=True)
    if args.write_guard:
        path = Path(args.write_guard)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
