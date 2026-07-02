#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PLANCK_PR3_PEAK_SCORE_ATTEMPT_GUARD_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_planck_pr3_peak_score_attempt_guard_v01_guard_only_score_blocked_"
    "no_likelihood_no_tau_response_claim_no_dark_sector_verdict"
)

ROW_FIELDS = [
    "guard_row_id",
    "guard_component",
    "input_artifact",
    "required_condition",
    "observed_status",
    "guard_decision",
    "blocks_score",
    "hard_failure_triggered",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "guard_rows_declared",
    "guard_pass_rows",
    "guard_block_rows",
    "observed_side_ready",
    "tau_side_response_ready",
    "score_attempt_allowed",
    "scores_computed",
    "cmb_likelihood_available",
    "hard_failures_triggered",
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


def guard_rows() -> list[dict[str, str]]:
    candidate_summary = read_csv(DERIVED / "tau_cmb_planck_pr3_peak_scoring_input_candidate_summary_v01.csv")[0]
    response_summary = read_csv(DERIVED / "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_summary_v01.csv")[0]
    rows = [
        {
            "guard_component": "observed_peak_candidate_table",
            "input_artifact": "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01",
            "required_condition": "observed_side_ready_rows equals candidate_rows_declared",
            "observed_status": (
                "PASS_OBSERVED_SIDE_READY"
                if candidate_summary["observed_side_ready_rows"] == candidate_summary["candidate_rows_declared"]
                else "BLOCKED_OBSERVED_SIDE_INCOMPLETE"
            ),
        },
        {
            "guard_component": "tau_side_prediction_or_null_response",
            "input_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01",
            "required_condition": "admissible_response_rows equals response_rows_declared",
            "observed_status": (
                "PASS_TAU_SIDE_RESPONSE_READY"
                if response_summary["admissible_response_rows"] == response_summary["response_rows_declared"]
                else "BLOCKED_TAU_SIDE_RESPONSE_MISSING"
            ),
        },
        {
            "guard_component": "score_entry_integrity",
            "input_artifact": "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01 + tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01",
            "required_condition": "score_ready_rows equals candidate_rows_declared and no likelihood is read before score entry",
            "observed_status": (
                "PASS_SCORE_ENTRY_ALLOWED"
                if candidate_summary["score_ready_rows"] == candidate_summary["candidate_rows_declared"]
                and response_summary["score_ready_rows"] == response_summary["response_rows_declared"]
                else "BLOCKED_SCORE_READY_ROWS_ZERO"
            ),
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        blocked = row["observed_status"].startswith("BLOCKED")
        out.append(
            {
                "guard_row_id": f"TCMBP3PSAG01_{index:03d}",
                "guard_decision": "SCORE_ATTEMPT_BLOCKED" if blocked else "GUARD_PASSED",
                "blocks_score": "true" if blocked else "false",
                "hard_failure_triggered": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                **row,
            }
        )
    return out


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    observed_ready = any(
        row["guard_component"] == "observed_peak_candidate_table" and row["guard_decision"] == "GUARD_PASSED"
        for row in rows
    )
    tau_ready = any(
        row["guard_component"] == "tau_side_prediction_or_null_response" and row["guard_decision"] == "GUARD_PASSED"
        for row in rows
    )
    blocked_rows = sum(row["guard_decision"] == "SCORE_ATTEMPT_BLOCKED" for row in rows)
    return {
        "summary_id": PACKET_ID,
        "guard_rows_declared": str(len(rows)),
        "guard_pass_rows": str(sum(row["guard_decision"] == "GUARD_PASSED" for row in rows)),
        "guard_block_rows": str(blocked_rows),
        "observed_side_ready": "true" if observed_ready else "false",
        "tau_side_response_ready": "true" if tau_ready else "false",
        "score_attempt_allowed": "false" if blocked_rows else "true",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "hard_failures_triggered": str(sum(row["hard_failure_triggered"] == "true" for row in rows)),
        "no_dark_cmb_verdict_allowed": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PLANCK_PR3_PEAK_SCORE_ATTEMPT_BLOCKED_TAU_SIDE_RESPONSE_MISSING",
        "next_required_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "score_attempt_guard",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "guard_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Planck PR3 Peak Score Attempt Guard v01",
        "",
        "**Doc class:** score-attempt guard",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** observed side ready; Tau-side response missing; score attempt blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Summary",
        "",
        f"- guard_rows_declared = {row['guard_rows_declared']}",
        f"- guard_pass_rows = {row['guard_pass_rows']}",
        f"- guard_block_rows = {row['guard_block_rows']}",
        f"- observed_side_ready = {row['observed_side_ready']}",
        f"- tau_side_response_ready = {row['tau_side_response_ready']}",
        f"- score_attempt_allowed = {row['score_attempt_allowed']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Guard Rows",
        "",
        "| guard_component | observed_status | guard_decision |",
        "| --- | --- | --- |",
    ]
    for guard in rows:
        lines.append(f"| {guard['guard_component']} | {guard['observed_status']} | {guard['guard_decision']} |")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This guard computes no score and reads no CMB likelihood. It only states that the Planck PR3 observed peak input is ready while the Tau-side prediction/null-response half is not ready.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = guard_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_score_attempt_guard_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_score_attempt_guard_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_planck_pr3_peak_score_attempt_guard_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_planck_pr3_peak_score_attempt_guard_v01.md", rows, row)
    print("TAU_CMB_PLANCK_PR3_PEAK_SCORE_ATTEMPT_GUARD_V01_BUILT")


if __name__ == "__main__":
    main()
