#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_ACOUSTIC_MINIMAL_OPERATOR_MODEL_ATTEMPT_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_acoustic_minimal_operator_model_attempt_v01_model_scaffold_only_"
    "no_executable_operator_no_peak_prediction_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "model_row_id",
    "operator_component",
    "symbolic_slot",
    "minimal_candidate_rule",
    "required_dependency",
    "attempt_status",
    "endpoint_blind_status",
    "dimension_status",
    "known_limit_status",
    "acceptance_decision",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "model_rows_declared",
    "candidate_rule_rows_declared",
    "dependency_blocked_rows",
    "dimensionally_closed_rows",
    "known_limit_closed_rows",
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


def model_rows() -> list[dict[str, str]]:
    rows = [
        {
            "operator_component": "domain_and_basis_lock",
            "symbolic_slot": "Dom(P_ac)",
            "minimal_candidate_rule": "Use a reduced acoustic-role basis with k, a, a_rec, ell, spectrum_role, and fixed comparison convention inherited from the Planck PR3 peak source-freeze chain.",
            "required_dependency": "tau_cmb_planck_pr3_peak_source_freeze_packet_v01 plus explicit Tau-side basis normalization",
            "attempt_status": "CANDIDATE_RULE_DECLARED_NOT_ACCEPTED",
            "endpoint_blind_status": "NO_ENDPOINT_RESIDUALS_READ",
            "dimension_status": "CONVENTION_PARTIAL_NOT_CLOSED",
            "known_limit_status": "LCDM_LIMIT_NOT_MATCHED",
        },
        {
            "operator_component": "effective_potential_input",
            "symbolic_slot": "Phi_tau_eff(a,k)",
            "minimal_candidate_rule": "Treat Phi_tau_eff as the Tau-side acoustic driving potential entering the reduced source slot.",
            "required_dependency": "tau_cmb_effective_potential_source_handoff_v01 with accepted endpoint-blind provenance and normalization",
            "attempt_status": "DEPENDENCY_BLOCKED",
            "endpoint_blind_status": "PROVENANCE_MISSING",
            "dimension_status": "POTENTIAL_NORMALIZATION_MISSING",
            "known_limit_status": "POISSON_OR_LCDM_POTENTIAL_LIMIT_NOT_MATCHED",
        },
        {
            "operator_component": "amplitude_input",
            "symbolic_slot": "A_tau(a,k)",
            "minimal_candidate_rule": "Treat A_tau as a bounded Tau response amplitude multiplying the acoustic driving term.",
            "required_dependency": "tau_cmb_density_amplitude_closure_v01 with accepted amplitude normalization",
            "attempt_status": "DEPENDENCY_BLOCKED",
            "endpoint_blind_status": "DERIVATION_TRACE_MISSING",
            "dimension_status": "AMPLITUDE_NORMALIZATION_MISSING",
            "known_limit_status": "OMEGA_C_H2_ROLE_NOT_MATCHED",
        },
        {
            "operator_component": "oscillator_kernel_rule",
            "symbolic_slot": "G_tau_ac(k,a;a_rec)",
            "minimal_candidate_rule": "Candidate scaffold: Theta_tau_ac(k,a_rec) = integral da G_tau_ac(k,a;a_rec) S_tau_ac(k,a).",
            "required_dependency": "endpoint-blind Green-function or reduced oscillator kernel with measure and boundary convention",
            "attempt_status": "FORMULA_SCAFFOLD_DECLARED_NOT_EXECUTABLE",
            "endpoint_blind_status": "KERNEL_PROVENANCE_MISSING",
            "dimension_status": "INTEGRATION_MEASURE_AND_KERNEL_DIMENSION_MISSING",
            "known_limit_status": "STANDARD_ACOUSTIC_OSCILLATOR_LIMIT_NOT_MATCHED",
        },
        {
            "operator_component": "baryon_loading_coupling",
            "symbolic_slot": "C_tau_gamma_b(k,a)",
            "minimal_candidate_rule": "Candidate scaffold: include a sign-locked coupling factor between the Tau acoustic response and baryon-photon loading.",
            "required_dependency": "coupling sign, scale, and zero-source limit under the same domain convention",
            "attempt_status": "FORMULA_SCAFFOLD_DECLARED_NOT_EXECUTABLE",
            "endpoint_blind_status": "COUPLING_PROVENANCE_MISSING",
            "dimension_status": "COUPLING_SIGN_AND_SCALE_MISSING",
            "known_limit_status": "ODD_EVEN_PEAK_ROLE_NOT_MATCHED",
        },
        {
            "operator_component": "projection_rule_to_peak_payload",
            "symbolic_slot": "Pi_peak[P_ac]",
            "minimal_candidate_rule": "Candidate scaffold: map Theta_tau_ac into predicted peak ell, predicted D_ell value, uncertainty, and spectrum role before comparison.",
            "required_dependency": "projection-to-peak rule, angular-diameter/sound-horizon convention, and endpoint-blind attestation",
            "attempt_status": "FORMULA_SCAFFOLD_DECLARED_NOT_EXECUTABLE",
            "endpoint_blind_status": "ATTESTATION_MISSING",
            "dimension_status": "PEAK_PAYLOAD_UNITS_AND_NORMALIZATION_MISSING",
            "known_limit_status": "PEAK_PHASE_AND_HEIGHT_LIMIT_NOT_MATCHED",
        },
        {
            "operator_component": "uncertainty_and_null_policy",
            "symbolic_slot": "sigma_tau_ac or N_tau_ac_null",
            "minimal_candidate_rule": "Require either finite prediction uncertainty under the same model or an accepted null-response control.",
            "required_dependency": "endpoint-blind uncertainty model or accepted null-response control",
            "attempt_status": "DEPENDENCY_BLOCKED",
            "endpoint_blind_status": "UNCERTAINTY_OR_NULL_PROVENANCE_MISSING",
            "dimension_status": "UNCERTAINTY_MODEL_MISSING",
            "known_limit_status": "NULL_LIMIT_NOT_ACCEPTED",
        },
        {
            "operator_component": "score_firewall",
            "symbolic_slot": "score_guard(P_ac)",
            "minimal_candidate_rule": "Keep CMB score entry closed until all candidate model rows are accepted and replayable.",
            "required_dependency": "accepted model rows plus accepted Planck prediction payload",
            "attempt_status": "FIREWALL_PRESERVED",
            "endpoint_blind_status": "FIREWALL_PRESERVED",
            "dimension_status": "NO_SCORE_OR_LIKELIHOOD_READ",
            "known_limit_status": "NO_VERDICT_READ",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        accepted = row["attempt_status"] == "ACCEPTED_EXECUTABLE_OPERATOR_MODEL"
        out.append(
            {
                "model_row_id": f"TCMBACMOM01_{index:03d}",
                "acceptance_decision": "ACCEPTED_OPERATOR_MODEL_ROW" if accepted else "REJECTED_OPERATOR_MODEL_ROW_NOT_EXECUTABLE",
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
        "model_rows_declared": str(len(rows)),
        "candidate_rule_rows_declared": str(sum("SCAFFOLD" in row["attempt_status"] or "CANDIDATE_RULE" in row["attempt_status"] for row in rows)),
        "dependency_blocked_rows": str(sum(row["attempt_status"] == "DEPENDENCY_BLOCKED" for row in rows)),
        "dimensionally_closed_rows": "0",
        "known_limit_closed_rows": "0",
        "operator_model_accepted_rows": "0",
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": "0",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "ACOUSTIC_MINIMAL_OPERATOR_MODEL_ATTEMPT_DECLARED_NOT_EXECUTABLE_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_acoustic_operator_dependency_unblock_plan_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "acoustic_minimal_operator_model_attempt",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "operator_target": "P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)",
        "model_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Acoustic Minimal Operator Model Attempt v01",
        "",
        "**Doc class:** acoustic minimal operator model attempt",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** formula scaffold declared; not executable; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact makes the first minimal `P_ac` model attempt after the explicit empty supply record. It declares the smallest formula scaffold that could later turn the acoustic source slot into a replayable Tau-side prediction path.",
        "",
        "The attempt is not accepted as an executable model in this version. It lacks closed endpoint-blind inputs, dimensional closure, known-limit matching, projection-to-peak normalization, and an uncertainty or accepted null-response policy.",
        "",
        "## Minimal Scaffold",
        "",
        "The attempted shape is:",
        "",
        "```text",
        "S_tau_ac(k,a) := P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)",
        "Theta_tau_ac(k,a_rec) = integral da G_tau_ac(k,a;a_rec) S_tau_ac(k,a)",
        "Pi_peak[P_ac] -> {ell_pred, D_ell_pred, sigma_tau, spectrum_role}",
        "```",
        "",
        "This is a scaffold only. None of these rows are accepted as a physical CMB prediction.",
        "",
        "## Summary",
        "",
        f"- model_rows_declared = {row['model_rows_declared']}",
        f"- candidate_rule_rows_declared = {row['candidate_rule_rows_declared']}",
        f"- dependency_blocked_rows = {row['dependency_blocked_rows']}",
        f"- dimensionally_closed_rows = {row['dimensionally_closed_rows']}",
        f"- known_limit_closed_rows = {row['known_limit_closed_rows']}",
        f"- operator_model_accepted_rows = {row['operator_model_accepted_rows']}",
        f"- executable_prediction_rows = {row['executable_prediction_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Model Rows",
        "",
        "| component | symbolic_slot | attempt_status | acceptance_decision |",
        "| --- | --- | --- | --- |",
    ]
    for model_row in rows:
        lines.append(
            f"| {model_row['operator_component']} | {model_row['symbolic_slot']} | "
            f"{model_row['attempt_status']} | {model_row['acceptance_decision']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This model attempt does not solve the acoustic operator, does not derive an executable `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = model_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_acoustic_minimal_operator_model_attempt_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_minimal_operator_model_attempt_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_acoustic_minimal_operator_model_attempt_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_acoustic_minimal_operator_model_attempt_v01.md", rows, row)
    print("TAU_CMB_ACOUSTIC_MINIMAL_OPERATOR_MODEL_ATTEMPT_V01_BUILT")


if __name__ == "__main__":
    main()
