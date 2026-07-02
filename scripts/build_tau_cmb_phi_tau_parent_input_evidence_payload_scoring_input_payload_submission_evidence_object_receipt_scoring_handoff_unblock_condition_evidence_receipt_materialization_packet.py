#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_"
    "unblock_condition_evidence_receipt_materialization_packet_v01_packet_schema_only_no_evidence_materialized_"
    "no_handoff_opened_no_receipt_accepted_no_evidence_accepted_no_execution_allowed_no_scoring_input_accepted_"
    "no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "packet_row_id",
    "evidence_object",
    "target_gate",
    "materialization_source",
    "requested_evidence_record",
    "receipt_candidate_record",
    "packet_slot_object",
    "materialization_status",
    "materialization_requirement",
    "provenance_requirement",
    "replay_requirement",
    "firewall_requirement",
    "acceptance_exit_gate",
    "request_open",
    "evidence_requested",
    "receipt_candidate_prepared",
    "receipt_candidate_audited",
    "receipt_candidate_audit_passed",
    "remediation_declared",
    "remediation_completed",
    "packet_declared",
    "evidence_materialized",
    "evidence_received",
    "receipt_accepted",
    "evidence_accepted",
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
    "unblock_condition_evidence_receipt_materialization_packet_rows_declared",
    "request_open_rows",
    "evidence_requested_rows",
    "receipt_candidate_prepared_rows",
    "receipt_candidate_audited_rows",
    "receipt_candidate_audit_passed_rows",
    "remediation_declared_rows",
    "remediation_completed_rows",
    "packet_declared_rows",
    "evidence_materialized_rows",
    "evidence_received_rows",
    "receipt_accepted_rows",
    "evidence_accepted_rows",
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
    "unblock_condition_evidence_receipt_materialization_packet_satisfied",
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


def packet_rows() -> list[dict[str, str]]:
    rows = [
        ("submission_payload_bundle", "payload_supply_gate", "payload_acceptance_record"),
        ("completion_evidence_bundle", "completion_evidence_gate", "completion_evidence_acceptance_record"),
        ("provenance_bundle", "provenance_gate", "provenance_acceptance_record"),
        ("replay_bundle", "replay_gate", "replay_acceptance_record"),
        ("hash_manifest_bundle", "hash_manifest_gate", "hash_manifest_acceptance_record"),
        ("endpoint_firewall_bundle", "endpoint_firewall_gate", "endpoint_firewall_acceptance_record"),
        (
            "acceptance_record_bundle",
            "payload_and_scoring_input_acceptance_gate",
            "payload_and_scoring_input_acceptance_record",
        ),
    ]
    return [
        {
            "packet_row_id": f"TCMBPTPIPEPSIPSEORSHUCERMP01_{index:03d}",
            "evidence_object": evidence_object,
            "target_gate": gate,
            "materialization_source": (
                "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
                "scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01"
            ),
            "requested_evidence_record": requested_record,
            "receipt_candidate_record": f"{requested_record}_receipt_candidate",
            "packet_slot_object": f"{requested_record}_materialization_packet",
            "materialization_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED",
            "materialization_requirement": "materialize endpoint-blind evidence object with stable path, schema, row ids, and sha256",
            "provenance_requirement": "bind source stage, generator script, runtime, source hashes, and artifact hashes before acceptance",
            "replay_requirement": "bind deterministic replay command, working directory, expected outputs, and expected hashes",
            "firewall_requirement": "endpoint-firewall evidence must be present before CMB endpoint labels, scores, or posterior information can be used",
            "acceptance_exit_gate": "may exit only after evidence object and receipt are materialized, audited, and accepted without endpoint leakage",
            "request_open": "true",
            "evidence_requested": "true",
            "receipt_candidate_prepared": "true",
            "receipt_candidate_audited": "true",
            "receipt_candidate_audit_passed": "true",
            "remediation_declared": "true",
            "remediation_completed": "false",
            "packet_declared": "true",
            "evidence_materialized": "false",
            "evidence_received": "false",
            "receipt_accepted": "false",
            "evidence_accepted": "false",
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
        for index, (evidence_object, gate, requested_record) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_V01",
            "unblock_condition_evidence_receipt_materialization_packet_rows_declared": len(rows),
            "request_open_rows": sum(row["request_open"] == "true" for row in rows),
            "evidence_requested_rows": sum(row["evidence_requested"] == "true" for row in rows),
            "receipt_candidate_prepared_rows": sum(row["receipt_candidate_prepared"] == "true" for row in rows),
            "receipt_candidate_audited_rows": sum(row["receipt_candidate_audited"] == "true" for row in rows),
            "receipt_candidate_audit_passed_rows": sum(row["receipt_candidate_audit_passed"] == "true" for row in rows),
            "remediation_declared_rows": sum(row["remediation_declared"] == "true" for row in rows),
            "remediation_completed_rows": sum(row["remediation_completed"] == "true" for row in rows),
            "packet_declared_rows": sum(row["packet_declared"] == "true" for row in rows),
            "evidence_materialized_rows": sum(row["evidence_materialized"] == "true" for row in rows),
            "evidence_received_rows": sum(row["evidence_received"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
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
            "unblock_condition_evidence_receipt_materialization_packet_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Materialization Packet v01

**Doc class:** parent-input evidence payload scoring input payload submission evidence object receipt scoring handoff unblock condition evidence receipt materialization packet
**Status:** materialization packet declared but no evidence materialized; scoring remains blocked

This artifact declares materialization packet slots for the seven requested
unblock-condition evidence records. It does not materialize, receive, accept, or
validate evidence.

```text
unblock_condition_evidence_receipt_materialization_packet_satisfied=false
packet_declared_rows=7
evidence_materialized_rows=0
evidence_received_rows=0
receipt_accepted_rows=0
evidence_accepted_rows=0
score_attempt_allowed_now=false
score_attempt_blocked_now=true
```

Next focused artifact:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01
```

## Claim Boundary

This artifact declares materialization packet slots only. It opens no scoring
handoff, materializes no evidence object, accepts no evidence object or receipt,
executes nothing, accepts no scoring input, derives no `Phi_tau_eff`, computes
no score, supplies no CMB likelihood, and permits no verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = packet_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
