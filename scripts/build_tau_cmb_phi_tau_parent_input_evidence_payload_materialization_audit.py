#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01_materialization_audit_only_"
    "no_payload_materialized_no_packet_accepted_no_receipt_validated_no_package_pass_no_certificate_pass_"
    "no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "packet_component",
    "target_payload_component",
    "materialization_audit_status",
    "audit_source",
    "packet_slot_object",
    "required_materialization_check",
    "dimension_check",
    "replay_check",
    "firewall_check",
    "receipt_binding_check",
    "audit_failure_reason",
    "audit_decision",
    "payload_materialized",
    "packet_accepted",
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
    "payload_materialized_rows",
    "packet_accepted_rows",
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
    "evidence_payload_materialization_audit_satisfied",
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
        ("manifest_packet_slot", "all_parent_payload_rows", "endpoint-blind manifest payload packet"),
        ("base_field_packet_slot", "base_field_state_payload_candidate", "B_tau state payload packet"),
        ("seed_packet_slot", "morphological_seed_payload_candidate", "seed_tau payload packet"),
        ("operator_packet_slot", "response_operator_payload_candidate", "R_tau response-operator payload packet"),
        ("gauge_normalization_packet_slot", "gauge_normalization_payload_candidate", "gauge/normalization payload packet"),
        ("endpoint_firewall_packet_slot", "endpoint_firewall_payload_candidate", "endpoint-firewall payload packet"),
        ("executable_replay_packet_slot", "provenance_replay_payload_candidate", "executable replay/provenance payload packet"),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPMA01_{index:03d}",
            "packet_component": component,
            "target_payload_component": target,
            "materialization_audit_status": "MATERIALIZATION_AUDIT_FAILED_NO_PAYLOAD_MATERIALIZED",
            "audit_source": "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01",
            "packet_slot_object": slot,
            "required_materialization_check": "payload object must exist with stable id and content hash",
            "dimension_check": "dimension and convention audit must be attached",
            "replay_check": "deterministic replay command and artifact path must be attached",
            "firewall_check": "endpoint-blindness firewall must be attached and passed",
            "receipt_binding_check": "receipt must bind packet object, content hash, replay command, and artifact path",
            "audit_failure_reason": "no materialized payload packet is available for audit",
            "audit_decision": "failed_until_packet_is_materialized_and_receipt_bound",
            "payload_materialized": "false",
            "packet_accepted": "false",
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
        for index, (component, target, slot) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "payload_materialized_rows": sum(row["payload_materialized"] == "true" for row in rows),
            "packet_accepted_rows": sum(row["packet_accepted"] == "true" for row in rows),
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
            "evidence_payload_materialization_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_AUDIT_FAILED_NO_PAYLOAD_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Materialization Audit v01

**Doc class:** parent-input evidence payload materialization audit
**Status:** materialization audit declared but failed because no payload packet is materialized; no packet accepted, no receipt validated, no package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_summary_v01.csv
```

This artifact audits whether declared materialization packet slots have been
materialized into endpoint-blind payload packets. No materialized payload packet is available for audit.

The evidence payload materialization audit is not satisfied:

```text
evidence_payload_materialization_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01
```

## Claim Boundary

This artifact audits materialization packet slots only. It materializes no
parent-side payload, validates no receipt, accepts no receipt, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
