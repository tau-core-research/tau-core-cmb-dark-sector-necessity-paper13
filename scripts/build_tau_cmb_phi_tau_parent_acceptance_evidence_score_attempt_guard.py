#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_score_attempt_guard_executed_and_denied_"
    "no_score_ready_input_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "guard_row_id",
    "decision_row_id",
    "handoff_row_id",
    "acceptance_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_decision_package",
    "guard_status",
    "score_attempt_guard_executed",
    "scoring_input_acceptance_decision_closed",
    "explicit_null_response_routed",
    "score_ready_input_available",
    "scoring_input_accepted",
    "score_attempt_allowed_now",
    "score_attempt_denied",
    "score_attempt_blocked_now",
    "payload_accepted",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "required_unblock_condition",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "score_attempt_guard_rows_declared",
    "score_attempt_guard_executed_rows",
    "scoring_input_acceptance_decision_closed_rows",
    "explicit_null_response_routed_rows",
    "score_ready_input_available_rows",
    "scoring_input_accepted_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_denied_rows",
    "score_attempt_blocked_now_rows",
    "payload_accepted_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "score_attempt_guard_satisfied",
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


def guard_rows(decision_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, decision in enumerate(decision_rows, start=1):
        guard_executable = (
            decision["scoring_input_acceptance_decision_closed"] == "true"
            and decision["explicit_null_response_routed"] == "true"
            and decision["score_ready_input_available"] == "false"
            and decision["scoring_input_accepted"] == "false"
        )
        rows.append(
            {
                "guard_row_id": f"TCMBPTAESAG01_{index:03d}",
                "decision_row_id": decision["decision_row_id"],
                "handoff_row_id": decision["handoff_row_id"],
                "acceptance_row_id": decision["acceptance_row_id"],
                "package_row_id": decision["package_row_id"],
                "evidence_object": decision["evidence_object"],
                "target_gate": decision["target_gate"],
                "source_decision_package": SOURCE_PREFIX,
                "guard_status": (
                    "SCORE_ATTEMPT_GUARD_EXECUTED_DENIED_NO_SCORE_READY_INPUT"
                    if guard_executable
                    else "SCORE_ATTEMPT_GUARD_BLOCKED_BY_DECISION_PACKAGE"
                ),
                "score_attempt_guard_executed": str(guard_executable).lower(),
                "scoring_input_acceptance_decision_closed": str(guard_executable).lower(),
                "explicit_null_response_routed": str(guard_executable).lower(),
                "score_ready_input_available": "false",
                "scoring_input_accepted": "false",
                "score_attempt_allowed_now": "false",
                "score_attempt_denied": str(guard_executable).lower(),
                "score_attempt_blocked_now": "true",
                "payload_accepted": "false",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "required_unblock_condition": "supply_real_score_ready_input_with_accepted_scoring_input",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORE_ATTEMPT_GUARD_V01",
            "score_attempt_guard_rows_declared": len(rows),
            "score_attempt_guard_executed_rows": sum(row["score_attempt_guard_executed"] == "true" for row in rows),
            "scoring_input_acceptance_decision_closed_rows": sum(
                row["scoring_input_acceptance_decision_closed"] == "true" for row in rows
            ),
            "explicit_null_response_routed_rows": sum(
                row["explicit_null_response_routed"] == "true" for row in rows
            ),
            "score_ready_input_available_rows": sum(row["score_ready_input_available"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_denied_rows": sum(row["score_attempt_denied"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "score_attempt_guard_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORE_ATTEMPT_GUARD_EXECUTED_DENIED_NO_SCORE_READY_INPUT",
            "next_required_artifact": "real_score_ready_input_supply_or_keep_null_response_locked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Score Attempt Guard v01

**Doc class:** score-attempt guard for accepted-evidence chain
**Status:** guard executed; score attempt denied because no score-ready input exists

This artifact consumes the scoring-input decision package. The guard is executed
for all seven rows and denies score attempts because the chain has an explicit
null-response route and no accepted score-ready input.

```text
score_attempt_guard_executed_rows=7
scoring_input_acceptance_decision_closed_rows=7
explicit_null_response_routed_rows=7
score_ready_input_available_rows=0
scoring_input_accepted_rows=0
score_attempt_denied_rows=7
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact executes a score-attempt guard only. It accepts no scoring input,
supplies no score-ready input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = guard_rows(read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"))
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORE_ATTEMPT_GUARD_V01_BUILT")


if __name__ == "__main__":
    main()
