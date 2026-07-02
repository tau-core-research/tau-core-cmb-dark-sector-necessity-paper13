#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_MATERIALIZATION_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01_materialization_spec_only_"
    "no_tau_prediction_no_score_no_likelihood_no_dark_sector_verdict"
)

ROW_FIELDS = [
    "materialization_row_id",
    "candidate_id",
    "source_peak_id",
    "cmb_role",
    "spectrum",
    "ell_center",
    "observed_value",
    "required_tau_payload_fields",
    "required_endpoint_blind_attestation",
    "required_convention_lock",
    "required_uncertainty_model",
    "tau_prediction_value_status",
    "tau_prediction_ell_status",
    "tau_prediction_amplitude_status",
    "tau_prediction_source_artifact_status",
    "materialization_acceptance_status",
    "score_entry_allowed",
    "score_blocker",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "materialization_rows_declared",
    "observed_candidate_rows_checked",
    "required_tau_payload_rows",
    "tau_prediction_value_rows",
    "tau_prediction_ell_rows",
    "tau_prediction_amplitude_rows",
    "tau_prediction_source_artifact_rows",
    "endpoint_blind_attestation_rows",
    "convention_lock_rows",
    "uncertainty_model_rows",
    "accepted_materialization_rows",
    "score_ready_rows",
    "missing_prediction_rows",
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


def materialization_rows() -> list[dict[str, str]]:
    candidates = read_csv(DERIVED / "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.csv")
    rows: list[dict[str, str]] = []
    required_fields = ";".join(
        [
            "tau_model_artifact_id",
            "endpoint_blind_derivation_trace",
            "predicted_ell_center",
            "predicted_observable_value",
            "prediction_uncertainty",
            "spectrum_role_convention",
            "normalization_convention",
            "comparison_rule_id",
        ]
    )
    for index, candidate in enumerate(candidates, start=1):
        rows.append(
            {
                "materialization_row_id": f"TCMBP3PTPM01_{index:03d}",
                "candidate_id": candidate["candidate_id"],
                "source_peak_id": candidate["source_peak_id"],
                "cmb_role": candidate["cmb_role"],
                "spectrum": candidate["spectrum"],
                "ell_center": candidate["ell_center"],
                "observed_value": candidate["observed_value"],
                "required_tau_payload_fields": required_fields,
                "required_endpoint_blind_attestation": "prediction_source_constructed_without_planck_peak_residuals",
                "required_convention_lock": "ell_Dell_units_spectrum_role_and_normalization_declared_before_score",
                "required_uncertainty_model": "finite_prediction_uncertainty_or_explicit_null_response_control",
                "tau_prediction_value_status": "MISSING",
                "tau_prediction_ell_status": "MISSING",
                "tau_prediction_amplitude_status": "MISSING",
                "tau_prediction_source_artifact_status": "MISSING",
                "materialization_acceptance_status": "BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED",
                "score_entry_allowed": "false",
                "score_blocker": "ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    missing_rows = sum(
        row["materialization_acceptance_status"] == "BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED"
        for row in rows
    )
    return {
        "summary_id": PACKET_ID,
        "materialization_rows_declared": str(len(rows)),
        "observed_candidate_rows_checked": str(len(rows)),
        "required_tau_payload_rows": str(len(rows)),
        "tau_prediction_value_rows": str(sum(row["tau_prediction_value_status"] == "SUPPLIED" for row in rows)),
        "tau_prediction_ell_rows": str(sum(row["tau_prediction_ell_status"] == "SUPPLIED" for row in rows)),
        "tau_prediction_amplitude_rows": str(sum(row["tau_prediction_amplitude_status"] == "SUPPLIED" for row in rows)),
        "tau_prediction_source_artifact_rows": str(
            sum(row["tau_prediction_source_artifact_status"] == "SUPPLIED" for row in rows)
        ),
        "endpoint_blind_attestation_rows": "0",
        "convention_lock_rows": "0",
        "uncertainty_model_rows": "0",
        "accepted_materialization_rows": str(
            sum(row["materialization_acceptance_status"] == "ACCEPTED_TAU_PREDICTION_PAYLOAD" for row in rows)
        ),
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "missing_prediction_rows": str(missing_rows),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "TAU_PEAK_PREDICTION_MATERIALIZATION_SPEC_READY_PAYLOAD_MISSING_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "tau_prediction_materialization_spec",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "materialization_rows": rows,
        "summary": row,
        "acceptance_rule": {
            "score_entry_allowed_only_if": [
                "each observed candidate row has a matching endpoint-blind Tau prediction or accepted null response",
                "predicted ell/value/uncertainty and source artifact are supplied for the same spectrum-role convention",
                "the prediction source is locked before reading endpoint residuals or Planck score outputs",
            ],
            "current_decision": "blocked",
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Planck PR3 Peak Tau Prediction Materialization v01",
        "",
        "**Doc class:** Tau-side prediction materialization specification",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** materialization contract ready; endpoint-blind Tau prediction payload missing; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact converts the previous score blocker into an explicit Tau-side payload contract. It states, row by row, what an endpoint-blind Tau acoustic prediction must provide before a Planck PR3 peak score can be attempted.",
        "",
        "It does not supply the prediction. It prevents the pipeline from treating a missing Tau response as a CMB failure, a likelihood result, or a dark-sector verdict.",
        "",
        "## Acceptance Rule",
        "",
        "A score entry is allowed only when every observed peak candidate has either a matching endpoint-blind Tau prediction or an accepted null-response control with locked spectrum role, normalization convention, predicted peak position/value, uncertainty model, and derivation provenance.",
        "",
        "## Summary",
        "",
        f"- materialization_rows_declared = {row['materialization_rows_declared']}",
        f"- required_tau_payload_rows = {row['required_tau_payload_rows']}",
        f"- tau_prediction_value_rows = {row['tau_prediction_value_rows']}",
        f"- tau_prediction_ell_rows = {row['tau_prediction_ell_rows']}",
        f"- endpoint_blind_attestation_rows = {row['endpoint_blind_attestation_rows']}",
        f"- accepted_materialization_rows = {row['accepted_materialization_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- missing_prediction_rows = {row['missing_prediction_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## First Rows",
        "",
        "| materialization_row_id | candidate_id | spectrum | ell_center | materialization_acceptance_status | score_blocker |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for materialization in rows[:8]:
        lines.append(
            f"| {materialization['materialization_row_id']} | {materialization['candidate_id']} | "
            f"{materialization['spectrum']} | {materialization['ell_center']} | "
            f"{materialization['materialization_acceptance_status']} | {materialization['score_blocker']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This is a materialization specification only. It is not a Tau acoustic prediction, not a CMB score, not a likelihood comparison, and not a decision about whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = materialization_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_materialization_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.md", rows, row)
    print("TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_MATERIALIZATION_V01_BUILT")


if __name__ == "__main__":
    main()
