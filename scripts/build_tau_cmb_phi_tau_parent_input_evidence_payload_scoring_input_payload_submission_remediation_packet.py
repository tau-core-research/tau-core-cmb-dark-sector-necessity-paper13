#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01_packet_shell_only_"
    "submission_remediation_packet_not_materialized_no_scoring_input_accepted_no_payload_accepted_no_package_pass_"
    "no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "packet_row_id",
    "scoring_input_component",
    "source_plan",
    "remediation_packet_status",
    "remediation_packet_slot",
    "required_payload_file",
    "required_remediation_action",
    "required_completion_evidence",
    "expected_completion_evidence_file",
    "expected_provenance_file",
    "expected_replay_command_file",
    "expected_hash_manifest_file",
    "expected_firewall_attestation_file",
    "endpoint_blind_requirement",
    "known_limit_requirement",
    "dimension_requirement",
    "acceptance_rule",
    "remediation_packet_declared",
    "remediation_packet_materialized",
    "remediation_completed",
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
    "payload_submission_remediation_packet_rows_declared",
    "remediation_packet_declared_rows",
    "remediation_packet_materialized_rows",
    "remediation_completed_rows",
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
    "evidence_payload_scoring_input_payload_submission_remediation_packet_satisfied",
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
        (
            "manifest_submission_remediation_packet",
            "manifest_remediation_slot",
            "manifest_payload.csv",
            "submit manifest payload plus provenance/hash/replay/firewall evidence",
            "manifest file exists, hashes match, endpoint-blind flag is declared",
        ),
        (
            "base_field_submission_remediation_packet",
            "base_field_remediation_slot",
            "b_tau_state_payload.csv",
            "submit base-field state payload with declared units or dimensionless normalization",
            "state payload exists, dimensional declarations are complete, provenance is attached",
        ),
        (
            "seed_submission_remediation_packet",
            "seed_remediation_slot",
            "seed_tau_payload.csv",
            "submit morphological seed payload with support and normalization metadata",
            "seed payload exists, support domain is declared, replay command is attached",
        ),
        (
            "operator_submission_remediation_packet",
            "operator_remediation_slot",
            "r_tau_operator_payload.csv",
            "submit response-operator payload with kernel dimensions and sign convention",
            "operator payload exists, kernel convention is declared, hash manifest is attached",
        ),
        (
            "gauge_normalization_submission_remediation_packet",
            "gauge_normalization_remediation_slot",
            "gauge_normalization_payload.csv",
            "submit gauge-normalization payload preventing readout-equivalent duplicate scoring",
            "gauge payload exists, normalization constants are fixed, equivalence rule is declared",
        ),
        (
            "endpoint_firewall_submission_remediation_packet",
            "endpoint_firewall_remediation_slot",
            "endpoint_firewall_payload.csv",
            "submit endpoint-blind firewall evidence excluding CMB target leakage and posterior tuning",
            "firewall payload exists, forbidden-target checks pass, attestation is attached",
        ),
        (
            "executable_replay_submission_remediation_packet",
            "executable_replay_remediation_slot",
            "executable_replay_payload.csv",
            "submit deterministic replay payload with environment pins and output hash targets",
            "replay payload exists, command is deterministic, environment hash is attached",
        ),
    ]
    return [
        {
            "packet_row_id": f"TCMBPTPIPEPSIPSRPK01_{index:03d}",
            "scoring_input_component": component,
            "source_plan": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01",
            "remediation_packet_status": "SUBMISSION_REMEDIATION_PACKET_SHELL_DECLARED_NOT_MATERIALIZED",
            "remediation_packet_slot": slot,
            "required_payload_file": payload_file,
            "required_remediation_action": action,
            "required_completion_evidence": evidence,
            "expected_completion_evidence_file": f"{payload_file}.completion.json",
            "expected_provenance_file": f"{payload_file}.provenance.json",
            "expected_replay_command_file": f"{payload_file}.replay.txt",
            "expected_hash_manifest_file": f"{payload_file}.hashes.json",
            "expected_firewall_attestation_file": f"{payload_file}.firewall.json",
            "endpoint_blind_requirement": "must be constructed without CMB target leakage or posterior score tuning",
            "known_limit_requirement": "must declare LCDM/GR/Newtonian or null limit compatibility status before scoring",
            "dimension_requirement": "must declare dimensional consistency or explicit dimensionless normalization",
            "acceptance_rule": "may be accepted only after remediation packet is materialized and a submitted packet passes audit",
            "remediation_packet_declared": "true",
            "remediation_packet_materialized": "false",
            "remediation_completed": "false",
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
        for index, (component, slot, payload_file, action, evidence) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_V01",
            "payload_submission_remediation_packet_rows_declared": len(rows),
            "remediation_packet_declared_rows": sum(row["remediation_packet_declared"] == "true" for row in rows),
            "remediation_packet_materialized_rows": sum(
                row["remediation_packet_materialized"] == "true" for row in rows
            ),
            "remediation_completed_rows": sum(row["remediation_completed"] == "true" for row in rows),
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
            "evidence_payload_scoring_input_payload_submission_remediation_packet_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_SHELL_DECLARED_NOT_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Remediation Packet v01

**Doc class:** parent-input evidence payload scoring input payload submission remediation packet shell
**Status:** remediation packet shell declared but not materialized; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_summary_v01.csv
```

This artifact converts the submission remediation plan into a remediation
packet shell. It declares remediation slots and expected completion,
provenance, replay, hash-manifest, and firewall-attestation files. It does not
materialize the packet, complete remediation, submit payload, or accept scoring
input.

The evidence payload scoring input payload submission remediation packet is
not satisfied:

```text
evidence_payload_scoring_input_payload_submission_remediation_packet_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01
```

## Claim Boundary

This artifact is a packet shell only. It accepts no parent-side payload,
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
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
