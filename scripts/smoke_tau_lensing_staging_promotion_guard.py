#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROMOTER = ROOT / "scripts/promote_tau_lensing_staging_payload.py"

ROUTES = [
    "direct_tau_PP_grid",
    "delta_PP_tau_against_named_fiducial_PP",
    "explicit_failure_no_endpoint_blind_grid",
]


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    decisions: dict[str, str] = {}
    for route in ROUTES:
        report = run_json([sys.executable, str(PROMOTER), "--route", route, "--dry-run"])
        decisions[route] = report["promotion_decision"]
        check(report["payload_copy_performed"] is False, f"{route} dry-run must not copy payloads")
        check(report["score_run"] is False, f"{route} promotion guard must not run score")
        check(report["dark_sector_verdict"] is False, f"{route} promotion guard must not issue verdict")
        check(
            report["promotion_decision"] in {"BLOCKED_STAGING_PRECHECK_FAILED", "DRY_RUN_PROMOTION_READY"},
            f"{route} unexpected promotion decision",
        )

    report = {
        "report_id": "tau_lensing_staging_promotion_guard_smoke_v01",
        "claim_boundary": "staging_promotion_guard_smoke_only_no_payload_copy_no_score_no_dark_sector_verdict",
        "route_decisions": decisions,
        "payload_copy_performed": False,
        "score_run": False,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
