#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01_receipt_audit_only_"
    "no_payload_received_no_receipt_validated_no_receipt_accepted_no_package_pass_no_certificate_pass_"
    "no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "certificate_component",
    "target_payload_component",
    "receipt_audit_status",
    "audit_source",
    "required_receipt_object",
    "audit_validation_rule",
    "payload_binding_requirement",
    "provenance_replay_requirement",
    "audit_failure_reason",
    "audit_decision",
    "payload_received",
    "receipt_candidate_declared",
    "receipt_validated",
    "receipt_accepted",
    "dimension_payload_received",
    "replay_payload_received",
    "firewall_payload_received",
    "evidence_package_passed",
    "certificate_passed",
    "payload_accepted",
    "scoring_input_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "audit_rows_declared",
    "receipt_candidate_declared_rows",
    "payload_received_rows",
    "receipt_validated_rows",
    "receipt_accepted_rows",
    "dimension_payload_received_rows",
    "replay_payload_received_rows",
    "firewall_payload_received_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "scoring_input_accepted_rows",
    "hard_failures_triggered",
    "evidence_payload_receipt_audit_satisfied",
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


def audit_rows() -> list[dict[str, str]]:
    rows = [
        ("certificate_candidate_manifest_identity", "all_parent_payload_rows", "receipt for manifest payload bundle"),
        ("base_field_dimension_replay_certificate_candidate", "base_field_state_payload_candidate", "receipt for B_tau payload bundle"),
        ("seed_dimension_replay_certificate_candidate", "morphological_seed_payload_candidate", "receipt for seed_tau payload bundle"),
        ("operator_dimension_replay_certificate_candidate", "response_operator_payload_candidate", "receipt for R_tau payload bundle"),
        ("gauge_normalization_replay_certificate_candidate", "gauge_normalization_payload_candidate", "receipt for gauge/normalization payload bundle"),
        ("payload_firewall_certificate_candidate", "endpoint_firewall_payload_candidate", "receipt for aggregate firewall payload bundle"),
        ("executable_replay_certificate_candidate", "provenance_replay_payload_candidate", "receipt for replay/provenance payload bundle"),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPRA01_{index:03d}",
            "certificate_component": component,
            "target_payload_component": target,
            "receipt_audit_status": "RECEIPT_AUDIT_FAILED_NO_PAYLOAD_RECEIVED",
            "audit_source": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01",
            "required_receipt_object": receipt,
            "audit_validation_rule": "receipt audit can pass only after matching payload and receipt records are present",
            "payload_binding_requirement": "receipt must bind to a concrete endpoint-blind payload object",
            "provenance_replay_requirement": "receipt must bind payload hash, replay command, and artifact path",
            "audit_failure_reason": "no payload record is available for receipt validation",
            "audit_decision": "failed_until_payload_and_receipt_are_supplied",
            "payload_received": "false",
            "receipt_candidate_declared": "true",
            "receipt_validated": "false",
            "receipt_accepted": "false",
            "dimension_payload_received": "false",
            "replay_payload_received": "false",
            "firewall_payload_received": "false",
            "evidence_package_passed": "false",
            "certificate_passed": "false",
            "payload_accepted": "false",
            "scoring_input_accepted": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (component, target, receipt) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "receipt_candidate_declared_rows": sum(row["receipt_candidate_declared"] == "true" for row in rows),
            "payload_received_rows": sum(row["payload_received"] == "true" for row in rows),
            "receipt_validated_rows": sum(row["receipt_validated"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "dimension_payload_received_rows": sum(row["dimension_payload_received"] == "true" for row in rows),
            "replay_payload_received_rows": sum(row["replay_payload_received"] == "true" for row in rows),
            "firewall_payload_received_rows": sum(row["firewall_payload_received"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_receipt_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_AUDIT_FAILED_NO_PAYLOAD_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Receipt Audit v01

**Doc class:** parent-input evidence payload receipt audit
**Status:** receipt audit declared but failed because no payload is received; no receipt validated, no receipt accepted, no package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_summary_v01.csv
```

This artifact audits whether declared receipt candidates can be validated
against concrete endpoint-blind evidence payload records. No payload record is available for receipt validation, so every receipt audit row fails.

The evidence payload receipt audit is not satisfied:

```text
evidence_payload_receipt_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01
```

## Claim Boundary

This artifact audits receipt candidates only. It receives no dimension, replay,
or firewall evidence payload, validates no receipt, accepts no receipt, provides
no evidence-package pass, provides no certificate pass, accepts no parent-side
Tau inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
