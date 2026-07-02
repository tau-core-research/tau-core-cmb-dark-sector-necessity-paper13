#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01_"
    "audit_only_submission_materialization_request_unfulfilled_no_scoring_input_accepted_no_payload_accepted_"
    "no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "scoring_input_component",
    "request_source",
    "request_audit_status",
    "request_audit_rule",
    "request_audit_finding",
    "required_packet_slot",
    "required_payload_file",
    "required_completion_evidence_file",
    "required_provenance_file",
    "required_replay_command_file",
    "required_hash_manifest_file",
    "required_firewall_attestation_file",
    "endpoint_blind_requirement",
    "known_limit_requirement",
    "dimension_requirement",
    "acceptance_rule",
    "materialization_requested",
    "request_audited",
    "request_audit_passed",
    "packet_materialized",
    "packet_submitted",
    "packet_audit_passed",
    "remediation_completed",
    "acceptance_allowed",
    "payload_accepted",
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
    "payload_submission_materialization_request_audit_rows_declared",
    "materialization_requested_rows",
    "request_audited_rows",
    "request_audit_passed_rows",
    "packet_materialized_rows",
    "packet_submitted_rows",
    "packet_audit_passed_rows",
    "remediation_completed_rows",
    "acceptance_allowed_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_payload_submission_materialization_request_audit_satisfied",
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
        ("manifest_submission_materialization_request_audit", "manifest_remediation_slot", "manifest_payload.csv"),
        ("base_field_submission_materialization_request_audit", "base_field_remediation_slot", "b_tau_state_payload.csv"),
        ("seed_submission_materialization_request_audit", "seed_remediation_slot", "seed_tau_payload.csv"),
        ("operator_submission_materialization_request_audit", "operator_remediation_slot", "r_tau_operator_payload.csv"),
        (
            "gauge_normalization_submission_materialization_request_audit",
            "gauge_normalization_remediation_slot",
            "gauge_normalization_payload.csv",
        ),
        (
            "endpoint_firewall_submission_materialization_request_audit",
            "endpoint_firewall_remediation_slot",
            "endpoint_firewall_payload.csv",
        ),
        (
            "executable_replay_submission_materialization_request_audit",
            "executable_replay_remediation_slot",
            "executable_replay_payload.csv",
        ),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPSIPSMRA01_{index:03d}",
            "scoring_input_component": component,
            "request_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01",
            "request_audit_status": "SUBMISSION_MATERIALIZATION_REQUEST_AUDITED_NOT_FULFILLED",
            "request_audit_rule": (
                "submission materialization request audit may pass only after requested packet, payload, "
                "completion evidence, provenance, replay command, hash manifest, and firewall attestation are supplied"
            ),
            "request_audit_finding": "submission materialization request is declared and audited, but no requested packet is materialized or submitted",
            "required_packet_slot": slot,
            "required_payload_file": payload_file,
            "required_completion_evidence_file": f"{payload_file}.completion.json",
            "required_provenance_file": f"{payload_file}.provenance.json",
            "required_replay_command_file": f"{payload_file}.replay.txt",
            "required_hash_manifest_file": f"{payload_file}.hashes.json",
            "required_firewall_attestation_file": f"{payload_file}.firewall.json",
            "endpoint_blind_requirement": "must be constructed without CMB target leakage or posterior score tuning",
            "known_limit_requirement": "must declare LCDM/GR/Newtonian or null limit compatibility status before scoring",
            "dimension_requirement": "must declare dimensional consistency or explicit dimensionless normalization",
            "acceptance_rule": "may be accepted only after supplied materialization packet passes endpoint-blind audit",
            "materialization_requested": "true",
            "request_audited": "true",
            "request_audit_passed": "false",
            "packet_materialized": "false",
            "packet_submitted": "false",
            "packet_audit_passed": "false",
            "remediation_completed": "false",
            "acceptance_allowed": "false",
            "payload_accepted": "false",
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
        for index, (component, slot, payload_file) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_AUDIT_V01",
            "payload_submission_materialization_request_audit_rows_declared": len(rows),
            "materialization_requested_rows": sum(row["materialization_requested"] == "true" for row in rows),
            "request_audited_rows": sum(row["request_audited"] == "true" for row in rows),
            "request_audit_passed_rows": sum(row["request_audit_passed"] == "true" for row in rows),
            "packet_materialized_rows": sum(row["packet_materialized"] == "true" for row in rows),
            "packet_submitted_rows": sum(row["packet_submitted"] == "true" for row in rows),
            "packet_audit_passed_rows": sum(row["packet_audit_passed"] == "true" for row in rows),
            "remediation_completed_rows": sum(row["remediation_completed"] == "true" for row in rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_payload_submission_materialization_request_audit_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_AUDIT_NOT_FULFILLED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Materialization Request Audit v01

**Doc class:** parent-input evidence payload scoring input payload submission materialization request audit
**Status:** materialization request audited but not fulfilled; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_summary_v01.csv
```

This artifact audits the payload-submission materialization request. The
request exists and is audited, but it is not fulfilled because no requested
packet is materialized or submitted and no completion, provenance, replay,
hash-manifest, or firewall-attestation evidence is supplied.

The evidence payload scoring input payload submission materialization request
audit is not satisfied:

```text
evidence_payload_scoring_input_payload_submission_materialization_request_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01
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
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
