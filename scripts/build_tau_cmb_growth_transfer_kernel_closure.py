#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_growth_transfer_kernel_closure_v01_partial_closure_no_operator_no_score_no_likelihood_no_verdict"

FIELDS = [
    "closure_row_id",
    "kernel_component",
    "closure_result",
    "evidence_source",
    "closure_statement",
    "remaining_blocker",
    "scorecard_update",
    "can_compute_growth_score",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "closure_rows_declared",
    "closed_rows",
    "partial_closure_rows",
    "blocked_rows",
    "hard_failures_triggered",
    "can_compute_growth_score",
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


def closure_rows() -> list[dict[str, str]]:
    rows = [
        {
            "kernel_component": "domain_specification",
            "closure_result": "PARTIAL_CLOSURE_DOMAIN_FAMILY_DECLARED",
            "evidence_source": "tau_cmb_growth_transfer_kernel_v01",
            "closure_statement": "the input family may be a Tau CMB response state, effective potential, effective density, or a tuple of these",
            "remaining_blocker": "select one endpoint-blind input object before numerical propagation",
            "scorecard_update": "domain ambiguity is narrowed but not score-ready",
        },
        {
            "kernel_component": "codomain_specification",
            "closure_result": "PARTIAL_CLOSURE_CODOMAIN_FAMILY_DECLARED",
            "evidence_source": "tau_cmb_growth_transfer_kernel_v01",
            "closure_statement": "the output family may be a growth/lensing-era perturbation, potential response, or transfer amplitude",
            "remaining_blocker": "select one observable-side comparison variable and normalization",
            "scorecard_update": "codomain ambiguity is narrowed but not score-ready",
        },
        {
            "kernel_component": "time_scale_convention",
            "closure_result": "CLOSED_REQUIRED_TIME_SCALE_GUARD",
            "evidence_source": "tau_cmb_growth_transfer_kernel_v01; tau_cmb_lensing_transfer_reduced_evaluation_v01",
            "closure_statement": "any kernel use must declare k convention, scale-factor convention, initial epoch, final epoch, and normalization point",
            "remaining_blocker": "concrete numeric convention still required for future evaluation",
            "scorecard_update": "formal convention guard is closed, but it does not make the growth row score-ready",
        },
        {
            "kernel_component": "operator_rule",
            "closure_result": "BLOCKED_OPERATOR_RULE_NOT_DERIVED",
            "evidence_source": "tau_cmb_growth_transfer_kernel_v01",
            "closure_statement": "no transfer operator, reduced evolution equation, or lawful propagation rule is supplied",
            "remaining_blocker": "derive Transfer_tau[X_tau_CMB](k,a) or explicitly fail the growth-transfer role",
            "scorecard_update": "growth score cannot be computed",
        },
        {
            "kernel_component": "cross_role_consistency",
            "closure_result": "BLOCKED_DEPENDENT_ROLES_STILL_OPEN",
            "evidence_source": "tau_cmb_density_amplitude_closure_v01; tau_cmb_acoustic_reduced_evaluation_v01; tau_cmb_lensing_transfer_reduced_evaluation_v01",
            "closure_statement": "density, acoustic, and lensing roles remain blocked, so kernel compatibility cannot be evaluated",
            "remaining_blocker": "close source, density, acoustic, lensing, and transfer conventions before aggregation",
            "scorecard_update": "prevents growth score promotion from an isolated formal kernel slot",
        },
        {
            "kernel_component": "explicit_failure_branch",
            "closure_result": "PARTIAL_CLOSURE_FAILURE_BRANCH_READY",
            "evidence_source": "tau_cmb_known_limit_failure_map_v01",
            "closure_statement": "the growth-transfer row has an explicit FAIL path if no lawful transfer kernel can be supplied",
            "remaining_blocker": "run the reduced checks or explicitly assign FAIL",
            "scorecard_update": "failure discipline is ready, but no growth decision is assigned",
        },
    ]
    return [
        {
            "closure_row_id": f"TCMBGTKC01_{index:03d}",
            "can_compute_growth_score": "false",
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
            "summary_id": "TAU_CMB_GROWTH_TRANSFER_KERNEL_CLOSURE_V01",
            "closure_rows_declared": len(rows),
            "closed_rows": sum(row["closure_result"].startswith("CLOSED") for row in rows),
            "partial_closure_rows": sum(row["closure_result"].startswith("PARTIAL_CLOSURE") for row in rows),
            "blocked_rows": sum(row["closure_result"].startswith("BLOCKED") for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "can_compute_growth_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "GROWTH_TRANSFER_KERNEL_PARTIAL_CLOSURE_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_radiation_guard_evaluation_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_growth_transfer_kernel_closure_v01.md").write_text(
        """# Tau CMB Growth Transfer Kernel Closure v01

**Doc class:** growth-transfer kernel blocker closure
**Status:** partial closure; growth score still blocked, no operator, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_growth_transfer_kernel_closure.py
```

Derived outputs:

```text
data/derived/tau_cmb_growth_transfer_kernel_closure_v01.csv
data/derived/tau_cmb_growth_transfer_kernel_closure_summary_v01.csv
```

This artifact closes only the protocol-level parts of the growth-transfer
kernel blocker. The domain and codomain families are narrowed, and the
time/scale convention guard is closed as a required precondition.

The physics-bearing blocker remains open because no transfer operator is
derived:

```text
Transfer_tau[X_tau_CMB](k,a)
```

Cross-role consistency also remains blocked because density, acoustic, and
lensing inputs are still not score-ready.

The growth score therefore remains blocked.

## Claim Boundary

This artifact is a partial closure only. It supplies no transfer operator,
computes no growth score, supplies no CMB likelihood, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = closure_rows()
    write_csv(DERIVED / "tau_cmb_growth_transfer_kernel_closure_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_growth_transfer_kernel_closure_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_GROWTH_TRANSFER_KERNEL_CLOSURE_V01_BUILT")


if __name__ == "__main__":
    main()
