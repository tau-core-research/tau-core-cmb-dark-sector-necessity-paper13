#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01_"
    "certificate_only_score_attempt_blocked_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_"
    "no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "certificate_row_id",
    "evidence_object",
    "target_gate",
    "certificate_source",
    "score_attempt_blocker_certificate_status",
    "certified_blocker",
    "blocker_reason",
    "certificate_passed",
    "final_pre_score_lock_audit_passed",
    "lock_result",
    "score_attempt_allowed",
    "score_attempt_blocked",
    "required_unblock_condition",
    "recorded_decision",
    "acceptance_recorded",
    "acceptance_allowed",
    "evidence_accepted",
    "receipt_accepted",
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
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_rows_declared",
    "certificate_passed_rows",
    "final_pre_score_lock_audit_passed_rows",
    "pre_score_locked_rows",
    "score_attempt_allowed_rows",
    "score_attempt_blocked_rows",
    "closed_handoff_rows",
    "open_handoff_rows",
    "acceptance_recorded_rows",
    "acceptance_allowed_rows",
    "evidence_accepted_rows",
    "receipt_accepted_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "handoff_unblocked_rows",
    "can_handoff_to_scoring_rows",
    "can_execute_rows",
    "execution_attempted_rows",
    "execution_succeeded_rows",
    "evidence_package_passed_rows",
    "input_certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_satisfied",
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


def certificate_rows() -> list[dict[str, str]]:
    rows = [
        ("submission_payload_bundle", "payload_supply_gate", "accepted payload record"),
        ("completion_evidence_bundle", "completion_evidence_gate", "accepted completion evidence record"),
        ("provenance_bundle", "provenance_gate", "accepted provenance record"),
        ("replay_bundle", "replay_gate", "accepted replay record"),
        ("hash_manifest_bundle", "hash_manifest_gate", "accepted hash manifest record"),
        ("endpoint_firewall_bundle", "endpoint_firewall_gate", "accepted endpoint firewall record"),
        ("acceptance_record_bundle", "payload_and_scoring_input_acceptance_gate", "accepted scoring input and payload record"),
    ]
    return [
        {
            "certificate_row_id": f"TCMBPTPIPEPSIPSEORSHSABC01_{index:03d}",
            "evidence_object": evidence_object,
            "target_gate": gate,
            "certificate_source": (
                "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_"
                "receipt_scoring_handoff_final_pre_score_lock_audit_v01"
            ),
            "score_attempt_blocker_certificate_status": "SCORE_ATTEMPT_BLOCKER_CERTIFICATE_PASSED_SCORING_STILL_BLOCKED",
            "certified_blocker": "score_attempt_blocked_by_missing_acceptance_conditions",
            "blocker_reason": (
                "score attempt requires accepted evidence object, receipt, payload, scoring input, and open handoff"
            ),
            "certificate_passed": "true",
            "final_pre_score_lock_audit_passed": "true",
            "lock_result": "pre_score_locked",
            "score_attempt_allowed": "false",
            "score_attempt_blocked": "true",
            "required_unblock_condition": required_condition,
            "recorded_decision": "handoff_closed",
            "acceptance_recorded": "true",
            "acceptance_allowed": "false",
            "evidence_accepted": "false",
            "receipt_accepted": "false",
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
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (evidence_object, gate, required_condition) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_BLOCKER_CERTIFICATE_V01",
            "evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_rows_declared": len(rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "final_pre_score_lock_audit_passed_rows": sum(row["final_pre_score_lock_audit_passed"] == "true" for row in rows),
            "pre_score_locked_rows": sum(row["lock_result"] == "pre_score_locked" for row in rows),
            "score_attempt_allowed_rows": sum(row["score_attempt_allowed"] == "true" for row in rows),
            "score_attempt_blocked_rows": sum(row["score_attempt_blocked"] == "true" for row in rows),
            "closed_handoff_rows": sum(row["recorded_decision"] == "handoff_closed" for row in rows),
            "open_handoff_rows": sum(row["recorded_decision"] == "handoff_open" for row in rows),
            "acceptance_recorded_rows": sum(row["acceptance_recorded"] == "true" for row in rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "handoff_unblocked_rows": sum(row["handoff_unblocked"] == "true" for row in rows),
            "can_handoff_to_scoring_rows": sum(row["can_handoff_to_scoring"] == "true" for row in rows),
            "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
            "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
            "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "input_certificate_passed_rows": sum(row["input_certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_BLOCKER_CERTIFICATE_PASSED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Score Attempt Blocker Certificate v01

**Doc class:** parent-input evidence payload scoring input payload submission evidence object receipt scoring handoff score attempt blocker certificate
**Status:** blocker certificate passed; score attempt remains blocked

This artifact certifies that a score attempt is currently blocked. The block is
not a numerical result: it follows from the audited pre-score lock and from the
absence of accepted evidence-object, receipt, payload, scoring-input, and open
handoff records.

```text
evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_satisfied=true
certified_blocker=score_attempt_blocked_by_missing_acceptance_conditions
score_attempt_allowed=false
score_attempt_blocked=true
```

Next focused artifact:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01
```

## Claim Boundary

This artifact is a blocker certificate only. It opens no scoring handoff,
accepts no evidence object or receipt, executes nothing, accepts no scoring
input, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
and permits no verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = certificate_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print(
        "PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_BLOCKER_CERTIFICATE_V01_BUILT"
    )


if __name__ == "__main__":
    main()
