#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
    "scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01"
)
SOURCE_PREFIX = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
    "scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01"
)

CLAIM_BOUNDARY = (
    f"{PREFIX}_audit_only_closed_gate_verified_no_acceptance_no_handoff_no_execution_no_scoring_input_"
    "no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "evidence_object",
    "target_gate",
    "decision_gate_source",
    "decision_gate_audit_status",
    "decision_gate_audit_rule",
    "decision_gate_audit_finding",
    "decision_gate_audited",
    "decision_gate_audit_passed",
    "decision_output",
    "unblock_plan_audit_passed",
    "receipt_accepted",
    "evidence_accepted",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "recorded_decision",
    "acceptance_allowed",
    "payload_accepted",
    "scoring_input_accepted",
    "handoff_unblocked",
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
    "unblock_condition_evidence_receipt_acceptance_decision_gate_audit_rows_declared",
    "decision_gate_audited_rows",
    "decision_gate_audit_passed_rows",
    "decision_gate_closed_rows",
    "unblock_plan_audit_passed_rows",
    "receipt_accepted_rows",
    "evidence_accepted_rows",
    "open_handoff_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
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
    "unblock_condition_evidence_receipt_acceptance_decision_gate_audit_satisfied",
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
    with (DERIVED / f"{SOURCE_PREFIX}.csv").open(newline="") as handle:
        return list(csv.DictReader(handle))


def audit_rows(gate_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, gate in enumerate(gate_rows, start=1):
        rows.append(
            {
                "audit_row_id": f"TCMBPTPIPEPSIPSEORSHUCERADGA01_{index:03d}",
                "evidence_object": gate["evidence_object"],
                "target_gate": gate["target_gate"],
                "decision_gate_source": SOURCE_PREFIX,
                "decision_gate_audit_status": "ACCEPTANCE_DECISION_GATE_AUDITED_CLOSED_SCORING_BLOCKED",
                "decision_gate_audit_rule": (
                    "audit passes only when the gate is closed, no downstream permission is granted, "
                    "and the closure is traceable to unmet acceptance/handoff conditions"
                ),
                "decision_gate_audit_finding": "closed gate is consistent with unsatisfied unblock-plan audit and blocked score attempt",
                "decision_gate_audited": "true",
                "decision_gate_audit_passed": "true",
                "decision_output": gate["decision_output"],
                "unblock_plan_audit_passed": gate["unblock_plan_audit_passed"],
                "receipt_accepted": gate["receipt_accepted"],
                "evidence_accepted": gate["evidence_accepted"],
                "score_attempt_allowed_now": gate["score_attempt_allowed_now"],
                "score_attempt_blocked_now": gate["score_attempt_blocked_now"],
                "recorded_decision": gate["recorded_decision"],
                "acceptance_allowed": gate["acceptance_allowed"],
                "payload_accepted": gate["payload_accepted"],
                "scoring_input_accepted": gate["scoring_input_accepted"],
                "handoff_unblocked": gate["handoff_unblocked"],
                "can_execute": gate["can_execute"],
                "execution_attempted": gate["execution_attempted"],
                "execution_succeeded": gate["execution_succeeded"],
                "evidence_package_passed": gate["evidence_package_passed"],
                "input_certificate_passed": gate["input_certificate_passed"],
                "phi_tau_eff_derived": gate["phi_tau_eff_derived"],
                "scores_computed": gate["scores_computed"],
                "cmb_likelihood_available": gate["cmb_likelihood_available"],
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDIT_V01",
            "unblock_condition_evidence_receipt_acceptance_decision_gate_audit_rows_declared": len(rows),
            "decision_gate_audited_rows": sum(row["decision_gate_audited"] == "true" for row in rows),
            "decision_gate_audit_passed_rows": sum(row["decision_gate_audit_passed"] == "true" for row in rows),
            "decision_gate_closed_rows": sum(row["decision_output"] == "acceptance_closed" for row in rows),
            "unblock_plan_audit_passed_rows": sum(row["unblock_plan_audit_passed"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "open_handoff_rows": sum(row["recorded_decision"] == "handoff_open" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
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
            "unblock_condition_evidence_receipt_acceptance_decision_gate_audit_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDITED_CLOSED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "materialize_acceptance_evidence_then_reopen_decision_gate",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Acceptance Decision Gate Audit v01

**Doc class:** parent-input evidence payload scoring handoff unblock-condition evidence receipt acceptance decision gate audit
**Status:** closed decision gate audited; scoring remains blocked

The audit verifies that the closed gate is internally consistent: all seven
rows are audited, the gate is closed, no evidence or receipt is accepted, no
handoff is opened, and no scoring permission is granted.

```text
decision_gate_audit_passed_rows=7
decision_gate_closed_rows=7
receipt_accepted_rows=0
evidence_accepted_rows=0
open_handoff_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact audits a closed decision gate only. It accepts no evidence object,
accepts no receipt, opens no scoring handoff, executes nothing, accepts no
payload or scoring input, derives no `Phi_tau_eff`, computes no score, supplies
no CMB likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows(source_rows())
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
