#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_scoring_input_decision_closed_by_explicit_null_response_"
    "handoff_opened_but_no_score_ready_input_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "decision_row_id",
    "handoff_row_id",
    "acceptance_row_id",
    "precheck_row_id",
    "materialization_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_handoff_package",
    "decision_status",
    "scoring_handoff_opened",
    "scoring_input_candidate_created",
    "scoring_input_acceptance_decision_closed",
    "scoring_input_accepted",
    "explicit_null_response_routed",
    "score_ready_input_available",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "payload_accepted",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "next_gate",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "scoring_input_decision_package_rows_declared",
    "scoring_handoff_opened_rows",
    "scoring_input_candidate_created_rows",
    "scoring_input_acceptance_decision_closed_rows",
    "scoring_input_accepted_rows",
    "explicit_null_response_routed_rows",
    "score_ready_input_available_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "payload_accepted_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "scoring_input_decision_package_satisfied",
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


def decision_rows(handoff_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, handoff in enumerate(handoff_rows, start=1):
        handoff_ready = (
            handoff["scoring_handoff_opened"] == "true"
            and handoff["scoring_input_candidate_created"] == "true"
            and handoff["scoring_input_accepted"] == "false"
        )
        rows.append(
            {
                "decision_row_id": f"TCMBPTAESID01_{index:03d}",
                "handoff_row_id": handoff["handoff_row_id"],
                "acceptance_row_id": handoff["acceptance_row_id"],
                "precheck_row_id": handoff["precheck_row_id"],
                "materialization_row_id": handoff["materialization_row_id"],
                "package_row_id": handoff["package_row_id"],
                "evidence_object": handoff["evidence_object"],
                "target_gate": handoff["target_gate"],
                "source_handoff_package": SOURCE_PREFIX,
                "decision_status": (
                    "SCORING_INPUT_DECISION_CLOSED_BY_EXPLICIT_NULL_RESPONSE"
                    if handoff_ready
                    else "SCORING_INPUT_DECISION_BLOCKED_BY_HANDOFF"
                ),
                "scoring_handoff_opened": str(handoff_ready).lower(),
                "scoring_input_candidate_created": str(handoff_ready).lower(),
                "scoring_input_acceptance_decision_closed": str(handoff_ready).lower(),
                "scoring_input_accepted": "false",
                "explicit_null_response_routed": str(handoff_ready).lower(),
                "score_ready_input_available": "false",
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "payload_accepted": "false",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "next_gate": "score_attempt_guard_or_wait_for_real_score_ready_input",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_INPUT_DECISION_PACKAGE_V01",
            "scoring_input_decision_package_rows_declared": len(rows),
            "scoring_handoff_opened_rows": sum(row["scoring_handoff_opened"] == "true" for row in rows),
            "scoring_input_candidate_created_rows": sum(
                row["scoring_input_candidate_created"] == "true" for row in rows
            ),
            "scoring_input_acceptance_decision_closed_rows": sum(
                row["scoring_input_acceptance_decision_closed"] == "true" for row in rows
            ),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "explicit_null_response_routed_rows": sum(
                row["explicit_null_response_routed"] == "true" for row in rows
            ),
            "score_ready_input_available_rows": sum(row["score_ready_input_available"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "scoring_input_decision_package_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_INPUT_DECISION_CLOSED_BY_EXPLICIT_NULL_RESPONSE_SCORE_STILL_BLOCKED",
            "next_required_artifact": "score_attempt_guard_or_real_score_ready_input_supply",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Scoring Input Decision Package v01

**Doc class:** scoring-input decision package from accepted evidence handoff
**Status:** decision closed by explicit null-response route; scoring remains blocked

This artifact consumes the scoring-handoff package. Because the handoff opens a
candidate route but does not supply a score-ready input, the decision is closed
by an explicit null-response route rather than by accepting a scoring input.

```text
scoring_handoff_opened_rows=7
scoring_input_candidate_created_rows=7
scoring_input_acceptance_decision_closed_rows=7
scoring_input_accepted_rows=0
explicit_null_response_routed_rows=7
score_ready_input_available_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact closes the scoring-input decision by explicit null response only.
It accepts no scoring input, supplies no score-ready input, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = decision_rows(read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"))
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_INPUT_DECISION_PACKAGE_V01_BUILT")


if __name__ == "__main__":
    main()
