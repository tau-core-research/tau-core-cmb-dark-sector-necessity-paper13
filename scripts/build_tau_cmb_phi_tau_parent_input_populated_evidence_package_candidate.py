#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01_populated_candidate_only_"
    "no_evidence_payload_supplied_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "candidate_row_id",
    "certificate_component",
    "target_payload_component",
    "populated_candidate_status",
    "candidate_source",
    "required_payload_record",
    "payload_population_rule",
    "endpoint_blindness_rule",
    "acceptance_gate",
    "scorecard_effect",
    "populated_candidate_declared",
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
    "candidate_rows_declared",
    "populated_candidate_declared_rows",
    "payload_record_declared_rows",
    "evidence_payload_supplied_rows",
    "dimension_payload_supplied_rows",
    "replay_payload_supplied_rows",
    "firewall_payload_supplied_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "scoring_input_accepted_rows",
    "hard_failures_triggered",
    "populated_evidence_package_candidate_satisfied",
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


def candidate_rows() -> list[dict[str, str]]:
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
            "candidate_row_id": f"TCMBPTPIPEPC01_{index:03d}",
            "certificate_component": component,
            "target_payload_component": target,
            "populated_candidate_status": "POPULATED_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_NOT_SUPPLIED",
            "candidate_source": "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01",
            "required_payload_record": payload,
            "payload_population_rule": "payload must be supplied as endpoint-blind evidence, not inferred from CMB scores or residuals",
            "endpoint_blindness_rule": "payload cannot read score outputs, residual tables, likelihood errors, or post-endpoint tuning fields",
            "acceptance_gate": "candidate cannot pass until payload is supplied and audited",
            "scorecard_effect": "keeps parent-side scoring acceptance blocked",
            "populated_candidate_declared": "true",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_CANDIDATE_V01",
            "candidate_rows_declared": len(rows),
            "populated_candidate_declared_rows": sum(row["populated_candidate_declared"] == "true" for row in rows),
            "payload_record_declared_rows": sum(row["payload_record_declared"] == "true" for row in rows),
            "evidence_payload_supplied_rows": sum(row["evidence_payload_supplied"] == "true" for row in rows),
            "dimension_payload_supplied_rows": sum(row["dimension_payload_supplied"] == "true" for row in rows),
            "replay_payload_supplied_rows": sum(row["replay_payload_supplied"] == "true" for row in rows),
            "firewall_payload_supplied_rows": sum(row["firewall_payload_supplied"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "populated_evidence_package_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Populated Evidence Package Candidate v01

**Doc class:** parent-input populated evidence package candidate
**Status:** populated-package payload records declared but not supplied; no evidence payload, no package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_summary_v01.csv
```

This artifact declares the payload records required for a populated evidence
package. It does not supply those payloads.

The populated evidence package candidate is not satisfied:

```text
populated_evidence_package_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01
```

## Claim Boundary

This artifact declares required populated-package payload records only. It
supplies no dimension, replay, or firewall evidence payload, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_CANDIDATE_V01_BUILT")


if __name__ == "__main__":
    main()
