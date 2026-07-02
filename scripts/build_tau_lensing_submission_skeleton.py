#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_submission_skeleton_v01.json"
STAGING = ROOT / "payload_staging"


ROUTE_FILES = {
    "direct_tau_PP_grid": [
        "tau_lensing_response_pp_grid_v01.csv",
        "tau_lensing_response_grid_route_declaration_v01.md",
        "tau_lensing_response_grid_provenance_v01.json",
    ],
    "delta_PP_tau_against_named_fiducial_PP": [
        "tau_lensing_response_delta_pp_v01.csv",
        "tau_lensing_response_fiducial_pp_reference_v01.json",
        "tau_lensing_response_grid_route_declaration_v01.md",
        "tau_lensing_response_grid_provenance_v01.json",
    ],
    "explicit_failure_no_endpoint_blind_grid": [
        "tau_lensing_response_grid_failure_statement_v01.md",
    ],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_if_missing(path: Path, text: str, overwrite: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return "kept_existing"
    path.write_text(text)
    return "written"


def grid_template(value_name: str) -> str:
    return "\n".join(
        [
            "# TEMPLATE_NOT_PAYLOAD",
            "# Staging skeleton only. Fill with exactly 3000 data rows before guarded promotion to payloads/.",
            "# Required submitted form: two numeric columns, comma separated.",
            "# column 1: L, exactly 10..3009",
            f"# column 2: {value_name}",
            "# Example rows:",
            "# 10,0.0",
            "# 11,0.0",
            "",
        ]
    )


def route_declaration_template(route: str) -> str:
    if route == "direct_tau_PP_grid":
        lines = [
            "# TEMPLATE_NOT_PAYLOAD",
            "selected_route: direct_tau_PP_grid",
            "numeric_grid_file: payloads/tau_lensing_response_pp_grid_v01.csv",
            "fiducial_reference_file: not_used",
            "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
            "index_alignment: L = 10 + i",
            "endpoint_blind_statement:",
        ]
    elif route == "delta_PP_tau_against_named_fiducial_PP":
        lines = [
            "# TEMPLATE_NOT_PAYLOAD",
            "selected_route: delta_PP_tau_against_named_fiducial_PP",
            "numeric_grid_file: payloads/tau_lensing_response_delta_pp_v01.csv",
            "fiducial_reference_file: payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
            "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
            "index_alignment: L = 10 + i",
            "endpoint_blind_statement:",
        ]
    else:
        lines = [
            "# TEMPLATE_NOT_PAYLOAD",
            "selected_route: explicit_failure_no_endpoint_blind_grid",
            "numeric_grid_file: not_used",
            "fiducial_reference_file: not_used",
            "provenance_file: not_used",
            "index_alignment: not_used",
            "endpoint_blind_statement: no endpoint-blind numeric grid can be submitted",
        ]
    return "\n".join(lines) + "\n"


def provenance_template(route: str) -> str:
    numeric_grid_file = (
        "payloads/tau_lensing_response_pp_grid_v01.csv"
        if route == "direct_tau_PP_grid"
        else "payloads/tau_lensing_response_delta_pp_v01.csv"
    )
    return (
        json.dumps(
            {
                "template_status": "TEMPLATE_NOT_PAYLOAD",
                "selected_route": route,
                "numeric_grid_file": numeric_grid_file,
                "numeric_grid_sha256": "",
                "source_chain": "",
                "input_artifacts": [],
                "derivation_script_or_formula": "",
                "created_utc": "",
                "author_or_agent": "",
                "no_endpoint_fit_statement": "",
                "notes": "Staging skeleton only. Remove template_status only after real endpoint-blind payload is filled.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def fiducial_template() -> str:
    return (
        json.dumps(
            {
                "template_status": "TEMPLATE_NOT_PAYLOAD",
                "fiducial_reference_file": "payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
                "fiducial_reference_sha256": "",
                "generated_utc": "",
                "files": [],
                "notes": "Staging skeleton only. Fill with the named fiducial PP reference hash before payload submission.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def failure_template() -> str:
    return "\n".join(
        [
            "# TEMPLATE_NOT_PAYLOAD",
            "selected_route: explicit_failure_no_endpoint_blind_grid",
            "failed_required_object: tau_PP_grid_or_delta_PP_tau",
            "reason:",
            "missing_parent_input:",
            "missing_derivation_rule:",
            "missing_numeric_kernel:",
            "missing_normalization:",
            "next_theoretical_blocker:",
            "",
        ]
    )


def file_text(route: str, filename: str) -> str:
    if filename.endswith("pp_grid_v01.csv"):
        return grid_template("tau_PP_value")
    if filename.endswith("delta_pp_v01.csv"):
        return grid_template("delta_PP_tau_value")
    if filename.endswith("route_declaration_v01.md"):
        return route_declaration_template(route)
    if filename.endswith("provenance_v01.json"):
        return provenance_template(route)
    if filename.endswith("fiducial_pp_reference_v01.json"):
        return fiducial_template()
    if filename.endswith("failure_statement_v01.md"):
        return failure_template()
    raise ValueError(f"unsupported skeleton filename: {filename}")


def build_skeleton(route: str, overwrite: bool) -> dict[str, Any]:
    route_dir = STAGING / route
    files: list[dict[str, str]] = []
    for filename in ROUTE_FILES[route]:
        path = route_dir / filename
        action = write_if_missing(path, file_text(route, filename), overwrite)
        files.append({"path": rel(path), "action": action})
    return {
        "report_id": "tau_lensing_submission_skeleton_v01",
        "claim_boundary": "submission_skeleton_only_not_payload_no_score_no_dark_sector_verdict",
        "selected_route": route,
        "staging_directory": rel(route_dir),
        "files": files,
        "promote_to_payloads_only_after_real_endpoint_blind_values_are_filled": True,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "fill_staging_files_with_real_endpoint_blind_route_evidence_then_run_guarded_staging_promotion",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create non-payload staging skeleton files for a Tau lensing route.")
    parser.add_argument("--route", choices=sorted(ROUTE_FILES), required=True)
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing staging skeleton files.")
    parser.add_argument(
        "--write-report",
        default=None,
        nargs="?",
        const=str(DEFAULT_REPORT),
        help=f"Optional JSON report path. Defaults to {DEFAULT_REPORT} when passed without a path.",
    )
    args = parser.parse_args()

    report = build_skeleton(args.route, args.overwrite)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
