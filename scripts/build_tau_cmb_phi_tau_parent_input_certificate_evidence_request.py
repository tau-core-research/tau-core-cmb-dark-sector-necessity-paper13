#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01_evidence_request_only_"
    "no_evidence_supplied_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "request_row_id",
    "certificate_component",
    "target_payload_component",
    "request_status",
    "request_source",
    "required_evidence_bundle",
    "dimension_evidence_request",
    "replay_evidence_request",
    "firewall_evidence_request",
    "acceptance_criterion",
    "scorecard_effect",
    "evidence_requested",
    "evidence_supplied",
    "dimension_evidence_supplied",
    "replay_evidence_supplied",
    "firewall_evidence_supplied",
    "certificate_passed",
    "payload_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "request_rows_declared",
    "evidence_requested_rows",
    "evidence_supplied_rows",
    "dimension_evidence_supplied_rows",
    "replay_evidence_supplied_rows",
    "firewall_evidence_supplied_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "hard_failures_triggered",
    "certificate_evidence_request_satisfied",
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


def request_rows() -> list[dict[str, str]]:
    rows = [
        {
            "certificate_component": "certificate_candidate_manifest_identity",
            "target_payload_component": "all_parent_payload_rows",
            "required_evidence_bundle": "complete certificate package manifest with stable row identifiers and artifact hashes",
            "dimension_evidence_request": "map every physical parent-input row to its dimension/unit certificate",
            "replay_evidence_request": "identify the endpoint-blind replay command and expected input hashes",
            "firewall_evidence_request": "identify the aggregate payload-firewall certificate and row coverage",
            "acceptance_criterion": "manifest evidence must cover all seven certificate rows before any payload acceptance",
            "scorecard_effect": "defines the evidence package needed before scoring can inspect parent inputs",
        },
        {
            "certificate_component": "base_field_dimension_replay_certificate_candidate",
            "target_payload_component": "base_field_state_payload_candidate",
            "required_evidence_bundle": "B_tau dimension/unit certificate plus endpoint-blind replay and firewall trace",
            "dimension_evidence_request": "prove B_tau dimensional/unit status before source construction",
            "replay_evidence_request": "replay B_tau candidate construction without score, residual, or likelihood outputs",
            "firewall_evidence_request": "prove no endpoint-derived fields enter B_tau",
            "acceptance_criterion": "base-field row can pass only when all three evidence classes are supplied and audited",
            "scorecard_effect": "keeps density-amplitude and potential-source scoring inputs blocked",
        },
        {
            "certificate_component": "seed_dimension_replay_certificate_candidate",
            "target_payload_component": "morphological_seed_payload_candidate",
            "required_evidence_bundle": "seed_tau scale/normalization certificate plus replay and firewall trace",
            "dimension_evidence_request": "prove seed_tau scale and normalization status before readout comparison",
            "replay_evidence_request": "replay seed_tau candidate construction without endpoint residual shapes",
            "firewall_evidence_request": "prove no CMB peak-shape or residual-derived fields enter seed_tau",
            "acceptance_criterion": "seed row can pass only when all three evidence classes are supplied and audited",
            "scorecard_effect": "keeps source-activation and readout-compatibility scoring inputs blocked",
        },
        {
            "certificate_component": "operator_dimension_replay_certificate_candidate",
            "target_payload_component": "response_operator_payload_candidate",
            "required_evidence_bundle": "R_tau dimensional-map certificate plus replay and firewall trace",
            "dimension_evidence_request": "prove the response-operator dimensional map preserves parent payload dimensions",
            "replay_evidence_request": "replay response-operator inputs without score outputs",
            "firewall_evidence_request": "prove no role-score or residual-tuning fields enter R_tau",
            "acceptance_criterion": "operator row can pass only when all three evidence classes are supplied and audited",
            "scorecard_effect": "keeps Phi_tau_eff derivation and transfer-kernel scoring inputs blocked",
        },
        {
            "certificate_component": "gauge_normalization_replay_certificate_candidate",
            "target_payload_component": "gauge_normalization_payload_candidate",
            "required_evidence_bundle": "gauge/sign/unit/normalization lock certificate plus replay and firewall trace",
            "dimension_evidence_request": "prove gauge, sign, unit, and normalization lock before endpoint comparison",
            "replay_evidence_request": "replay metadata lock before endpoint evaluation",
            "firewall_evidence_request": "prove no post-endpoint normalization choice enters metadata",
            "acceptance_criterion": "normalization row can pass only when all three evidence classes are supplied and audited",
            "scorecard_effect": "keeps acoustic, lensing, and growth comparisons outside scoring acceptance",
        },
        {
            "certificate_component": "payload_firewall_certificate_candidate",
            "target_payload_component": "endpoint_firewall_payload_candidate",
            "required_evidence_bundle": "aggregate payload-firewall certificate covering every parent-input row",
            "dimension_evidence_request": "reference all physical-row dimension certificates",
            "replay_evidence_request": "reference replay trace used to rebuild the payload candidate",
            "firewall_evidence_request": "certify every payload row against score, residual, and likelihood-derived inputs",
            "acceptance_criterion": "payload firewall can pass only after row-level certificates are supplied and audited",
            "scorecard_effect": "blocks accepting the full parent-input payload",
        },
        {
            "certificate_component": "executable_replay_certificate_candidate",
            "target_payload_component": "provenance_replay_payload_candidate",
            "required_evidence_bundle": "endpoint-blind executable replay certificate with input provenance hashes",
            "dimension_evidence_request": "reference all physical-row dimension checks used by replay",
            "replay_evidence_request": "execute without reading score outputs, residual tables, or likelihood errors",
            "firewall_evidence_request": "provide the input trace used by the payload-firewall certificate",
            "acceptance_criterion": "replay certificate can pass only when the replay is executable and endpoint-blind",
            "scorecard_effect": "blocks transition from evidence request into scoring input acceptance",
        },
    ]
    return [
        {
            "request_row_id": f"TCMBPTPICER01_{index:03d}",
            "request_status": "EVIDENCE_REQUESTED_NOT_SUPPLIED",
            "request_source": "tau_cmb_phi_tau_parent_input_certificate_audit_v01",
            "evidence_requested": "true",
            "evidence_supplied": "false",
            "dimension_evidence_supplied": "false",
            "replay_evidence_supplied": "false",
            "firewall_evidence_supplied": "false",
            "certificate_passed": "false",
            "payload_accepted": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_REQUEST_V01",
            "request_rows_declared": len(rows),
            "evidence_requested_rows": sum(row["evidence_requested"] == "true" for row in rows),
            "evidence_supplied_rows": sum(row["evidence_supplied"] == "true" for row in rows),
            "dimension_evidence_supplied_rows": sum(row["dimension_evidence_supplied"] == "true" for row in rows),
            "replay_evidence_supplied_rows": sum(row["replay_evidence_supplied"] == "true" for row in rows),
            "firewall_evidence_supplied_rows": sum(row["firewall_evidence_supplied"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "certificate_evidence_request_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_REQUESTED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Certificate Evidence Request v01

**Doc class:** parent-input certificate evidence request
**Status:** evidence requirements declared but not supplied; no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_evidence_request.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_summary_v01.csv
```

This artifact converts the failed certificate audit into a concrete evidence
request. All seven rows request evidence, but no evidence is supplied in this
artifact.

The certificate evidence request is not satisfied:

```text
certificate_evidence_request_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01
```

## Claim Boundary

This artifact requests certificate evidence only. It supplies no dimension,
replay, or firewall evidence, provides no certificate pass, accepts no
parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score, supplies no
CMB likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = request_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_certificate_evidence_request_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_REQUEST_V01_BUILT")


if __name__ == "__main__":
    main()
