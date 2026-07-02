#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_scoring_input_fulfillment_packet_v01.json"


ROUTES: dict[str, dict[str, Any]] = {
    "direct_tau_PP_grid": {
        "staging_files": [
            "payload_staging/direct_tau_PP_grid/tau_lensing_response_pp_grid_v01.csv",
            "payload_staging/direct_tau_PP_grid/tau_lensing_response_grid_route_declaration_v01.md",
            "payload_staging/direct_tau_PP_grid/tau_lensing_response_grid_provenance_v01.json",
        ],
        "payload_files": [
            "payloads/tau_lensing_response_pp_grid_v01.csv",
            "payloads/tau_lensing_response_grid_route_declaration_v01.md",
            "payloads/tau_lensing_response_grid_provenance_v01.json",
        ],
        "required_fulfillment": [
            "3000 finite endpoint-blind tau_PP values indexed by L=10..3009",
            "route declaration with selected_route=direct_tau_PP_grid and non-empty endpoint_blind_statement",
            "provenance JSON without template_status",
            "numeric_grid_sha256 matching the staged grid file",
            "source_chain naming Tau-side parent inputs, not ACT/Planck residuals",
            "derivation_script_or_formula naming the replayable derivation or frozen formula",
            "no_endpoint_fit_statement excluding residual, reduced-chi2, score, or verdict tuning",
        ],
        "dry_run_command": "make staging-promote-direct-dry-run",
        "promotion_command": "make staging-promote-direct",
        "post_promotion_commands": [
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
        "staging_files": [
            "payload_staging/delta_PP_tau_against_named_fiducial_PP/tau_lensing_response_delta_pp_v01.csv",
            "payload_staging/delta_PP_tau_against_named_fiducial_PP/tau_lensing_response_fiducial_pp_reference_v01.json",
            "payload_staging/delta_PP_tau_against_named_fiducial_PP/tau_lensing_response_grid_route_declaration_v01.md",
            "payload_staging/delta_PP_tau_against_named_fiducial_PP/tau_lensing_response_grid_provenance_v01.json",
        ],
        "payload_files": [
            "payloads/tau_lensing_response_delta_pp_v01.csv",
            "payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
            "payloads/tau_lensing_response_grid_route_declaration_v01.md",
            "payloads/tau_lensing_response_grid_provenance_v01.json",
        ],
        "required_fulfillment": [
            "3000 finite endpoint-blind delta_PP_tau values indexed by L=10..3009",
            "fiducial reference JSON with fiducial_reference_file and fiducial_reference_sha256",
            "route declaration with selected_route=delta_PP_tau_against_named_fiducial_PP and non-empty endpoint_blind_statement",
            "provenance JSON without template_status",
            "numeric_grid_sha256 matching the staged delta grid file",
            "source_chain naming Tau-side parent inputs and named fiducial source, not ACT/Planck residuals",
            "derivation_script_or_formula naming the replayable derivation or frozen formula",
            "no_endpoint_fit_statement excluding residual, reduced-chi2, score, or verdict tuning",
        ],
        "dry_run_command": "make staging-promote-delta-dry-run",
        "promotion_command": "make staging-promote-delta",
        "post_promotion_commands": [
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
        "staging_files": [
            "payload_staging/explicit_failure_no_endpoint_blind_grid/tau_lensing_response_grid_failure_statement_v01.md",
        ],
        "payload_files": [
            "payloads/tau_lensing_response_grid_failure_statement_v01.md",
        ],
        "required_fulfillment": [
            "failure statement without TEMPLATE_NOT_PAYLOAD marker",
            "selected_route=explicit_failure_no_endpoint_blind_grid",
            "failed_required_object",
            "reason",
            "missing_parent_input",
            "missing_derivation_rule",
            "missing_numeric_kernel",
            "missing_normalization",
            "next_theoretical_blocker",
        ],
        "dry_run_command": "make staging-promote-failure-dry-run",
        "promotion_command": "make staging-promote-failure",
        "post_promotion_commands": [
            "make intake",
            "make evidence-check",
            "make route-submission-audit",
            "make score-report",
            "make score-output-audit",
        ],
    },
}


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def build_packet() -> dict[str, Any]:
    route_packets = {}
    for route, spec in ROUTES.items():
        route_packets[route] = {
            **spec,
            "staging_presence": {path: exists(path) for path in spec["staging_files"]},
            "payload_presence": {path: exists(path) for path in spec["payload_files"]},
        }
    failure_payload_present = all(
        route_packets["explicit_failure_no_endpoint_blind_grid"]["payload_presence"].values()
    )
    current_blocker = (
        "endpoint_blind_numeric_tau_grid_not_derivable_failure_route_recorded"
        if failure_payload_present
        else "real_endpoint_blind_tau_route_evidence_not_submitted"
    )
    next_required_action = (
        "supply_endpoint_blind_formula_spec_then_run_make_tau-grid-from-formula"
        if failure_payload_present
        else "fill_exactly_one_staging_route_packet_then_run_matching_dry_run_promotion"
    )
    return {
        "report_id": "tau_lensing_scoring_input_fulfillment_packet_v01",
        "claim_boundary": "scoring_input_fulfillment_packet_only_no_payload_acceptance_no_score_no_dark_sector_verdict",
        "purpose": "single_next_packet_for_fulfilling_the_tau_lensing_score_input_blocker",
        "current_blocker": current_blocker,
        "accepted_route_count_required": "exactly_one",
        "route_packets": route_packets,
        "tau_grid_production_path": {
            "contract": "docs/cmb_tau_lensing_grid_formula_materializer_contract_v01.md",
            "production_status_command": "make tau-grid-production-status",
            "production_status": "data/derived/cmb_tau_lensing_grid_production_status_v01.json",
            "physical_derivation_intake_audit_command": "make tau-grid-derivation-intake-audit",
            "physical_derivation_intake_audit": (
                "data/derived/cmb_tau_lensing_physical_derivation_intake_audit_v01.json"
            ),
            "physical_derivation_intake_smoke_command": "make tau-grid-derivation-intake-smoke",
            "physical_derivation_intake_smoke": (
                "data/derived/cmb_tau_lensing_derivation_intake_audit_smoke_v01.json"
            ),
            "route_b_metadata_template_command": "make tau-grid-route-b-template",
            "route_b_metadata_template": (
                "payload_templates/tau_lensing_route_b_direct_l_space_METADATA_TEMPLATE_v01.json"
            ),
            "route_b_parent_source_request_command": "make tau-grid-route-b-parent-request",
            "route_b_parent_source_request": "docs/cmb_tau_lensing_route_b_parent_source_request_v01.md",
            "route_b_parent_source_request_packet": (
                "data/derived/cmb_tau_lensing_route_b_parent_source_request_v01.json"
            ),
            "route_b_parent_source_formula_template_command": "make tau-grid-route-b-parent-formula-template",
            "route_b_parent_source_formula_template": (
                "payload_templates/tau_lensing_route_b_parent_source_formula_spec_TEMPLATE_v01.json"
            ),
            "route_b_parent_source_formula_candidate_command": "make tau-grid-route-b-parent-formula-candidate",
            "route_b_parent_source_formula_candidate_report": (
                "data/derived/cmb_tau_lensing_route_b_parent_source_formula_spec_candidate_v01.json"
            ),
            "route_b_parent_source_formula_spec_required": (
                "payload_staging/tau_lensing_route_b_parent_source_formula_spec_v01.json"
            ),
            "route_b_parent_source_formula_audit_command": "make tau-grid-route-b-parent-formula-audit",
            "route_b_parent_source_formula_audit": (
                "data/derived/cmb_tau_lensing_route_b_parent_source_formula_spec_audit_v01.json"
            ),
            "route_b_parent_source_from_formula_dry_run_command": (
                "make tau-grid-route-b-parent-from-formula-dry-run"
            ),
            "route_b_parent_source_from_formula_write_staging_command": (
                "make tau-grid-route-b-parent-from-formula-write-staging"
            ),
            "route_b_parent_source_formula_materialization_report": (
                "data/derived/cmb_tau_lensing_route_b_parent_source_formula_materialization_v01.json"
            ),
            "route_b_parent_source_config_template_command": "make tau-grid-route-b-parent-template",
            "route_b_parent_source_config_template": (
                "payload_templates/tau_lensing_route_b_parent_source_CONFIG_TEMPLATE_v01.json"
            ),
            "route_b_parent_source_table_template_command": "make tau-grid-route-b-parent-table-template",
            "route_b_parent_source_table_template": (
                "payload_templates/tau_lensing_route_b_parent_source_TABLE_TEMPLATE_v01.csv"
            ),
            "route_b_parent_source_table_precheck_command": "make tau-grid-route-b-parent-table-precheck",
            "route_b_parent_source_table_precheck": (
                "data/derived/cmb_tau_lensing_route_b_parent_source_precheck_v01.json"
            ),
            "route_b_parent_source_dry_run_command": "make tau-grid-route-b-parent-dry-run",
            "route_b_parent_source_write_staging_command": "make tau-grid-route-b-parent-write-staging",
            "route_b_parent_source_smoke_command": "make tau-grid-route-b-parent-smoke",
            "route_b_parent_source_smoke": (
                "data/derived/cmb_tau_lensing_route_b_parent_source_materializer_smoke_v01.json"
            ),
            "template_command": "make tau-grid-formula-template",
            "upstream_table_contract": "docs/cmb_tau_lensing_upstream_table_formula_spec_contract_v01.md",
            "upstream_table_template_command": "make tau-grid-upstream-table-template",
            "upstream_metadata_template_command": "make tau-grid-upstream-metadata-template",
            "physical_candidate_request_command": "make tau-grid-physical-candidate-request",
            "physical_candidate_request": "docs/cmb_tau_lensing_physical_candidate_upstream_request_v01.md",
            "physical_candidate_agent_prompt": (
                "docs/cmb_tau_lensing_physical_candidate_upstream_agent_prompt_v01.md"
            ),
            "physical_candidate_scaffold_command": "make tau-grid-physical-candidate-scaffold",
            "physical_candidate_table_template": (
                "payload_templates/tau_lensing_physical_candidate_upstream_l_response_TABLE_TEMPLATE_v01.csv"
            ),
            "physical_candidate_metadata_template": (
                "payload_templates/tau_lensing_physical_candidate_upstream_l_response_METADATA_TEMPLATE_v01.json"
            ),
            "nonzero_probe_command": "make tau-grid-nonzero-probe",
            "nonzero_upstream_precheck_command": "make tau-grid-nonzero-precheck",
            "physical_candidate_upstream_precheck_command": "make tau-grid-physical-candidate-precheck",
            "nonzero_probe_package_command": "make tau-grid-nonzero-probe-package",
            "physical_candidate_package_command": "make tau-grid-physical-candidate-package",
            "zero_response_control_command": "make tau-grid-zero-control",
            "zero_response_control_package_command": "make tau-grid-zero-control-package",
            "upstream_table_spec_command": "make tau-grid-upstream-table-spec",
            "upstream_handoff_dry_run_command": "make tau-grid-handoff-dry-run",
            "upstream_handoff_write_staging_command": "make tau-grid-handoff-write-staging",
            "candidate_command": "make tau-grid-spec-candidate",
            "candidate_spec": "payload_staging/tau_lensing_grid_formula_spec_candidate_v01.json",
            "candidate_audit": "data/derived/cmb_tau_lensing_grid_formula_spec_candidate_audit_v01.json",
            "equation_packet_command": "make tau-grid-equation-packet",
            "equation_packet": "data/derived/cmb_tau_lensing_grid_equation_packet_v01.json",
            "materialization_command": "make tau-grid-from-formula",
            "required_spec": "payload_staging/tau_lensing_grid_formula_spec_v01.json",
            "materializer_script": "scripts/materialize_tau_lensing_grid_from_formula_spec.py",
            "output_routes": {
                "direct_tau_PP_grid": "payload_staging/direct_tau_PP_grid/tau_lensing_response_pp_grid_v01.csv",
                "delta_PP_tau_against_named_fiducial_PP": (
                    "payload_staging/delta_PP_tau_against_named_fiducial_PP/"
                    "tau_lensing_response_delta_pp_v01.csv"
                ),
            },
            "claim_boundary": "formula_to_grid_materialization_only_no_score_no_dark_sector_verdict",
        },
        "forbidden_sources": [
            "ACT residuals",
            "Planck residuals",
            "reduced chi2 tuning",
            "score output tuning",
            "dark-sector verdict preference",
            "template payloads",
        ],
        "next_required_action": next_required_action,
        "score_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Tau lensing scoring input fulfillment packet.")
    parser.add_argument(
        "--write-packet",
        default=None,
        nargs="?",
        const=str(DEFAULT_PACKET),
        help=f"Optional JSON packet path. Defaults to {DEFAULT_PACKET} when passed without a path.",
    )
    args = parser.parse_args()
    packet = build_packet()
    text = json.dumps(packet, indent=2, sort_keys=True)
    if args.write_packet:
        path = Path(args.write_packet)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
