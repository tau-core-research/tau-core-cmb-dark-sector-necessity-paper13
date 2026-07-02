#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "payload_templates/tau_lensing_physical_candidate_upstream_l_response_TABLE_TEMPLATE_v01.csv"
DEFAULT_METADATA = ROOT / "payload_templates/tau_lensing_physical_candidate_upstream_l_response_METADATA_TEMPLATE_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_physical_candidate_upstream_scaffold_v01.json"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def write_table_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["L", "tau_response_value"])
        writer.writerow(["# TEMPLATE_NOT_PAYLOAD", "replace with exact integer L=10..3009 and finite values"])
        writer.writerow(["# REQUIRED_ROWS", "3000"])
        writer.writerow(["# ALLOWED_ROUTE_A", "tau_PP(L) from Phi_tau_eff -> T_tau_CMB -> Projection_PP"])
        writer.writerow(["# ALLOWED_ROUTE_B", "delta_PP_tau(L) from endpoint-blind Tau-derived direct L-space rule"])


def write_metadata_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "template_status": "TEMPLATE_NOT_PAYLOAD",
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "l_column": "L",
        "value_column": "tau_response_value",
        "formula_role": "endpoint_blind_tau_derived_lensing_l_response_physical_candidate",
        "route_family": "choose_one_of_route_A_transfer_projection_or_route_B_direct_L_space",
        "endpoint_blind_statement": (
            "FILL: state why all parameters and response values were fixed before ACT/Planck endpoint "
            "residuals, reduced chi2, score output, or dark-sector verdict readout."
        ),
        "parameter_policy": (
            "FILL: list fixed Tau-side inputs and state the parameter fixation rule; no endpoint tuning."
        ),
        "source_chain": [
            "FILL: Tau-side parent source artifact path",
            "FILL: derivation script or proof packet path",
            "FILL: normalization/known-limit audit path",
        ],
        "normalization_statement": (
            "FILL: define the dimensionless delta_PP_tau(L) or tau_PP(L) normalization and sign convention."
        ),
        "known_limit_statement": (
            "FILL: state the zero/null/LCDM comparison limit and what happens when Tau source is absent."
        ),
        "derivation_script_or_formula": (
            "FILL: replayable formula or script command that produces the exact 3000-row table."
        ),
        "route_A_transfer_projection_requirements": [
            "rho_tau_eff(a,k) = A_tau(a,k) * rho_ref(a)",
            "k^2 Phi_tau_eff(a,k) = 4*pi*G*a^2*rho_tau_eff(a,k)*Delta_tau(a,k)",
            "Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]",
            "tau_PP(L) = Projection_PP[Phi_lens_tau](L)",
        ],
        "route_B_direct_L_space_requirements": [
            "delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L)",
            "F_tau_L parameters fixed from Tau-side evidence before endpoint score readout",
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
        "claim_boundary": (
            "physical_candidate_upstream_scaffold_template_not_payload_no_grid_no_score_no_dark_sector_verdict"
        ),
        "notes": (
            "Remove template_status only after this metadata describes a real Tau-derived endpoint-blind "
            "3000-row upstream response table."
        ),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Write physical-candidate Tau-grid upstream table/metadata templates.")
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    table = Path(args.table).resolve()
    metadata = Path(args.metadata).resolve()
    write_table_template(table)
    write_metadata_template(metadata)
    report = {
        "report_id": "cmb_tau_lensing_physical_candidate_upstream_scaffold_v01",
        "claim_boundary": "physical_candidate_upstream_scaffold_only_templates_no_grid_no_score_no_dark_sector_verdict",
        "scaffold_status": "PHYSICAL_CANDIDATE_UPSTREAM_TEMPLATE_WRITTEN",
        "table_template": rel(table),
        "metadata_template": rel(metadata),
        "template_status": "TEMPLATE_NOT_PAYLOAD",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "copy templates into payload_staging only after replacing all FILL fields with Tau-derived "
            "endpoint-blind content, then run make tau-grid-physical-candidate-precheck"
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
