#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_density_amplitude_derivation_v01_conditional_definition_no_fit_no_likelihood_no_verdict"

FIELDS = [
    "density_row_id",
    "derivation_component",
    "symbol",
    "definition_or_requirement",
    "dimension_status",
    "endpoint_blindness_status",
    "omega_c_h2_role_status",
    "current_blocker",
    "scorecard_effect",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "density_rows_declared",
    "conditional_dimension_passes",
    "endpoint_blind_derivations_available",
    "omega_c_h2_role_matches",
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


def density_rows() -> list[dict[str, str]]:
    rows = [
        {
            "derivation_component": "reference_density_normalization",
            "symbol": "rho_cdm_ref(a)",
            "definition_or_requirement": "standard comparison density normalization for the Omega_c h^2 role",
            "dimension_status": "DENSITY_DIMENSION_DECLARED",
            "endpoint_blindness_status": "REFERENCE_OBJECT_NOT_TAU_DERIVED",
            "omega_c_h2_role_status": "COMPARISON_SLOT_DECLARED_UNRESOLVED",
            "current_blocker": "reference normalization chosen but not yet tied to a Tau-derived amplitude",
            "scorecard_effect": "sets the denominator needed for A_tau definition",
            "blocks_no_dark_claim": "true",
        },
        {
            "derivation_component": "tau_effective_density_slot",
            "symbol": "rho_tau_eff(a,k)",
            "definition_or_requirement": "Tau CMB effective density-like source slot",
            "dimension_status": "DENSITY_DIMENSION_DECLARED_FORMULA_UNFILLED",
            "endpoint_blindness_status": "TAU_SOURCE_DERIVATION_NOT_SUPPLIED",
            "omega_c_h2_role_status": "DENSITY_ROLE_TARGET_DECLARED_UNRESOLVED",
            "current_blocker": "rho_tau_eff is still a source slot rather than a derived function",
            "scorecard_effect": "blocks quantitative density score until filled",
            "blocks_no_dark_claim": "true",
        },
        {
            "derivation_component": "dimensionless_amplitude_definition",
            "symbol": "A_tau(a,k)",
            "definition_or_requirement": "A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)",
            "dimension_status": "CONDITIONAL_DIMENSION_PASS_IF_BOTH_DENSITIES_SHARE_NORMALIZATION",
            "endpoint_blindness_status": "DEFINITION_ONLY_ENDPOINT_BLIND_DERIVATION_NOT_SUPPLIED",
            "omega_c_h2_role_status": "FORMAL_AMPLITUDE_SLOT_DECLARED_UNRESOLVED",
            "current_blocker": "A_tau value and Tau-side derivation are not supplied",
            "scorecard_effect": "can support a reduced density benchmark after Tau-side amplitude derivation",
            "blocks_no_dark_claim": "true",
        },
        {
            "derivation_component": "endpoint_blindness_gate",
            "symbol": "endpoint_blind(A_tau)",
            "definition_or_requirement": "A_tau must be derived before CMB residual fitting or likelihood tuning",
            "dimension_status": "NOT_A_DIMENSIONAL_CLAIM",
            "endpoint_blindness_status": "REQUIRED_NOT_PROVED",
            "omega_c_h2_role_status": "GUARD_DECLARED_NOT_PASSED",
            "current_blocker": "no provenance rule proves independence from CMB residual fitting",
            "scorecard_effect": "prevents density score promotion from fitted residual to source derivation",
            "blocks_no_dark_claim": "true",
        },
        {
            "derivation_component": "omega_c_h2_comparison_gate",
            "symbol": "Omega_c h^2 role",
            "definition_or_requirement": "compare A_tau-induced density role to the standard inferred density role",
            "dimension_status": "COMPARISON_GATE_NOT_A_NEW_UNIT_CLAIM",
            "endpoint_blindness_status": "WAITING_FOR_A_TAU_DERIVATION",
            "omega_c_h2_role_status": "NOT_EVALUATED_NO_NUMERICAL_COMPARISON",
            "current_blocker": "no benchmark, likelihood, or numeric A_tau prediction",
            "scorecard_effect": "keeps density row not scoreable beyond formal definition",
            "blocks_no_dark_claim": "true",
        },
    ]
    return [
        {
            "density_row_id": f"TCMBDAD01_{index:03d}",
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
            "summary_id": "TAU_CMB_DENSITY_AMPLITUDE_DERIVATION_V01",
            "density_rows_declared": len(rows),
            "conditional_dimension_passes": sum(
                row["dimension_status"].startswith("CONDITIONAL_DIMENSION_PASS") for row in rows
            ),
            "endpoint_blind_derivations_available": 0,
            "omega_c_h2_role_matches": 0,
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "DENSITY_AMPLITUDE_DEFINITION_DECLARED_DERIVATION_AND_MATCH_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_role_reduced_benchmark_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_density_amplitude_derivation_v01.md").write_text(
        """# Tau CMB Density Amplitude Derivation v01

**Doc class:** density-amplitude derivation scaffold
**Status:** conditional definition declared; no endpoint-blind derivation, no fit, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_density_amplitude_derivation.py
```

Derived outputs:

```text
data/derived/tau_cmb_density_amplitude_derivation_v01.csv
data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv
```

This artifact declares the formal amplitude slot:

```text
A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)
```

This is conditionally dimensionless if `rho_tau_eff` and `rho_cdm_ref` are
both density-normalized under the same convention. That conditional dimension
check is useful, but it is not yet a Tau-side derivation of `A_tau`, not an
Omega_c h^2 match, and not a CMB likelihood result.

The density role remains blocked until `A_tau(a,k)` is derived endpoint-blind
from Tau-side data rather than tuned from CMB residuals.

## Claim Boundary

This artifact declares a conditional density-amplitude definition only. It
computes no numerical amplitude, proves no endpoint-blind derivation, matches no Omega_c h^2 role, computes no score, supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = density_rows()
    write_csv(DERIVED / "tau_cmb_density_amplitude_derivation_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_density_amplitude_derivation_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_DENSITY_AMPLITUDE_DERIVATION_V01_BUILT")


if __name__ == "__main__":
    main()
