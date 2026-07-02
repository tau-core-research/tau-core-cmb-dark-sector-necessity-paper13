#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01_contract_only_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "contract_row_id",
    "contract_component",
    "symbol_or_object",
    "contract_status",
    "evidence_source",
    "contract_requirement",
    "endpoint_exclusion_rule",
    "remaining_blocker",
    "scorecard_effect",
    "endpoint_blind_contract_satisfied",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "contract_rows_declared",
    "declared_rows",
    "partial_rows",
    "blocked_rows",
    "satisfied_rows",
    "hard_failures_triggered",
    "endpoint_blind_contract_satisfied",
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


def contract_rows() -> list[dict[str, str]]:
    rows = [
        {
            "contract_component": "parent_side_input_provenance",
            "symbol_or_object": "provenance(parent -> Phi_tau_eff)",
            "contract_status": "BLOCKED_PARENT_SIDE_INPUT_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "contract_requirement": "supply parent-side Tau response inputs before any CMB role comparison",
            "endpoint_exclusion_rule": "CMB endpoint residuals and role scores cannot define the parent-side source",
            "remaining_blocker": "no parent-side input manifest is supplied",
            "scorecard_effect": "blocks every score row that depends on Phi_tau_eff",
        },
        {
            "contract_component": "endpoint_exclusion_rule",
            "symbol_or_object": "endpoint_blind(Phi_tau_eff)",
            "contract_status": "DECLARED_ENDPOINT_EXCLUSION_RULE",
            "evidence_source": "tau_cmb_scoring_execution_gate_v01",
            "contract_requirement": "exclude CMB endpoint residuals, likelihood residuals, and score labels from construction",
            "endpoint_exclusion_rule": "construction data must be upstream of the CMB endpoint evaluation",
            "remaining_blocker": "the exclusion rule is declared but not yet replayed against a derivation package",
            "scorecard_effect": "prevents circular scoring",
        },
        {
            "contract_component": "derivation_rule_required",
            "symbol_or_object": "rule(parent -> Phi_tau_eff(a,k))",
            "contract_status": "BLOCKED_DERIVATION_RULE_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_effective_source_equation_v01",
            "contract_requirement": "provide an explicit rule mapping Tau response data into Phi_tau_eff(a,k)",
            "endpoint_exclusion_rule": "the rule cannot be fitted from acoustic peaks, lensing residuals, or CMB likelihood error",
            "remaining_blocker": "no symbolic or numerical derivation rule is supplied",
            "scorecard_effect": "blocks acoustic, lensing, growth, and radiation role scoring",
        },
        {
            "contract_component": "normalization_lock",
            "symbol_or_object": "norm(Phi_tau_eff)",
            "contract_status": "PARTIAL_CONTRACT_NORMALIZATION_REQUIRED",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "contract_requirement": "lock a single normalization before comparing acoustic and lensing readouts",
            "endpoint_exclusion_rule": "normalization cannot be chosen to reduce endpoint residuals after seeing scores",
            "remaining_blocker": "normalization convention remains a requirement, not an implemented lock",
            "scorecard_effect": "prevents convention drift between role rows",
        },
        {
            "contract_component": "audit_replay_package",
            "symbol_or_object": "replay(parent -> Phi_tau_eff -> CMB roles)",
            "contract_status": "BLOCKED_REPLAY_PACKAGE_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_minimal_scoring_input_contract_v01",
            "contract_requirement": "provide a reproducible replay package proving that construction is endpoint-blind",
            "endpoint_exclusion_rule": "replay metadata must show no endpoint-derived inputs entered the source path",
            "remaining_blocker": "no replay package exists",
            "scorecard_effect": "prevents score execution from accepting the source",
        },
        {
            "contract_component": "failure_branch",
            "symbol_or_object": "fail_if_contract_unsatisfied",
            "contract_status": "PARTIAL_CONTRACT_FAILURE_BRANCH_READY",
            "evidence_source": "tau_cmb_scoring_execution_gate_v01",
            "contract_requirement": "declare failure behavior if endpoint-blind construction cannot be demonstrated",
            "endpoint_exclusion_rule": "an unsatisfied contract must not be converted into an approximate fit",
            "remaining_blocker": "failure branch is declared but not triggered by a completed derivation attempt",
            "scorecard_effect": "keeps no-dark and dark-sector verdicts blocked until source provenance is settled",
        },
    ]
    return [
        {
            "contract_row_id": f"TCMBEBPTDC01_{index:03d}",
            "endpoint_blind_contract_satisfied": "false",
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
            "summary_id": "TAU_CMB_ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_V01",
            "contract_rows_declared": len(rows),
            "declared_rows": sum(row["contract_status"].startswith("DECLARED") for row in rows),
            "partial_rows": sum(row["contract_status"].startswith("PARTIAL") for row in rows),
            "blocked_rows": sum(row["contract_status"].startswith("BLOCKED") for row in rows),
            "satisfied_rows": sum(row["endpoint_blind_contract_satisfied"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "endpoint_blind_contract_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_DECLARED_UNSATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_provenance_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.md").write_text(
        """# Tau CMB Endpoint-Blind Phi Tau Derivation Contract v01

**Doc class:** endpoint-blind source-derivation contract
**Status:** contract declared but unsatisfied; no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_endpoint_blind_phi_tau_derivation_contract.py
```

Derived outputs:

```text
data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.csv
data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_summary_v01.csv
```

This artifact declares the minimum endpoint-blind derivation contract for:

```text
Phi_tau_eff(a,k)
```

It does not derive `Phi_tau_eff`. Instead, it states what must be true before
the source may enter acoustic, lensing, growth, or radiation scoring. CMB
endpoint residuals, likelihood residuals, and role-score labels are excluded
from the construction path.

The endpoint-blind contract is not satisfied:

```text
endpoint_blind_contract_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_provenance_v01
```

## Claim Boundary

This artifact is a derivation contract only. It derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, declares no reproduction or
failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = contract_rows()
    write_csv(DERIVED / "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_endpoint_blind_phi_tau_derivation_contract_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_V01_BUILT")


if __name__ == "__main__":
    main()
