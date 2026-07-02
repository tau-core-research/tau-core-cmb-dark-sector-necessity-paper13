#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = ROOT / "payload_staging/tau_lensing_grid_formula_spec_candidate_v01.json"
DEFAULT_AUDIT = ROOT / "data/derived/cmb_tau_lensing_grid_formula_spec_candidate_audit_v01.json"

SOURCE_TERM = ROOT / "data/derived/tau_cmb_minimal_source_term_candidate_v01.csv"
DIMENSION_PRECHECK = ROOT / "data/derived/tau_cmb_source_term_dimensional_precheck_v01.csv"
PHI_CONTRACT = ROOT / "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.csv"
HANDOFF = ROOT / "data/derived/tau_cmb_effective_potential_source_handoff_v01.csv"
MATERIALIZER_CONTRACT = ROOT / "docs/cmb_tau_lensing_grid_formula_materializer_contract_v01.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"row not found in {key}={value}")


def build_candidate_spec() -> dict[str, Any]:
    return {
        "template_status": "CANDIDATE_NOT_PAYLOAD",
        "spec_id": "tau_lensing_grid_formula_spec_candidate_v01",
        "claim_boundary": "formula_spec_candidate_only_no_grid_no_score_no_dark_sector_verdict",
        "selected_route": "direct_tau_PP_grid",
        "endpoint_blind_statement": (
            "Candidate requires parent-side Tau source evidence before CMB endpoint evaluation; "
            "current artifacts do not yet satisfy the endpoint-blind Phi_tau_eff contract."
        ),
        "parameter_policy": "parameters_must_be_fixed_from_parent_side_tau_evidence_before_ACT_or_Planck_score_readout",
        "source_chain": [
            rel(SOURCE_TERM),
            rel(DIMENSION_PRECHECK),
            rel(PHI_CONTRACT),
            rel(HANDOFF),
            rel(MATERIALIZER_CONTRACT),
        ],
        "formula_family": "power_law_cutoff_response_v01",
        "formula_role": "candidate_adapter_for_tau_PP_or_delta_PP_tau_after_tau_side_derivation",
        "parameters": {
            "amplitude": None,
            "L0": None,
            "tilt": None,
            "cutoff_L": None,
            "cutoff_power": None,
            "turnover_L": None,
            "turnover_power": None,
        },
        "normalization_statement": (
            "Not locked. Requires a shared Phi_tau_eff normalization and lensing PP projection convention."
        ),
        "known_limit_statement": (
            "Not locked. Requires an LCDM-role reproduce/approximate/fail limit map before score use."
        ),
        "derivation_script_or_formula": (
            "Candidate chain: X_tau_CMB -> A_tau(a,k) -> rho_tau_eff(a,k) -> "
            "Phi_tau_eff(a,k) -> T_tau_CMB(k,a) -> tau_PP(L) or delta_PP_tau(L). "
            "The final L-space formula parameters are not supplied."
        ),
        "alternate_materialization_handoff": {
            "formula_family": "tabulated_l_response_v01",
            "required_upstream_object": "endpoint-blind Tau-derived L,value table with exact L=10..3009 alignment",
            "preferred_when": "a Tau-side derivation script already produced tau_PP(L) or delta_PP_tau(L)",
        },
        "materializable_now": False,
        "notes": "This candidate deliberately cannot be passed to the materializer as a payload formula spec.",
    }


def build_audit() -> dict[str, Any]:
    source_rows = read_csv_rows(SOURCE_TERM)
    precheck_rows = read_csv_rows(DIMENSION_PRECHECK)
    phi_rows = read_csv_rows(PHI_CONTRACT)
    handoff_rows = read_csv_rows(HANDOFF)

    density_precheck = find_row(precheck_rows, "candidate_row_id", "TCMBMSC01_002")
    poisson_precheck = find_row(precheck_rows, "candidate_row_id", "TCMBMSC01_003")
    transfer_precheck = find_row(precheck_rows, "candidate_row_id", "TCMBMSC01_004")
    phi_parent = find_row(phi_rows, "contract_row_id", "TCMBEBPTDC01_001")
    phi_rule = find_row(phi_rows, "contract_row_id", "TCMBEBPTDC01_003")
    normalization = find_row(phi_rows, "contract_row_id", "TCMBEBPTDC01_004")
    lensing_handoff = find_row(handoff_rows, "handoff_row_id", "TCMBEPSH01_006")

    blocking_items = [
        {
            "object": "A_tau(a,k)",
            "status": density_precheck["precheck_result"],
            "required_condition": density_precheck["required_condition"],
            "unresolved_dependency": density_precheck["unresolved_dependency"],
        },
        {
            "object": "Phi_tau_eff(a,k)",
            "status": poisson_precheck["precheck_result"],
            "required_condition": poisson_precheck["required_condition"],
            "unresolved_dependency": poisson_precheck["unresolved_dependency"],
        },
        {
            "object": "Transfer_tau / T_tau_CMB(k,a)",
            "status": transfer_precheck["precheck_result"],
            "required_condition": transfer_precheck["required_condition"],
            "unresolved_dependency": transfer_precheck["unresolved_dependency"],
        },
        {
            "object": "parent-side Phi_tau_eff provenance",
            "status": phi_parent["contract_status"],
            "required_condition": phi_parent["contract_requirement"],
            "unresolved_dependency": phi_parent["remaining_blocker"],
        },
        {
            "object": "rule(parent -> Phi_tau_eff)",
            "status": phi_rule["contract_status"],
            "required_condition": phi_rule["contract_requirement"],
            "unresolved_dependency": phi_rule["remaining_blocker"],
        },
        {
            "object": "norm(Phi_tau_eff)",
            "status": normalization["contract_status"],
            "required_condition": normalization["contract_requirement"],
            "unresolved_dependency": normalization["remaining_blocker"],
        },
        {
            "object": "Phi_tau_eff(a,k) -> lensing projection",
            "status": lensing_handoff["handoff_status"],
            "required_condition": lensing_handoff["handoff_requirement"],
            "unresolved_dependency": lensing_handoff["remaining_blocker"],
        },
    ]

    ready_conditions = [
        "A_tau(a,k) supplied as a dimensionless Tau-response amplitude",
        "rho_tau_eff(a,k) density normalization selected",
        "Fourier k, scale factor a, potential normalization, and Delta_tau convention declared",
        "parent-side Phi_tau_eff derivation rule supplied without endpoint-score construction data",
        "Transfer_tau or direct L-space delta_PP_tau rule supplied",
        "power_law_cutoff_response_v01 parameters fixed before score readout, or a new formula family added",
    ]

    candidate = build_candidate_spec()
    return {
        "report_id": "cmb_tau_lensing_grid_formula_spec_candidate_audit_v01",
        "claim_boundary": "formula_spec_candidate_audit_only_no_grid_no_score_no_dark_sector_verdict",
        "candidate_spec": rel(DEFAULT_CANDIDATE),
        "candidate_spec_status": "CANDIDATE_NOT_PAYLOAD",
        "materializable_now": False,
        "materializer_command_when_ready": "make tau-grid-from-formula",
        "materializer_contract": rel(MATERIALIZER_CONTRACT),
        "candidate_formula_family": candidate["formula_family"],
        "candidate_route": candidate["selected_route"],
        "blocking_items": blocking_items,
        "ready_conditions": ready_conditions,
        "accepted_materializer_families": [
            "power_law_cutoff_response_v01",
            "tabulated_l_response_v01",
        ],
        "preferred_grid_handoff": (
            "tabulated_l_response_v01 if a parent-side Tau derivation emits an endpoint-blind L,value table; "
            "power_law_cutoff_response_v01 only if its parameters are independently fixed before score readout"
        ),
        "source_skeleton_rows_used": [row["candidate_row_id"] for row in source_rows],
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "replace candidate placeholder parameters with a parent-side endpoint-blind Tau derivation, "
            "then remove CANDIDATE_NOT_PAYLOAD and run make tau-grid-from-formula"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an audit-only candidate spec for Tau lensing grid materialization.")
    parser.add_argument("--write-candidate", nargs="?", const=str(DEFAULT_CANDIDATE))
    parser.add_argument("--write-audit", nargs="?", const=str(DEFAULT_AUDIT))
    args = parser.parse_args()

    candidate = build_candidate_spec()
    audit = build_audit()

    if args.write_candidate:
        path = Path(args.write_candidate)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n")
    if args.write_audit:
        path = Path(args.write_audit)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")

    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
