#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_lensing_transfer_benchmark_v01_benchmark_only_no_fit_no_likelihood_no_verdict"

FIELDS = [
    "benchmark_row_id",
    "benchmark_component",
    "observable_role",
    "tau_quantity_to_test",
    "reduced_benchmark_condition",
    "current_status",
    "required_input",
    "hard_failure_if",
    "scorecard_effect",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "benchmark_rows_declared",
    "evaluated_rows",
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


def benchmark_rows() -> list[dict[str, str]]:
    rows = [
        {
            "benchmark_component": "lensing_potential_source_presence",
            "observable_role": "CMB lensing gravitational-potential source",
            "tau_quantity_to_test": "Phi_tau_eff(a,k)",
            "reduced_benchmark_condition": "Phi_tau_eff must be a defined potential-like source over the lensing-relevant redshift/scale range",
            "required_input": "metric handoff convention and effective potential normalization",
            "hard_failure_if": "no Tau potential-like source can be propagated into the lensing kernel",
            "scorecard_effect": "keeps lensing score blocked until potential handoff exists",
        },
        {
            "benchmark_component": "transfer_kernel_presence",
            "observable_role": "source propagation into lensing readout",
            "tau_quantity_to_test": "T_tau_CMB(k,a)",
            "reduced_benchmark_condition": "a transfer kernel must map CMB-era response to lensing-era potential response",
            "required_input": "Transfer_tau definition, time/scale convention, and normalization",
            "hard_failure_if": "no lawful transfer kernel connects the CMB-era Tau source to lensing readout",
            "scorecard_effect": "separates potential-slot existence from lensing-transfer support",
        },
        {
            "benchmark_component": "projection_geometry_convention",
            "observable_role": "lensing projection geometry",
            "tau_quantity_to_test": "Phi_tau_eff(a,k), T_tau_CMB(k,a), and projection kernel convention",
            "reduced_benchmark_condition": "lensing comparison must declare line-of-sight/projection convention before amplitude or shape claims",
            "required_input": "projection kernel, distance convention, and reference epoch/range",
            "hard_failure_if": "lensing comparison mixes incompatible projection or distance conventions",
            "scorecard_effect": "guards against false lensing matches from convention mismatch",
        },
        {
            "benchmark_component": "amplitude_shape_support",
            "observable_role": "CMB lensing amplitude and shape support",
            "tau_quantity_to_test": "Phi_tau_eff(a,k) and T_tau_CMB(k,a)",
            "reduced_benchmark_condition": "Tau transfer must support the direction of lensing amplitude/shape constraints before full likelihood",
            "required_input": "reduced lensing amplitude/shape benchmark",
            "hard_failure_if": "Tau response predicts an incompatible lensing amplitude or scale-shape tendency",
            "scorecard_effect": "can later support partial or quantitative lensing score",
        },
        {
            "benchmark_component": "cross_readout_consistency",
            "observable_role": "consistency between acoustic, density, and lensing source roles",
            "tau_quantity_to_test": "A_tau(a,k), Phi_tau_eff(a,k), and T_tau_CMB(k,a)",
            "reduced_benchmark_condition": "lensing support must not contradict the density/amplitude or acoustic role scaffolds",
            "required_input": "density amplitude definition, acoustic benchmark status, and transfer convention",
            "hard_failure_if": "lensing role requires a Tau source incompatible with acoustic or density roles",
            "scorecard_effect": "prepares cross-role consistency before score aggregation",
        },
        {
            "benchmark_component": "explicit_failure_branch",
            "observable_role": "known-limit failure discipline",
            "tau_quantity_to_test": "cmb_lensing_potential decision state",
            "reduced_benchmark_condition": "if lensing transfer cannot be supplied, the row must move to FAIL rather than remain ambiguous",
            "required_input": "known-limit/failure map update after benchmark evaluation",
            "hard_failure_if": "lensing failure is hidden as an unevaluated residual or unconstrained transfer",
            "scorecard_effect": "prepares lensing row for reproduce/approximate/fail assignment",
        },
    ]
    return [
        {
            "benchmark_row_id": f"TCMBLTB01_{index:03d}",
            "current_status": "DECLARED_NOT_EVALUATED",
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
            "summary_id": "TAU_CMB_LENSING_TRANSFER_BENCHMARK_V01",
            "benchmark_rows_declared": len(rows),
            "evaluated_rows": sum(row["current_status"] != "DECLARED_NOT_EVALUATED" for row in rows),
            "hard_failures_triggered": 0,
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "LENSING_TRANSFER_BENCHMARK_DECLARED_NOT_EVALUATED",
            "next_required_artifact": "tau_cmb_growth_transfer_kernel_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_lensing_transfer_benchmark_v01.md").write_text(
        """# Tau CMB Lensing Transfer Benchmark v01

**Doc class:** reduced lensing-transfer benchmark
**Status:** benchmark declared; no evaluation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_lensing_transfer_benchmark.py
```

Derived outputs:

```text
data/derived/tau_cmb_lensing_transfer_benchmark_v01.csv
data/derived/tau_cmb_lensing_transfer_benchmark_summary_v01.csv
```

This artifact declares the reduced checks that must be evaluated before a CMB
lensing score can be promoted:

```text
lensing potential source presence
transfer kernel presence
projection geometry convention
amplitude / shape support
cross-readout consistency
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_EVALUATED
```

The benchmark does not evaluate Planck or ACT lensing data. It only states what
`Phi_tau_eff` and `T_tau_CMB` would have to provide before the lensing scorecard
row can be promoted.

## Claim Boundary

This artifact declares reduced lensing-transfer benchmark conditions only. It
evaluates no lensing spectrum, computes no score, supplies no CMB likelihood,
declares no lensing success or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = benchmark_rows()
    write_csv(DERIVED / "tau_cmb_lensing_transfer_benchmark_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_lensing_transfer_benchmark_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_LENSING_TRANSFER_BENCHMARK_V01_BUILT")


if __name__ == "__main__":
    main()
