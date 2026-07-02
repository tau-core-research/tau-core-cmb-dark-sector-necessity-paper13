#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PHI_TAU_EFF_ACOUSTIC_INPUT_ACCEPTANCE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01_acceptance_audit_only_"
    "no_accepted_effective_potential_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "acceptance_row_id",
    "input_component",
    "symbol_or_role",
    "acceptance_requirement",
    "evidence_source",
    "acceptance_status",
    "blocking_condition",
    "score_effect",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "acceptance_rows_declared",
    "accepted_rows",
    "blocked_rows",
    "partial_rows",
    "phi_tau_eff_source_slot_accepted",
    "phi_tau_eff_acoustic_input_accepted",
    "operator_model_accepted_rows",
    "derived_source_rows",
    "executable_prediction_rows",
    "accepted_planck_payload_rows",
    "score_ready_rows",
    "scores_computed",
    "cmb_likelihood_available",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def acceptance_rows() -> list[dict[str, str]]:
    rows = [
        {
            "input_component": "source_slot_identity",
            "symbol_or_role": "Phi_tau_eff(a,k)",
            "acceptance_requirement": "The acoustic input must use the declared common effective-potential source slot.",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "acceptance_status": "ACCEPTED_SOURCE_SLOT_IDENTITY_ONLY",
            "blocking_condition": "none_for_identity_only",
            "score_effect": "keeps_acoustic_input_target_explicit_but_does_not_enable_score",
        },
        {
            "input_component": "endpoint_blind_provenance",
            "symbol_or_role": "provenance(Phi_tau_eff)",
            "acceptance_requirement": "Provide a construction independent of CMB residual fitting, role scores, and endpoint labels.",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "acceptance_status": "BLOCKED_ENDPOINT_BLIND_PROVENANCE_NOT_ACCEPTED",
            "blocking_condition": "no accepted endpoint-blind derivation trace for Phi_tau_eff",
            "score_effect": "blocks_acoustic_source_acceptance",
        },
        {
            "input_component": "normalization_convention",
            "symbol_or_role": "norm(Phi_tau_eff)",
            "acceptance_requirement": "Lock normalization compatible with the acoustic role and later lensing cross-role use.",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "acceptance_status": "PARTIAL_NORMALIZATION_DECLARED_NOT_ACCEPTED",
            "blocking_condition": "normalization convention is declared as required but not selected",
            "score_effect": "blocks_amplitude_and_cross_role_comparison",
        },
        {
            "input_component": "timing_sign_convention",
            "symbol_or_role": "time/sign(Phi_tau_eff)",
            "acceptance_requirement": "Supply pre-recombination timing and sign convention for acoustic phase and peak-height checks.",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "acceptance_status": "BLOCKED_TIMING_SIGN_NOT_ACCEPTED",
            "blocking_condition": "no source-time dependence or sign convention is accepted",
            "score_effect": "blocks_acoustic_phase_and_height_prediction",
        },
        {
            "input_component": "baryon_photon_coupling_role",
            "symbol_or_role": "coupling(Phi_tau_eff, baryon-photon response)",
            "acceptance_requirement": "Preserve the baryon-loading odd/even peak role without fitting endpoint residuals.",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "acceptance_status": "BLOCKED_COUPLING_ROLE_NOT_ACCEPTED",
            "blocking_condition": "no accepted coupling role or sign is supplied",
            "score_effect": "blocks_odd_even_peak_height_response",
        },
        {
            "input_component": "score_firewall",
            "symbol_or_role": "score_guard(Phi_tau_eff acoustic input)",
            "acceptance_requirement": "Keep score entry closed until all Phi_tau_eff acoustic input rows are accepted.",
            "evidence_source": "tau_cmb_planck_pr3_peak_score_attempt_guard_v01",
            "acceptance_status": "FIREWALL_PRESERVED",
            "blocking_condition": "upstream Phi_tau_eff input rows are not accepted",
            "score_effect": "prevents_premature_score_or_dark_sector_verdict",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        out.append(
            {
                "acceptance_row_id": f"TCMBPTEAIA01_{index:03d}",
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                **row,
            }
        )
    return out


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    accepted = sum(row["acceptance_status"].startswith("ACCEPTED") for row in rows)
    blocked = sum(row["acceptance_status"].startswith("BLOCKED") for row in rows)
    partial = sum(row["acceptance_status"].startswith("PARTIAL") for row in rows)
    return {
        "summary_id": PACKET_ID,
        "acceptance_rows_declared": str(len(rows)),
        "accepted_rows": str(accepted),
        "blocked_rows": str(blocked),
        "partial_rows": str(partial),
        "phi_tau_eff_source_slot_accepted": "true",
        "phi_tau_eff_acoustic_input_accepted": "false",
        "operator_model_accepted_rows": "1",
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": "0",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PHI_TAU_EFF_ACOUSTIC_INPUT_IDENTITY_ACCEPTED_INPUT_BLOCKED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_eff_acoustic_input_acceptance_audit",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "acceptance_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Phi Tau Eff Acoustic Input Acceptance v01",
        "",
        "**Doc class:** Phi_tau_eff acoustic input acceptance audit",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** source-slot identity accepted; full acoustic input blocked; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact audits whether `Phi_tau_eff(a,k)` can be accepted as the effective-potential input for the acoustic operator after the domain/basis lock. The source-slot identity is accepted, but the full acoustic input is not accepted because endpoint-blind provenance, normalization, timing/sign, and baryon-photon coupling remain unresolved.",
        "",
        "## Summary",
        "",
        f"- acceptance_rows_declared = {row['acceptance_rows_declared']}",
        f"- accepted_rows = {row['accepted_rows']}",
        f"- blocked_rows = {row['blocked_rows']}",
        f"- partial_rows = {row['partial_rows']}",
        f"- phi_tau_eff_source_slot_accepted = {row['phi_tau_eff_source_slot_accepted']}",
        f"- phi_tau_eff_acoustic_input_accepted = {row['phi_tau_eff_acoustic_input_accepted']}",
        f"- operator_model_accepted_rows = {row['operator_model_accepted_rows']}",
        f"- executable_prediction_rows = {row['executable_prediction_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Acceptance Rows",
        "",
        "| component | symbol_or_role | acceptance_status |",
        "| --- | --- | --- |",
    ]
    for acceptance_row in rows:
        lines.append(
            f"| {acceptance_row['input_component']} | {acceptance_row['symbol_or_role']} | "
            f"{acceptance_row['acceptance_status']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This acceptance audit does not accept an executable effective potential, does not solve the acoustic operator, does not derive an executable `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = acceptance_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_eff_acoustic_input_acceptance_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.md", rows, row)
    print("TAU_CMB_PHI_TAU_EFF_ACOUSTIC_INPUT_ACCEPTANCE_V01_BUILT")


if __name__ == "__main__":
    main()
