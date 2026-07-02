#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01_package_candidate_only_"
    "no_evidence_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "package_row_id",
    "certificate_component",
    "target_payload_component",
    "package_candidate_status",
    "package_source",
    "package_candidate_content",
    "required_dimension_evidence_slot",
    "required_replay_evidence_slot",
    "required_firewall_evidence_slot",
    "package_acceptance_gate",
    "scorecard_effect",
    "package_candidate_declared",
    "dimension_evidence_slot_declared",
    "replay_evidence_slot_declared",
    "firewall_evidence_slot_declared",
    "evidence_payload_supplied",
    "evidence_package_passed",
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
    "package_rows_declared",
    "package_candidate_rows",
    "dimension_slots_declared",
    "replay_slots_declared",
    "firewall_slots_declared",
    "evidence_payload_supplied_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "hard_failures_triggered",
    "certificate_evidence_package_candidate_satisfied",
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


def package_rows() -> list[dict[str, str]]:
    rows = [
        {
            "certificate_component": "certificate_candidate_manifest_identity",
            "target_payload_component": "all_parent_payload_rows",
            "package_candidate_content": "package manifest candidate with stable row identifiers, artifact slots, and hash slots",
            "required_dimension_evidence_slot": "all physical-row dimension/unit certificate slots",
            "required_replay_evidence_slot": "endpoint-blind replay command and expected input-hash slots",
            "required_firewall_evidence_slot": "aggregate payload-firewall certificate and coverage slots",
            "package_acceptance_gate": "package can be audited only after all seven evidence payload slots are populated",
            "scorecard_effect": "keeps package outside scoring acceptance until evidence payloads are supplied and audited",
        },
        {
            "certificate_component": "base_field_dimension_replay_certificate_candidate",
            "target_payload_component": "base_field_state_payload_candidate",
            "package_candidate_content": "B_tau evidence package candidate with dimension, replay, and firewall slots",
            "required_dimension_evidence_slot": "B_tau dimension/unit certificate slot",
            "required_replay_evidence_slot": "B_tau endpoint-blind replay trace slot",
            "required_firewall_evidence_slot": "B_tau endpoint-firewall trace slot",
            "package_acceptance_gate": "base-field slot can pass only after all evidence payloads are populated and audited",
            "scorecard_effect": "keeps density-amplitude and potential-source scoring inputs blocked",
        },
        {
            "certificate_component": "seed_dimension_replay_certificate_candidate",
            "target_payload_component": "morphological_seed_payload_candidate",
            "package_candidate_content": "seed_tau evidence package candidate with scale, replay, and firewall slots",
            "required_dimension_evidence_slot": "seed_tau scale/normalization certificate slot",
            "required_replay_evidence_slot": "seed_tau endpoint-blind replay trace slot",
            "required_firewall_evidence_slot": "seed_tau endpoint-firewall trace slot",
            "package_acceptance_gate": "seed slot can pass only after all evidence payloads are populated and audited",
            "scorecard_effect": "keeps source-activation and readout-compatibility scoring inputs blocked",
        },
        {
            "certificate_component": "operator_dimension_replay_certificate_candidate",
            "target_payload_component": "response_operator_payload_candidate",
            "package_candidate_content": "R_tau evidence package candidate with dimensional-map, replay, and firewall slots",
            "required_dimension_evidence_slot": "R_tau dimensional-map certificate slot",
            "required_replay_evidence_slot": "R_tau endpoint-blind replay trace slot",
            "required_firewall_evidence_slot": "R_tau endpoint-firewall trace slot",
            "package_acceptance_gate": "operator slot can pass only after all evidence payloads are populated and audited",
            "scorecard_effect": "keeps Phi_tau_eff derivation and transfer-kernel scoring inputs blocked",
        },
        {
            "certificate_component": "gauge_normalization_replay_certificate_candidate",
            "target_payload_component": "gauge_normalization_payload_candidate",
            "package_candidate_content": "gauge/normalization evidence package candidate with lock, replay, and firewall slots",
            "required_dimension_evidence_slot": "gauge/sign/unit/normalization lock certificate slot",
            "required_replay_evidence_slot": "metadata-lock replay trace slot",
            "required_firewall_evidence_slot": "post-endpoint-normalization firewall trace slot",
            "package_acceptance_gate": "normalization slot can pass only after all evidence payloads are populated and audited",
            "scorecard_effect": "keeps acoustic, lensing, and growth comparisons outside scoring acceptance",
        },
        {
            "certificate_component": "payload_firewall_certificate_candidate",
            "target_payload_component": "endpoint_firewall_payload_candidate",
            "package_candidate_content": "aggregate payload-firewall evidence package candidate",
            "required_dimension_evidence_slot": "references to all row-level dimension evidence slots",
            "required_replay_evidence_slot": "references to all row-level replay evidence slots",
            "required_firewall_evidence_slot": "payload-wide firewall certificate slot",
            "package_acceptance_gate": "aggregate firewall slot can pass only after row-level package slots are populated and audited",
            "scorecard_effect": "blocks accepting the full parent-input payload",
        },
        {
            "certificate_component": "executable_replay_certificate_candidate",
            "target_payload_component": "provenance_replay_payload_candidate",
            "package_candidate_content": "executable replay evidence package candidate with provenance hash slots",
            "required_dimension_evidence_slot": "references to physical-row dimension checks used by replay",
            "required_replay_evidence_slot": "endpoint-blind executable replay trace and input provenance hash slots",
            "required_firewall_evidence_slot": "input trace slot for the payload-firewall certificate",
            "package_acceptance_gate": "replay slot can pass only after executable endpoint-blind replay evidence is populated and audited",
            "scorecard_effect": "blocks transition from package candidate to scoring input acceptance",
        },
    ]
    return [
        {
            "package_row_id": f"TCMBPTPICEPC01_{index:03d}",
            "package_candidate_status": "EVIDENCE_PACKAGE_CANDIDATE_DECLARED_UNPOPULATED",
            "package_source": "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01",
            "package_candidate_declared": "true",
            "dimension_evidence_slot_declared": "true",
            "replay_evidence_slot_declared": "true",
            "firewall_evidence_slot_declared": "true",
            "evidence_payload_supplied": "false",
            "evidence_package_passed": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_CANDIDATE_V01",
            "package_rows_declared": len(rows),
            "package_candidate_rows": sum(row["package_candidate_declared"] == "true" for row in rows),
            "dimension_slots_declared": sum(row["dimension_evidence_slot_declared"] == "true" for row in rows),
            "replay_slots_declared": sum(row["replay_evidence_slot_declared"] == "true" for row in rows),
            "firewall_slots_declared": sum(row["firewall_evidence_slot_declared"] == "true" for row in rows),
            "evidence_payload_supplied_rows": sum(row["evidence_payload_supplied"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "certificate_evidence_package_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_UNPOPULATED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Certificate Evidence Package Candidate v01

**Doc class:** parent-input certificate evidence package candidate
**Status:** evidence package slots declared but unpopulated; no evidence package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_summary_v01.csv
```

This artifact turns the evidence request into an evidence-package candidate.
All seven rows declare package slots, but no evidence payload is supplied in this artifact.

The certificate evidence package candidate is not satisfied:

```text
certificate_evidence_package_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01
```

## Claim Boundary

This artifact declares evidence-package slots only. It supplies no dimension,
replay, or firewall evidence payload, provides no evidence-package pass,
provides no certificate pass, accepts no parent-side Tau inputs, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, declares no
reproduction or failure, validates no Tau-response source, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = package_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_CANDIDATE_V01_BUILT")


if __name__ == "__main__":
    main()
