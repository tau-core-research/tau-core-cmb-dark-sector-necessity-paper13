#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01_"
    "execution_packet_declared_blocked_payload_not_supplied_no_scoring_input_accepted_no_payload_accepted_"
    "no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "execution_row_id",
    "scoring_input_component",
    "source_audit",
    "execution_packet_status",
    "required_payload_file",
    "required_completion_evidence_file",
    "required_provenance_file",
    "required_replay_command_file",
    "required_hash_manifest_file",
    "required_firewall_attestation_file",
    "execution_command_template",
    "execution_prerequisite_rule",
    "fulfillment_requested",
    "request_audited",
    "request_audit_passed",
    "payload_supplied",
    "completion_evidence_supplied",
    "provenance_supplied",
    "replay_supplied",
    "hash_manifest_supplied",
    "firewall_attestation_supplied",
    "payload_accepted",
    "scoring_input_accepted",
    "execution_packet_declared",
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
    "payload_submission_execution_packet_rows_declared",
    "execution_packet_declared_rows",
    "can_execute_rows",
    "execution_attempted_rows",
    "execution_succeeded_rows",
    "payload_supplied_rows",
    "completion_evidence_supplied_rows",
    "provenance_supplied_rows",
    "replay_supplied_rows",
    "hash_manifest_supplied_rows",
    "firewall_attestation_supplied_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_payload_submission_execution_packet_satisfied",
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


def execution_rows() -> list[dict[str, str]]:
    rows = [
        ("manifest_submission_execution_packet", "manifest_payload.csv"),
        ("base_field_submission_execution_packet", "b_tau_state_payload.csv"),
        ("seed_submission_execution_packet", "seed_tau_payload.csv"),
        ("operator_submission_execution_packet", "r_tau_operator_payload.csv"),
        ("gauge_normalization_submission_execution_packet", "gauge_normalization_payload.csv"),
        ("endpoint_firewall_submission_execution_packet", "endpoint_firewall_payload.csv"),
        ("executable_replay_submission_execution_packet", "executable_replay_payload.csv"),
    ]
    return [
        {
            "execution_row_id": f"TCMBPTPIPEPSIPSEP01_{index:03d}",
            "scoring_input_component": component,
            "source_audit": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01",
            "execution_packet_status": "SUBMISSION_EXECUTION_PACKET_DECLARED_BLOCKED_PAYLOAD_NOT_SUPPLIED",
            "required_payload_file": payload_file,
            "required_completion_evidence_file": f"{payload_file}.completion.json",
            "required_provenance_file": f"{payload_file}.provenance.json",
            "required_replay_command_file": f"{payload_file}.replay.txt",
            "required_hash_manifest_file": f"{payload_file}.hashes.json",
            "required_firewall_attestation_file": f"{payload_file}.firewall.json",
            "execution_command_template": f"BLOCKED_UNTIL_PAYLOAD_ACCEPTED component={component} payload={payload_file}",
            "execution_prerequisite_rule": "may execute only after payload, completion evidence, provenance, replay, hash manifest, firewall attestation, payload acceptance, and scoring-input acceptance are all true",
            "fulfillment_requested": "true",
            "request_audited": "true",
            "request_audit_passed": "false",
            "payload_supplied": "false",
            "completion_evidence_supplied": "false",
            "provenance_supplied": "false",
            "replay_supplied": "false",
            "hash_manifest_supplied": "false",
            "firewall_attestation_supplied": "false",
            "payload_accepted": "false",
            "scoring_input_accepted": "false",
            "execution_packet_declared": "true",
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
        for index, (component, payload_file) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_V01",
            "payload_submission_execution_packet_rows_declared": len(rows),
            "execution_packet_declared_rows": sum(row["execution_packet_declared"] == "true" for row in rows),
            "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
            "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
            "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
            "payload_supplied_rows": sum(row["payload_supplied"] == "true" for row in rows),
            "completion_evidence_supplied_rows": sum(
                row["completion_evidence_supplied"] == "true" for row in rows
            ),
            "provenance_supplied_rows": sum(row["provenance_supplied"] == "true" for row in rows),
            "replay_supplied_rows": sum(row["replay_supplied"] == "true" for row in rows),
            "hash_manifest_supplied_rows": sum(row["hash_manifest_supplied"] == "true" for row in rows),
            "firewall_attestation_supplied_rows": sum(row["firewall_attestation_supplied"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_payload_submission_execution_packet_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_DECLARED_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Execution Packet v01

**Doc class:** parent-input evidence payload scoring input payload submission execution packet
**Status:** execution packet declared but blocked; no payload supplied, no payload accepted, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_summary_v01.csv
```

This artifact declares the execution packet that would be needed after a
successful payload submission. It does not run the packet because the required
payload, completion evidence, provenance, replay, hash-manifest, firewall
attestation, payload acceptance, and scoring-input acceptance are absent.

The evidence payload scoring input payload submission execution packet is not
satisfied:

```text
evidence_payload_scoring_input_payload_submission_execution_packet_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01
```

## Claim Boundary

This artifact is an execution-packet scaffold only. It executes nothing,
accepts no parent-side payload, provides no evidence-package pass, provides no
certificate pass, accepts no scoring input, derives no `Phi_tau_eff`, computes
no score, supplies no CMB likelihood, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = execution_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
