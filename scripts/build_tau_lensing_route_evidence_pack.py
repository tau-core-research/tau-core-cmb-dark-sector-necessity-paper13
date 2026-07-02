#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "scripts/extract_tau_lensing_scoring_todo.py"
DEFAULT_PACK = ROOT / "data/derived/cmb_tau_lensing_route_evidence_pack_v01.json"

ROUTE_PACK = {
    "direct_tau_PP_grid": {
        "submission_files": [
            "payloads/tau_lensing_response_pp_grid_v01.csv",
            "payloads/tau_lensing_response_grid_route_declaration_v01.md",
            "payloads/tau_lensing_response_grid_provenance_v01.json",
        ],
        "safe_templates": [
            "payload_templates/tau_lensing_response_pp_grid_v01.csv",
            "payloads/tau_lensing_response_grid_route_declaration_TEMPLATE_v01.md",
            "payload_templates/tau_lensing_response_payload_provenance_v01.json",
            "payload_templates/tau_lensing_response_firewall_v01.md",
            "payload_templates/tau_lensing_response_claim_boundary_v01.md",
        ],
        "post_submission_commands": [
            "make payload-checklist",
            "make staging-promote-direct-dry-run",
            "make staging-promote-direct",
            "make prepare-direct-hash",
            "make intake",
            "make evidence-check",
            "make route-submission-audit",
            "make materialize-replay",
            "make preflight",
            "make score-attempt-guard",
            "make score-report",
            "make score-output-audit",
        ],
    },
    "delta_PP_tau_against_named_fiducial_PP": {
        "submission_files": [
            "payloads/tau_lensing_response_delta_pp_v01.csv",
            "payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
            "payloads/tau_lensing_response_grid_route_declaration_v01.md",
            "payloads/tau_lensing_response_grid_provenance_v01.json",
        ],
        "safe_templates": [
            "payload_templates/tau_lensing_response_delta_pp_v01.csv",
            "payload_templates/tau_lensing_response_payload_hashes_v01.json",
            "payloads/tau_lensing_response_grid_route_declaration_TEMPLATE_v01.md",
            "payload_templates/tau_lensing_response_payload_provenance_v01.json",
            "payload_templates/tau_lensing_response_firewall_v01.md",
            "payload_templates/tau_lensing_response_claim_boundary_v01.md",
        ],
        "post_submission_commands": [
            "make payload-checklist",
            "make staging-promote-delta-dry-run",
            "make staging-promote-delta",
            "make prepare-delta-hash",
            "make intake",
            "make evidence-check",
            "make route-submission-audit",
            "make materialize-replay",
            "make preflight",
            "make score-attempt-guard",
            "make score-report",
            "make score-output-audit",
        ],
    },
    "explicit_failure_no_endpoint_blind_grid": {
        "submission_files": [
            "payloads/tau_lensing_response_grid_failure_statement_v01.md",
        ],
        "safe_templates": [
            "payloads/tau_lensing_response_grid_failure_statement_TEMPLATE_v01.md",
        ],
        "post_submission_commands": [
            "make payload-checklist",
            "make staging-promote-failure-dry-run",
            "make staging-promote-failure",
            "make intake",
            "make evidence-check",
            "make route-submission-audit",
            "make score-report",
            "make score-output-audit",
        ],
    },
}


def run_todo() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(TODO), "--write-todo"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def build_pack(todo: dict[str, Any]) -> dict[str, Any]:
    missing_by_route = todo.get("missing_files_by_route", {})
    route_options: dict[str, dict[str, Any]] = {}
    for route, spec in ROUTE_PACK.items():
        route_options[route] = {
            **spec,
            "currently_missing_files": missing_by_route.get(route, spec["submission_files"]),
            "promote_to_payloads_only_after_real_evidence_is_filled": True,
        }
    return {
        "report_id": "tau_lensing_route_evidence_pack_v01",
        "claim_boundary": "route_evidence_pack_only_templates_no_payload_no_score_no_dark_sector_verdict",
        "source_todo_report_id": todo.get("report_id"),
        "todo_status": todo.get("todo_status"),
        "selected_route_count": todo.get("selected_route_count", 0),
        "route_options": route_options,
        "forbidden_shortcuts": [
            "do_not_copy_TEMPLATE_NOT_PAYLOAD_files_to_payloads_as_real_inputs",
            "do_not_select_route_from_ACT_or_Planck_residuals",
            "do_not_tune_grid_to_reduced_chi2_or_dark_sector_preference",
        ],
        "next_required_action": "fill_exactly_one_staging_route_evidence_set_then_run_guarded_staging_promotion",
        "score_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a safe Tau lensing route evidence submission pack.")
    parser.add_argument(
        "--write-pack",
        default=None,
        nargs="?",
        const=str(DEFAULT_PACK),
        help=f"Optional JSON pack path. Defaults to {DEFAULT_PACK} when passed without a path.",
    )
    args = parser.parse_args()

    pack = build_pack(run_todo())
    text = json.dumps(pack, indent=2, sort_keys=True)
    if args.write_pack:
        path = Path(args.write_pack)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
