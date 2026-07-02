#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_scoring_execution_gate_v01_gate_only_scoring_blocked_no_likelihood_no_verdict"

FIELDS = [
    "gate_row_id",
    "cmb_role",
    "contract_status",
    "score_entry_allowed",
    "execution_gate_decision",
    "blocking_reason",
    "required_before_run",
    "hard_failure_triggered",
    "score_computed",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "gate_rows_declared",
    "run_allowed_rows",
    "run_blocked_rows",
    "score_computed_rows",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def gate_rows() -> list[dict[str, str]]:
    contract_rows = read_csv(DERIVED / "tau_cmb_minimal_scoring_input_contract_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(contract_rows, start=1):
        rows.append(
            {
                "gate_row_id": f"TCMBSG01_{index:03d}",
                "cmb_role": row["cmb_role"],
                "contract_status": row["current_contract_status"],
                "score_entry_allowed": row["score_entry_allowed"],
                "execution_gate_decision": "SCORING_BLOCKED",
                "blocking_reason": row["missing_condition"],
                "required_before_run": row["contract_requirement"],
                "hard_failure_triggered": row["hard_failure_triggered"],
                "score_computed": "false",
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
            "summary_id": "TAU_CMB_SCORING_EXECUTION_GATE_V01",
            "gate_rows_declared": len(rows),
            "run_allowed_rows": sum(row["execution_gate_decision"] == "SCORING_RUN_ALLOWED" for row in rows),
            "run_blocked_rows": sum(row["execution_gate_decision"] == "SCORING_BLOCKED" for row in rows),
            "score_computed_rows": sum(row["score_computed"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_EXECUTION_GATE_BLOCKED_ALL_ROWS",
            "next_required_artifact": "tau_cmb_scoring_input_fulfillment_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_scoring_execution_gate_v01.md").write_text(
        """# Tau CMB Scoring Execution Gate v01

**Doc class:** scoring execution gate
**Status:** scoring blocked; no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scoring_execution_gate.py
```

Derived outputs:

```text
data/derived/tau_cmb_scoring_execution_gate_v01.csv
data/derived/tau_cmb_scoring_execution_gate_summary_v01.csv
```

This artifact decides whether the CMB scorecard is allowed to run from the
minimal scoring input contract. In v01 every contract input is unsatisfied, so
every execution gate row remains:

```text
SCORING_BLOCKED
```

Therefore no score is computed:

```text
run_allowed_rows = 0
score_computed_rows = 0
```

This is the last guard before a future scoring attempt. It prevents the paper
from converting scaffolds, blockers, or unresolved decisions into numerical
scores.

## Claim Boundary

This artifact is a scoring execution gate only. It computes no score, supplies
no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = gate_rows()
    write_csv(DERIVED / "tau_cmb_scoring_execution_gate_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_scoring_execution_gate_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_SCORING_EXECUTION_GATE_V01_BUILT")


if __name__ == "__main__":
    main()
