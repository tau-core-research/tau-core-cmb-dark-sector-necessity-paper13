#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01_"
    "audit_only_evidence_object_request_audited_not_supplied_no_execution_allowed_no_scoring_input_accepted_"
    "no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "evidence_object",
    "blocked_gate",
    "request_source",
    "request_audit_status",
    "request_audit_rule",
    "request_audit_finding",
    "required_evidence_file",
    "required_evidence_content",
    "required_schema_or_units",
    "required_acceptance_check",
    "required_firewall_check",
    "required_replay_check",
    "required_hash_check",
    "evidence_requested",
    "request_audited",
    "request_audit_passed",
    "evidence_supplied",
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
    "evidence_object_request_audit_rows_declared",
    "evidence_requested_rows",
    "request_audited_rows",
    "request_audit_passed_rows",
    "evidence_supplied_rows",
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
    "evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_satisfied",
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
        (
            "submission_payload_bundle_request_audit",
            "payload_supply_gate",
            "submission_payload_bundle.csv",
            "all seven requested payload files bound to component ids and stable paths",
            "csv columns: component_id, payload_file, source_path, construction_stage, endpoint_blind_flag",
        ),
        (
            "completion_evidence_bundle_request_audit",
            "completion_evidence_gate",
            "completion_evidence_bundle.json",
            "per-payload evidence that each requested slot is populated and complete",
            "json object keyed by component_id with completed=true and completion_timestamp",
        ),
        (
            "provenance_bundle_request_audit",
            "provenance_gate",
            "provenance_bundle.json",
            "source paths, construction stage, timestamps, authorship, and hash provenance",
            "json object keyed by component_id with source_path, created_at, stage, sha256",
        ),
        (
            "replay_bundle_request_audit",
            "replay_gate",
            "replay_bundle.txt",
            "deterministic replay commands and environment pins for each payload construction",
            "line-oriented command manifest with component_id, command, environment_hash",
        ),
        (
            "hash_manifest_bundle_request_audit",
            "hash_manifest_gate",
            "hash_manifest_bundle.json",
            "row-level and file-level hashes for every submitted payload and evidence file",
            "json object keyed by artifact path with sha256 and byte size",
        ),
        (
            "endpoint_firewall_bundle_request_audit",
            "endpoint_firewall_gate",
            "endpoint_firewall_bundle.json",
            "endpoint-blind firewall attestation excluding CMB target leakage and posterior tuning",
            "json object keyed by component_id with endpoint_blind=true and forbidden_target_check=pass",
        ),
        (
            "acceptance_record_bundle_request_audit",
            "payload_and_scoring_input_acceptance_gate",
            "acceptance_record_bundle.json",
            "payload acceptance and scoring-input acceptance record after all upstream evidence passes",
            "json object with payload_accepted, scoring_input_accepted, accepted_by, accepted_at",
        ),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPSIPSEORA01_{index:03d}",
            "evidence_object": evidence_object,
            "blocked_gate": gate,
            "request_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01",
            "request_audit_status": "EVIDENCE_OBJECT_REQUEST_AUDITED_NOT_SUPPLIED",
            "request_audit_rule": "request audit may pass only after every requested evidence object is supplied, replayable, hash-bound, endpoint-blind, and acceptance-checkable",
            "request_audit_finding": "evidence object request is declared and audited, but no requested evidence object is supplied",
            "required_evidence_file": filename,
            "required_evidence_content": content,
            "required_schema_or_units": schema,
            "required_acceptance_check": "must pass audit before payload or scoring-input acceptance can be true",
            "required_firewall_check": "must exclude endpoint target leakage and posterior score tuning",
            "required_replay_check": "must provide deterministic replay or an explicit non-executable blocker",
            "required_hash_check": "must bind every supplied evidence object to a stable sha256 hash",
            "evidence_requested": "true",
            "request_audited": "true",
            "request_audit_passed": "false",
            "evidence_supplied": "false",
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
        for index, (evidence_object, gate, filename, content, schema) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_AUDIT_V01",
            "evidence_object_request_audit_rows_declared": len(rows),
            "evidence_requested_rows": sum(row["evidence_requested"] == "true" for row in rows),
            "request_audited_rows": sum(row["request_audited"] == "true" for row in rows),
            "request_audit_passed_rows": sum(row["request_audit_passed"] == "true" for row in rows),
            "evidence_supplied_rows": sum(row["evidence_supplied"] == "true" for row in rows),
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
            "evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_AUDITED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Request Audit v01

**Doc class:** parent-input evidence payload scoring input payload submission evidence object request audit
**Status:** evidence object request audited but not supplied; no execution allowed, no payload accepted, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_summary_v01.csv
```

This artifact audits the concrete evidence object request. The seven evidence
objects are requested and audited as requirements, but none is supplied,
audited as evidence, or accepted.

The evidence payload scoring input payload submission evidence object request
audit is not satisfied:

```text
evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01
```

## Claim Boundary

This artifact is an audit only. It executes nothing, accepts no parent-side
payload, provides no evidence-package pass, provides no certificate pass,
accepts no scoring input, derives no `Phi_tau_eff`, computes no score, supplies
no CMB likelihood, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
