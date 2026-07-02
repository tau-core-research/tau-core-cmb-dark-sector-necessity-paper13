#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "scripts/smoke_tau_lensing_scoring_gates.py"
POSITIVE_SMOKE = ROOT / "scripts/smoke_tau_lensing_positive_score_path.py"
FIREWALL_SMOKE = ROOT / "scripts/smoke_tau_lensing_firewall_blocker_path.py"
GOOD_ROUTE_SMOKE = ROOT / "scripts/smoke_tau_lensing_good_route_submission_path.py"
ENV = ROOT / "scripts/check_tau_lensing_scoring_environment.py"
READINESS = ROOT / "scripts/decide_tau_lensing_score_readiness.py"
UNBLOCK = ROOT / "scripts/build_tau_lensing_score_unblock_bundle.py"
SUBMISSION_AUDIT = ROOT / "scripts/audit_tau_lensing_route_submission.py"
DEFAULT_GATE = ROOT / "data/derived/cmb_tau_lensing_score_gate_v01.json"
LOCK_DIR = ROOT / ".tmp/tau_lensing_score_gate.lock"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


@contextlib.contextmanager
def score_gate_lock(timeout_seconds: float = 60.0):
    LOCK_DIR.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    acquired = False
    while not acquired:
        try:
            LOCK_DIR.mkdir()
            acquired = True
        except FileExistsError:
            if time.monotonic() - start > timeout_seconds:
                raise TimeoutError(f"timed out waiting for score gate lock: {LOCK_DIR}")
            time.sleep(0.1)
    try:
        yield
    finally:
        if acquired:
            LOCK_DIR.rmdir()


def build_gate(*, with_regression_smokes: bool = False) -> dict[str, Any]:
    environment = run_json([sys.executable, str(ENV), "--write-report"])
    readiness = run_json([sys.executable, str(READINESS), "--write-decision"])
    unblock = run_json([sys.executable, str(UNBLOCK), "--write-bundle"])
    submission_audit = run_json([sys.executable, str(SUBMISSION_AUDIT), "--write-audit"])
    smoke: dict[str, Any] = {}
    positive_smoke: dict[str, Any] = {}
    firewall_smoke: dict[str, Any] = {}
    good_route_smoke: dict[str, Any] = {}
    if with_regression_smokes:
        smoke = run_json([sys.executable, str(SMOKE)])
        positive_smoke = run_json([sys.executable, str(POSITIVE_SMOKE)])
        firewall_smoke = run_json([sys.executable, str(FIREWALL_SMOKE)])
        good_route_smoke = run_json([sys.executable, str(GOOD_ROUTE_SMOKE)])
        smoke_passed = smoke.get("smoke_passed") is True
        positive_score_path_smoke_passed = (
            positive_smoke.get("projection_replay_valid_shape") is True
            and positive_smoke.get("score_schema_validated") is True
            and positive_smoke.get("tau_evidence_used") is False
            and positive_smoke.get("score_is_physical_tau_score") is False
            and positive_smoke.get("dark_sector_verdict") is False
        )
        firewall_blocker_smoke_passed = (
            firewall_smoke.get("smoke_passed") is True
            and firewall_smoke.get("readiness_decision") == "BLOCKED_ON_ROUTE_EVIDENCE_FIREWALL"
            and firewall_smoke.get("score_run") is False
            and firewall_smoke.get("dark_sector_verdict") is False
        )
        good_route_submission_smoke_passed = (
            good_route_smoke.get("smoke_passed") is True
            and good_route_smoke.get("submission_audit_decision") == "NUMERIC_ROUTE_READY_FOR_MATERIALIZE_REPLAY"
            and good_route_smoke.get("numeric_route_ready_for_materializer") is True
            and good_route_smoke.get("projection_replay_valid_shape") is True
            and good_route_smoke.get("score_is_physical_tau_score") is False
            and good_route_smoke.get("dark_sector_verdict") is False
        )
    else:
        smoke_passed = True
        positive_score_path_smoke_passed = True
        firewall_blocker_smoke_passed = True
        good_route_submission_smoke_passed = True
    act_environment_ready = environment.get("environment_ready_for_reduced_score_once_tau_replay_exists") is True
    readiness_ready = readiness.get("readiness_decision") == "READY_TO_SCORE"
    score_gate_passed = (
        readiness_ready
        and smoke_passed
        and positive_score_path_smoke_passed
        and firewall_blocker_smoke_passed
        and good_route_submission_smoke_passed
        and act_environment_ready
    )
    return {
        "report_id": "tau_lensing_score_gate_v01",
        "claim_boundary": "score_gate_only_no_score_run_no_dark_sector_verdict",
        "score_gate_passed": score_gate_passed,
        "score_gate_pass_requires_all_smokes_and_environment": with_regression_smokes,
        "regression_smokes_run": with_regression_smokes,
        "smoke_passed": smoke_passed,
        "positive_score_path_smoke_passed": positive_score_path_smoke_passed,
        "firewall_blocker_smoke_passed": firewall_blocker_smoke_passed,
        "firewall_blocker_smoke_submission_audit_decision": firewall_smoke.get("submission_audit_decision"),
        "firewall_blocker_smoke_ready_for_materializer": (
            firewall_smoke.get("numeric_route_ready_for_materializer") is True
        ),
        "good_route_submission_smoke_passed": good_route_submission_smoke_passed,
        "good_route_submission_smoke_audit_decision": good_route_smoke.get("submission_audit_decision"),
        "good_route_submission_smoke_ready_for_materializer": (
            good_route_smoke.get("numeric_route_ready_for_materializer") is True
        ),
        "act_environment_ready": act_environment_ready,
        "readiness_decision": readiness.get("readiness_decision"),
        "route_submission_audit_decision": submission_audit.get("audit_decision"),
        "route_submission_ready_for_materializer": submission_audit.get("numeric_route_ready_for_materializer") is True,
        "blocking_layer": readiness.get("blocking_layer"),
        "selected_route_count": readiness.get("selected_route_count"),
        "projection_replay_written": readiness.get("projection_replay_written"),
        "preflight_ready": readiness.get("preflight_ready"),
        "pipeline_ready": readiness.get("pipeline_ready"),
        "unblock_next_required_action": unblock.get("next_required_action"),
        "next_commands": unblock.get("next_commands"),
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the aggregate Tau lensing score gate.")
    parser.add_argument(
        "--with-regression-smokes",
        action="store_true",
        help="Also run synthetic regression smokes. Use away from real route payload submission.",
    )
    parser.add_argument(
        "--write-gate",
        default=None,
        nargs="?",
        const=str(DEFAULT_GATE),
        help=f"Optional JSON gate path. Defaults to {DEFAULT_GATE} when passed without a path.",
    )
    args = parser.parse_args()

    with score_gate_lock():
        gate = build_gate(with_regression_smokes=args.with_regression_smokes)
    text = json.dumps(gate, indent=2, sort_keys=True)
    if args.write_gate:
        path = Path(args.write_gate)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
