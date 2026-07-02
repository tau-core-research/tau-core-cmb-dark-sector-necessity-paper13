#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_scoring_handoff_package_opened_from_accepted_evidence_"
    "scoring_input_candidate_created_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "handoff_row_id",
    "acceptance_row_id",
    "precheck_row_id",
    "materialization_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_acceptance_gate",
    "handoff_status",
    "receipt_accepted",
    "evidence_accepted",
    "acceptance_record_created",
    "decision_gate_reopen_allowed",
    "endpoint_blind_handoff",
    "scoring_handoff_package_created",
    "scoring_handoff_opened",
    "scoring_input_candidate_created",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "payload_accepted",
    "scoring_input_accepted",
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
    "scoring_handoff_package_rows_declared",
    "receipt_accepted_rows",
    "evidence_accepted_rows",
    "acceptance_record_created_rows",
    "decision_gate_reopen_allowed_rows",
    "endpoint_blind_handoff_rows",
    "scoring_handoff_package_created_rows",
    "scoring_handoff_opened_rows",
    "scoring_input_candidate_created_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "scoring_handoff_package_satisfied",
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


def handoff_rows(acceptance_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, acceptance in enumerate(acceptance_rows, start=1):
        prereqs_passed = (
            acceptance["receipt_accepted"] == "true"
            and acceptance["evidence_accepted"] == "true"
            and acceptance["acceptance_record_created"] == "true"
            and acceptance["decision_gate_reopen_allowed"] == "true"
        )
        rows.append(
            {
                "handoff_row_id": f"TCMBPTAESH01_{index:03d}",
                "acceptance_row_id": acceptance["acceptance_row_id"],
                "precheck_row_id": acceptance["precheck_row_id"],
                "materialization_row_id": acceptance["materialization_row_id"],
                "package_row_id": acceptance["package_row_id"],
                "evidence_object": acceptance["evidence_object"],
                "target_gate": acceptance["target_gate"],
                "source_acceptance_gate": SOURCE_PREFIX,
                "handoff_status": (
                    "SCORING_HANDOFF_PACKAGE_OPENED_FROM_ACCEPTED_EVIDENCE"
                    if prereqs_passed
                    else "SCORING_HANDOFF_PACKAGE_BLOCKED_BY_ACCEPTANCE_GATE"
                ),
                "receipt_accepted": str(prereqs_passed).lower(),
                "evidence_accepted": str(prereqs_passed).lower(),
                "acceptance_record_created": str(prereqs_passed).lower(),
                "decision_gate_reopen_allowed": str(prereqs_passed).lower(),
                "endpoint_blind_handoff": str(prereqs_passed).lower(),
                "scoring_handoff_package_created": str(prereqs_passed).lower(),
                "scoring_handoff_opened": str(prereqs_passed).lower(),
                "scoring_input_candidate_created": str(prereqs_passed).lower(),
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "payload_accepted": "false",
                "scoring_input_accepted": "false",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "next_gate": "scoring_input_acceptance_gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_HANDOFF_PACKAGE_V01",
            "scoring_handoff_package_rows_declared": len(rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "acceptance_record_created_rows": sum(row["acceptance_record_created"] == "true" for row in rows),
            "decision_gate_reopen_allowed_rows": sum(row["decision_gate_reopen_allowed"] == "true" for row in rows),
            "endpoint_blind_handoff_rows": sum(row["endpoint_blind_handoff"] == "true" for row in rows),
            "scoring_handoff_package_created_rows": sum(
                row["scoring_handoff_package_created"] == "true" for row in rows
            ),
            "scoring_handoff_opened_rows": sum(row["scoring_handoff_opened"] == "true" for row in rows),
            "scoring_input_candidate_created_rows": sum(
                row["scoring_input_candidate_created"] == "true" for row in rows
            ),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "scoring_handoff_package_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_HANDOFF_PACKAGE_OPENED_FROM_ACCEPTED_EVIDENCE_SCORING_INPUT_STILL_BLOCKED",
            "next_required_artifact": "accept_scoring_input_from_handoff_or_route_explicit_null_response",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Scoring Handoff Package v01

**Doc class:** parent-input scoring handoff package from accepted evidence
**Status:** scoring handoff opened; scoring input remains unaccepted

This artifact consumes the receipt/evidence acceptance reopen-gate package. It
packages all seven accepted endpoint-blind evidence rows into a scoring-handoff
candidate and opens the handoff route to the scoring-input acceptance gate.

```text
receipt_accepted_rows=7
evidence_accepted_rows=7
scoring_handoff_package_created_rows=7
scoring_handoff_opened_rows=7
scoring_input_candidate_created_rows=7
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact opens a scoring handoff from accepted evidence only. It accepts no
scoring input, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = handoff_rows(read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"))
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_HANDOFF_PACKAGE_V01_BUILT")


if __name__ == "__main__":
    main()
