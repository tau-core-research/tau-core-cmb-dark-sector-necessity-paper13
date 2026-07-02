#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01_"
    "conditions_only_score_attempt_still_blocked_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_"
    "no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "condition_row_id",
    "evidence_object",
    "target_gate",
    "condition_source",
    "score_attempt_unblock_condition_status",
    "unblock_condition",
    "condition_required",
    "condition_satisfied",
    "condition_gap",
    "score_attempt_allowed_if_satisfied",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "blocker_certificate_passed",
    "recorded_decision",
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
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "score_attempt_unblock_condition_rows_declared",
    "condition_required_rows",
    "condition_satisfied_rows",
    "condition_gap_rows",
    "score_attempt_allowed_if_satisfied_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "blocker_certificate_passed_rows",
    "open_handoff_rows",
    "acceptance_allowed_rows",
    "evidence_accepted_rows",
    "receipt_accepted_rows",
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
    "score_attempt_unblock_conditions_satisfied",
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


def condition_rows() -> list[dict[str, str]]:
    rows = [
        ("submission_payload_bundle", "payload_supply_gate", "accepted_payload_record"),
        ("completion_evidence_bundle", "completion_evidence_gate", "accepted_completion_evidence_record"),
        ("provenance_bundle", "provenance_gate", "accepted_provenance_record"),
        ("replay_bundle", "replay_gate", "accepted_replay_record"),
        ("hash_manifest_bundle", "hash_manifest_gate", "accepted_hash_manifest_record"),
        ("endpoint_firewall_bundle", "endpoint_firewall_gate", "accepted_endpoint_firewall_record"),
        ("acceptance_record_bundle", "payload_and_scoring_input_acceptance_gate", "accepted_payload_and_scoring_input_record"),
    ]
    return [
        {
            "condition_row_id": f"TCMBPTPIPEPSIPSEORSHSAUC01_{index:03d}",
            "evidence_object": evidence_object,
            "target_gate": gate,
            "condition_source": (
                "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_"
                "receipt_scoring_handoff_score_attempt_blocker_certificate_v01"
            ),
            "score_attempt_unblock_condition_status": "SCORE_ATTEMPT_UNBLOCK_CONDITION_DECLARED_NOT_SATISFIED",
            "unblock_condition": condition,
            "condition_required": "true",
            "condition_satisfied": "false",
            "condition_gap": "missing_accepted_record",
            "score_attempt_allowed_if_satisfied": "true",
            "score_attempt_allowed_now": "false",
            "score_attempt_blocked_now": "true",
            "blocker_certificate_passed": "true",
            "recorded_decision": "handoff_closed",
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
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (evidence_object, gate, condition) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_UNBLOCK_CONDITIONS_V01",
            "score_attempt_unblock_condition_rows_declared": len(rows),
            "condition_required_rows": sum(row["condition_required"] == "true" for row in rows),
            "condition_satisfied_rows": sum(row["condition_satisfied"] == "true" for row in rows),
            "condition_gap_rows": sum(row["condition_gap"] != "none" for row in rows),
            "score_attempt_allowed_if_satisfied_rows": sum(row["score_attempt_allowed_if_satisfied"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "blocker_certificate_passed_rows": sum(row["blocker_certificate_passed"] == "true" for row in rows),
            "open_handoff_rows": sum(row["recorded_decision"] == "handoff_open" for row in rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
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
            "score_attempt_unblock_conditions_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORE_ATTEMPT_UNBLOCK_CONDITIONS_DECLARED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Score Attempt Unblock Conditions v01

**Doc class:** parent-input evidence payload scoring input payload submission evidence object receipt scoring handoff score attempt unblock conditions
**Status:** unblock conditions declared; scoring remains blocked

This artifact declares the minimal conditions that must be satisfied before a
score attempt can be considered. Each condition is required, but none is
currently satisfied.

```text
score_attempt_unblock_conditions_satisfied=false
score_attempt_allowed_now=false
score_attempt_blocked_now=true
```

The required conditions are accepted records for payload, completion evidence,
provenance, replay, hash manifest, endpoint firewall, and the combined payload
and scoring-input acceptance gate.

Next focused artifact:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01
```

## Claim Boundary

This artifact declares unblock conditions only. It opens no scoring handoff,
accepts no evidence object or receipt, executes nothing, accepts no scoring
input, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
and permits no verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = condition_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print(
        "PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_UNBLOCK_CONDITIONS_V01_BUILT"
    )


if __name__ == "__main__":
    main()
