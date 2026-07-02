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
FIREWALL = ROOT / "scripts/check_tau_lensing_route_evidence_firewall.py"
GRID_VALIDATOR = ROOT / "scripts/validate_tau_lensing_grid_payload.py"
DEFAULT_REPLAY = ROOT / "payloads/tau_lensing_pp_grid_projection_replay_v01.json"

ROUTE_TO_GRID = {
    "direct_tau_PP_grid": (ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv", "direct_tau_PP_grid"),
    "delta_PP_tau_against_named_fiducial_PP": (
        ROOT / "payloads/tau_lensing_response_delta_pp_v01.csv",
        "delta_PP_tau",
    ),
}


def run_json(cmd: list[str]) -> dict[str, Any]:
    completed = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def blocked_report(intake: dict[str, Any], firewall: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "report_id": "tau_lensing_projection_replay_materialization_blocked_v01",
        "claim_boundary": "projection_replay_materialization_only_no_score_no_dark_sector_verdict",
        "projection_replay_written": False,
        "score_run": False,
        "dark_sector_verdict": False,
        "blocking_intake": intake,
        "blocking_firewall": firewall,
        "next_required_action": intake.get("next_required_action"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize Tau lensing projection replay from the selected route, without scoring."
    )
    parser.add_argument(
        "--replay-out",
        default=str(DEFAULT_REPLAY),
        help="Output replay JSON path produced by the grid validator.",
    )
    args = parser.parse_args()

    intake = run_json([sys.executable, str(INTAKE)])
    selected = intake.get("selected_routes", [])
    if intake.get("intake_decision") != "ONE_ROUTE_ACCEPTED_FOR_NEXT_VALIDATION" or len(selected) != 1:
        print(json.dumps(blocked_report(intake), indent=2, sort_keys=True))
        return

    firewall = run_json([sys.executable, str(FIREWALL)])
    if firewall.get("firewall_passed") is not True:
        report = blocked_report(intake, firewall)
        report["next_required_action"] = firewall.get("next_required_action")
        print(json.dumps(report, indent=2, sort_keys=True))
        return

    route = selected[0]
    if route == "explicit_failure_no_endpoint_blind_grid":
        report = blocked_report(intake, firewall)
        report["next_required_action"] = "record_failure_route_score_remains_blocked"
        print(json.dumps(report, indent=2, sort_keys=True))
        return

    if route not in ROUTE_TO_GRID:
        raise ValueError(f"unsupported selected route: {route}")

    grid_path, validator_route = ROUTE_TO_GRID[route]
    replay_out = Path(args.replay_out)
    validation = run_json(
        [
            sys.executable,
            str(GRID_VALIDATOR),
            str(grid_path),
            "--route",
            validator_route,
            "--project",
            "--write-replay",
            str(replay_out),
        ]
    )
    report = {
        "report_id": "tau_lensing_projection_replay_materialization_completed_v01",
        "claim_boundary": "projection_replay_materialization_only_no_score_no_dark_sector_verdict",
        "selected_route": route,
        "validator_route": validator_route,
        "grid_file": str(grid_path.relative_to(ROOT)),
        "replay_file": str(replay_out.relative_to(ROOT) if replay_out.is_relative_to(ROOT) else replay_out),
        "projection_replay_written": True,
        "projection_replay_valid_shape": validation.get("projection_replay", {}).get("projected_shape") == [18],
        "validation_report": validation,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "run_preflight_then_score_pipeline",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
