#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_growth_transfer_kernel_v01_kernel_spec_only_no_fit_no_likelihood_no_verdict"

FIELDS = [
    "kernel_row_id",
    "kernel_component",
    "role",
    "symbol_or_object",
    "required_specification",
    "current_status",
    "dimension_or_normalization_status",
    "hard_failure_if",
    "scorecard_effect",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "kernel_rows_declared",
    "specified_rows",
    "dimension_or_normalization_rows_declared",
    "hard_failures_triggered",
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


def kernel_rows() -> list[dict[str, str]]:
    rows = [
        {
            "kernel_component": "domain_specification",
            "role": "input side of growth transfer",
            "symbol_or_object": "X_tau_CMB or Phi_tau_eff(a,k)",
            "required_specification": "declare whether the kernel acts on response state, effective potential, effective density, or a tuple of them",
            "dimension_or_normalization_status": "DOMAIN_DECLARED_NOT_SPECIFIED",
            "hard_failure_if": "no lawful input object can be selected from the Tau CMB source scaffold",
            "scorecard_effect": "blocks all growth-transfer scoring until the kernel domain is specified",
        },
        {
            "kernel_component": "codomain_specification",
            "role": "output side of growth transfer",
            "symbol_or_object": "growth/lensing-era perturbation or potential response",
            "required_specification": "declare output object and whether it is a density contrast, potential, transfer amplitude, or comparison variable",
            "dimension_or_normalization_status": "CODOMAIN_DECLARED_NOT_SPECIFIED",
            "hard_failure_if": "no observable-side output object can be compared to growth or lensing roles",
            "scorecard_effect": "prevents hidden handoff from CMB source to late-time growth residual",
        },
        {
            "kernel_component": "time_scale_convention",
            "role": "epoch and scale propagation convention",
            "symbol_or_object": "T_tau_CMB(k,a)",
            "required_specification": "declare k convention, scale factor convention, initial epoch, final epoch, and normalization point",
            "dimension_or_normalization_status": "K_A_NORMALIZATION_DECLARED_NOT_FILLED",
            "hard_failure_if": "kernel mixes incompatible k/a conventions or has no normalization point",
            "scorecard_effect": "guards against false growth or lensing agreement from convention drift",
        },
        {
            "kernel_component": "operator_rule",
            "role": "actual propagation rule",
            "symbol_or_object": "Transfer_tau[X_tau_CMB](k,a)",
            "required_specification": "supply an operator rule, reduced evolution equation, or explicit failure statement",
            "dimension_or_normalization_status": "OPERATOR_RULE_MISSING",
            "hard_failure_if": "no transfer operator can propagate CMB-era Tau response to later readout",
            "scorecard_effect": "keeps transfer score at not-computed until a rule exists",
        },
        {
            "kernel_component": "cross_role_consistency",
            "role": "compatibility with density, acoustic, and lensing roles",
            "symbol_or_object": "A_tau(a,k), Phi_tau_eff(a,k), T_tau_CMB(k,a)",
            "required_specification": "kernel must not require a source behavior incompatible with density amplitude, acoustic benchmark, or lensing benchmark",
            "dimension_or_normalization_status": "CONSISTENCY_GATE_DECLARED_NOT_EVALUATED",
            "hard_failure_if": "growth kernel requires assumptions contradicting another CMB role scaffold",
            "scorecard_effect": "prepares score aggregation without role-by-role contradiction",
        },
        {
            "kernel_component": "explicit_failure_branch",
            "role": "known-limit failure discipline",
            "symbol_or_object": "growth_seed_and_transfer_consistency decision state",
            "required_specification": "if a transfer kernel cannot be supplied, move the growth role to FAIL rather than leaving it ambiguous",
            "dimension_or_normalization_status": "FAILURE_BRANCH_DECLARED_NOT_TRIGGERED",
            "hard_failure_if": "transfer failure is hidden as an unconstrained residual or omitted propagation step",
            "scorecard_effect": "prepares growth row for reproduce/approximate/fail assignment",
        },
    ]
    return [
        {
            "kernel_row_id": f"TCMBGTK01_{index:03d}",
            "current_status": "DECLARED_NOT_SPECIFIED",
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
            "summary_id": "TAU_CMB_GROWTH_TRANSFER_KERNEL_V01",
            "kernel_rows_declared": len(rows),
            "specified_rows": sum(row["current_status"] != "DECLARED_NOT_SPECIFIED" for row in rows),
            "dimension_or_normalization_rows_declared": sum(row["dimension_or_normalization_status"] != "" for row in rows),
            "hard_failures_triggered": 0,
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "GROWTH_TRANSFER_KERNEL_DECLARED_NOT_SPECIFIED",
            "next_required_artifact": "tau_cmb_radiation_guard_bound_check_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_growth_transfer_kernel_v01.md").write_text(
        """# Tau CMB Growth Transfer Kernel v01

**Doc class:** transfer-kernel specification scaffold
**Status:** kernel requirements declared; no operator rule, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_growth_transfer_kernel.py
```

Derived outputs:

```text
data/derived/tau_cmb_growth_transfer_kernel_v01.csv
data/derived/tau_cmb_growth_transfer_kernel_summary_v01.csv
```

This artifact declares what a Tau CMB growth-transfer kernel must specify:

```text
domain
codomain
time/scale convention
operator rule
cross-role consistency
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_SPECIFIED
```

The artifact does not provide a transfer operator and does not compare against
growth, lensing, or structure data. It only prevents the project from treating
an unspecified propagation step as an available Tau response.

## Claim Boundary

This artifact declares transfer-kernel requirements only. It supplies no operator rule, evaluates no growth data, computes no score, supplies no CMB likelihood, validates no Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = kernel_rows()
    write_csv(DERIVED / "tau_cmb_growth_transfer_kernel_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_growth_transfer_kernel_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_GROWTH_TRANSFER_KERNEL_V01_BUILT")


if __name__ == "__main__":
    main()
