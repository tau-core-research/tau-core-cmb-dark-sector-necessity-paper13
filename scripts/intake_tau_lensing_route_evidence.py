#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_evidence_intake_report_v01.json"

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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def file_status(paths: list[Path]) -> dict[str, Any]:
    present = [rel(path) for path in paths if path.exists()]
    missing = [rel(path) for path in paths if not path.exists()]
    return {
        "complete": len(missing) == 0,
        "present_count": len(present),
        "missing_count": len(missing),
        "present_files": present,
        "missing_files": missing,
    }


def next_action(selected: list[str], statuses: dict[str, dict[str, Any]]) -> str:
    if len(selected) > 1:
        return "resolve_route_collision_keep_exactly_one_allowed_route"
    if selected == ["direct_tau_PP_grid"]:
        return "run_validate_direct_grid_then_projection_replay"
    if selected == ["delta_PP_tau_against_named_fiducial_PP"]:
        return "run_validate_delta_grid_then_projection_replay"
    if selected == ["explicit_failure_no_endpoint_blind_grid"]:
        return "record_failure_route_score_remains_blocked"
    if statuses["direct_tau_PP_grid"]["present_count"] > 0:
        return "complete_or_remove_partial_direct_route_files"
    if statuses["delta_PP_tau_against_named_fiducial_PP"]["present_count"] > 0:
        return "complete_or_remove_partial_delta_route_files"
    if statuses["explicit_failure_no_endpoint_blind_grid"]["present_count"] > 0:
        return "complete_or_remove_partial_failure_route_files"
    return "fill_exactly_one_staging_route_evidence_set_then_run_guarded_staging_promotion"


def build_report() -> dict[str, Any]:
    statuses = {
        "direct_tau_PP_grid": file_status(DIRECT_FILES),
        "delta_PP_tau_against_named_fiducial_PP": file_status(DELTA_FILES),
        "explicit_failure_no_endpoint_blind_grid": file_status(FAILURE_FILES),
    }
    selected = [route for route, status in statuses.items() if status["complete"]]
    return {
        "report_id": "tau_lensing_route_evidence_intake_v01",
        "claim_boundary": "route_evidence_intake_only_no_grid_validation_no_score_no_dark_sector_verdict",
        "selected_route_count": len(selected),
        "selected_routes": selected,
        "route_status": statuses,
        "intake_decision": (
            "ONE_ROUTE_ACCEPTED_FOR_NEXT_VALIDATION"
            if len(selected) == 1
            else "ROUTE_EVIDENCE_INTAKE_BLOCKED"
        ),
        "accepted_for_tau_score": False,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": next_action(selected, statuses),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify submitted Tau lensing route evidence.")
    parser.add_argument(
        "--write-report",
        default=None,
        help=f"Optional JSON report path. Defaults to {DEFAULT_REPORT} when passed without an explicit path.",
        nargs="?",
        const=str(DEFAULT_REPORT),
    )
    args = parser.parse_args()

    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
