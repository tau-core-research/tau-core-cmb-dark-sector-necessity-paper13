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
STAGING = ROOT / "payload_staging"
PAYLOADS = ROOT / "payloads"
PRECHECK = ROOT / "scripts/precheck_tau_lensing_staging_promotion.py"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_staging_promotion_report_v01.json"


ROUTE_FILES = {
    "direct_tau_PP_grid": {
        "tau_lensing_response_pp_grid_v01.csv": "tau_lensing_response_pp_grid_v01.csv",
        "tau_lensing_response_grid_route_declaration_v01.md": "tau_lensing_response_grid_route_declaration_v01.md",
        "tau_lensing_response_grid_provenance_v01.json": "tau_lensing_response_grid_provenance_v01.json",
    },
    "delta_PP_tau_against_named_fiducial_PP": {
        "tau_lensing_response_delta_pp_v01.csv": "tau_lensing_response_delta_pp_v01.csv",
        "tau_lensing_response_fiducial_pp_reference_v01.json": "tau_lensing_response_fiducial_pp_reference_v01.json",
        "tau_lensing_response_grid_route_declaration_v01.md": "tau_lensing_response_grid_route_declaration_v01.md",
        "tau_lensing_response_grid_provenance_v01.json": "tau_lensing_response_grid_provenance_v01.json",
    },
    "explicit_failure_no_endpoint_blind_grid": {
        "tau_lensing_response_grid_failure_statement_v01.md": "tau_lensing_response_grid_failure_statement_v01.md",
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def build_report(route: str, *, dry_run: bool, allow_replace: bool) -> dict[str, Any]:
    precheck = run_json([sys.executable, str(PRECHECK), "--route", route, "--write-report"])
    mapping = ROUTE_FILES[route]
    planned_copies = [
        {
            "source": rel(STAGING / route / source_name),
            "destination": rel(PAYLOADS / destination_name),
        }
        for source_name, destination_name in mapping.items()
    ]
    existing_destinations = [
        item["destination"]
        for item in planned_copies
        if (ROOT / item["destination"]).exists()
    ]

    archived_destinations: list[dict[str, str]] = []

    if precheck.get("promotion_ready") is not True:
        decision = "BLOCKED_STAGING_PRECHECK_FAILED"
        promoted = False
        next_required_action = "repair_staging_files_before_payload_promotion"
    elif existing_destinations and not allow_replace:
        decision = "BLOCKED_DESTINATION_PAYLOAD_EXISTS"
        promoted = False
        next_required_action = "remove_or_archive_existing_payload_route_before_promotion"
    elif dry_run:
        decision = "DRY_RUN_REPLACEMENT_PROMOTION_READY" if existing_destinations else "DRY_RUN_PROMOTION_READY"
        promoted = False
        next_required_action = "rerun_without_dry_run_to_promote_reviewed_payload"
    else:
        PAYLOADS.mkdir(parents=True, exist_ok=True)
        if existing_destinations:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            archive_dir = PAYLOADS / "archive" / f"{route}_{stamp}"
            archive_dir.mkdir(parents=True, exist_ok=True)
            for destination in existing_destinations:
                source = ROOT / destination
                archive_path = archive_dir / source.name
                shutil.copy2(source, archive_path)
                archived_destinations.append(
                    {"source": rel(source), "archive": rel(archive_path)}
                )
        for source_name, destination_name in mapping.items():
            shutil.copy2(STAGING / route / source_name, PAYLOADS / destination_name)
        decision = "REPLACED_EXISTING_PAYLOADS" if existing_destinations else "PROMOTED_TO_PAYLOADS"
        promoted = True
        next_required_action = "run_make_intake_then_make_evidence_check"

    return {
        "report_id": "tau_lensing_staging_promotion_report_v01",
        "claim_boundary": "staging_promotion_report_only_no_score_no_dark_sector_verdict",
        "selected_route": route,
        "promotion_decision": decision,
        "promotion_ready": precheck.get("promotion_ready") is True,
        "dry_run": dry_run,
        "payload_copy_performed": promoted,
        "planned_copies": planned_copies,
        "existing_destinations": existing_destinations,
        "allow_replace": allow_replace,
        "archived_destinations": archived_destinations,
        "blocking_precheck": precheck if precheck.get("promotion_ready") is not True else None,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": next_required_action,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote a reviewed Tau lensing staging route into payloads/.")
    parser.add_argument("--route", choices=sorted(ROUTE_FILES), required=True)
    parser.add_argument("--dry-run", action="store_true", help="Check promotion readiness without copying files.")
    parser.add_argument("--allow-replace", action="store_true", help="Archive and replace existing payload files.")
    parser.add_argument(
        "--write-report",
        default=None,
        nargs="?",
        const=str(DEFAULT_REPORT),
        help=f"Optional JSON report path. Defaults to {DEFAULT_REPORT} when passed without a path.",
    )
    args = parser.parse_args()

    report = build_report(args.route, dry_run=args.dry_run, allow_replace=args.allow_replace)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
