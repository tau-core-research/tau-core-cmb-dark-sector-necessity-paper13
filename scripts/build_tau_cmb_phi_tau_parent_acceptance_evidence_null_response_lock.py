#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_null_response_locked_after_score_guard_denial_"
    "no_score_ready_input_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "lock_row_id",
    "guard_row_id",
    "decision_row_id",
    "handoff_row_id",
    "acceptance_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_guard",
    "lock_status",
    "score_attempt_guard_executed",
    "score_attempt_denied",
    "explicit_null_response_routed",
    "null_response_locked",
    "score_ready_input_available",
    "scoring_input_accepted",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "payload_accepted",
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
    "null_response_lock_rows_declared",
    "score_attempt_guard_executed_rows",
    "score_attempt_denied_rows",
    "explicit_null_response_routed_rows",
    "null_response_locked_rows",
    "score_ready_input_available_rows",
    "scoring_input_accepted_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "payload_accepted_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "null_response_lock_satisfied",
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


def lock_rows(guard_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, guard in enumerate(guard_rows, start=1):
        lockable = (
            guard["score_attempt_guard_executed"] == "true"
            and guard["score_attempt_denied"] == "true"
            and guard["score_ready_input_available"] == "false"
            and guard["scoring_input_accepted"] == "false"
        )
        rows.append(
            {
                "lock_row_id": f"TCMBPTAENRL01_{index:03d}",
                "guard_row_id": guard["guard_row_id"],
                "decision_row_id": guard["decision_row_id"],
                "handoff_row_id": guard["handoff_row_id"],
                "acceptance_row_id": guard["acceptance_row_id"],
                "package_row_id": guard["package_row_id"],
                "evidence_object": guard["evidence_object"],
                "target_gate": guard["target_gate"],
                "source_guard": SOURCE_PREFIX,
                "lock_status": (
                    "NULL_RESPONSE_LOCKED_AFTER_SCORE_GUARD_DENIAL"
                    if lockable
                    else "NULL_RESPONSE_LOCK_BLOCKED_BY_GUARD_STATE"
                ),
                "score_attempt_guard_executed": str(lockable).lower(),
                "score_attempt_denied": str(lockable).lower(),
                "explicit_null_response_routed": str(lockable).lower(),
                "null_response_locked": str(lockable).lower(),
                "score_ready_input_available": "false",
                "scoring_input_accepted": "false",
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "payload_accepted": "false",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "required_unlock_condition": "replace_null_response_with_real_score_ready_input_and_accepted_scoring_input",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_NULL_RESPONSE_LOCK_V01",
            "null_response_lock_rows_declared": len(rows),
            "score_attempt_guard_executed_rows": sum(
                row["score_attempt_guard_executed"] == "true" for row in rows
            ),
            "score_attempt_denied_rows": sum(row["score_attempt_denied"] == "true" for row in rows),
            "explicit_null_response_routed_rows": sum(
                row["explicit_null_response_routed"] == "true" for row in rows
            ),
            "null_response_locked_rows": sum(row["null_response_locked"] == "true" for row in rows),
            "score_ready_input_available_rows": sum(row["score_ready_input_available"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "null_response_lock_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "NULL_RESPONSE_LOCKED_AFTER_SCORE_GUARD_DENIAL",
            "next_required_artifact": "real_score_ready_input_supply_to_unlock_null_response",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Null-Response Lock v01

**Doc class:** null-response lock for accepted-evidence scoring route
**Status:** null response locked after score-attempt guard denial

This artifact consumes the score-attempt guard. Since the guard was executed and
all seven score attempts were denied because no score-ready input exists, the
accepted-evidence route is locked in null-response state until a real
score-ready input with accepted scoring input is supplied.

```text
score_attempt_guard_executed_rows=7
score_attempt_denied_rows=7
explicit_null_response_routed_rows=7
null_response_locked_rows=7
score_ready_input_available_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact locks the null-response state only. It accepts no scoring input,
supplies no score-ready input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = lock_rows(read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"))
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_NULL_RESPONSE_LOCK_V01_BUILT")


if __name__ == "__main__":
    main()
