#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01_audit_only_"
    "submission_packet_audited_payload_not_submitted_no_scoring_input_accepted_no_payload_accepted_"
    "no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "scoring_input_component",
    "packet_source",
    "submission_packet_audit_status",
    "submission_packet_audit_rule",
    "submission_packet_audit_finding",
    "submission_packet_slot",
    "required_payload_file",
    "required_payload_content",
    "required_schema_or_units",
    "required_provenance_file",
    "required_replay_command_file",
    "required_hash_manifest_file",
    "required_firewall_attestation_file",
    "endpoint_blind_requirement",
    "known_limit_requirement",
    "dimension_requirement",
    "acceptance_rule",
    "submission_packet_declared",
    "submission_packet_audited",
    "submission_packet_audit_passed",
    "payload_submitted",
    "provenance_submitted",
    "replay_submitted",
    "hash_manifest_submitted",
    "firewall_attestation_submitted",
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
    "payload_submission_packet_audit_rows_declared",
    "submission_packet_declared_rows",
    "submission_packet_audited_rows",
    "submission_packet_audit_passed_rows",
    "payload_submitted_rows",
    "provenance_submitted_rows",
    "replay_submitted_rows",
    "hash_manifest_submitted_rows",
    "firewall_attestation_submitted_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_payload_submission_packet_audit_satisfied",
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
            "manifest_payload_submission_packet_audit",
            "manifest_submission_slot",
            "manifest_payload.csv",
            "machine-readable row manifest tying every supplied payload file to component, version, source, and hash",
            "csv columns: component_id, version, source_path, sha256, construction_stage, endpoint_blind_flag",
        ),
        (
            "base_field_payload_submission_packet_audit",
            "base_field_submission_slot",
            "b_tau_state_payload.csv",
            "parent-side base-field state variables needed before any Phi_tau_eff construction",
            "declared units or dimensionless normalization for each state variable",
        ),
        (
            "seed_payload_submission_packet_audit",
            "seed_submission_slot",
            "seed_tau_payload.csv",
            "morphological seed descriptors and their admissible support domain",
            "dimensionless seed labels plus support coordinates and normalization convention",
        ),
        (
            "operator_payload_submission_packet_audit",
            "operator_submission_slot",
            "r_tau_operator_payload.csv",
            "response-operator entries or kernel parameters used to map parent input toward Phi_tau_eff",
            "operator dimensions, kernel normalization, and sign convention declared per entry",
        ),
        (
            "gauge_normalization_payload_submission_packet_audit",
            "gauge_normalization_submission_slot",
            "gauge_normalization_payload.csv",
            "gauge and normalization choices sufficient to prevent readout-equivalent duplicate scoring",
            "dimensionless gauge labels plus fixed normalization constants",
        ),
        (
            "endpoint_firewall_payload_submission_packet_audit",
            "endpoint_firewall_submission_slot",
            "endpoint_firewall_payload.csv",
            "endpoint-blind firewall evidence excluding CMB target leakage and posterior tuning",
            "boolean firewall flags plus source-stage timestamps and forbidden-target checks",
        ),
        (
            "executable_replay_payload_submission_packet_audit",
            "executable_replay_submission_slot",
            "executable_replay_payload.csv",
            "deterministic commands and environment pins needed to replay payload construction",
            "command text, environment hash, dependency pins, and output hash targets",
        ),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPSIPSPA01_{index:03d}",
            "scoring_input_component": component,
            "packet_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01",
            "submission_packet_audit_status": "PAYLOAD_SUBMISSION_PACKET_AUDITED_NOT_SUBMITTED",
            "submission_packet_audit_rule": "submission packet audit may pass only after payload, provenance, replay, hash manifest, and firewall attestation are submitted",
            "submission_packet_audit_finding": "submission packet shell is declared and audited, but no required payload evidence is submitted",
            "submission_packet_slot": slot,
            "required_payload_file": payload_file,
            "required_payload_content": payload_content,
            "required_schema_or_units": schema_or_units,
            "required_provenance_file": f"{payload_file}.provenance.json",
            "required_replay_command_file": f"{payload_file}.replay.txt",
            "required_hash_manifest_file": f"{payload_file}.hashes.json",
            "required_firewall_attestation_file": f"{payload_file}.firewall.json",
            "endpoint_blind_requirement": "must be constructed without CMB target leakage or posterior score tuning",
            "known_limit_requirement": "must declare LCDM/GR/Newtonian or null limit compatibility status before scoring",
            "dimension_requirement": "must declare dimensional consistency or explicit dimensionless normalization",
            "acceptance_rule": "may be accepted only after submitted payload, provenance, replay, hash manifest, and firewall attestation pass audit",
            "submission_packet_declared": "true",
            "submission_packet_audited": "true",
            "submission_packet_audit_passed": "false",
            "payload_submitted": "false",
            "provenance_submitted": "false",
            "replay_submitted": "false",
            "hash_manifest_submitted": "false",
            "firewall_attestation_submitted": "false",
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
        for index, (component, slot, payload_file, payload_content, schema_or_units) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_AUDIT_V01",
            "payload_submission_packet_audit_rows_declared": len(rows),
            "submission_packet_declared_rows": sum(row["submission_packet_declared"] == "true" for row in rows),
            "submission_packet_audited_rows": sum(row["submission_packet_audited"] == "true" for row in rows),
            "submission_packet_audit_passed_rows": sum(row["submission_packet_audit_passed"] == "true" for row in rows),
            "payload_submitted_rows": sum(row["payload_submitted"] == "true" for row in rows),
            "provenance_submitted_rows": sum(row["provenance_submitted"] == "true" for row in rows),
            "replay_submitted_rows": sum(row["replay_submitted"] == "true" for row in rows),
            "hash_manifest_submitted_rows": sum(row["hash_manifest_submitted"] == "true" for row in rows),
            "firewall_attestation_submitted_rows": sum(
                row["firewall_attestation_submitted"] == "true" for row in rows
            ),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_payload_submission_packet_audit_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_AUDITED_NOT_SUBMITTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Packet Audit v01

**Doc class:** parent-input evidence payload scoring input payload submission packet audit
**Status:** submission packet audited but payload not submitted; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_summary_v01.csv
```

This artifact audits the payload submission packet shell. The shell is
declared and audited, but no required payload, provenance, replay,
hash-manifest, or firewall-attestation evidence is submitted.

The evidence payload scoring input payload submission packet audit is not
satisfied:

```text
evidence_payload_scoring_input_payload_submission_packet_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01
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
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
