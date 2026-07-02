#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "payload_templates/tau_lensing_route_b_direct_l_space_METADATA_TEMPLATE_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_metadata_template_v01.json"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def route_b_template() -> dict:
    return {
        "template_status": "TEMPLATE_NOT_PAYLOAD",
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "l_column": "L",
        "value_column": "tau_response_value",
        "formula_role": "endpoint_blind_tau_derived_lensing_l_response_physical_candidate",
        "route_family": "route_B_direct_L_space",
        "endpoint_blind_statement": (
            "FILL: Endpoint-blind parent_tau_source response values are fixed before any endpoint "
            "or score readout."
        ),
        "parameter_policy": (
            "FILL: No endpoint or score tuning is allowed; all F_tau_L parameters are fixed from "
            "Tau-side parent evidence before the 3000-row table is generated."
        ),
        "source_chain": [
            "FILL: Tau parent_tau_source evidence artifact",
            "FILL: F_tau_L derivation/proof artifact",
            "FILL: replay script that writes payload_staging/tau_lensing_upstream_l_response_v01.csv",
        ],
        "normalization_statement": (
            "FILL: dimensionless delta_PP_tau normalization fixed by parent_tau_source convention."
        ),
        "known_limit_statement": (
            "FILL: delta_PP_tau tends to zero when parent_tau_source is absent or null-gauged."
        ),
        "derivation_script_or_formula": (
            "FILL: delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L)"
        ),
        "route_B_direct_L_space_requirements": [
            "parent_tau_source is named and endpoint-blind",
            "F_tau_L is replayable or mathematically specified",
            "readout_profile and scale_profile are fixed before endpoint score readout",
            "output table has exact L=10..3009 alignment",
        ],
        "forbidden_inputs": [
            "ACT residuals",
            "Planck residuals",
            "reduced chi2 tuning",
            "score output tuning",
            "dark-sector verdict preference",
            "diagnostic probe parameters",
            "zero-control definitions promoted as physical response",
        ],
        "claim_boundary": "route_b_direct_l_space_metadata_template_not_payload_no_grid_no_score_no_dark_sector_verdict",
        "notes": (
            "This is a Route B metadata template only. Remove template_status and all FILL fields only "
            "after the matching 3000-row table is produced from Tau-side evidence."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a Route B direct L-space metadata template.")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    template = Path(args.template).resolve()
    template.parent.mkdir(parents=True, exist_ok=True)
    template.write_text(json.dumps(route_b_template(), indent=2, sort_keys=True) + "\n")
    report = {
        "report_id": "cmb_tau_lensing_route_b_metadata_template_v01",
        "claim_boundary": "route_b_metadata_template_only_no_grid_no_score_no_dark_sector_verdict",
        "template_status": "TEMPLATE_NOT_PAYLOAD",
        "template": rel(template),
        "route_family": "route_B_direct_L_space",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "replace FILL fields and template_status with Tau-derived endpoint-blind Route B derivation metadata"
        ),
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
