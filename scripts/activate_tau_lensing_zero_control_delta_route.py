#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAYLOADS = ROOT / "payloads"
ARCHIVE = PAYLOADS / "archive"
FAILURE = PAYLOADS / "tau_lensing_response_grid_failure_statement_v01.md"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_zero_control_delta_activation_v01.json"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def run_json(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            json.dumps(
                {
                    "command": command,
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                indent=2,
                sort_keys=True,
            )
        )
    return json.loads(completed.stdout)


def archive_failure() -> Path | None:
    if not FAILURE.exists():
        return None
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archived = ARCHIVE / f"tau_lensing_response_grid_failure_statement_v01.archived_{stamp}.md"
    shutil.copy2(FAILURE, archived)
    FAILURE.unlink()
    return archived


def restore_failure(archived: Path | None) -> None:
    if archived is not None and archived.exists() and not FAILURE.exists():
        shutil.copy2(archived, FAILURE)


def main() -> None:
    parser = argparse.ArgumentParser(description="Activate the zero-control delta route as the single active route.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    dry_run = run_json(
        [
            sys.executable,
            "scripts/promote_tau_lensing_staging_payload.py",
            "--route",
            "delta_PP_tau_against_named_fiducial_PP",
            "--dry-run",
            "--write-report",
        ]
    )
    if dry_run.get("promotion_decision") != "DRY_RUN_PROMOTION_READY":
        report = {
            "report_id": "cmb_tau_lensing_zero_control_delta_activation_v01",
            "claim_boundary": "zero_control_delta_activation_only_no_score_no_dark_sector_verdict",
            "activation_decision": "BLOCKED_DELTA_DRY_RUN_NOT_READY",
            "dry_run": dry_run,
            "score_run": False,
            "dark_sector_verdict": False,
            "next_required_action": "repair_delta_staging_package_before_activation",
        }
    else:
        archived = archive_failure()
        try:
            promotion = run_json(
                [
                    sys.executable,
                    "scripts/promote_tau_lensing_staging_payload.py",
                    "--route",
                    "delta_PP_tau_against_named_fiducial_PP",
                    "--write-report",
                ]
            )
            if promotion.get("promotion_decision") != "PROMOTED_TO_PAYLOADS":
                restore_failure(archived)
                activation_decision = "BLOCKED_PROMOTION_FAILED_FAILURE_RESTORED"
            else:
                activation_decision = "ZERO_CONTROL_DELTA_ROUTE_ACTIVATED"
            intake = run_json([sys.executable, "scripts/intake_tau_lensing_route_evidence.py", "--write-report"])
            firewall = run_json([sys.executable, "scripts/check_tau_lensing_route_evidence_firewall.py", "--write-report"])
            report = {
                "report_id": "cmb_tau_lensing_zero_control_delta_activation_v01",
                "claim_boundary": "zero_control_delta_activation_only_no_score_no_dark_sector_verdict",
                "activation_decision": activation_decision,
                "archived_failure_statement": rel(archived) if archived else None,
                "promotion": promotion,
                "intake": intake,
                "firewall": firewall,
                "score_run": False,
                "dark_sector_verdict": False,
                "next_required_action": (
                    "run_materialize_replay_then_preflight"
                    if activation_decision == "ZERO_CONTROL_DELTA_ROUTE_ACTIVATED"
                    else "inspect_promotion_report"
                ),
            }
        except Exception:
            restore_failure(archived)
            raise

    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
