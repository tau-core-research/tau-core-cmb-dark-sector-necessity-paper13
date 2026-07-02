#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01_unblock_plan_only_"
    "no_unblock_completed_no_scoring_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "plan_row_id",
    "rank",
    "acceptance_component",
    "blocked_source",
    "unblock_target_artifact",
    "unblock_action",
    "completion_criterion",
    "stop_rule",
    "scorecard_effect",
    "plan_declared",
    "unblock_completed",
    "evidence_package_passed",
    "certificate_passed",
    "payload_accepted",
    "phi_tau_eff_derivable",
    "scoring_input_accepted",
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
    "plan_rows_declared",
    "plan_declared_rows",
    "unblock_completed_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "payload_accepted_rows",
    "phi_tau_eff_derivable_rows",
    "scoring_input_accepted_rows",
    "scores_computed",
    "cmb_likelihood_available",
    "hard_failures_triggered",
    "scoring_acceptance_unblock_plan_satisfied",
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


def plan_rows() -> list[dict[str, str]]:
    rows = [
        {
            "rank": "1",
            "acceptance_component": "evidence_package_acceptance",
            "blocked_source": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01",
            "unblock_target_artifact": "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01",
            "unblock_action": "supply populated dimension, replay, firewall, artifact-hash, and coverage payloads",
            "completion_criterion": "all evidence payload slots are populated and auditable without endpoint residual inputs",
            "stop_rule": "if any payload slot depends on score, residual, or likelihood outputs, stop and record firewall failure",
            "scorecard_effect": "first required step before parent-side scoring acceptance can be reconsidered",
        },
        {
            "rank": "2",
            "acceptance_component": "certificate_acceptance",
            "blocked_source": "tau_cmb_phi_tau_parent_input_certificate_audit_v01",
            "unblock_target_artifact": "tau_cmb_phi_tau_parent_input_certificate_pass_candidate_v01",
            "unblock_action": "audit populated evidence package against row-level dimension, replay, and firewall certificate criteria",
            "completion_criterion": "all required row-level certificates pass with executable replay and endpoint firewall coverage",
            "stop_rule": "if any certificate remains missing or endpoint-contaminated, keep certificate acceptance blocked",
            "scorecard_effect": "required before any certificate-backed Phi_tau_eff source construction",
        },
        {
            "rank": "3",
            "acceptance_component": "payload_acceptance",
            "blocked_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "unblock_target_artifact": "tau_cmb_phi_tau_parent_input_payload_acceptance_candidate_v01",
            "unblock_action": "accept the parent-input payload only after package and certificate pass are available",
            "completion_criterion": "payload passes firewall, provenance, dimension, replay, and certificate gates",
            "stop_rule": "if payload acceptance would precede certificate pass, stop and keep scoring blocked",
            "scorecard_effect": "required before parent-side fields can enter scoring inputs",
        },
        {
            "rank": "4",
            "acceptance_component": "phi_tau_eff_derivation_acceptance",
            "blocked_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "unblock_target_artifact": "tau_cmb_phi_tau_eff_endpoint_blind_derivation_candidate_v01",
            "unblock_action": "derive Phi_tau_eff only from accepted parent inputs under endpoint-blind replay",
            "completion_criterion": "Phi_tau_eff derivation has accepted inputs, executable replay, dimension consistency, and endpoint firewall proof",
            "stop_rule": "if Phi_tau_eff uses CMB residuals, scores, or likelihood errors as construction inputs, stop and record failure",
            "scorecard_effect": "required before Tau response scoring or CMB residual comparison can be attempted",
        },
        {
            "rank": "5",
            "acceptance_component": "cmb_scoring_acceptance",
            "blocked_source": "tau_cmb_scoring_execution_gate_v01",
            "unblock_target_artifact": "tau_cmb_phi_tau_parent_input_scoring_acceptance_candidate_v01",
            "unblock_action": "allow CMB scoring only after parent-input acceptance and Phi_tau_eff derivation pass",
            "completion_criterion": "scoring input acceptance is recorded before any score, likelihood, or verdict is computed",
            "stop_rule": "if acceptance is incomplete, score rows remain not computed and verdicts remain blocked",
            "scorecard_effect": "last gate before a future CMB scorecard execution can be considered",
        },
    ]
    return [
        {
            "plan_row_id": f"TCMBPTPISAUP01_{index:03d}",
            "plan_declared": "true",
            "unblock_completed": "false",
            "evidence_package_passed": "false",
            "certificate_passed": "false",
            "payload_accepted": "false",
            "phi_tau_eff_derivable": "false",
            "scoring_input_accepted": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_UNBLOCK_PLAN_V01",
            "plan_rows_declared": len(rows),
            "plan_declared_rows": sum(row["plan_declared"] == "true" for row in rows),
            "unblock_completed_rows": sum(row["unblock_completed"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "phi_tau_eff_derivable_rows": sum(row["phi_tau_eff_derivable"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "scoring_acceptance_unblock_plan_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_OPEN",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Scoring Acceptance Unblock Plan v01

**Doc class:** parent-input scoring acceptance unblock plan
**Status:** unblock plan declared but open; no unblock completed, no scoring acceptance, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_summary_v01.csv
```

This artifact ranks the five steps required to unblock parent-side scoring
acceptance. No unblock step is completed in this artifact.

The scoring acceptance unblock plan is not satisfied:

```text
scoring_acceptance_unblock_plan_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01
```

## Claim Boundary

This artifact declares an unblock plan only. It accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = plan_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_UNBLOCK_PLAN_V01_BUILT")


if __name__ == "__main__":
    main()
