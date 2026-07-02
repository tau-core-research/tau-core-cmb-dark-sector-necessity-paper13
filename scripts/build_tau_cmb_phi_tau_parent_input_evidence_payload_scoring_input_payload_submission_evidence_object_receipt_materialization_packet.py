#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01_"
    "packet_schema_only_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_execution_allowed_"
    "no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "packet_row_id",
    "evidence_object",
    "blocked_gate",
    "materialization_source",
    "materialization_status",
    "packet_slot_object",
    "required_evidence_file",
    "required_receipt_file",
    "materialization_requirement",
    "provenance_requirement",
    "replay_requirement",
    "firewall_requirement",
    "acceptance_exit_gate",
    "packet_declared",
    "evidence_materialized",
    "receipt_validated",
    "receipt_accepted",
    "evidence_audited",
    "evidence_accepted",
    "payload_accepted",
    "scoring_input_accepted",
    "can_execute",
    "execution_attempted",
    "execution_succeeded",
    "evidence_package_passed",
    "certificate_passed",
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
    "evidence_object_receipt_materialization_packet_rows_declared",
    "packet_declared_rows",
    "evidence_materialized_rows",
    "receipt_validated_rows",
    "receipt_accepted_rows",
    "evidence_audited_rows",
    "evidence_accepted_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "can_execute_rows",
    "execution_attempted_rows",
    "execution_succeeded_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_satisfied",
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
        ("submission_payload_bundle", "payload_supply_gate", "submission_payload_bundle.csv"),
        ("completion_evidence_bundle", "completion_evidence_gate", "completion_evidence_bundle.json"),
        ("provenance_bundle", "provenance_gate", "provenance_bundle.json"),
        ("replay_bundle", "replay_gate", "replay_bundle.txt"),
        ("hash_manifest_bundle", "hash_manifest_gate", "hash_manifest_bundle.json"),
        ("endpoint_firewall_bundle", "endpoint_firewall_gate", "endpoint_firewall_bundle.json"),
        ("acceptance_record_bundle", "payload_and_scoring_input_acceptance_gate", "acceptance_record_bundle.json"),
    ]
    return [
        {
            "packet_row_id": f"TCMBPTPIPEPSIPSEORMP01_{index:03d}",
            "evidence_object": evidence_object,
            "blocked_gate": gate,
            "materialization_source": (
                "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_"
                "receipt_candidate_remediation_plan_v01"
            ),
            "materialization_status": "EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED",
            "packet_slot_object": f"{evidence_object}_materialization_packet",
            "required_evidence_file": filename,
            "required_receipt_file": f"{filename}.receipt.json",
            "materialization_requirement": "materialize endpoint-blind evidence object with stable path, schema, row ids, and sha256",
            "provenance_requirement": "bind source stage, generator script, source hashes, and artifact hashes before acceptance",
            "replay_requirement": "bind deterministic replay command, working directory, and expected output paths",
            "firewall_requirement": "endpoint-firewall evidence must be present before any CMB endpoint labels or posterior scores are used",
            "acceptance_exit_gate": "may exit only after evidence object and receipt are materialized, validated, and audit-passed without endpoint leakage",
            "packet_declared": "true",
            "evidence_materialized": "false",
            "receipt_validated": "false",
            "receipt_accepted": "false",
            "evidence_audited": "false",
            "evidence_accepted": "false",
            "payload_accepted": "false",
            "scoring_input_accepted": "false",
            "can_execute": "false",
            "execution_attempted": "false",
            "execution_succeeded": "false",
            "evidence_package_passed": "false",
            "certificate_passed": "false",
            "phi_tau_eff_derived": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (evidence_object, gate, filename) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_V01",
            "evidence_object_receipt_materialization_packet_rows_declared": len(rows),
            "packet_declared_rows": sum(row["packet_declared"] == "true" for row in rows),
            "evidence_materialized_rows": sum(row["evidence_materialized"] == "true" for row in rows),
            "receipt_validated_rows": sum(row["receipt_validated"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_audited_rows": sum(row["evidence_audited"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
            "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
            "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Materialization Packet v01

**Doc class:** parent-input evidence payload scoring input payload submission evidence object receipt materialization packet
**Status:** packet schema declared but no evidence materialized; no receipt validated, no receipt accepted, no execution allowed, no payload accepted, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_summary_v01.csv
```

This artifact declares materialization packet slots for the requested evidence
and receipt objects. It does not materialize, validate, accept, or execute any
evidence object.

The evidence payload scoring input payload submission evidence object receipt
materialization packet is not satisfied:

```text
evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01
```

## Claim Boundary

This artifact declares materialization packet slots only. It materializes no
evidence object, validates no receipt, accepts no receipt, executes nothing,
accepts no parent-side payload, provides no evidence-package pass, provides no
certificate pass, accepts no scoring input, derives no `Phi_tau_eff`, computes
no score, supplies no CMB likelihood, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = packet_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print(
        "PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_V01_BUILT"
    )


if __name__ == "__main__":
    main()
