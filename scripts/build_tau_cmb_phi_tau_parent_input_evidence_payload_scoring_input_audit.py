#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01_audit_only_"
    "scoring_input_rejected_no_payload_accepted_no_package_pass_no_certificate_pass_"
    "no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "scoring_input_component",
    "audited_candidate_source",
    "audit_status",
    "audit_rule",
    "audit_finding",
    "required_accepted_payload",
    "required_acceptance_decision",
    "required_scoring_contract",
    "acceptance_allowed",
    "payload_accepted",
    "scoring_input_candidate_declared",
    "scoring_input_audited",
    "scoring_input_audit_passed",
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
    "audit_rows_declared",
    "scoring_input_audited_rows",
    "scoring_input_audit_passed_rows",
    "acceptance_allowed_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_audit_satisfied",
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
        ("manifest_scoring_input_audit", "accepted manifest payload"),
        ("base_field_scoring_input_audit", "accepted B_tau state payload"),
        ("seed_scoring_input_audit", "accepted seed_tau payload"),
        ("operator_scoring_input_audit", "accepted R_tau response-operator payload"),
        ("gauge_normalization_scoring_input_audit", "accepted gauge/normalization payload"),
        ("endpoint_firewall_scoring_input_audit", "accepted endpoint-firewall payload"),
        ("executable_replay_scoring_input_audit", "accepted executable replay/provenance payload"),
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPEPSIA01_{index:03d}",
            "scoring_input_component": component,
            "audited_candidate_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01",
            "audit_status": "SCORING_INPUT_AUDITED_REJECTED_ACCEPTANCE_DECISION_CLOSED",
            "audit_rule": "scoring input may pass audit only after accepted endpoint-blind payload and minimal scoring contract satisfaction",
            "audit_finding": "required accepted payload is absent because acceptance decision gate is closed",
            "required_accepted_payload": required,
            "required_acceptance_decision": "acceptance_allowed must be true before scoring input audit can pass",
            "required_scoring_contract": "minimal scoring input contract must be satisfied before any score is computed",
            "acceptance_allowed": "false",
            "payload_accepted": "false",
            "scoring_input_candidate_declared": "true",
            "scoring_input_audited": "true",
            "scoring_input_audit_passed": "false",
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
        for index, (component, required) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "scoring_input_audited_rows": sum(row["scoring_input_audited"] == "true" for row in rows),
            "scoring_input_audit_passed_rows": sum(row["scoring_input_audit_passed"] == "true" for row in rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_audit_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_AUDIT_REJECTED_ACCEPTANCE_DECISION_CLOSED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Audit v01

**Doc class:** parent-input evidence payload scoring input audit
**Status:** scoring input candidates audited and rejected for scoring acceptance; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_summary_v01.csv
```

This artifact audits the declared scoring-input candidates. The audit rejects
all candidates for scoring acceptance because accepted endpoint-blind evidence
payloads are absent and the acceptance decision gate remains closed.

The evidence payload scoring input audit is not satisfied:

```text
evidence_payload_scoring_input_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01
```

## Claim Boundary

This artifact is an audit only. It accepts no parent-side payload, provides no
evidence-package pass, provides no certificate pass, accepts no scoring input,
derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
