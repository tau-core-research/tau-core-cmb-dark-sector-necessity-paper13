#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHECKLIST = ROOT / "data/derived/cmb_tau_lensing_payload_acceptance_checklist_v01.json"


def route_checklist() -> dict[str, Any]:
    common_forbidden = [
        "do_not_copy_TEMPLATE_NOT_PAYLOAD_files_to_payloads_as_real_inputs",
        "do_not_select_route_from_ACT_or_Planck_residuals",
        "do_not_select_route_from_reduced_chi2",
        "do_not_select_route_from_dark_sector_verdict_preference",
        "do_not_submit_endpoint-fit_or_posterior-tuned_grid",
    ]
    numeric_grid_requirements = [
        "exactly_3000_numeric_rows",
        "two_columns_preferred_L_value",
        "L_column_exactly_10_to_3009_if_present",
        "all_values_finite",
        "no_TEMPLATE_NOT_PAYLOAD_marker",
        "numeric_grid_sha256_recorded_in_provenance",
    ]
    return {
        "direct_tau_PP_grid": {
            "required_files": [
                "payloads/tau_lensing_response_pp_grid_v01.csv",
                "payloads/tau_lensing_response_grid_route_declaration_v01.md",
                "payloads/tau_lensing_response_grid_provenance_v01.json",
            ],
            "numeric_grid_requirements": numeric_grid_requirements,
            "route_declaration_required_fragments": [
                "selected_route: direct_tau_PP_grid",
                "numeric_grid_file: payloads/tau_lensing_response_pp_grid_v01.csv",
                "fiducial_reference_file: not_used",
                "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
                "index_alignment: L = 10 + i",
            ],
            "provenance_required_keys": [
                "selected_route",
                "numeric_grid_file",
                "numeric_grid_sha256",
                "source_chain",
                "derivation_script_or_formula",
                "no_endpoint_fit_statement",
            ],
            "hash_command": "make prepare-direct-hash",
            "validation_command": "make validate-direct-grid",
            "post_submission_commands": [
                "make staging-promote-direct-dry-run",
                "make staging-promote-direct",
                "make prepare-direct-hash",
                "make intake",
                "make evidence-check",
                "make route-submission-audit",
                "make materialize-replay",
                "make preflight",
                "make score-report",
            ],
        },
        "delta_PP_tau_against_named_fiducial_PP": {
            "required_files": [
                "payloads/tau_lensing_response_delta_pp_v01.csv",
                "payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
                "payloads/tau_lensing_response_grid_route_declaration_v01.md",
                "payloads/tau_lensing_response_grid_provenance_v01.json",
            ],
            "numeric_grid_requirements": numeric_grid_requirements,
            "route_declaration_required_fragments": [
                "selected_route: delta_PP_tau_against_named_fiducial_PP",
                "numeric_grid_file: payloads/tau_lensing_response_delta_pp_v01.csv",
                "fiducial_reference_file: payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
                "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
                "index_alignment: L = 10 + i",
            ],
            "provenance_required_keys": [
                "selected_route",
                "numeric_grid_file",
                "numeric_grid_sha256",
                "source_chain",
                "derivation_script_or_formula",
                "no_endpoint_fit_statement",
            ],
            "fiducial_required_keys": [
                "fiducial_reference_file",
                "fiducial_reference_sha256",
            ],
            "hash_command": "make prepare-delta-hash",
            "validation_command": "make validate-delta-grid",
            "post_submission_commands": [
                "make staging-promote-delta-dry-run",
                "make staging-promote-delta",
                "make prepare-delta-hash",
                "make intake",
                "make evidence-check",
                "make route-submission-audit",
                "make materialize-replay",
                "make preflight",
                "make score-report",
            ],
        },
        "explicit_failure_no_endpoint_blind_grid": {
            "required_files": [
                "payloads/tau_lensing_response_grid_failure_statement_v01.md",
            ],
            "failure_statement_required_keys": [
                "selected_route",
                "failed_required_object",
                "reason",
                "missing_parent_input",
                "missing_derivation_rule",
                "missing_numeric_kernel",
                "missing_normalization",
                "next_theoretical_blocker",
            ],
            "post_submission_commands": [
                "make staging-promote-failure-dry-run",
                "make staging-promote-failure",
                "make intake",
                "make evidence-check",
                "make route-submission-audit",
                "make score-report",
            ],
        },
        "forbidden_shortcuts": common_forbidden,
    }


def build_checklist() -> dict[str, Any]:
    return {
        "report_id": "tau_lensing_payload_acceptance_checklist_v01",
        "claim_boundary": "payload_acceptance_checklist_only_no_payload_validation_no_score_no_dark_sector_verdict",
        "purpose": "pre_submission_checklist_for_exactly_one_tau_lensing_route_payload",
        "accepted_route_count_required": "exactly_one",
        "route_checklist": route_checklist(),
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "fill_exactly_one_route_evidence_set_then_run_make_route_submission_audit",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Tau lensing payload acceptance checklist.")
    parser.add_argument(
        "--write-checklist",
        default=None,
        nargs="?",
        const=str(DEFAULT_CHECKLIST),
        help=f"Optional JSON checklist path. Defaults to {DEFAULT_CHECKLIST} when passed without a path.",
    )
    args = parser.parse_args()
    checklist = build_checklist()
    text = json.dumps(checklist, indent=2, sort_keys=True)
    if args.write_checklist:
        path = Path(args.write_checklist)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
