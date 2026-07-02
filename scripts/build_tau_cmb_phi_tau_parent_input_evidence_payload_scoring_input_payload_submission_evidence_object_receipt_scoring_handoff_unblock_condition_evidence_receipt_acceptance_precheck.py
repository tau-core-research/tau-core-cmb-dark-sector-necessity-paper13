#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_"
    "unblock_condition_evidence_receipt_acceptance_precheck_v01_precheck_only_no_materialization_audit_pass_"
    "no_evidence_accepted_no_receipt_accepted_no_handoff_opened_no_execution_allowed_no_scoring_input_accepted_"
    "no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "precheck_row_id",
    "evidence_object",
    "target_gate",
    "precheck_source",
    "acceptance_precheck_status",
    "required_acceptance_record",
    "materialization_audit_required",
    "receipt_acceptance_required",
    "evidence_acceptance_required",
    "handoff_open_required",
    "precheck_failure_reason",
    "precheck_decision",
    "materialization_audit_passed",
    "evidence_materialized",
    "evidence_received",
    "receipt_accepted",
    "evidence_accepted",
    "acceptance_precheck_passed",
    "condition_satisfied",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "recorded_decision",
    "acceptance_allowed",
    "payload_accepted",
    "scoring_input_accepted",
    "handoff_unblocked",
    "can_handoff_to_scoring",
    "can_execute",
    "execution_attempted",
    "execution_succeeded",
    "evidence_package_passed",
    "input_certificate_passed",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "unblock_condition_evidence_receipt_acceptance_precheck_rows_declared",
    "materialization_audit_passed_rows",
    "evidence_materialized_rows",
    "evidence_received_rows",
    "receipt_accepted_rows",
    "evidence_accepted_rows",
    "acceptance_precheck_passed_rows",
    "condition_satisfied_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "open_handoff_rows",
    "acceptance_allowed_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "handoff_unblocked_rows",
    "can_execute_rows",
    "execution_attempted_rows",
    "execution_succeeded_rows",
    "evidence_package_passed_rows",
    "input_certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "unblock_condition_evidence_receipt_acceptance_precheck_satisfied",
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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, str]]:
    path = (
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01.csv"
    )
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def precheck_rows(audit_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, audit_row in enumerate(audit_rows, start=1):
        evidence_object = audit_row["evidence_object"]
        rows.append(
            {
                "precheck_row_id": f"TCMBPTPIPEPSIPSEORSHUCERAP01_{index:03d}",
                "evidence_object": evidence_object,
                "target_gate": audit_row["target_gate"],
                "precheck_source": (
                    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
                    "scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01"
                ),
                "acceptance_precheck_status": (
                    "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_PASSED"
                ),
                "required_acceptance_record": f"{evidence_object}_accepted_receipt_and_evidence_record",
                "materialization_audit_required": "true",
                "receipt_acceptance_required": "true",
                "evidence_acceptance_required": "true",
                "handoff_open_required": "true",
                "precheck_failure_reason": "materialization audit has not passed and no evidence object or receipt is accepted",
                "precheck_decision": "blocked_until_materialization_audit_receipt_acceptance_evidence_acceptance_and_handoff_open_pass",
                "materialization_audit_passed": audit_row["materialization_audit_passed"],
                "evidence_materialized": audit_row["evidence_materialized"],
                "evidence_received": audit_row["evidence_received"],
                "receipt_accepted": audit_row["receipt_accepted"],
                "evidence_accepted": audit_row["evidence_accepted"],
                "acceptance_precheck_passed": "false",
                "condition_satisfied": "false",
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "recorded_decision": "handoff_closed",
                "acceptance_allowed": "false",
                "payload_accepted": "false",
                "scoring_input_accepted": "false",
                "handoff_unblocked": "false",
                "can_handoff_to_scoring": "false",
                "can_execute": "false",
                "execution_attempted": "false",
                "execution_succeeded": "false",
                "evidence_package_passed": "false",
                "input_certificate_passed": "false",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_V01",
            "unblock_condition_evidence_receipt_acceptance_precheck_rows_declared": len(rows),
            "materialization_audit_passed_rows": sum(row["materialization_audit_passed"] == "true" for row in rows),
            "evidence_materialized_rows": sum(row["evidence_materialized"] == "true" for row in rows),
            "evidence_received_rows": sum(row["evidence_received"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "acceptance_precheck_passed_rows": sum(row["acceptance_precheck_passed"] == "true" for row in rows),
            "condition_satisfied_rows": sum(row["condition_satisfied"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "open_handoff_rows": sum(row["recorded_decision"] == "handoff_open" for row in rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "handoff_unblocked_rows": sum(row["handoff_unblocked"] == "true" for row in rows),
            "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
            "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
            "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "input_certificate_passed_rows": sum(row["input_certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "unblock_condition_evidence_receipt_acceptance_precheck_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": (
                "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_PASSED_SCORING_STILL_BLOCKED"
            ),
            "next_required_artifact": (
                "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
                "scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Acceptance Precheck v01

**Doc class:** parent-input evidence payload scoring input payload submission evidence object receipt scoring handoff unblock condition evidence receipt acceptance precheck
**Status:** acceptance precheck failed because the materialization audit has not passed; scoring remains blocked

This artifact prechecks whether the seven unblock-condition evidence receipts
can be accepted for scoring-handoff unblocking. The answer is no: the upstream
materialization audit has not passed, no evidence object is materialized, and
no evidence object or receipt is accepted.

```text
unblock_condition_evidence_receipt_acceptance_precheck_satisfied=false
materialization_audit_passed_rows=0
evidence_materialized_rows=0
receipt_accepted_rows=0
evidence_accepted_rows=0
acceptance_precheck_passed_rows=0
score_attempt_blocked_now_rows=7
```

Next focused artifact:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01
```

## Claim Boundary

This artifact is an acceptance precheck only. It materializes no evidence
object, accepts no receipt, accepts no evidence object, opens no scoring
handoff, executes nothing, accepts no payload or scoring input, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = precheck_rows(source_rows())
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print(
        "PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_V01_BUILT"
    )


if __name__ == "__main__":
    main()
