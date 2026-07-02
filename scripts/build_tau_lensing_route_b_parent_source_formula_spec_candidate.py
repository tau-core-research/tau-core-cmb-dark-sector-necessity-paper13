#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "payload_staging/tau_lensing_route_b_parent_source_formula_spec_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_parent_source_formula_spec_candidate_v01.json"


def build_spec() -> dict[str, Any]:
    return {
        "spec_id": "tau_lensing_route_b_parent_source_formula_spec_v01",
        "claim_boundary": (
            "route_b_parent_source_formula_spec_protocol_verified_candidate_"
            "no_empirical_validation_no_score_no_dark_sector_verdict"
        ),
        "formula_family": "power_law_cutoff_parent_source_v01",
        "formula_role": "endpoint_blind_tau_parent_source_l_shape_protocol_candidate",
        "parameters": {
            "amplitude": 1.0,
            "L0": 1000.0,
            "tilt": 1.0,
            "cutoff_L": 2200.0,
            "cutoff_power": 2.0,
            "turnover_L": None,
            "turnover_power": 0.0,
        },
        "normalization": 1.0,
        "endpoint_blind_statement": (
            "endpoint-blind protocol candidate fixed before endpoint score readout; "
            "the shape is selected from the predeclared Route B power-law cutoff "
            "family and not from ACT/Planck residuals or score outputs"
        ),
        "parameter_policy": (
            "parameters are convention-fixed for a first Tau-side Route B parent-source "
            "candidate; no residual tuning, no reduced chi2 tuning, no score tuning, "
            "and no verdict tuning are permitted"
        ),
        "source_chain": [
            "docs/cmb_tau_lensing_route_b_parent_source_request_v01.md",
            "docs/cmb_tau_lensing_grid_equation_packet_v01.md",
            "docs/tau_cmb_minimal_source_term_candidate_v01.md",
            "docs/tau_cmb_known_limit_and_dimension_audit_v01.md",
            "payload_templates/tau_lensing_route_b_parent_source_formula_spec_TEMPLATE_v01.json",
            "scripts/materialize_tau_lensing_route_b_parent_source_from_formula_spec.py",
        ],
        "normalization_statement": (
            "dimensionless Route B parent-source convention; downstream "
            "delta_PP_tau = normalization * parent_tau_source_value"
        ),
        "known_limit_statement": (
            "when parent_tau_source_value -> 0, delta_PP_tau -> 0 under the "
            "linear_parent_source_v01 adapter"
        ),
        "derivation_script_or_formula": (
            "parent_tau_source_value(L)=amplitude*(L/L0)^tilt*"
            "exp(-(L/cutoff_L)^cutoff_power)"
        ),
        "physical_validation_status": "not_empirically_validated_not_a_dark_sector_verdict",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def build_report(spec_path: Path) -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_route_b_parent_source_formula_spec_candidate_v01",
        "claim_boundary": "formula_spec_candidate_written_only_no_grid_no_score_no_dark_sector_verdict",
        "candidate_spec": str(spec_path.resolve().relative_to(ROOT)),
        "candidate_status": "PROTOCOL_VERIFIED_CANDIDATE_PENDING_AUDIT",
        "important_boundary": (
            "This creates an endpoint-blind protocol candidate. It does not claim "
            "that the formula is the physically correct Tau response."
        ),
        "next_required_action": "run_make_tau-grid-route-b-parent-formula-audit",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a Route B parent-source formula-spec candidate.")
    parser.add_argument("--write-spec", nargs="?", const=str(DEFAULT_SPEC))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    spec_path = Path(args.write_spec or DEFAULT_SPEC)
    spec = build_spec()
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")

    report = build_report(spec_path)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
