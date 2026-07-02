#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_PAYLOAD_SUPPLY_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01_explicit_empty_supply_"
    "no_tau_prediction_no_null_response_no_score_no_likelihood_no_dark_sector_verdict"
)

ROW_FIELDS = [
    "payload_supply_row_id",
    "materialization_row_id",
    "candidate_id",
    "source_peak_id",
    "cmb_role",
    "spectrum",
    "ell_center",
    "observed_value",
    "supply_mode",
    "tau_model_artifact_id",
    "endpoint_blind_derivation_trace_status",
    "predicted_ell_center",
    "predicted_observable_value",
    "prediction_uncertainty",
    "spectrum_role_convention_status",
    "normalization_convention_status",
    "comparison_rule_status",
    "endpoint_blind_attestation_status",
    "null_response_control_status",
    "payload_acceptance_decision",
    "score_entry_allowed",
    "score_blocker",
    "hard_failure_triggered",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "payload_supply_rows_declared",
    "materialization_rows_checked",
    "explicit_empty_supply_rows",
    "tau_prediction_payload_rows",
    "null_response_control_rows",
    "endpoint_blind_attestation_rows",
    "convention_lock_rows",
    "comparison_rule_rows",
    "accepted_payload_rows",
    "rejected_payload_rows",
    "score_ready_rows",
    "hard_failures_triggered",
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


def payload_rows() -> list[dict[str, str]]:
    materializations = read_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(materializations, start=1):
        rows.append(
            {
                "payload_supply_row_id": f"TCMBP3PTPS01_{index:03d}",
                "materialization_row_id": row["materialization_row_id"],
                "candidate_id": row["candidate_id"],
                "source_peak_id": row["source_peak_id"],
                "cmb_role": row["cmb_role"],
                "spectrum": row["spectrum"],
                "ell_center": row["ell_center"],
                "observed_value": row["observed_value"],
                "supply_mode": "EXPLICIT_EMPTY_SUPPLY_NO_ENDPOINT_BLIND_TAU_ACOUSTIC_PREDICTION_AVAILABLE",
                "tau_model_artifact_id": "MISSING_TAU_ACOUSTIC_PREDICTION_SOURCE_ARTIFACT",
                "endpoint_blind_derivation_trace_status": "MISSING",
                "predicted_ell_center": "NA",
                "predicted_observable_value": "NA",
                "prediction_uncertainty": "NA",
                "spectrum_role_convention_status": "MISSING",
                "normalization_convention_status": "MISSING",
                "comparison_rule_status": "MISSING",
                "endpoint_blind_attestation_status": "MISSING",
                "null_response_control_status": "NOT_SUPPLIED",
                "payload_acceptance_decision": "REJECTED_NO_TAU_PREDICTION_OR_NULL_RESPONSE_PAYLOAD",
                "score_entry_allowed": "false",
                "score_blocker": "TAU_PEAK_PAYLOAD_SUPPLY_EXPLICITLY_EMPTY",
                "hard_failure_triggered": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "payload_supply_rows_declared": str(len(rows)),
        "materialization_rows_checked": str(len(rows)),
        "explicit_empty_supply_rows": str(
            sum(row["supply_mode"] == "EXPLICIT_EMPTY_SUPPLY_NO_ENDPOINT_BLIND_TAU_ACOUSTIC_PREDICTION_AVAILABLE" for row in rows)
        ),
        "tau_prediction_payload_rows": str(sum(row["predicted_ell_center"] != "NA" for row in rows)),
        "null_response_control_rows": str(sum(row["null_response_control_status"] == "SUPPLIED" for row in rows)),
        "endpoint_blind_attestation_rows": str(sum(row["endpoint_blind_attestation_status"] == "SUPPLIED" for row in rows)),
        "convention_lock_rows": str(
            sum(
                row["spectrum_role_convention_status"] == "SUPPLIED"
                and row["normalization_convention_status"] == "SUPPLIED"
                for row in rows
            )
        ),
        "comparison_rule_rows": str(sum(row["comparison_rule_status"] == "SUPPLIED" for row in rows)),
        "accepted_payload_rows": str(
            sum(row["payload_acceptance_decision"] == "ACCEPTED_TAU_PREDICTION_OR_NULL_RESPONSE_PAYLOAD" for row in rows)
        ),
        "rejected_payload_rows": str(
            sum(row["payload_acceptance_decision"] == "REJECTED_NO_TAU_PREDICTION_OR_NULL_RESPONSE_PAYLOAD" for row in rows)
        ),
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "hard_failures_triggered": str(sum(row["hard_failure_triggered"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "TAU_PEAK_PREDICTION_PAYLOAD_SUPPLY_EXPLICIT_EMPTY_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_acoustic_tau_prediction_source_derivation_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "tau_prediction_payload_supply_and_acceptance_decision",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "payload_supply_rows": rows,
        "summary": row,
        "decision": {
            "what_changed": "The missing Tau-side payload is now explicitly supplied as an empty, rejected payload record for each Planck PR3 peak row.",
            "why_no_score": "No endpoint-blind Tau acoustic prediction and no accepted null-response control is present.",
            "next_work": "derive or supply a real endpoint-blind Tau acoustic source/prediction artifact before attempting peak scoring",
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Planck PR3 Peak Tau Prediction Payload Supply v01",
        "",
        "**Doc class:** Tau-side prediction payload supply and acceptance decision",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** explicit empty Tau-side payload supplied; all rows rejected for score entry",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact takes the materialization contract and supplies a concrete decision record for every Planck PR3 peak candidate row. The supply is explicitly empty: no endpoint-blind Tau acoustic prediction and no accepted null-response control is available in this version.",
        "",
        "The value of this artifact is closure, not physics. It prevents the pipeline from looping over missing payload gates and redirects the next step to an actual Tau acoustic source derivation.",
        "",
        "## Summary",
        "",
        f"- payload_supply_rows_declared = {row['payload_supply_rows_declared']}",
        f"- explicit_empty_supply_rows = {row['explicit_empty_supply_rows']}",
        f"- tau_prediction_payload_rows = {row['tau_prediction_payload_rows']}",
        f"- null_response_control_rows = {row['null_response_control_rows']}",
        f"- accepted_payload_rows = {row['accepted_payload_rows']}",
        f"- rejected_payload_rows = {row['rejected_payload_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## First Rows",
        "",
        "| payload_supply_row_id | candidate_id | spectrum | supply_mode | payload_acceptance_decision | score_blocker |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for payload in rows[:8]:
        lines.append(
            f"| {payload['payload_supply_row_id']} | {payload['candidate_id']} | {payload['spectrum']} | "
            f"{payload['supply_mode']} | {payload['payload_acceptance_decision']} | {payload['score_blocker']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This is an explicit empty supply and rejection artifact. It is not a Tau acoustic prediction, not an accepted null-response control, not a CMB score, not a likelihood comparison, and not a decision about whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = payload_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.md", rows, row)
    print("TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_PAYLOAD_SUPPLY_V01_BUILT")


if __name__ == "__main__":
    main()
