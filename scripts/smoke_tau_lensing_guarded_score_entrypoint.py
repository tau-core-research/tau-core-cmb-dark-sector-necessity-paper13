#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TMP_RECEIPT = ROOT / ".tmp/tau_lensing_guarded_blocked_smoke_receipt.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    if TMP_RECEIPT.exists():
        TMP_RECEIPT.unlink()
    guarded = run_json(
        [
            sys.executable,
            "scripts/run_tau_lensing_guarded_score_report.py",
            "--write-receipt",
            str(TMP_RECEIPT),
        ]
    )
    receipt = json.loads(TMP_RECEIPT.read_text())
    TMP_RECEIPT.unlink()
    check(guarded["report_id"] == "tau_lensing_guarded_score_blocked_v01", "guarded score must block now")
    check(guarded["score_attempt_allowed"] is False, "guarded score must not allow score attempt now")
    check(guarded["score_run"] is False, "guarded score must not run score while blocked")
    check(guarded["physical_tau_score_run"] is False, "guarded score must not report physical score run")
    check(guarded["dark_sector_verdict"] is False, "guarded score must not issue verdict")
    check(
        guarded["readiness_decision"] == "BLOCKED_ON_TAU_ROUTE_EVIDENCE",
        "guarded score must preserve route-evidence blocker",
    )
    check(receipt["receipt_status"] == "BLOCKED_BEFORE_SCORE_EXECUTION", "blocked receipt status mismatch")
    check(receipt["score_run"] is False, "blocked receipt must not mark score run")

    report = {
        "report_id": "tau_lensing_guarded_score_entrypoint_smoke_v01",
        "claim_boundary": "guarded_score_entrypoint_smoke_only_no_score_run_no_dark_sector_verdict",
        "guarded_report_id": guarded["report_id"],
        "readiness_decision": guarded["readiness_decision"],
        "score_attempt_allowed": guarded["score_attempt_allowed"],
        "receipt_status": receipt["receipt_status"],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
