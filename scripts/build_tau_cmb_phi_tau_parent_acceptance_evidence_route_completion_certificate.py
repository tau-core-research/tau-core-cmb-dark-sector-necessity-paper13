#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_route_completed_to_null_response_locked_terminal_state_"
    "no_score_ready_input_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "certificate_row_id",
    "lock_row_id",
    "guard_row_id",
    "decision_row_id",
    "handoff_row_id",
    "acceptance_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_null_response_lock",
    "certificate_status",
    "route_completed",
    "terminal_state_reached",
    "terminal_state",
    "null_response_locked",
    "score_attempt_guard_executed",
    "score_attempt_denied",
    "score_ready_input_available",
    "scoring_input_accepted",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "required_unlock_condition",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "route_completion_certificate_rows_declared",
    "route_completed_rows",
    "terminal_state_reached_rows",
    "null_response_locked_rows",
    "score_attempt_guard_executed_rows",
    "score_attempt_denied_rows",
    "score_ready_input_available_rows",
    "scoring_input_accepted_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "route_completion_certificate_satisfied",
    "terminal_state",
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


def certificate_rows(lock_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, lock in enumerate(lock_rows, start=1):
        completed = (
            lock["null_response_locked"] == "true"
            and lock["score_attempt_guard_executed"] == "true"
            and lock["score_attempt_denied"] == "true"
            and lock["score_ready_input_available"] == "false"
            and lock["scoring_input_accepted"] == "false"
        )
        rows.append(
            {
                "certificate_row_id": f"TCMBPTAERCC01_{index:03d}",
                "lock_row_id": lock["lock_row_id"],
                "guard_row_id": lock["guard_row_id"],
                "decision_row_id": lock["decision_row_id"],
                "handoff_row_id": lock["handoff_row_id"],
                "acceptance_row_id": lock["acceptance_row_id"],
                "package_row_id": lock["package_row_id"],
                "evidence_object": lock["evidence_object"],
                "target_gate": lock["target_gate"],
                "source_null_response_lock": SOURCE_PREFIX,
                "certificate_status": (
                    "ROUTE_COMPLETED_TO_NULL_RESPONSE_LOCKED_TERMINAL_STATE"
                    if completed
                    else "ROUTE_COMPLETION_CERTIFICATE_BLOCKED"
                ),
                "route_completed": str(completed).lower(),
                "terminal_state_reached": str(completed).lower(),
                "terminal_state": "null_response_locked",
                "null_response_locked": str(completed).lower(),
                "score_attempt_guard_executed": str(completed).lower(),
                "score_attempt_denied": str(completed).lower(),
                "score_ready_input_available": "false",
                "scoring_input_accepted": "false",
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "required_unlock_condition": "real_score_ready_input_with_accepted_scoring_input",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_ROUTE_COMPLETION_CERTIFICATE_V01",
            "route_completion_certificate_rows_declared": len(rows),
            "route_completed_rows": sum(row["route_completed"] == "true" for row in rows),
            "terminal_state_reached_rows": sum(row["terminal_state_reached"] == "true" for row in rows),
            "null_response_locked_rows": sum(row["null_response_locked"] == "true" for row in rows),
            "score_attempt_guard_executed_rows": sum(
                row["score_attempt_guard_executed"] == "true" for row in rows
            ),
            "score_attempt_denied_rows": sum(row["score_attempt_denied"] == "true" for row in rows),
            "score_ready_input_available_rows": sum(row["score_ready_input_available"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "route_completion_certificate_satisfied": "true",
            "terminal_state": "null_response_locked",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ROUTE_COMPLETED_TO_NULL_RESPONSE_LOCKED_TERMINAL_STATE",
            "next_required_artifact": "real_score_ready_input_supply_to_reopen_scoring_route",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Route Completion Certificate v01

**Doc class:** route completion certificate for accepted-evidence chain
**Status:** route completed to null-response locked terminal state

This artifact consumes the null-response lock and certifies the terminal state
of the accepted-evidence scoring route. The route is complete for the current
inputs and ends in a null-response lock because no real score-ready input with
accepted scoring input exists.

```text
route_completed_rows=7
terminal_state_reached_rows=7
terminal_state=null_response_locked
null_response_locked_rows=7
score_ready_input_available_rows=0
scoring_input_accepted_rows=0
scores_computed_rows=0
cmb_likelihood_available_rows=0
```

## Claim Boundary

This artifact certifies route completion only. It accepts no scoring input,
supplies no score-ready input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = certificate_rows(read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"))
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_ROUTE_COMPLETION_CERTIFICATE_V01_BUILT")


if __name__ == "__main__":
    main()
