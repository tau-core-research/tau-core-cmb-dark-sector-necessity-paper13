#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
    "scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01"
)

CLAIM_BOUNDARY = (
    f"{PREFIX}_unblock_plan_only_no_unblock_completed_no_materialization_audit_pass_no_evidence_accepted_"
    "no_receipt_accepted_no_handoff_opened_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_"
    "no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "unblock_row_id",
    "evidence_object",
    "target_gate",
    "unblock_source",
    "unblock_plan_status",
    "required_acceptance_record",
    "required_unblock_action",
    "required_exit_condition",
    "unblock_priority",
    "materialization_audit_required",
    "receipt_acceptance_required",
    "evidence_acceptance_required",
    "handoff_open_required",
    "materialization_audit_passed",
    "evidence_materialized",
    "evidence_received",
    "receipt_accepted",
    "evidence_accepted",
    "acceptance_precheck_passed",
    "unblock_completed",
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
    "unblock_condition_evidence_receipt_acceptance_unblock_plan_rows_declared",
    "materialization_audit_required_rows",
    "receipt_acceptance_required_rows",
    "evidence_acceptance_required_rows",
    "handoff_open_required_rows",
    "materialization_audit_passed_rows",
    "evidence_materialized_rows",
    "evidence_received_rows",
    "receipt_accepted_rows",
    "evidence_accepted_rows",
    "acceptance_precheck_passed_rows",
    "unblock_completed_rows",
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
    "unblock_condition_evidence_receipt_acceptance_unblock_plan_satisfied",
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
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.csv"
    )
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def unblock_rows(precheck_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, precheck in enumerate(precheck_rows, start=1):
        rows.append(
            {
                "unblock_row_id": f"TCMBPTPIPEPSIPSEORSHUCERAU01_{index:03d}",
                "evidence_object": precheck["evidence_object"],
                "target_gate": precheck["target_gate"],
                "unblock_source": (
                    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
                    "scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01"
                ),
                "unblock_plan_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
                "required_acceptance_record": precheck["required_acceptance_record"],
                "required_unblock_action": (
                    "pass materialization audit, accept receipt, accept evidence object, and open scoring handoff"
                ),
                "required_exit_condition": (
                    "score attempt may be allowed only after materialization audit pass, accepted receipt, "
                    "accepted evidence object, accepted payload/scoring input, and open handoff are recorded"
                ),
                "unblock_priority": str(index),
                "materialization_audit_required": precheck["materialization_audit_required"],
                "receipt_acceptance_required": precheck["receipt_acceptance_required"],
                "evidence_acceptance_required": precheck["evidence_acceptance_required"],
                "handoff_open_required": precheck["handoff_open_required"],
                "materialization_audit_passed": precheck["materialization_audit_passed"],
                "evidence_materialized": precheck["evidence_materialized"],
                "evidence_received": precheck["evidence_received"],
                "receipt_accepted": precheck["receipt_accepted"],
                "evidence_accepted": precheck["evidence_accepted"],
                "acceptance_precheck_passed": precheck["acceptance_precheck_passed"],
                "unblock_completed": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_V01",
            "unblock_condition_evidence_receipt_acceptance_unblock_plan_rows_declared": len(rows),
            "materialization_audit_required_rows": sum(row["materialization_audit_required"] == "true" for row in rows),
            "receipt_acceptance_required_rows": sum(row["receipt_acceptance_required"] == "true" for row in rows),
            "evidence_acceptance_required_rows": sum(row["evidence_acceptance_required"] == "true" for row in rows),
            "handoff_open_required_rows": sum(row["handoff_open_required"] == "true" for row in rows),
            "materialization_audit_passed_rows": sum(row["materialization_audit_passed"] == "true" for row in rows),
            "evidence_materialized_rows": sum(row["evidence_materialized"] == "true" for row in rows),
            "evidence_received_rows": sum(row["evidence_received"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "acceptance_precheck_passed_rows": sum(row["acceptance_precheck_passed"] == "true" for row in rows),
            "unblock_completed_rows": sum(row["unblock_completed"] == "true" for row in rows),
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
            "unblock_condition_evidence_receipt_acceptance_unblock_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": (
                "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED_SCORING_STILL_BLOCKED"
            ),
            "next_required_artifact": (
                "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
                "scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Acceptance Unblock Plan v01

**Doc class:** parent-input evidence payload scoring handoff unblock-condition evidence receipt acceptance unblock plan
**Status:** unblock plan declared but not completed; scoring remains blocked

This artifact declares the concrete exit requirements after the
unblock-condition evidence receipt acceptance precheck. The score attempt can
only proceed after materialization audit pass, accepted receipt, accepted
evidence object, accepted payload/scoring input, and open handoff are recorded.

```text
unblock_condition_evidence_receipt_acceptance_unblock_plan_satisfied=false
materialization_audit_required_rows=7
receipt_acceptance_required_rows=7
evidence_acceptance_required_rows=7
handoff_open_required_rows=7
unblock_completed_rows=0
score_attempt_blocked_now_rows=7
```

Next focused artifact:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01
```

## Claim Boundary

This artifact declares unblock requirements only. It materializes no evidence
object, accepts no receipt, accepts no evidence object, opens no scoring
handoff, executes nothing, accepts no payload or scoring input, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = unblock_rows(source_rows())
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print(
        "PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_V01_BUILT"
    )


if __name__ == "__main__":
    main()
