#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_certificate_audit_v01_candidate_audit_only_"
    "no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "certificate_component",
    "target_payload_component",
    "audit_status",
    "audited_source",
    "audit_finding",
    "missing_evidence",
    "dimension_audit_result",
    "replay_audit_result",
    "firewall_audit_result",
    "acceptance_decision",
    "scorecard_effect",
    "candidate_audited",
    "certificate_evidence_supplied",
    "dimension_audit_passed",
    "replay_audit_passed",
    "firewall_audit_passed",
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
    "audited_rows",
    "audit_passed_rows",
    "audit_failed_rows",
    "certificate_evidence_supplied_rows",
    "dimension_audit_passed_rows",
    "replay_audit_passed_rows",
    "firewall_audit_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "hard_failures_triggered",
    "certificate_audit_satisfied",
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
            "audit_finding": "candidate manifest is present but contains no supplied/pass certificate evidence",
            "missing_evidence": "accepted certificate package index, replay trace, and payload firewall certificate",
            "scorecard_effect": "keeps parent-input package outside scoring acceptance",
        },
        {
            "certificate_component": "base_field_dimension_replay_certificate_candidate",
            "target_payload_component": "base_field_state_payload_candidate",
            "audit_finding": "base-field certificate candidate is auditable but unpassed",
            "missing_evidence": "B_tau dimension/unit proof, endpoint-blind replay trace, and endpoint-firewall proof",
            "scorecard_effect": "keeps density-amplitude and potential-source scoring inputs blocked",
        },
        {
            "certificate_component": "seed_dimension_replay_certificate_candidate",
            "target_payload_component": "morphological_seed_payload_candidate",
            "audit_finding": "seed certificate candidate is auditable but unpassed",
            "missing_evidence": "seed_tau scale proof, seed replay trace, and endpoint-firewall proof",
            "scorecard_effect": "keeps source-activation and readout-compatibility scoring inputs blocked",
        },
        {
            "certificate_component": "operator_dimension_replay_certificate_candidate",
            "target_payload_component": "response_operator_payload_candidate",
            "audit_finding": "response-operator certificate candidate is auditable but unpassed",
            "missing_evidence": "R_tau dimensional-map proof, operator replay trace, and endpoint-firewall proof",
            "scorecard_effect": "keeps Phi_tau_eff derivation and transfer-kernel scoring inputs blocked",
        },
        {
            "certificate_component": "gauge_normalization_replay_certificate_candidate",
            "target_payload_component": "gauge_normalization_payload_candidate",
            "audit_finding": "gauge/normalization certificate candidate is auditable but unpassed",
            "missing_evidence": "gauge/sign/unit/normalization proof, metadata-lock replay, and endpoint-firewall proof",
            "scorecard_effect": "keeps acoustic, lensing, and growth comparisons outside scoring acceptance",
        },
        {
            "certificate_component": "payload_firewall_certificate_candidate",
            "target_payload_component": "endpoint_firewall_payload_candidate",
            "audit_finding": "payload-firewall certificate candidate is blocked because input-row certificates are absent",
            "missing_evidence": "row-level certificate evidence plus aggregate payload-firewall pass",
            "scorecard_effect": "blocks accepting the full parent-input payload",
        },
        {
            "certificate_component": "executable_replay_certificate_candidate",
            "target_payload_component": "provenance_replay_payload_candidate",
            "audit_finding": "executable-replay certificate candidate is blocked because no replay trace is supplied",
            "missing_evidence": "endpoint-blind executable replay trace and input provenance hash",
            "scorecard_effect": "blocks transition from candidate package to scoring input acceptance",
        },
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPICA01_{index:03d}",
            "audit_status": "AUDIT_FAIL_MISSING_CERTIFICATE_EVIDENCE",
            "audited_source": "tau_cmb_phi_tau_parent_input_certificate_candidate_v01",
            "dimension_audit_result": "fail_no_dimension_certificate_supplied",
            "replay_audit_result": "fail_no_replay_certificate_supplied",
            "firewall_audit_result": "fail_no_firewall_certificate_supplied",
            "acceptance_decision": "reject_for_scoring_input_acceptance",
            "candidate_audited": "true",
            "certificate_evidence_supplied": "false",
            "dimension_audit_passed": "false",
            "replay_audit_passed": "false",
            "firewall_audit_passed": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "audited_rows": sum(row["candidate_audited"] == "true" for row in rows),
            "audit_passed_rows": sum(row["audit_status"].startswith("AUDIT_PASS") for row in rows),
            "audit_failed_rows": sum(row["audit_status"].startswith("AUDIT_FAIL") for row in rows),
            "certificate_evidence_supplied_rows": sum(row["certificate_evidence_supplied"] == "true" for row in rows),
            "dimension_audit_passed_rows": sum(row["dimension_audit_passed"] == "true" for row in rows),
            "replay_audit_passed_rows": sum(row["replay_audit_passed"] == "true" for row in rows),
            "firewall_audit_passed_rows": sum(row["firewall_audit_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "certificate_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_AUDIT_FAILED_MISSING_EVIDENCE",
            "next_required_artifact": "tau_cmb_phi_tau_parent_certificate_closure_decision_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_certificate_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Certificate Audit v01

**Doc class:** parent-input certificate-candidate audit
**Status:** candidate certificates audited and rejected for scoring acceptance; no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_summary_v01.csv
```

This artifact audits the seven certificate candidates declared in
`tau_cmb_phi_tau_parent_input_certificate_candidate_v01`.
All seven candidates fail the audit because no certificate evidence is supplied.

The certificate audit is not satisfied:

```text
certificate_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_certificate_closure_decision_v01
```

## Claim Boundary

This artifact audits certificate candidates only. It supplies no dimension,
replay, or firewall certificate, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_certificate_audit_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_certificate_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
