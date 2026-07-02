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
DEFAULT_TODO = ROOT / "data/derived/cmb_tau_lensing_scoring_todo_v01.json"


ROUTE_COMMANDS = {
    "direct_tau_PP_grid": [
        "make staging-promote-direct-dry-run",
        "make staging-promote-direct",
        "make prepare-direct-hash",
        "make intake",
        "make evidence-check",
        "make route-submission-audit",
        "make materialize-replay",
        "make preflight",
        "make score-attempt-guard",
        "make score-report",
        "make score-output-audit",
    ],
    "delta_PP_tau_against_named_fiducial_PP": [
        "make staging-promote-delta-dry-run",
        "make staging-promote-delta",
        "make prepare-delta-hash",
        "make intake",
        "make evidence-check",
        "make route-submission-audit",
        "make materialize-replay",
        "make preflight",
        "make score-attempt-guard",
        "make score-report",
        "make score-output-audit",
    ],
    "explicit_failure_no_endpoint_blind_grid": [
        "make staging-promote-failure-dry-run",
        "make staging-promote-failure",
        "make intake",
        "make evidence-check",
        "make route-submission-audit",
        "make score-report",
    ],
}


def run_pipeline() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(PIPELINE), "--dry-run", "--write-report"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def build_todo(report: dict[str, Any]) -> dict[str, Any]:
    intake = report.get("blocking_intake", {})
    route_status = intake.get("route_status", {})
    selected = intake.get("selected_routes", [])
    selected_route = selected[0] if len(selected) == 1 else None

    if report.get("pipeline_ready") is True:
        todo_status = "READY_TO_RUN_SCORE_OR_SCORE_ALREADY_RUN"
        next_commands = ["make score-attempt-guard", "make score-report", "make score-output-audit"]
        missing_by_route: dict[str, list[str]] = {}
    elif selected_route:
        todo_status = "ROUTE_SELECTED_CONTINUE_GATE_SEQUENCE"
        next_commands = ROUTE_COMMANDS.get(selected_route, ["make score-report"])
        missing_by_route = {
            route: status.get("missing_files", [])
            for route, status in route_status.items()
            if route == selected_route
        }
    else:
        todo_status = "SUBMIT_EXACTLY_ONE_ROUTE_EVIDENCE_SET"
        next_commands = [
            "make payload-checklist",
            "make staging-promote-direct-dry-run or make staging-promote-delta-dry-run or make staging-promote-failure-dry-run",
            "make staging-promote-direct or make staging-promote-delta or make staging-promote-failure after dry-run promotion is ready",
            "make intake",
            "make evidence-check",
            "make route-submission-audit",
            "make materialize-replay",
            "make preflight",
            "make score-attempt-guard",
            "make score-report only if score-attempt-guard allows",
            "make score-output-audit",
        ]
        missing_by_route = {
            route: status.get("missing_files", [])
            for route, status in route_status.items()
        }

    return {
        "report_id": "tau_lensing_scoring_todo_v01",
        "claim_boundary": "scoring_todo_only_no_score_run_no_dark_sector_verdict",
        "todo_status": todo_status,
        "pipeline_report_id": report.get("report_id"),
        "pipeline_ready": report.get("pipeline_ready") is True,
        "score_run": report.get("score_run") is True,
        "dark_sector_verdict": False,
        "selected_route_count": intake.get("selected_route_count", 0),
        "selected_routes": selected,
        "missing_files_by_route": missing_by_route,
        "next_commands": next_commands,
        "next_required_action": report.get("next_required_action"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the next concrete Tau lensing scoring todo.")
    parser.add_argument(
        "--write-todo",
        default=None,
        nargs="?",
        const=str(DEFAULT_TODO),
        help=f"Optional JSON todo path. Defaults to {DEFAULT_TODO} when passed without a path.",
    )
    args = parser.parse_args()

    todo = build_todo(run_pipeline())
    text = json.dumps(todo, indent=2, sort_keys=True)
    if args.write_todo:
        path = Path(args.write_todo)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
