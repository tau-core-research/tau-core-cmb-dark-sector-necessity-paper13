#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01_acceptance_precheck_only_"
    "no_scoring_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "precheck_row_id",
    "acceptance_component",
    "source_artifact",
    "precheck_status",
    "blocking_condition",
    "required_unblock_condition",
    "scorecard_effect",
    "precheck_executed",
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
    "precheck_rows_declared",
    "precheck_executed_rows",
    "blocked_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "payload_accepted_rows",
    "phi_tau_eff_derivable_rows",
    "scoring_input_accepted_rows",
    "scores_computed",
    "cmb_likelihood_available",
    "hard_failures_triggered",
    "scoring_acceptance_precheck_satisfied",
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


def precheck_rows() -> list[dict[str, str]]:
    rows = [
        {
            "acceptance_component": "evidence_package_acceptance",
            "source_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01",
            "blocking_condition": "evidence package audit failed because evidence payloads are unpopulated",
            "required_unblock_condition": "supply and pass a populated evidence package audit",
            "scorecard_effect": "blocks all parent-input acceptance into scoring",
        },
        {
            "acceptance_component": "certificate_acceptance",
            "source_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01",
            "blocking_condition": "no dimension, replay, or firewall certificate has passed",
            "required_unblock_condition": "pass row-level dimension, replay, and firewall certificates",
            "scorecard_effect": "blocks certificate-backed Phi_tau_eff source construction",
        },
        {
            "acceptance_component": "payload_acceptance",
            "source_artifact": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "blocking_condition": "parent-input payload remains unaccepted by payload firewall and certificate gates",
            "required_unblock_condition": "accept parent-input payload only after evidence package and certificate pass",
            "scorecard_effect": "blocks importing parent-side payload fields into scoring inputs",
        },
        {
            "acceptance_component": "phi_tau_eff_derivation_acceptance",
            "source_artifact": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "blocking_condition": "Phi_tau_eff derivation remains blocked because accepted parent inputs are absent",
            "required_unblock_condition": "derive Phi_tau_eff only from accepted parent inputs under endpoint-blind replay",
            "scorecard_effect": "blocks Tau response scoring and CMB residual comparison",
        },
        {
            "acceptance_component": "cmb_scoring_acceptance",
            "source_artifact": "tau_cmb_scoring_execution_gate_v01",
            "blocking_condition": "CMB scoring cannot run because scoring inputs are not accepted",
            "required_unblock_condition": "run scoring only after parent-input acceptance and Phi_tau_eff derivation pass",
            "scorecard_effect": "keeps scores, likelihoods, and verdicts unavailable",
        },
    ]
    return [
        {
            "precheck_row_id": f"TCMBPTPISAP01_{index:03d}",
            "precheck_status": "SCORING_ACCEPTANCE_PRECHECK_BLOCKED",
            "precheck_executed": "true",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_PRECHECK_V01",
            "precheck_rows_declared": len(rows),
            "precheck_executed_rows": sum(row["precheck_executed"] == "true" for row in rows),
            "blocked_rows": sum(row["precheck_status"] == "SCORING_ACCEPTANCE_PRECHECK_BLOCKED" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "phi_tau_eff_derivable_rows": sum(row["phi_tau_eff_derivable"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "scoring_acceptance_precheck_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_PRECHECK_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Scoring Acceptance Precheck v01

**Doc class:** parent-input scoring acceptance precheck
**Status:** scoring acceptance precheck executed and blocked; no scoring acceptance, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_summary_v01.csv
```

This artifact performs the scoring-acceptance precheck for parent-side Tau
inputs. All five precheck rows are blocked because the evidence package,
certificate pass, payload acceptance, and `Phi_tau_eff` derivation gates have
not passed.

The scoring acceptance precheck is not satisfied:

```text
scoring_acceptance_precheck_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01
```

## Claim Boundary

This artifact performs a scoring-acceptance precheck only. It accepts no
parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score, supplies no
CMB likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = precheck_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_PRECHECK_V01_BUILT")


if __name__ == "__main__":
    main()
