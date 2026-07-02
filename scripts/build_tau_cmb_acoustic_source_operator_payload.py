#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_acoustic_source_operator_payload_v01_operator_payload_contract_only_"
    "no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "operator_row_id",
    "operator_component",
    "symbolic_slot",
    "required_payload_content",
    "source_dependency",
    "payload_status",
    "acceptance_decision",
    "endpoint_blind_status",
    "dimension_or_convention_status",
    "planck_peak_prediction_effect",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "operator_rows_declared",
    "required_operator_payload_rows",
    "payload_supplied_rows",
    "payload_accepted_rows",
    "payload_rejected_rows",
    "endpoint_blind_pass_rows",
    "dimension_convention_pass_rows",
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


def operator_rows() -> list[dict[str, str]]:
    rows = [
        {
            "operator_component": "domain_and_basis_lock",
            "symbolic_slot": "Dom(P_ac)",
            "required_payload_content": "Declare k, a, ell, recombination epoch, sound-horizon, spectrum-role, and readout basis conventions before any peak comparison.",
            "source_dependency": "tau_cmb_acoustic_tau_prediction_source_derivation_v01",
            "payload_status": "REQUIRED_NOT_SUPPLIED",
            "endpoint_blind_status": "NO_ENDPOINT_RESIDUALS_READ",
            "dimension_or_convention_status": "CONVENTION_LOCK_MISSING",
            "planck_peak_prediction_effect": "blocks_mapping_to_predicted_ell_rows",
        },
        {
            "operator_component": "effective_potential_input",
            "symbolic_slot": "Phi_tau_eff(a,k)",
            "required_payload_content": "Supply the endpoint-blind effective-potential input used by the acoustic driving term.",
            "source_dependency": "tau_cmb_effective_potential_source_handoff_v01",
            "payload_status": "REQUIRED_NOT_SUPPLIED",
            "endpoint_blind_status": "PROVENANCE_MISSING",
            "dimension_or_convention_status": "POTENTIAL_NORMALIZATION_MISSING",
            "planck_peak_prediction_effect": "blocks_phase_and_amplitude_response",
        },
        {
            "operator_component": "amplitude_input",
            "symbolic_slot": "A_tau(a,k)",
            "required_payload_content": "Supply endpoint-blind source amplitude normalization compatible with the density role.",
            "source_dependency": "tau_cmb_density_amplitude_derivation_v01",
            "payload_status": "REQUIRED_NOT_SUPPLIED",
            "endpoint_blind_status": "DERIVATION_TRACE_MISSING",
            "dimension_or_convention_status": "AMPLITUDE_NORMALIZATION_MISSING",
            "planck_peak_prediction_effect": "blocks_relative_peak_height_rows",
        },
        {
            "operator_component": "oscillator_kernel_rule",
            "symbolic_slot": "G_tau_ac(k,a;a_rec)",
            "required_payload_content": "Supply a reduced oscillator response kernel or rule translating S_tau_ac into phase and envelope predictions.",
            "source_dependency": "tau_cmb_acoustic_reduced_evaluation_v01",
            "payload_status": "REQUIRED_NOT_SUPPLIED",
            "endpoint_blind_status": "KERNEL_PROVENANCE_MISSING",
            "dimension_or_convention_status": "OSCILLATOR_CONVENTION_MISSING",
            "planck_peak_prediction_effect": "blocks_peak_phase_rows",
        },
        {
            "operator_component": "baryon_loading_coupling",
            "symbolic_slot": "C_tau_gamma_b(k,a)",
            "required_payload_content": "Supply coupling sign and normalization relative to baryon loading.",
            "source_dependency": "tau_cmb_acoustic_reduced_evaluation_v01",
            "payload_status": "REQUIRED_NOT_SUPPLIED",
            "endpoint_blind_status": "COUPLING_PROVENANCE_MISSING",
            "dimension_or_convention_status": "COUPLING_SIGN_AND_SCALE_MISSING",
            "planck_peak_prediction_effect": "blocks_odd_even_peak_height_rows",
        },
        {
            "operator_component": "projection_rule_to_peak_payload",
            "symbolic_slot": "Pi_peak[P_ac]",
            "required_payload_content": "Map operator output to predicted ell, predicted D_ell value, and uncertainty rows without reading endpoint residuals.",
            "source_dependency": "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01",
            "payload_status": "REQUIRED_NOT_SUPPLIED",
            "endpoint_blind_status": "ATTESTATION_MISSING",
            "dimension_or_convention_status": "COMPARISON_RULE_MISSING",
            "planck_peak_prediction_effect": "blocks_all_36_planck_peak_payload_rows",
        },
        {
            "operator_component": "uncertainty_and_null_policy",
            "symbolic_slot": "sigma_tau_ac or N_tau_ac_null",
            "required_payload_content": "Supply finite prediction uncertainty or accepted null-response control under the same domain and convention.",
            "source_dependency": "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01",
            "payload_status": "REQUIRED_NOT_SUPPLIED",
            "endpoint_blind_status": "UNCERTAINTY_OR_NULL_PROVENANCE_MISSING",
            "dimension_or_convention_status": "UNCERTAINTY_MODEL_MISSING",
            "planck_peak_prediction_effect": "blocks_score_weighting_or_null_substitution",
        },
        {
            "operator_component": "score_firewall",
            "symbolic_slot": "score_guard(P_ac)",
            "required_payload_content": "Keep score entry closed until all operator payload rows are accepted.",
            "source_dependency": "tau_cmb_planck_pr3_peak_score_attempt_guard_v01",
            "payload_status": "FIREWALL_DECLARED",
            "endpoint_blind_status": "FIREWALL_PRESERVED",
            "dimension_or_convention_status": "NO_SCORE_OR_LIKELIHOOD_READ",
            "planck_peak_prediction_effect": "prevents_premature_dark_sector_verdict",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        accepted = row["payload_status"] == "SUPPLIED_ACCEPTED"
        out.append(
            {
                "operator_row_id": f"TCMBACSOP01_{index:03d}",
                "acceptance_decision": "ACCEPTED_OPERATOR_PAYLOAD_ROW" if accepted else "REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED",
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                **row,
            }
        )
    return out


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "operator_rows_declared": str(len(rows)),
        "required_operator_payload_rows": str(sum(row["payload_status"] == "REQUIRED_NOT_SUPPLIED" for row in rows)),
        "payload_supplied_rows": str(sum(row["payload_status"].startswith("SUPPLIED") for row in rows)),
        "payload_accepted_rows": str(sum(row["acceptance_decision"] == "ACCEPTED_OPERATOR_PAYLOAD_ROW" for row in rows)),
        "payload_rejected_rows": str(
            sum(
                row["acceptance_decision"] == "REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED"
                and row["payload_status"] == "REQUIRED_NOT_SUPPLIED"
                for row in rows
            )
        ),
        "endpoint_blind_pass_rows": str(sum(row["endpoint_blind_status"] == "FIREWALL_PRESERVED" for row in rows)),
        "dimension_convention_pass_rows": str(sum(row["dimension_or_convention_status"] == "NO_SCORE_OR_LIKELIHOOD_READ" for row in rows)),
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_CONTRACT_DECLARED_PAYLOAD_NOT_SUPPLIED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_acoustic_source_operator_payload_supply_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "acoustic_source_operator_payload_contract",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "operator_target": "P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)",
        "operator_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Acoustic Source Operator Payload v01",
        "",
        "**Doc class:** acoustic source-operator payload contract",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** operator payload contract declared; no operator payload accepted; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact turns the formal `P_ac` slot into a concrete operator-payload contract. It specifies the rows that must be supplied before `S_tau_ac(k,a)` can become an executable Tau-side acoustic source for Planck PR3 peak prediction.",
        "",
        "No operator solution is supplied here.",
        "",
        "## Summary",
        "",
        f"- operator_rows_declared = {row['operator_rows_declared']}",
        f"- required_operator_payload_rows = {row['required_operator_payload_rows']}",
        f"- payload_supplied_rows = {row['payload_supplied_rows']}",
        f"- payload_accepted_rows = {row['payload_accepted_rows']}",
        f"- derived_source_rows = {row['derived_source_rows']}",
        f"- executable_prediction_rows = {row['executable_prediction_rows']}",
        f"- accepted_planck_payload_rows = {row['accepted_planck_payload_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Operator Payload Rows",
        "",
        "| component | symbolic_slot | payload_status | acceptance_decision |",
        "| --- | --- | --- | --- |",
    ]
    for operator_row in rows:
        lines.append(
            f"| {operator_row['operator_component']} | {operator_row['symbolic_slot']} | "
            f"{operator_row['payload_status']} | {operator_row['acceptance_decision']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This is an operator-payload contract only. It does not solve the acoustic operator, does not derive `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = operator_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_acoustic_source_operator_payload_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_source_operator_payload_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_acoustic_source_operator_payload_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_acoustic_source_operator_payload_v01.md", rows, row)
    print("TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_V01_BUILT")


if __name__ == "__main__":
    main()
