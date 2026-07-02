#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01_"
    "request_only_submission_payload_fulfillment_not_supplied_no_scoring_input_accepted_no_payload_accepted_"
    "no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "request_row_id",
    "scoring_input_component",
    "source_audit",
    "fulfillment_request_status",
    "required_payload_file",
    "required_payload_content",
    "required_schema_or_units",
    "required_completion_evidence_file",
    "required_provenance_file",
    "required_replay_command_file",
    "required_hash_manifest_file",
    "required_firewall_attestation_file",
    "endpoint_blind_requirement",
    "known_limit_requirement",
    "dimension_requirement",
    "acceptance_rule",
    "fulfillment_requested",
    "payload_supplied",
    "completion_evidence_supplied",
    "provenance_supplied",
    "replay_supplied",
    "hash_manifest_supplied",
    "firewall_attestation_supplied",
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
    "payload_submission_fulfillment_request_rows_declared",
    "fulfillment_requested_rows",
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
    "evidence_payload_scoring_input_payload_submission_fulfillment_request_satisfied",
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


def request_rows() -> list[dict[str, str]]:
    rows = [
        (
            "manifest_submission_payload_fulfillment_request",
            "manifest_payload.csv",
            "machine-readable row manifest tying every supplied payload file to component, version, source, and hash",
            "csv columns: component_id, version, source_path, sha256, construction_stage, endpoint_blind_flag",
        ),
        (
            "base_field_submission_payload_fulfillment_request",
            "b_tau_state_payload.csv",
            "parent-side base-field state variables needed before any Phi_tau_eff construction",
            "declared units or dimensionless normalization for each state variable",
        ),
        (
            "seed_submission_payload_fulfillment_request",
            "seed_tau_payload.csv",
            "morphological seed descriptors and their admissible support domain",
            "dimensionless seed labels plus support coordinates and normalization convention",
        ),
        (
            "operator_submission_payload_fulfillment_request",
            "r_tau_operator_payload.csv",
            "response-operator entries or kernel parameters used to map parent input toward Phi_tau_eff",
            "operator dimensions, kernel normalization, and sign convention declared per entry",
        ),
        (
            "gauge_normalization_submission_payload_fulfillment_request",
            "gauge_normalization_payload.csv",
            "gauge and normalization choices sufficient to prevent readout-equivalent duplicate scoring",
            "dimensionless gauge labels plus fixed normalization constants",
        ),
        (
            "endpoint_firewall_submission_payload_fulfillment_request",
            "endpoint_firewall_payload.csv",
            "endpoint-blind firewall evidence excluding CMB target leakage and posterior tuning",
            "boolean firewall flags plus source-stage timestamps and forbidden-target checks",
        ),
        (
            "executable_replay_submission_payload_fulfillment_request",
            "executable_replay_payload.csv",
            "deterministic commands and environment pins needed to replay payload construction",
            "command text, environment hash, dependency pins, and output hash targets",
        ),
    ]
    return [
        {
            "request_row_id": f"TCMBPTPIPEPSIPSFR01_{index:03d}",
            "scoring_input_component": component,
            "source_audit": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01",
            "fulfillment_request_status": "SUBMISSION_PAYLOAD_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED",
            "required_payload_file": payload_file,
            "required_payload_content": payload_content,
            "required_schema_or_units": schema_or_units,
            "required_completion_evidence_file": f"{payload_file}.completion.json",
            "required_provenance_file": f"{payload_file}.provenance.json",
            "required_replay_command_file": f"{payload_file}.replay.txt",
            "required_hash_manifest_file": f"{payload_file}.hashes.json",
            "required_firewall_attestation_file": f"{payload_file}.firewall.json",
            "endpoint_blind_requirement": "must be constructed without CMB target leakage or posterior score tuning",
            "known_limit_requirement": "must declare LCDM/GR/Newtonian or null limit compatibility status before scoring",
            "dimension_requirement": "must declare dimensional consistency or explicit dimensionless normalization",
            "acceptance_rule": "may be accepted only after supplied payload, completion evidence, provenance, replay, hash manifest, and firewall attestation pass audit",
            "fulfillment_requested": "true",
            "payload_supplied": "false",
            "completion_evidence_supplied": "false",
            "provenance_supplied": "false",
            "replay_supplied": "false",
            "hash_manifest_supplied": "false",
            "firewall_attestation_supplied": "false",
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
        for index, (component, payload_file, payload_content, schema_or_units) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_V01",
            "payload_submission_fulfillment_request_rows_declared": len(rows),
            "fulfillment_requested_rows": sum(row["fulfillment_requested"] == "true" for row in rows),
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
            "evidence_payload_scoring_input_payload_submission_fulfillment_request_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Fulfillment Request v01

**Doc class:** parent-input evidence payload scoring input payload submission fulfillment request
**Status:** fulfillment request declared but payload not supplied; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_summary_v01.csv
```

This artifact converts the failed payload-submission materialization-packet
audit into a concrete payload fulfillment request. It specifies the seven
required payload slots, minimum content, completion evidence, provenance,
replay, hash-manifest, firewall-attestation, endpoint-blind, known-limit, and
dimensional requirements. It does not supply or accept any payload.

The evidence payload scoring input payload submission fulfillment request is
not satisfied:

```text
evidence_payload_scoring_input_payload_submission_fulfillment_request_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01
```

## Claim Boundary

This artifact is a request only. It accepts no parent-side payload, provides no
evidence-package pass, provides no certificate pass, accepts no scoring input,
derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = request_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
