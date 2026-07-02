#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01_populated_audit_only_"
    "no_evidence_payload_supplied_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "certificate_component",
    "target_payload_component",
    "populated_audit_status",
    "audited_source",
    "audit_finding",
    "missing_payload_record",
    "endpoint_blindness_audit_result",
    "payload_population_audit_result",
    "package_acceptance_decision",
    "scorecard_effect",
    "populated_candidate_audited",
    "payload_record_declared",
    "evidence_payload_supplied",
    "dimension_payload_supplied",
    "replay_payload_supplied",
    "firewall_payload_supplied",
    "evidence_package_passed",
    "certificate_passed",
    "payload_accepted",
    "scoring_input_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "audit_rows_declared",
    "populated_candidate_audited_rows",
    "payload_record_declared_rows",
    "populated_audit_passed_rows",
    "populated_audit_failed_rows",
    "evidence_payload_supplied_rows",
    "dimension_payload_supplied_rows",
    "replay_payload_supplied_rows",
    "firewall_payload_supplied_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "scoring_input_accepted_rows",
    "hard_failures_triggered",
    "populated_evidence_package_audit_satisfied",
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
        ("certificate_candidate_manifest_identity", "all_parent_payload_rows", "manifest payload with artifact hashes and coverage map"),
        ("base_field_dimension_replay_certificate_candidate", "base_field_state_payload_candidate", "B_tau dimension certificate, replay trace, and firewall payload"),
        ("seed_dimension_replay_certificate_candidate", "morphological_seed_payload_candidate", "seed_tau scale certificate, replay trace, and firewall payload"),
        ("operator_dimension_replay_certificate_candidate", "response_operator_payload_candidate", "R_tau dimensional-map certificate, replay trace, and firewall payload"),
        ("gauge_normalization_replay_certificate_candidate", "gauge_normalization_payload_candidate", "gauge/sign/unit/normalization certificate, replay trace, and firewall payload"),
        ("payload_firewall_certificate_candidate", "endpoint_firewall_payload_candidate", "aggregate payload-firewall certificate payload"),
        ("executable_replay_certificate_candidate", "provenance_replay_payload_candidate", "endpoint-blind executable replay trace and provenance hashes"),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPA01_{index:03d}",
            "certificate_component": component,
            "target_payload_component": target,
            "populated_audit_status": "POPULATED_EVIDENCE_PACKAGE_AUDIT_FAIL_PAYLOAD_NOT_SUPPLIED",
            "audited_source": "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01",
            "audit_finding": "required payload record is declared but not supplied",
            "missing_payload_record": payload,
            "endpoint_blindness_audit_result": "not_auditable_without_payload",
            "payload_population_audit_result": "fail_payload_not_supplied",
            "package_acceptance_decision": "reject_populated_package_for_scoring_input_acceptance",
            "scorecard_effect": "keeps parent-side scoring acceptance blocked",
            "populated_candidate_audited": "true",
            "payload_record_declared": "true",
            "evidence_payload_supplied": "false",
            "dimension_payload_supplied": "false",
            "replay_payload_supplied": "false",
            "firewall_payload_supplied": "false",
            "evidence_package_passed": "false",
            "certificate_passed": "false",
            "payload_accepted": "false",
            "scoring_input_accepted": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (component, target, payload) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "populated_candidate_audited_rows": sum(row["populated_candidate_audited"] == "true" for row in rows),
            "payload_record_declared_rows": sum(row["payload_record_declared"] == "true" for row in rows),
            "populated_audit_passed_rows": sum(row["populated_audit_status"].startswith("POPULATED_EVIDENCE_PACKAGE_AUDIT_PASS") for row in rows),
            "populated_audit_failed_rows": sum(row["populated_audit_status"].startswith("POPULATED_EVIDENCE_PACKAGE_AUDIT_FAIL") for row in rows),
            "evidence_payload_supplied_rows": sum(row["evidence_payload_supplied"] == "true" for row in rows),
            "dimension_payload_supplied_rows": sum(row["dimension_payload_supplied"] == "true" for row in rows),
            "replay_payload_supplied_rows": sum(row["replay_payload_supplied"] == "true" for row in rows),
            "firewall_payload_supplied_rows": sum(row["firewall_payload_supplied"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "populated_evidence_package_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_AUDIT_FAILED_PAYLOAD_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Populated Evidence Package Audit v01

**Doc class:** parent-input populated evidence package audit
**Status:** populated-package candidate audited and rejected; no evidence payload, no package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_populated_evidence_package_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_summary_v01.csv
```

This artifact audits the populated evidence package candidate. All seven rows
fail because the required payload records are declared but not supplied.

The populated evidence package audit is not satisfied:

```text
populated_evidence_package_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01
```

## Claim Boundary

This artifact audits required populated-package payload records only. It
supplies no dimension, replay, or firewall evidence payload, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
