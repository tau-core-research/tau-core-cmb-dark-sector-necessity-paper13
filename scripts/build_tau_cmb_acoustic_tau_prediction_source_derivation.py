#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_acoustic_tau_prediction_source_derivation_v01_derivation_spine_only_"
    "no_acoustic_source_solution_no_peak_prediction_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "derivation_row_id",
    "derivation_component",
    "symbolic_object",
    "definition_or_requirement",
    "input_artifact",
    "input_status",
    "derivation_status",
    "endpoint_blind_status",
    "dimension_or_convention_status",
    "planck_peak_payload_effect",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "derivation_rows_declared",
    "formal_definition_rows",
    "dependency_rows",
    "missing_dependency_rows",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, str]]:
    rows = [
        {
            "derivation_component": "formal_acoustic_source_target",
            "symbolic_object": "S_tau_ac(k,a)",
            "definition_or_requirement": "Define the target source slot S_tau_ac(k,a) := P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a), where P_ac is an unfilled acoustic projection operator.",
            "input_artifact": "tau_cmb_effective_source_equation_v01; tau_cmb_acoustic_reduced_evaluation_v01",
            "input_status": "FORMAL_TARGET_AVAILABLE_SOURCE_OPERATOR_UNFILLED",
            "derivation_status": "FORMAL_DEFINITION_ONLY_NOT_DERIVED",
            "endpoint_blind_status": "ENDPOINT_BLINDNESS_REQUIRED_NOT_PROVED_FOR_SOURCE",
            "dimension_or_convention_status": "TARGET_REQUIRES_LOCKED_K_A_ELL_D_ELL_AND_RECOMBINATION_CONVENTIONS",
            "planck_peak_payload_effect": "does_not_accept_planck_peak_payload",
        },
        {
            "derivation_component": "effective_potential_dependency",
            "symbolic_object": "Phi_tau_eff(a,k)",
            "definition_or_requirement": "Supply endpoint-blind effective potential entering the recombination-era acoustic driving term.",
            "input_artifact": "tau_cmb_effective_source_equation_v01; tau_cmb_effective_potential_source_handoff_v01",
            "input_status": "TARGET_DECLARED_HANDOFF_INCOMPLETE",
            "derivation_status": "BLOCKED_EFFECTIVE_POTENTIAL_NOT_DERIVED",
            "endpoint_blind_status": "PROVENANCE_REQUIRED_NOT_SUPPLIED",
            "dimension_or_convention_status": "POTENTIAL_ROLE_DECLARED_NORMALIZATION_NOT_LOCKED",
            "planck_peak_payload_effect": "blocks_predicted_peak_position_and_value",
        },
        {
            "derivation_component": "amplitude_dependency",
            "symbolic_object": "A_tau(a,k)",
            "definition_or_requirement": "Supply endpoint-blind amplitude normalization for relative peak-height support.",
            "input_artifact": "tau_cmb_density_amplitude_derivation_v01; tau_cmb_density_amplitude_closure_v01",
            "input_status": "FORMAL_RATIO_DECLARED_VALUE_NOT_DERIVED",
            "derivation_status": "BLOCKED_AMPLITUDE_NOT_DERIVED",
            "endpoint_blind_status": "ENDPOINT_BLIND_DERIVATION_REQUIRED_NOT_AVAILABLE",
            "dimension_or_convention_status": "CONDITIONAL_DIMENSION_PASS_ONLY",
            "planck_peak_payload_effect": "blocks_predicted_observable_amplitude",
        },
        {
            "derivation_component": "oscillator_response_dependency",
            "symbolic_object": "Theta_tau_ac(k,a)",
            "definition_or_requirement": "Supply reduced photon-baryon oscillator response or Green-function rule driven by S_tau_ac.",
            "input_artifact": "tau_cmb_acoustic_role_reduced_benchmark_v01; tau_cmb_acoustic_reduced_evaluation_v01",
            "input_status": "BENCHMARK_DECLARED_RESPONSE_NOT_EVALUATED",
            "derivation_status": "BLOCKED_OSCILLATOR_RESPONSE_NOT_DERIVED",
            "endpoint_blind_status": "RESPONSE_RULE_REQUIRED_BEFORE_PLANCK_RESIDUALS",
            "dimension_or_convention_status": "SOUND_HORIZON_AND_RECOMBINATION_CONVENTION_REQUIRED",
            "planck_peak_payload_effect": "blocks_peak_phase_prediction",
        },
        {
            "derivation_component": "baryon_loading_dependency",
            "symbolic_object": "B_tau_gamma_b(k,a)",
            "definition_or_requirement": "Supply Tau-source coupling law and sign convention relative to baryon loading.",
            "input_artifact": "tau_cmb_acoustic_reduced_evaluation_v01",
            "input_status": "COUPLING_SIGN_MISSING",
            "derivation_status": "BLOCKED_BARYON_LOADING_COUPLING_NOT_DERIVED",
            "endpoint_blind_status": "COUPLING_MUST_BE_DECLARED_BEFORE_SCORE",
            "dimension_or_convention_status": "COUPLING_SIGN_AND_NORMALIZATION_REQUIRED",
            "planck_peak_payload_effect": "blocks_relative_peak_height_prediction",
        },
        {
            "derivation_component": "planck_peak_payload_handoff",
            "symbolic_object": "P_tau_peak_payload",
            "definition_or_requirement": "Map S_tau_ac into predicted ell/value/uncertainty rows only after the source and response dependencies are derived.",
            "input_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01",
            "input_status": "EXPLICIT_EMPTY_SUPPLY_REJECTED",
            "derivation_status": "BLOCKED_NO_ACCEPTED_TAU_PEAK_PAYLOAD",
            "endpoint_blind_status": "ATTESTATION_MISSING",
            "dimension_or_convention_status": "COMPARISON_RULE_MISSING",
            "planck_peak_payload_effect": "keeps_all_36_peak_rows_rejected",
        },
        {
            "derivation_component": "null_response_control_dependency",
            "symbolic_object": "N_tau_ac_null",
            "definition_or_requirement": "Accepted null-response control may replace a prediction only if it has matching domain, convention, and endpoint-blind provenance.",
            "input_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01",
            "input_status": "NULL_RESPONSE_NOT_SUPPLIED",
            "derivation_status": "BLOCKED_NO_ACCEPTED_NULL_RESPONSE_CONTROL",
            "endpoint_blind_status": "NULL_CONTROL_PROVENANCE_MISSING",
            "dimension_or_convention_status": "MATCHING_DOMAIN_AND_CONVENTION_REQUIRED",
            "planck_peak_payload_effect": "cannot_unblock_score_as_null_control",
        },
        {
            "derivation_component": "score_firewall",
            "symbolic_object": "score(P_tau_peak_payload,Planck_PR3_peaks)",
            "definition_or_requirement": "Score may be attempted only after all Tau prediction or null-response rows are accepted endpoint-blind.",
            "input_artifact": "tau_cmb_planck_pr3_peak_score_attempt_guard_v01",
            "input_status": "SCORE_ATTEMPT_BLOCKED",
            "derivation_status": "FIREWALL_CLOSED",
            "endpoint_blind_status": "FIREWALL_PRESERVED",
            "dimension_or_convention_status": "NO_LIKELIHOOD_OR_SCORE_READ",
            "planck_peak_payload_effect": "prevents_dark_sector_verdict",
        },
    ]
    return [
        {
            "derivation_row_id": f"TCMBATPSD01_{index:03d}",
            "score_entry_allowed": "false",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "derivation_rows_declared": str(len(rows)),
        "formal_definition_rows": str(sum(row["derivation_status"].startswith("FORMAL_DEFINITION") for row in rows)),
        "dependency_rows": str(sum("dependency" in row["derivation_component"] for row in rows)),
        "missing_dependency_rows": str(sum(row["derivation_status"].startswith("BLOCKED") for row in rows)),
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_SPINE_DECLARED_SOURCE_NOT_DERIVED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_acoustic_source_operator_payload_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "acoustic_tau_prediction_source_derivation_spine",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "formal_source_target": "S_tau_ac(k,a) := P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)",
        "derivation_rows": rows,
        "summary": row,
        "score_rule": "No peak score is allowed until an endpoint-blind source/operator payload or accepted null-response control supplies all Planck peak prediction rows.",
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Acoustic Tau Prediction Source Derivation v01",
        "",
        "**Doc class:** acoustic Tau prediction source derivation spine",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** formal source target declared; source/operator not derived; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact consolidates the acoustic Tau-side blocker into one derivation spine. It declares the minimal source target needed before the Planck PR3 peak payload can be populated:",
        "",
        "```text",
        "S_tau_ac(k,a) := P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)",
        "```",
        "",
        "`P_ac` is not supplied here. The equation is a target definition for the required source/operator payload, not a physical CMB solution.",
        "",
        "## Summary",
        "",
        f"- derivation_rows_declared = {row['derivation_rows_declared']}",
        f"- formal_definition_rows = {row['formal_definition_rows']}",
        f"- missing_dependency_rows = {row['missing_dependency_rows']}",
        f"- derived_source_rows = {row['derived_source_rows']}",
        f"- executable_prediction_rows = {row['executable_prediction_rows']}",
        f"- accepted_planck_payload_rows = {row['accepted_planck_payload_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Derivation Spine",
        "",
        "| component | symbolic_object | derivation_status | planck_peak_payload_effect |",
        "| --- | --- | --- | --- |",
    ]
    for source_row in rows:
        lines.append(
            f"| {source_row['derivation_component']} | {source_row['symbolic_object']} | "
            f"{source_row['derivation_status']} | {source_row['planck_peak_payload_effect']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This is a derivation spine only. It does not derive an acoustic source, does not solve photon-baryon dynamics, does not predict Planck peak positions or amplitudes, does not compute a score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = source_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_acoustic_tau_prediction_source_derivation_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_tau_prediction_source_derivation_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_acoustic_tau_prediction_source_derivation_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_acoustic_tau_prediction_source_derivation_v01.md", rows, row)
    print("TAU_CMB_ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_V01_BUILT")


if __name__ == "__main__":
    main()
