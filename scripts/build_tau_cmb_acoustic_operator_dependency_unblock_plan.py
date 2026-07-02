#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_acoustic_operator_dependency_unblock_plan_v01_unblock_plan_only_"
    "no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "unblock_row_id",
    "operator_component",
    "symbolic_slot",
    "blocking_condition",
    "required_unblock_artifact",
    "acceptance_requirement",
    "priority_order",
    "unblock_status",
    "score_effect_if_completed",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "unblock_rows_declared",
    "critical_unblock_rows",
    "completed_unblock_rows",
    "pending_unblock_rows",
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


def unblock_rows() -> list[dict[str, str]]:
    rows = [
        {
            "operator_component": "domain_and_basis_lock",
            "symbolic_slot": "Dom(P_ac)",
            "blocking_condition": "Tau-side acoustic domain, measure, recombination-time convention, and spectrum-role basis are not accepted.",
            "required_unblock_artifact": "tau_cmb_acoustic_domain_basis_lock_acceptance_v01",
            "acceptance_requirement": "Declare k, a, a_rec, ell, integration measure, spectrum role, and comparison convention without endpoint residual reads.",
            "priority_order": "1",
            "score_effect_if_completed": "enables_dimension_replay_for_later_rows",
        },
        {
            "operator_component": "effective_potential_input",
            "symbolic_slot": "Phi_tau_eff(a,k)",
            "blocking_condition": "Endpoint-blind Phi_tau_eff provenance and normalization are not accepted.",
            "required_unblock_artifact": "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01",
            "acceptance_requirement": "Provide accepted effective-potential source handoff, normalization, sign convention, and known-limit role.",
            "priority_order": "2",
            "score_effect_if_completed": "unblocks_acoustic_driving_term_input",
        },
        {
            "operator_component": "amplitude_input",
            "symbolic_slot": "A_tau(a,k)",
            "blocking_condition": "Tau response amplitude normalization is not accepted for the acoustic role.",
            "required_unblock_artifact": "tau_cmb_acoustic_amplitude_input_acceptance_v01",
            "acceptance_requirement": "Provide bounded amplitude rule with endpoint-blind derivation trace and density-role compatibility.",
            "priority_order": "3",
            "score_effect_if_completed": "unblocks_relative_peak_height_input",
        },
        {
            "operator_component": "oscillator_kernel_rule",
            "symbolic_slot": "G_tau_ac(k,a;a_rec)",
            "blocking_condition": "No executable reduced oscillator or Green-function kernel is accepted.",
            "required_unblock_artifact": "tau_cmb_acoustic_oscillator_kernel_acceptance_v01",
            "acceptance_requirement": "Provide replayable kernel rule, integration measure, boundary convention, and dimensional check.",
            "priority_order": "4",
            "score_effect_if_completed": "unblocks_phase_and_envelope_prediction",
        },
        {
            "operator_component": "baryon_loading_coupling",
            "symbolic_slot": "C_tau_gamma_b(k,a)",
            "blocking_condition": "Baryon-photon loading sign and scale coupling are not accepted.",
            "required_unblock_artifact": "tau_cmb_acoustic_baryon_loading_coupling_acceptance_v01",
            "acceptance_requirement": "Provide sign-locked coupling, scale convention, zero-source limit, and odd/even peak-role check.",
            "priority_order": "5",
            "score_effect_if_completed": "unblocks_odd_even_peak_height_response",
        },
        {
            "operator_component": "projection_rule_to_peak_payload",
            "symbolic_slot": "Pi_peak[P_ac]",
            "blocking_condition": "No accepted projection maps operator output into Planck peak prediction rows.",
            "required_unblock_artifact": "tau_cmb_acoustic_peak_projection_payload_acceptance_v01",
            "acceptance_requirement": "Map accepted operator output to ell_pred, D_ell_pred, uncertainty, spectrum role, and normalization before comparison.",
            "priority_order": "6",
            "score_effect_if_completed": "unblocks_planck_peak_prediction_payload",
        },
        {
            "operator_component": "uncertainty_and_null_policy",
            "symbolic_slot": "sigma_tau_ac or N_tau_ac_null",
            "blocking_condition": "No finite uncertainty model or accepted null-response control is available.",
            "required_unblock_artifact": "tau_cmb_acoustic_uncertainty_or_null_policy_acceptance_v01",
            "acceptance_requirement": "Provide finite prediction uncertainty under the same conventions or an accepted null-response control.",
            "priority_order": "7",
            "score_effect_if_completed": "unblocks_score_weighting_or_null_substitution",
        },
        {
            "operator_component": "score_firewall",
            "symbolic_slot": "score_guard(P_ac)",
            "blocking_condition": "Score entry must remain closed until rows 1-7 are completed and replayable.",
            "required_unblock_artifact": "tau_cmb_acoustic_operator_score_entry_firewall_release_v01",
            "acceptance_requirement": "Release only after all upstream rows are accepted and the Planck prediction payload exists.",
            "priority_order": "8",
            "score_effect_if_completed": "would_allow_score_attempt_only_after_upstream_completion",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        out.append(
            {
                "unblock_row_id": f"TCMBACODUP01_{index:03d}",
                "unblock_status": "DECLARED_NOT_COMPLETED",
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
        "unblock_rows_declared": str(len(rows)),
        "critical_unblock_rows": "7",
        "completed_unblock_rows": "0",
        "pending_unblock_rows": str(len(rows)),
        "operator_model_accepted_rows": "0",
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": "0",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_DECLARED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_acoustic_domain_basis_lock_acceptance_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "acoustic_operator_dependency_unblock_plan",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "unblock_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Acoustic Operator Dependency Unblock Plan v01",
        "",
        "**Doc class:** acoustic operator dependency unblock plan",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** unblock plan declared; no dependency completed; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact turns the failed minimal acoustic operator model attempt into an ordered dependency-unblock plan. It does not solve the operator. It identifies the exact artifacts that must be completed before a Planck peak score can be attempted.",
        "",
        "## Summary",
        "",
        f"- unblock_rows_declared = {row['unblock_rows_declared']}",
        f"- critical_unblock_rows = {row['critical_unblock_rows']}",
        f"- completed_unblock_rows = {row['completed_unblock_rows']}",
        f"- pending_unblock_rows = {row['pending_unblock_rows']}",
        f"- operator_model_accepted_rows = {row['operator_model_accepted_rows']}",
        f"- executable_prediction_rows = {row['executable_prediction_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Ordered Unblock Rows",
        "",
        "| priority | component | required_unblock_artifact | unblock_status |",
        "| --- | --- | --- | --- |",
    ]
    for unblock_row in rows:
        lines.append(
            f"| {unblock_row['priority_order']} | {unblock_row['operator_component']} | "
            f"{unblock_row['required_unblock_artifact']} | {unblock_row['unblock_status']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This unblock plan does not solve the acoustic operator, does not derive an executable `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = unblock_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_acoustic_operator_dependency_unblock_plan_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_operator_dependency_unblock_plan_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_acoustic_operator_dependency_unblock_plan_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_acoustic_operator_dependency_unblock_plan_v01.md", rows, row)
    print("TAU_CMB_ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_V01_BUILT")


if __name__ == "__main__":
    main()
