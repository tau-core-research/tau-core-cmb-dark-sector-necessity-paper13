#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01_package_audit_only_"
    "no_evidence_payload_no_evidence_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "certificate_component",
    "target_payload_component",
    "package_audit_status",
    "audited_source",
    "audit_finding",
    "missing_payload",
    "dimension_slot_audit_result",
    "replay_slot_audit_result",
    "firewall_slot_audit_result",
    "package_acceptance_decision",
    "scorecard_effect",
    "package_candidate_audited",
    "evidence_payload_supplied",
    "dimension_payload_supplied",
    "replay_payload_supplied",
    "firewall_payload_supplied",
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
    "audit_rows_declared",
    "package_candidate_audited_rows",
    "package_audit_passed_rows",
    "package_audit_failed_rows",
    "evidence_payload_supplied_rows",
    "dimension_payload_supplied_rows",
    "replay_payload_supplied_rows",
    "firewall_payload_supplied_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "hard_failures_triggered",
    "certificate_evidence_package_audit_satisfied",
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


def audit_rows() -> list[dict[str, str]]:
    rows = [
        {
            "certificate_component": "certificate_candidate_manifest_identity",
            "target_payload_component": "all_parent_payload_rows",
            "audit_finding": "package manifest slots are declared, but no evidence payload or artifact hashes are supplied",
            "missing_payload": "complete package manifest payload with stable artifact hashes",
            "scorecard_effect": "keeps package outside scoring acceptance",
        },
        {
            "certificate_component": "base_field_dimension_replay_certificate_candidate",
            "target_payload_component": "base_field_state_payload_candidate",
            "audit_finding": "B_tau package slots are declared, but dimension, replay, and firewall payloads are absent",
            "missing_payload": "B_tau dimension certificate, endpoint-blind replay trace, and firewall trace payloads",
            "scorecard_effect": "keeps density-amplitude and potential-source scoring inputs blocked",
        },
        {
            "certificate_component": "seed_dimension_replay_certificate_candidate",
            "target_payload_component": "morphological_seed_payload_candidate",
            "audit_finding": "seed_tau package slots are declared, but scale, replay, and firewall payloads are absent",
            "missing_payload": "seed_tau scale certificate, endpoint-blind replay trace, and firewall trace payloads",
            "scorecard_effect": "keeps source-activation and readout-compatibility scoring inputs blocked",
        },
        {
            "certificate_component": "operator_dimension_replay_certificate_candidate",
            "target_payload_component": "response_operator_payload_candidate",
            "audit_finding": "R_tau package slots are declared, but dimensional-map, replay, and firewall payloads are absent",
            "missing_payload": "R_tau dimensional-map certificate, endpoint-blind replay trace, and firewall trace payloads",
            "scorecard_effect": "keeps Phi_tau_eff derivation and transfer-kernel scoring inputs blocked",
        },
        {
            "certificate_component": "gauge_normalization_replay_certificate_candidate",
            "target_payload_component": "gauge_normalization_payload_candidate",
            "audit_finding": "gauge/normalization package slots are declared, but lock, replay, and firewall payloads are absent",
            "missing_payload": "gauge/sign/unit/normalization lock certificate, metadata replay, and firewall trace payloads",
            "scorecard_effect": "keeps acoustic, lensing, and growth comparisons outside scoring acceptance",
        },
        {
            "certificate_component": "payload_firewall_certificate_candidate",
            "target_payload_component": "endpoint_firewall_payload_candidate",
            "audit_finding": "aggregate firewall package slot is declared, but row-level payloads and aggregate firewall payload are absent",
            "missing_payload": "row-level evidence payload references and payload-wide firewall certificate payload",
            "scorecard_effect": "blocks accepting the full parent-input payload",
        },
        {
            "certificate_component": "executable_replay_certificate_candidate",
            "target_payload_component": "provenance_replay_payload_candidate",
            "audit_finding": "executable replay package slot is declared, but executable trace and provenance hashes are absent",
            "missing_payload": "endpoint-blind executable replay trace and input provenance hash payloads",
            "scorecard_effect": "blocks transition from package audit to scoring input acceptance",
        },
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPICEPA01_{index:03d}",
            "package_audit_status": "PACKAGE_AUDIT_FAIL_UNPOPULATED_EVIDENCE_PAYLOAD",
            "audited_source": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01",
            "dimension_slot_audit_result": "slot_declared_payload_missing",
            "replay_slot_audit_result": "slot_declared_payload_missing",
            "firewall_slot_audit_result": "slot_declared_payload_missing",
            "package_acceptance_decision": "reject_package_for_scoring_input_acceptance",
            "package_candidate_audited": "true",
            "evidence_payload_supplied": "false",
            "dimension_payload_supplied": "false",
            "replay_payload_supplied": "false",
            "firewall_payload_supplied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "package_candidate_audited_rows": sum(row["package_candidate_audited"] == "true" for row in rows),
            "package_audit_passed_rows": sum(row["package_audit_status"].startswith("PACKAGE_AUDIT_PASS") for row in rows),
            "package_audit_failed_rows": sum(row["package_audit_status"].startswith("PACKAGE_AUDIT_FAIL") for row in rows),
            "evidence_payload_supplied_rows": sum(row["evidence_payload_supplied"] == "true" for row in rows),
            "dimension_payload_supplied_rows": sum(row["dimension_payload_supplied"] == "true" for row in rows),
            "replay_payload_supplied_rows": sum(row["replay_payload_supplied"] == "true" for row in rows),
            "firewall_payload_supplied_rows": sum(row["firewall_payload_supplied"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "certificate_evidence_package_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_AUDIT_FAILED_UNPOPULATED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Certificate Evidence Package Audit v01

**Doc class:** parent-input certificate evidence package audit
**Status:** evidence package candidate audited and rejected; no evidence payload, no evidence package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_summary_v01.csv
```

This artifact audits the evidence-package candidate. All seven rows fail the
package audit because the evidence slots are declared but no evidence payload is
supplied.

The certificate evidence package audit is not satisfied:

```text
certificate_evidence_package_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01
```

## Claim Boundary

This artifact audits evidence-package slots only. It supplies no dimension,
replay, or firewall evidence payload, provides no evidence-package pass,
provides no certificate pass, accepts no parent-side Tau inputs, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, declares no
reproduction or failure, validates no Tau-response source, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
