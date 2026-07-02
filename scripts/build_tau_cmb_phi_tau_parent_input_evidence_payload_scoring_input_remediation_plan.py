#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01_plan_only_"
    "remediation_not_completed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_"
    "no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "remediation_row_id",
    "scoring_input_component",
    "audit_source",
    "remediation_status",
    "blocking_finding",
    "required_remediation_action",
    "minimal_acceptance_evidence",
    "acceptance_exit_condition",
    "scoring_contract_exit_condition",
    "remediation_completed",
    "acceptance_allowed",
    "payload_accepted",
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
    "remediation_rows_declared",
    "remediation_completed_rows",
    "acceptance_allowed_rows",
    "payload_accepted_rows",
    "scoring_input_audit_passed_rows",
    "scoring_input_accepted_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_remediation_plan_satisfied",
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


def remediation_rows() -> list[dict[str, str]]:
    rows = [
        (
            "manifest_scoring_input_remediation",
            "provide accepted manifest payload with row inventory and component hashes",
            "accepted manifest payload plus row-count/hash replay evidence",
        ),
        (
            "base_field_scoring_input_remediation",
            "provide accepted B_tau state payload with units and normalization",
            "accepted B_tau state payload plus dimension/normalization replay evidence",
        ),
        (
            "seed_scoring_input_remediation",
            "provide accepted seed_tau payload with morphological seed provenance",
            "accepted seed_tau payload plus provenance and endpoint-blind construction evidence",
        ),
        (
            "operator_scoring_input_remediation",
            "provide accepted R_tau response-operator payload with action domain",
            "accepted R_tau payload plus operator-domain and sign-convention replay evidence",
        ),
        (
            "gauge_normalization_scoring_input_remediation",
            "provide accepted gauge and normalization payload with null-mode handling",
            "accepted gauge/normalization payload plus null-mode and scale replay evidence",
        ),
        (
            "endpoint_firewall_scoring_input_remediation",
            "provide accepted endpoint-firewall payload proving endpoint-blind construction",
            "accepted endpoint-firewall payload plus leakage/firewall replay evidence",
        ),
        (
            "executable_replay_scoring_input_remediation",
            "provide accepted executable replay/provenance payload",
            "accepted replay payload plus deterministic command, environment, and artifact hashes",
        ),
    ]
    return [
        {
            "remediation_row_id": f"TCMBPTPIPEPSIRP01_{index:03d}",
            "scoring_input_component": component,
            "audit_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01",
            "remediation_status": "REMEDIATION_REQUIRED_NOT_COMPLETED",
            "blocking_finding": "required accepted payload is absent because acceptance decision gate is closed",
            "required_remediation_action": action,
            "minimal_acceptance_evidence": evidence,
            "acceptance_exit_condition": "acceptance_allowed=true and payload_accepted=true under endpoint-blind firewall",
            "scoring_contract_exit_condition": "minimal scoring input contract satisfied before any score is computed",
            "remediation_completed": "false",
            "acceptance_allowed": "false",
            "payload_accepted": "false",
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
        for index, (component, action, evidence) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PLAN_V01",
            "remediation_rows_declared": len(rows),
            "remediation_completed_rows": sum(row["remediation_completed"] == "true" for row in rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_audit_passed_rows": sum(row["scoring_input_audit_passed"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_remediation_plan_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Remediation Plan v01

**Doc class:** parent-input evidence payload scoring input remediation plan
**Status:** remediation plan declared but not completed; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_summary_v01.csv
```

This artifact states the minimal remediation actions required after the
scoring-input audit rejected all candidates. It is a plan only: no remediation
step is completed, no payload is accepted, and no scoring input is accepted.

The evidence payload scoring input remediation plan is not satisfied:

```text
evidence_payload_scoring_input_remediation_plan_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01
```

## Claim Boundary

This artifact is a remediation plan only. It accepts no parent-side payload,
provides no evidence-package pass, provides no certificate pass, accepts no
scoring input, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = remediation_rows()
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
