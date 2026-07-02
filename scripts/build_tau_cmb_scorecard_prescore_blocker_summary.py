#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_scorecard_prescore_blocker_summary_v01_summary_only_no_score_no_likelihood_no_verdict"

FIELDS = [
    "blocker_row_id",
    "cmb_role",
    "decision_state",
    "blocking_artifact",
    "blocking_reason",
    "minimum_next_input",
    "score_gate_status",
    "hard_failure_triggered",
    "score_ready",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "blocker_rows_declared",
    "score_ready_rows",
    "score_blocked_rows",
    "unresolved_rows",
    "hard_failures_triggered",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

BLOCKING_ARTIFACTS = {
    "acoustic_peak_phase_and_height": "tau_cmb_acoustic_reduced_evaluation_v01",
    "omega_c_h2_density_inference": "tau_cmb_density_amplitude_closure_v01",
    "cmb_lensing_potential": "tau_cmb_lensing_transfer_reduced_evaluation_v01",
    "damping_tail_and_radiation_guard": "tau_cmb_radiation_guard_evaluation_v01",
    "growth_seed_and_transfer_consistency": "tau_cmb_growth_transfer_kernel_closure_v01",
    "known_limit_or_explicit_failure": "tau_cmb_known_limit_decision_update_v01",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def blocker_rows() -> list[dict[str, str]]:
    decisions = read_csv(DERIVED / "tau_cmb_known_limit_decision_update_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(decisions, start=1):
        rows.append(
            {
                "blocker_row_id": f"TCMBSPS01_{index:03d}",
                "cmb_role": row["cmb_role"],
                "decision_state": row["updated_decision_state"],
                "blocking_artifact": BLOCKING_ARTIFACTS[row["cmb_role"]],
                "blocking_reason": row["decision_reason"],
                "minimum_next_input": row["next_required_input"],
                "score_gate_status": "SCORE_BLOCKED_UNRESOLVED_EVIDENCE",
                "hard_failure_triggered": row["hard_failure_triggered"],
                "score_ready": row["score_ready"],
                "blocks_no_dark_claim": row["blocks_no_dark_claim"],
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_SCORECARD_PRESCORE_BLOCKER_SUMMARY_V01",
            "blocker_rows_declared": len(rows),
            "score_ready_rows": sum(row["score_ready"] == "true" for row in rows),
            "score_blocked_rows": sum(row["score_ready"] == "false" for row in rows),
            "unresolved_rows": sum(row["decision_state"].startswith("UNRESOLVED") for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PRESCORE_BLOCKERS_SUMMARIZED_ALL_SCORE_ROWS_BLOCKED",
            "next_required_artifact": "tau_cmb_minimal_scoring_input_contract_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_scorecard_prescore_blocker_summary_v01.md").write_text(
        """# Tau CMB Scorecard Prescore Blocker Summary v01

**Doc class:** pre-score blocker summary
**Status:** all score rows blocked; no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scorecard_prescore_blocker_summary.py
```

Derived outputs:

```text
data/derived/tau_cmb_scorecard_prescore_blocker_summary_v01.csv
data/derived/tau_cmb_scorecard_prescore_blocker_summary_summary_v01.csv
```

This artifact summarizes the state after the focused v01 closure/evaluation
sequence. It does not add new physics. It records the minimum blocker for each
CMB role before scoring can begin.

Every score row remains blocked:

```text
score_ready_rows = 0
score_blocked_rows = 6
```

The pre-score blocker summary therefore prevents a premature scorecard
promotion and identifies the next contract to build:

```text
tau_cmb_minimal_scoring_input_contract_v01
```

## Claim Boundary

This artifact is a blocker summary only. It computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = blocker_rows()
    write_csv(DERIVED / "tau_cmb_scorecard_prescore_blocker_summary_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_scorecard_prescore_blocker_summary_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_SCORECARD_PRESCORE_BLOCKER_SUMMARY_V01_BUILT")


if __name__ == "__main__":
    main()
