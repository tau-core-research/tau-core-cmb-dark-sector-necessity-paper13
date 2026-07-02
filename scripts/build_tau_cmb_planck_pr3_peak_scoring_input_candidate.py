#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PLANCK_PR3_PEAK_SCORING_INPUT_CANDIDATE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01_observed_side_candidate_only_"
    "no_tau_prediction_no_score_no_likelihood_no_dark_sector_verdict"
)

CANDIDATE_FIELDS = [
    "candidate_id",
    "source_peak_id",
    "cmb_role",
    "observable_family",
    "spectrum",
    "peak_rank",
    "ell_center",
    "observed_value",
    "sigma_minus",
    "sigma_plus",
    "best_fit_value",
    "observed_minus_bestfit",
    "comparison_rule",
    "observed_side_ready",
    "tau_prediction_required",
    "tau_prediction_supplied",
    "null_response_supplied",
    "score_entry_allowed",
    "score_blocker",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "candidate_rows_declared",
    "observed_side_ready_rows",
    "comparison_rule_declared_rows",
    "tau_prediction_required_rows",
    "tau_prediction_supplied_rows",
    "null_response_supplied_rows",
    "score_ready_rows",
    "observed_side_fulfillment_score",
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


def comparison_rule(spectrum: str) -> str:
    if spectrum == "TE":
        return "compare signed TE extremum ell_center and signed D_ell against endpoint-blind Tau prediction"
    return f"compare {spectrum} peak ell_center and D_ell against endpoint-blind Tau prediction"


def candidate_rows() -> list[dict[str, str]]:
    peaks = read_csv(DERIVED / "tau_cmb_planck_pr3_peak_observable_table_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(peaks, start=1):
        spectrum = row["spectrum"]
        rows.append(
            {
                "candidate_id": f"TCMBP3PSC01_{index:03d}",
                "source_peak_id": row["peak_id"],
                "cmb_role": "acoustic_peak_phase_and_height",
                "observable_family": "planck_pr3_binned_peak_observable",
                "spectrum": spectrum,
                "peak_rank": row["peak_rank"],
                "ell_center": row["ell_center"],
                "observed_value": row["D_ell"],
                "sigma_minus": row["sigma_minus"],
                "sigma_plus": row["sigma_plus"],
                "best_fit_value": row["best_fit_D_ell"],
                "observed_minus_bestfit": row["data_minus_bestfit"],
                "comparison_rule": comparison_rule(spectrum),
                "observed_side_ready": "true",
                "tau_prediction_required": "true",
                "tau_prediction_supplied": "false",
                "null_response_supplied": "false",
                "score_entry_allowed": "false",
                "score_blocker": "TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    observed_ready = sum(row["observed_side_ready"] == "true" for row in rows)
    tau_supplied = sum(row["tau_prediction_supplied"] == "true" for row in rows)
    null_supplied = sum(row["null_response_supplied"] == "true" for row in rows)
    score_ready = sum(row["score_entry_allowed"] == "true" for row in rows)
    return {
        "summary_id": PACKET_ID,
        "candidate_rows_declared": str(len(rows)),
        "observed_side_ready_rows": str(observed_ready),
        "comparison_rule_declared_rows": str(sum(bool(row["comparison_rule"]) for row in rows)),
        "tau_prediction_required_rows": str(sum(row["tau_prediction_required"] == "true" for row in rows)),
        "tau_prediction_supplied_rows": str(tau_supplied),
        "null_response_supplied_rows": str(null_supplied),
        "score_ready_rows": str(score_ready),
        "observed_side_fulfillment_score": f"{observed_ready / len(rows):.6f}" if rows else "0.000000",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "no_dark_cmb_verdict_allowed": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "OBSERVED_PEAK_SCORING_INPUT_CANDIDATE_READY_TAU_PREDICTION_MISSING_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "observed_side_scoring_input_candidate",
        "status": "observed Planck PR3 peak inputs materialized; Tau prediction/null-response missing; score blocked",
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_rows": rows,
        "summary": row,
        "scoring_boundary": {
            "allowed_now": "observed-side input completeness checks",
            "not_allowed_now": [
                "Tau prediction comparison",
                "CMB likelihood evaluation",
                "aggregate score",
                "no-dark or dark-sector verdict",
            ],
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Planck PR3 Peak Scoring Input Candidate v01",
        "",
        "**Doc class:** observed-side scoring input candidate",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** observed Planck PR3 peak inputs ready; Tau prediction/null-response missing; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact converts the Planck PR3 TT/TE/EE peak-observable table into a scoring-input candidate for the acoustic peak phase/height role.",
        "",
        "It fills the observed side of the comparison. It does not supply a Tau-side prediction, null response, likelihood, score, or verdict.",
        "",
        "## Candidate Summary",
        "",
        f"- candidate_rows_declared = {row['candidate_rows_declared']}",
        f"- observed_side_ready_rows = {row['observed_side_ready_rows']}",
        f"- comparison_rule_declared_rows = {row['comparison_rule_declared_rows']}",
        f"- tau_prediction_required_rows = {row['tau_prediction_required_rows']}",
        f"- tau_prediction_supplied_rows = {row['tau_prediction_supplied_rows']}",
        f"- null_response_supplied_rows = {row['null_response_supplied_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- observed_side_fulfillment_score = {row['observed_side_fulfillment_score']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## First Candidate Rows",
        "",
        "| candidate_id | source_peak_id | spectrum | ell_center | observed_value | score_blocker |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for candidate in rows[:8]:
        lines.append(
            f"| {candidate['candidate_id']} | {candidate['source_peak_id']} | {candidate['spectrum']} | "
            f"{candidate['ell_center']} | {candidate['observed_value']} | {candidate['score_blocker']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This is a protocol-readiness artifact. The observed side is complete, but no Tau-side acoustic prediction or null response has been supplied, so scoring remains blocked.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = candidate_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.csv", rows, CANDIDATE_FIELDS)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_scoring_input_candidate_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.md", rows, row)
    print("TAU_CMB_PLANCK_PR3_PEAK_SCORING_INPUT_CANDIDATE_V01_BUILT")


if __name__ == "__main__":
    main()
