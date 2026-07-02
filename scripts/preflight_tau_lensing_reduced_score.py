#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


DIRECT_FILES = [
    ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv",
    ROOT / "payloads/tau_lensing_response_grid_route_declaration_v01.md",
    ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json",
]
DELTA_FILES = [
    ROOT / "payloads/tau_lensing_response_delta_pp_v01.csv",
    ROOT / "payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
    ROOT / "payloads/tau_lensing_response_grid_route_declaration_v01.md",
    ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json",
]
FAILURE_FILES = [
    ROOT / "payloads/tau_lensing_response_grid_failure_statement_v01.md",
]
REPLAY_FILE = ROOT / "payloads/tau_lensing_pp_grid_projection_replay_v01.json"
FIREWALL = ROOT / "scripts/check_tau_lensing_route_evidence_firewall.py"
RUNNER = ROOT / "scripts/run_tau_lensing_reduced_score.py"
OUTPUT_VALIDATOR = ROOT / "scripts/validate_tau_lensing_reduced_score_output.py"


def exists_all(paths: list[Path]) -> bool:
    return all(path.exists() for path in paths)


def route_status() -> dict[str, Any]:
    direct = exists_all(DIRECT_FILES)
    delta = exists_all(DELTA_FILES)
    failure = exists_all(FAILURE_FILES)
    selected_count = sum([direct, delta, failure])
    return {
        "direct_route_complete": direct,
        "delta_route_complete": delta,
        "failure_route_complete": failure,
        "exactly_one_route_complete": selected_count == 1,
        "selected_route_count": selected_count,
        "missing_direct_files": [str(path.relative_to(ROOT)) for path in DIRECT_FILES if not path.exists()],
        "missing_delta_files": [str(path.relative_to(ROOT)) for path in DELTA_FILES if not path.exists()],
        "missing_failure_files": [str(path.relative_to(ROOT)) for path in FAILURE_FILES if not path.exists()],
    }


def replay_status() -> dict[str, Any]:
    if not REPLAY_FILE.exists():
        return {"projection_replay_exists": False, "projection_replay_valid_shape": False}
    replay = json.loads(REPLAY_FILE.read_text())
    projection = replay.get("projection_replay", {})
    return {
        "projection_replay_exists": True,
        "projection_replay_score_computed_false": replay.get("score_computed") is False,
        "projection_replay_dark_sector_verdict_false": replay.get("dark_sector_verdict") is False,
        "projection_replay_valid_shape": projection.get("projected_shape") == [18],
    }


def firewall_status() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(FIREWALL)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    report = json.loads(completed.stdout)
    return {
        "firewall_passed": report.get("firewall_passed") is True,
        "selected_route": report.get("selected_route"),
        "next_required_action": report.get("next_required_action"),
    }


def next_action(ready: bool, routes: dict[str, Any], firewall: dict[str, Any], replay: dict[str, Any]) -> str:
    if ready:
        return "run_make_score_attempt_guard_then_make_score_report_if_allowed"
    if routes["selected_route_count"] != 1:
        return "fill_exactly_one_staging_route_evidence_set_then_run_guarded_staging_promotion"
    if routes["failure_route_complete"]:
        return "preserve_failure_route_no_score_run"
    if firewall["firewall_passed"] is not True:
        return firewall.get("next_required_action") or "repair_route_evidence_or_record_failure"
    if replay.get("projection_replay_exists") is not True or replay.get("projection_replay_valid_shape") is not True:
        return "run_make_materialize_replay"
    return "inspect_preflight_blocker"


def main() -> None:
    routes = route_status()
    replay = replay_status()
    firewall = firewall_status()
    ready = (
        routes["exactly_one_route_complete"]
        and not routes["failure_route_complete"]
        and firewall["firewall_passed"] is True
        and replay.get("projection_replay_exists") is True
        and replay.get("projection_replay_score_computed_false") is True
        and replay.get("projection_replay_dark_sector_verdict_false") is True
        and replay.get("projection_replay_valid_shape") is True
        and RUNNER.exists()
        and OUTPUT_VALIDATOR.exists()
    )
    report = {
        "report_id": "tau_lensing_reduced_score_preflight_v01",
        "claim_boundary": "score_preflight_only_no_score_run_no_dark_sector_verdict",
        "ready_for_reduced_score_execution": ready,
        "route_status": routes,
        "firewall_status": firewall,
        "projection_replay_status": replay,
        "runner_exists": RUNNER.exists(),
        "output_validator_exists": OUTPUT_VALIDATOR.exists(),
        "next_required_action": next_action(ready, routes, firewall, replay),
        "score_run": False,
        "dark_sector_verdict": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
