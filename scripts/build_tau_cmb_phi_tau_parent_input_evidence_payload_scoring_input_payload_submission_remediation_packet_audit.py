#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01_"
    "audit_only_submission_remediation_packet_audit_rejected_not_materialized_no_scoring_input_accepted_"
    "no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "scoring_input_component",
    "packet_source",
    "packet_audit_status",
    "packet_audit_rule",
    "packet_audit_finding",
    "required_packet_slot",
    "required_payload_evidence",
    "required_completion_evidence",
    "required_provenance_evidence",
    "required_replay_evidence",
    "required_hash_evidence",
    "required_firewall_evidence",
    "packet_declared",
    "packet_materialized",
    "packet_submitted",
    "packet_audit_passed",
    "remediation_completed",
    "acceptance_allowed",
    "payload_accepted",
    "scoring_input_audit_passed",
    "scoring_input_accepted",
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
    "payload_submission_remediation_packet_audit_rows_declared",
    "packet_declared_rows",
    "packet_materialized_rows",
    "packet_submitted_rows",
    "packet_audit_passed_rows",
    "remediation_completed_rows",
    "acceptance_allowed_rows",
    "payload_accepted_rows",
    "scoring_input_audit_passed_rows",
    "scoring_input_accepted_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_payload_submission_remediation_packet_audit_satisfied",
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
        ("manifest_submission_remediation_packet_audit", "manifest_remediation_slot", "manifest payload"),
        ("base_field_submission_remediation_packet_audit", "base_field_remediation_slot", "B_tau state payload"),
        ("seed_submission_remediation_packet_audit", "seed_remediation_slot", "seed_tau payload"),
        ("operator_submission_remediation_packet_audit", "operator_remediation_slot", "R_tau operator payload"),
        (
            "gauge_normalization_submission_remediation_packet_audit",
            "gauge_normalization_remediation_slot",
            "gauge-normalization payload",
        ),
        (
            "endpoint_firewall_submission_remediation_packet_audit",
            "endpoint_firewall_remediation_slot",
            "endpoint-firewall payload",
        ),
        ("executable_replay_submission_remediation_packet_audit", "executable_replay_remediation_slot", "replay payload"),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPSIPSRPKA01_{index:03d}",
            "scoring_input_component": component,
            "packet_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01",
            "packet_audit_status": "SUBMISSION_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED",
            "packet_audit_rule": (
                "submission remediation packet audit may pass only after materialized packet, submitted payload, "
                "completion evidence, provenance, replay command, hash manifest, and endpoint-blind firewall attestation"
            ),
            "packet_audit_finding": "remediation packet shell is declared but no packet is materialized or submitted",
            "required_packet_slot": slot,
            "required_payload_evidence": f"accepted {payload} required before scoring input acceptance",
            "required_completion_evidence": "completion evidence file required and must match the declared remediation action",
            "required_provenance_evidence": "provenance file required and must bind the payload to parent-input construction",
            "required_replay_evidence": "deterministic replay command required before acceptance",
            "required_hash_evidence": "stable artifact hash and replay hash required before audit can pass",
            "required_firewall_evidence": "endpoint-blind construction and leakage firewall attestation required",
            "packet_declared": "true",
            "packet_materialized": "false",
            "packet_submitted": "false",
            "packet_audit_passed": "false",
            "remediation_completed": "false",
            "acceptance_allowed": "false",
            "payload_accepted": "false",
            "scoring_input_audit_passed": "false",
            "scoring_input_accepted": "false",
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
        for index, (component, slot, payload) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_AUDIT_V01",
            "payload_submission_remediation_packet_audit_rows_declared": len(rows),
            "packet_declared_rows": sum(row["packet_declared"] == "true" for row in rows),
            "packet_materialized_rows": sum(row["packet_materialized"] == "true" for row in rows),
            "packet_submitted_rows": sum(row["packet_submitted"] == "true" for row in rows),
            "packet_audit_passed_rows": sum(row["packet_audit_passed"] == "true" for row in rows),
            "remediation_completed_rows": sum(row["remediation_completed"] == "true" for row in rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_audit_passed_rows": sum(row["scoring_input_audit_passed"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_payload_submission_remediation_packet_audit_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Remediation Packet Audit v01

**Doc class:** parent-input evidence payload scoring input payload submission remediation packet audit
**Status:** remediation packet audit rejected because packet is not materialized; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_summary_v01.csv
```

This artifact audits the payload-submission remediation packet shell. The audit
rejects every packet slot because no remediation packet is materialized,
submitted, completed, hash-bound, replay-bound, or endpoint-firewall attested.

The evidence payload scoring input payload submission remediation packet audit
is not satisfied:

```text
evidence_payload_scoring_input_payload_submission_remediation_packet_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01
```

## Claim Boundary

This artifact is an audit only. It accepts no parent-side payload, provides no
evidence-package pass, provides no certificate pass, accepts no scoring input,
derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
