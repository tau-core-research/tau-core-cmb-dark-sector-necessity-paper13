#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01_"
    "packet_shell_only_submission_actual_payload_absent_no_scoring_input_accepted_no_payload_accepted_"
    "no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "packet_row_id",
    "scoring_input_component",
    "request_audit_source",
    "packet_status",
    "packet_shell_slot",
    "expected_payload_file",
    "expected_completion_evidence_file",
    "expected_provenance_file",
    "expected_replay_command_file",
    "expected_hash_manifest_file",
    "expected_firewall_attestation_file",
    "endpoint_blind_requirement",
    "known_limit_requirement",
    "dimension_requirement",
    "acceptance_rule",
    "packet_shell_declared",
    "actual_payload_present",
    "actual_completion_evidence_present",
    "actual_provenance_present",
    "actual_replay_command_present",
    "actual_hash_manifest_present",
    "actual_firewall_attestation_present",
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
    "payload_submission_materialization_packet_rows_declared",
    "packet_shell_declared_rows",
    "actual_payload_present_rows",
    "actual_completion_evidence_present_rows",
    "actual_provenance_present_rows",
    "actual_replay_command_present_rows",
    "actual_hash_manifest_present_rows",
    "actual_firewall_attestation_present_rows",
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
    "evidence_payload_scoring_input_payload_submission_materialization_packet_satisfied",
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
        ("manifest_submission_materialization_packet", "manifest_remediation_slot", "manifest_payload.csv"),
        ("base_field_submission_materialization_packet", "base_field_remediation_slot", "b_tau_state_payload.csv"),
        ("seed_submission_materialization_packet", "seed_remediation_slot", "seed_tau_payload.csv"),
        ("operator_submission_materialization_packet", "operator_remediation_slot", "r_tau_operator_payload.csv"),
        (
            "gauge_normalization_submission_materialization_packet",
            "gauge_normalization_remediation_slot",
            "gauge_normalization_payload.csv",
        ),
        ("endpoint_firewall_submission_materialization_packet", "endpoint_firewall_remediation_slot", "endpoint_firewall_payload.csv"),
        ("executable_replay_submission_materialization_packet", "executable_replay_remediation_slot", "executable_replay_payload.csv"),
    ]
    return [
        {
            "packet_row_id": f"TCMBPTPIPEPSIPSMP01_{index:03d}",
            "scoring_input_component": component,
            "request_audit_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01",
            "packet_status": "SUBMISSION_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT",
            "packet_shell_slot": slot,
            "expected_payload_file": payload_file,
            "expected_completion_evidence_file": f"{payload_file}.completion.json",
            "expected_provenance_file": f"{payload_file}.provenance.json",
            "expected_replay_command_file": f"{payload_file}.replay.txt",
            "expected_hash_manifest_file": f"{payload_file}.hashes.json",
            "expected_firewall_attestation_file": f"{payload_file}.firewall.json",
            "endpoint_blind_requirement": "must be constructed without CMB target leakage or posterior score tuning",
            "known_limit_requirement": "must declare LCDM/GR/Newtonian or null limit compatibility status before scoring",
            "dimension_requirement": "must declare dimensional consistency or explicit dimensionless normalization",
            "acceptance_rule": "may be accepted only after actual payload, completion evidence, provenance, replay, hashes, and firewall attestation are supplied and audited",
            "packet_shell_declared": "true",
            "actual_payload_present": "false",
            "actual_completion_evidence_present": "false",
            "actual_provenance_present": "false",
            "actual_replay_command_present": "false",
            "actual_hash_manifest_present": "false",
            "actual_firewall_attestation_present": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_V01",
            "payload_submission_materialization_packet_rows_declared": len(rows),
            "packet_shell_declared_rows": sum(row["packet_shell_declared"] == "true" for row in rows),
            "actual_payload_present_rows": sum(row["actual_payload_present"] == "true" for row in rows),
            "actual_completion_evidence_present_rows": sum(
                row["actual_completion_evidence_present"] == "true" for row in rows
            ),
            "actual_provenance_present_rows": sum(row["actual_provenance_present"] == "true" for row in rows),
            "actual_replay_command_present_rows": sum(row["actual_replay_command_present"] == "true" for row in rows),
            "actual_hash_manifest_present_rows": sum(row["actual_hash_manifest_present"] == "true" for row in rows),
            "actual_firewall_attestation_present_rows": sum(
                row["actual_firewall_attestation_present"] == "true" for row in rows
            ),
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
            "evidence_payload_scoring_input_payload_submission_materialization_packet_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Materialization Packet v01

**Doc class:** parent-input evidence payload scoring input payload submission materialization packet shell
**Status:** materialization packet shell declared but actual payload absent; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_summary_v01.csv
```

This artifact declares the payload-submission materialization packet shell
requested by the materialization-request audit. It names the expected payload,
completion-evidence, provenance, replay, hash-manifest, and
firewall-attestation files for each slot. It does not include actual payloads
and no packet is materialized or submitted.

The evidence payload scoring input payload submission materialization packet is
not satisfied:

```text
evidence_payload_scoring_input_payload_submission_materialization_packet_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01
```

## Claim Boundary

This artifact declares a packet shell only. It accepts no parent-side payload,
provides no evidence-package pass, provides no certificate pass, accepts no
scoring input, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = packet_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
