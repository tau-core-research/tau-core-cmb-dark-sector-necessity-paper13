#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    intake = run_json([sys.executable, "scripts/intake_tau_lensing_route_evidence.py"])
    failure_route_recorded = intake.get("selected_routes") == ["explicit_failure_no_endpoint_blind_grid"]
    no_route_recorded = intake["intake_decision"] == "ROUTE_EVIDENCE_INTAKE_BLOCKED" and intake["selected_route_count"] == 0
    check(no_route_recorded or failure_route_recorded, "intake must either block without route or record explicit failure route")
    check(intake["score_run"] is False, "intake must not run score")
    check(intake["dark_sector_verdict"] is False, "intake must not issue verdict")

    firewall = run_json([sys.executable, "scripts/check_tau_lensing_route_evidence_firewall.py"])
    check(
        firewall["firewall_passed"] is failure_route_recorded,
        "firewall must pass only for the explicit failure route in current-state smoke",
    )
    check(firewall["score_run"] is False, "firewall must not run score")
    check(firewall["dark_sector_verdict"] is False, "firewall must not issue verdict")

    materializer = run_json([sys.executable, "scripts/materialize_tau_lensing_projection_replay.py"])
    check(materializer["projection_replay_written"] is False, "materializer must not write replay without route")
    check(materializer["score_run"] is False, "materializer must not run score")
    check(materializer["dark_sector_verdict"] is False, "materializer must not issue verdict")

    environment = run_json([sys.executable, "scripts/check_tau_lensing_scoring_environment.py"])
    check(
        environment["environment_ready_for_reduced_score_once_tau_replay_exists"] is True,
        "ACT-side scoring environment must be ready",
    )
    check(environment["score_run"] is False, "environment check must not run score")
    check(environment["dark_sector_verdict"] is False, "environment check must not issue verdict")

    preflight = run_json([sys.executable, "scripts/preflight_tau_lensing_reduced_score.py"])
    check(preflight["ready_for_reduced_score_execution"] is False, "preflight must not be ready without route")
    check(preflight["score_run"] is False, "preflight must not run score")
    check(preflight["dark_sector_verdict"] is False, "preflight must not issue verdict")

    pipeline = run_json([sys.executable, "scripts/run_tau_lensing_scoring_pipeline.py"])
    check(pipeline["pipeline_ready"] is False, "pipeline must not be ready without route")
    check(pipeline["score_run"] is False, "pipeline must not run score")
    check(pipeline["dark_sector_verdict"] is False, "pipeline must not issue verdict")

    todo = run_json([sys.executable, "scripts/extract_tau_lensing_scoring_todo.py"])
    check(
        todo["todo_status"] in {"SUBMIT_EXACTLY_ONE_ROUTE_EVIDENCE_SET", "ROUTE_SELECTED_CONTINUE_GATE_SEQUENCE"},
        "todo must request route evidence or preserve the recorded failure route",
    )
    check(todo["score_run"] is False, "todo must not run score")
    check(todo["dark_sector_verdict"] is False, "todo must not issue verdict")

    pack = run_json([sys.executable, "scripts/build_tau_lensing_route_evidence_pack.py"])
    check(pack["selected_route_count"] in {0, 1}, "pack must report no route or the recorded failure route")
    check(pack["score_run"] is False, "pack must not run score")
    check(pack["dark_sector_verdict"] is False, "pack must not issue verdict")

    report = {
        "report_id": "tau_lensing_scoring_gates_smoke_v01",
        "claim_boundary": "scoring_gates_smoke_only_no_score_run_no_dark_sector_verdict",
        "smoke_passed": True,
        "checked_gates": [
            "intake",
            "evidence_firewall",
            "materializer",
            "scoring_environment",
            "preflight",
            "pipeline",
            "todo",
            "route_pack",
        ],
        "score_run": False,
        "dark_sector_verdict": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
