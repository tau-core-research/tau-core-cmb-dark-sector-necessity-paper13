#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_OR_NULL_RESPONSE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01_"
    "tau_side_response_audit_only_no_prediction_no_null_response_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "response_row_id",
    "candidate_id",
    "source_peak_id",
    "cmb_role",
    "spectrum",
    "ell_center",
    "observed_value",
    "tau_prediction_required",
    "tau_prediction_status",
    "tau_prediction_value",
    "tau_prediction_source_artifact",
    "null_response_status",
    "null_response_value",
    "null_response_source_artifact",
    "admissible_response_status",
    "score_entry_allowed",
    "score_blocker",
    "hard_failure_triggered",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "response_rows_declared",
    "observed_candidate_rows_checked",
    "tau_prediction_required_rows",
    "tau_prediction_supplied_rows",
    "null_response_supplied_rows",
    "admissible_response_rows",
    "score_ready_rows",
    "explicit_missing_response_rows",
    "hard_failures_triggered",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_cmb_verdict_allowed",
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


def response_rows() -> list[dict[str, str]]:
    candidates = read_csv(DERIVED / "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(candidates, start=1):
        rows.append(
            {
                "response_row_id": f"TCMBP3PTNR01_{index:03d}",
                "candidate_id": row["candidate_id"],
                "source_peak_id": row["source_peak_id"],
                "cmb_role": row["cmb_role"],
                "spectrum": row["spectrum"],
                "ell_center": row["ell_center"],
                "observed_value": row["observed_value"],
                "tau_prediction_required": row["tau_prediction_required"],
                "tau_prediction_status": "NOT_SUPPLIED",
                "tau_prediction_value": "NA",
                "tau_prediction_source_artifact": "MISSING_ENDPOINT_BLIND_TAU_ACOUSTIC_PREDICTION",
                "null_response_status": "NOT_SUPPLIED",
                "null_response_value": "NA",
                "null_response_source_artifact": "MISSING_ACCEPTED_NULL_RESPONSE_CONTROL",
                "admissible_response_status": "NO_ADMISSIBLE_TAU_RESPONSE_OR_NULL_RESPONSE",
                "score_entry_allowed": "false",
                "score_blocker": "TAU_SIDE_PREDICTION_AND_NULL_RESPONSE_BOTH_MISSING",
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
        "response_rows_declared": str(len(rows)),
        "observed_candidate_rows_checked": str(len(rows)),
        "tau_prediction_required_rows": str(sum(row["tau_prediction_required"] == "true" for row in rows)),
        "tau_prediction_supplied_rows": str(sum(row["tau_prediction_status"] == "SUPPLIED" for row in rows)),
        "null_response_supplied_rows": str(sum(row["null_response_status"] == "SUPPLIED" for row in rows)),
        "admissible_response_rows": str(
            sum(row["admissible_response_status"] == "ADMISSIBLE_TAU_RESPONSE_OR_NULL_RESPONSE" for row in rows)
        ),
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "explicit_missing_response_rows": str(
            sum(row["admissible_response_status"] == "NO_ADMISSIBLE_TAU_RESPONSE_OR_NULL_RESPONSE" for row in rows)
        ),
        "hard_failures_triggered": str(sum(row["hard_failure_triggered"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "no_dark_cmb_verdict_allowed": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "TAU_SIDE_PEAK_RESPONSE_AUDITED_NO_PREDICTION_OR_NULL_RESPONSE_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_planck_pr3_peak_score_attempt_guard_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "tau_side_response_audit",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "response_rows": rows,
        "summary": row,
        "required_to_unblock_scoring": [
            "endpoint-blind Tau acoustic peak prediction for each candidate row",
            "or an accepted null-response control with matching domain and convention",
            "plus a comparison rule that does not read endpoint residuals during source construction",
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Planck PR3 Peak Tau Prediction or Null Response v01",
        "",
        "**Doc class:** Tau-side response audit",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** observed candidate rows checked; no endpoint-blind Tau prediction or accepted null response supplied; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact audits the Tau-side half of the Planck PR3 peak scoring input. The observed Planck peak candidates are ready, but a score requires either a Tau-side endpoint-blind prediction or an accepted null-response control for the same rows.",
        "",
        "No such Tau-side response is supplied here. The artifact therefore blocks score entry without converting the absence into a physical failure or dark-sector verdict.",
        "",
        "## Summary",
        "",
        f"- response_rows_declared = {row['response_rows_declared']}",
        f"- tau_prediction_required_rows = {row['tau_prediction_required_rows']}",
        f"- tau_prediction_supplied_rows = {row['tau_prediction_supplied_rows']}",
        f"- null_response_supplied_rows = {row['null_response_supplied_rows']}",
        f"- admissible_response_rows = {row['admissible_response_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- explicit_missing_response_rows = {row['explicit_missing_response_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## First Rows",
        "",
        "| response_row_id | candidate_id | source_peak_id | spectrum | tau_prediction_status | null_response_status | score_blocker |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for response in rows[:8]:
        lines.append(
            f"| {response['response_row_id']} | {response['candidate_id']} | {response['source_peak_id']} | "
            f"{response['spectrum']} | {response['tau_prediction_status']} | {response['null_response_status']} | "
            f"{response['score_blocker']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This is not a Tau Core acoustic prediction, not a null-response proof, not a CMB likelihood, and not a dark-sector decision. It is a scoring guard artifact: the observed side is available, while the Tau-side response is missing.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = response_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.md", rows, row)
    print("TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_OR_NULL_RESPONSE_V01_BUILT")


if __name__ == "__main__":
    main()
