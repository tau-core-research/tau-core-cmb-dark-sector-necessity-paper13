#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_density_amplitude_closure_v01_partial_closure_no_score_no_likelihood_no_verdict"

FIELDS = [
    "closure_row_id",
    "closure_check",
    "symbol_or_object",
    "closure_result",
    "evidence_source",
    "remaining_blocker",
    "scorecard_update",
    "can_compute_density_score",
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
    "can_compute_density_score",
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
            "closure_check": "density_ratio_dimension_check",
            "symbol_or_object": "A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)",
            "closure_result": "CLOSED_CONDITIONAL_DIMENSIONLESS_RATIO",
            "evidence_source": "tau_cmb_density_amplitude_derivation_v01",
            "remaining_blocker": "requires shared density normalization convention before numerical use",
            "scorecard_update": "formal amplitude slot remains usable as a reduced benchmark target",
            "can_compute_density_score": "false",
            "hard_failure_triggered": "false",
        },
        {
            "closure_check": "tau_effective_density_formula",
            "symbol_or_object": "rho_tau_eff(a,k)",
            "closure_result": "BLOCKED_FORMULA_NOT_DERIVED",
            "evidence_source": "tau_cmb_effective_source_equation_v01",
            "remaining_blocker": "rho_tau_eff is still a source slot rather than a derived function",
            "scorecard_update": "density row cannot be quantitatively scored",
            "can_compute_density_score": "false",
            "hard_failure_triggered": "false",
        },
        {
            "closure_check": "endpoint_blind_amplitude_derivation",
            "symbol_or_object": "endpoint_blind(A_tau)",
            "closure_result": "BLOCKED_ENDPOINT_BLIND_DERIVATION_MISSING",
            "evidence_source": "tau_cmb_density_amplitude_derivation_v01",
            "remaining_blocker": "no provenance rule proves independence from CMB residual fitting",
            "scorecard_update": "density row must remain not-ready",
            "can_compute_density_score": "false",
            "hard_failure_triggered": "false",
        },
        {
            "closure_check": "omega_c_h2_role_comparison",
            "symbol_or_object": "Omega_c h^2 role",
            "closure_result": "BLOCKED_NO_NUMERICAL_COMPARISON",
            "evidence_source": "tau_cmb_known_limit_failure_map_v01",
            "remaining_blocker": "no benchmark, likelihood, or numeric A_tau prediction",
            "scorecard_update": "no reproduce/approximate/fail decision can be assigned",
            "can_compute_density_score": "false",
            "hard_failure_triggered": "false",
        },
        {
            "closure_check": "density_stop_rule",
            "symbol_or_object": "omega_c_h2_density_inference scorecard row",
            "closure_result": "PARTIAL_CLOSURE_DERIVATION_MISSING",
            "evidence_source": "tau_cmb_scorecard_blocker_closure_plan_v01",
            "remaining_blocker": "derive endpoint-blind A_tau or explicitly fail the density role",
            "scorecard_update": "do not proceed by fitting CMB residuals",
            "can_compute_density_score": "false",
            "hard_failure_triggered": "false",
        },
    ]
    return [
        {
            "closure_row_id": f"TCMBDAC01_{index:03d}",
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
            "summary_id": "TAU_CMB_DENSITY_AMPLITUDE_CLOSURE_V01",
            "closure_rows_declared": len(rows),
            "closed_rows": sum(row["closure_result"].startswith("CLOSED") for row in rows),
            "partial_closure_rows": sum(row["closure_result"].startswith("PARTIAL_CLOSURE") for row in rows),
            "blocked_rows": sum(row["closure_result"].startswith("BLOCKED") for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "can_compute_density_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "DENSITY_AMPLITUDE_PARTIAL_CLOSURE_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_reduced_evaluation_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_density_amplitude_closure_v01.md").write_text(
        """# Tau CMB Density Amplitude Closure v01

**Doc class:** density-amplitude blocker closure
**Status:** partial closure; density score still blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_density_amplitude_closure.py
```

Derived outputs:

```text
data/derived/tau_cmb_density_amplitude_closure_v01.csv
data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv
```

This artifact closes only the formal part of the density-amplitude blocker:

```text
A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)
```

is a conditionally dimensionless ratio if both densities share a normalization.
The blocker is not fully closed because `rho_tau_eff(a,k)` and endpoint-blind
`A_tau(a,k)` are not derived, and the `Omega_c h^2` role is not compared.

The density score therefore remains blocked.

## Claim Boundary

This artifact is a partial closure only. It computes no density score, supplies
no CMB likelihood, declares no Omega_c h^2 match, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = closure_rows()
    write_csv(DERIVED / "tau_cmb_density_amplitude_closure_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_density_amplitude_closure_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_DENSITY_AMPLITUDE_CLOSURE_V01_BUILT")


if __name__ == "__main__":
    main()
