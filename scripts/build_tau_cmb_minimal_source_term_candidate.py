#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_minimal_source_term_candidate_v01_skeleton_only_no_likelihood_no_verdict"

FIELDS = [
    "candidate_row_id",
    "source_term_component",
    "candidate_symbol",
    "candidate_expression_skeleton",
    "intended_lcdm_role",
    "required_input",
    "dimension_requirement",
    "current_status",
    "dimensional_precheck_status",
    "lcdm_role_match_status",
    "failure_mode_if_not_supplied",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "candidate_components_declared",
    "formula_skeletons_declared",
    "dimensionally_precheckable_skeletons",
    "dimensional_consistency_proved_components",
    "lcdm_role_matches_claimed",
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


def candidate_rows() -> list[dict[str, str]]:
    rows = [
        {
            "source_term_component": "carrier_to_response_state",
            "candidate_symbol": "X_tau_CMB",
            "candidate_expression_skeleton": "X_tau_CMB = Response_tau_CMB(B_tau_base_CMB, delta_M_CMB; OI, ell, h)",
            "intended_lcdm_role": "construct a CMB-era response state before metric handoff",
            "required_input": "base carrier, endpoint-blind CMB disturbance seed, observer-interface profile, scale mode, expansion context",
            "dimension_requirement": "operator domain and codomain must be specified before unit checking",
            "dimensional_precheck_status": "NOT_PRECHECKABLE_OPERATOR_UNFILLED",
            "failure_mode_if_not_supplied": "no lawful Tau CMB response state is available",
            "blocks_no_dark_claim": "true",
        },
        {
            "source_term_component": "effective_density_source",
            "candidate_symbol": "rho_tau_eff(a,k)",
            "candidate_expression_skeleton": "rho_tau_eff(a,k) = A_tau(a,k) rho_cdm_ref(a)",
            "intended_lcdm_role": "occupy the density-like source slot normally inferred as Omega_c h^2",
            "required_input": "dimensionless amplitude A_tau(a,k) derived from Tau response, not fitted from residuals",
            "dimension_requirement": "A_tau must be dimensionless if rho_cdm_ref carries density units",
            "dimensional_precheck_status": "CONDITIONALLY_PRECHECKABLE_IF_A_TAU_DIMENSIONLESS",
            "failure_mode_if_not_supplied": "no density-like non-baryonic source replacement is available",
            "blocks_no_dark_claim": "true",
        },
        {
            "source_term_component": "effective_potential_poisson_slot",
            "candidate_symbol": "Phi_tau_eff(a,k)",
            "candidate_expression_skeleton": "k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)",
            "intended_lcdm_role": "provide the standard-form potential source slot for acoustic and lensing checks",
            "required_input": "rho_tau_eff, dimensionless contrast Delta_tau, and stated Fourier/scale-factor convention",
            "dimension_requirement": "standard Poisson-normalized comparison slot; convention must be declared before proof",
            "dimensional_precheck_status": "CONDITIONALLY_PRECHECKABLE_IF_STANDARD_POISSON_CONVENTION_DECLARED",
            "failure_mode_if_not_supplied": "no metric-potential handoff exists for CMB acoustic and lensing roles",
            "blocks_no_dark_claim": "true",
        },
        {
            "source_term_component": "transfer_kernel_slot",
            "candidate_symbol": "T_tau_CMB(k,a)",
            "candidate_expression_skeleton": "T_tau_CMB(k,a) = Transfer_tau[X_tau_CMB](k,a)",
            "intended_lcdm_role": "connect early response to scale-dependent growth and CMB lensing transfer",
            "required_input": "transfer rule, initial condition convention, and propagation law",
            "dimension_requirement": "transfer kernel must be dimensionless or explicitly normalized",
            "dimensional_precheck_status": "NOT_PRECHECKABLE_TRANSFER_RULE_UNFILLED",
            "failure_mode_if_not_supplied": "no growth/lensing transfer comparison can be run",
            "blocks_no_dark_claim": "true",
        },
        {
            "source_term_component": "radiation_guard_slot",
            "candidate_symbol": "Delta_N_eff_tau",
            "candidate_expression_skeleton": "Delta_N_eff_tau <= Delta_N_eff_bound",
            "intended_lcdm_role": "guard damping-tail and relativistic-degree constraints",
            "required_input": "Tau radiation-like contribution and external bound convention",
            "dimension_requirement": "dimensionless effective relativistic-degree contribution",
            "dimensional_precheck_status": "CONDITIONALLY_PRECHECKABLE_DIMENSIONLESS_GUARD",
            "failure_mode_if_not_supplied": "Tau response may overproduce radiation-like CMB damping effects",
            "blocks_no_dark_claim": "false",
        },
        {
            "source_term_component": "known_limit_branch",
            "candidate_symbol": "LCDM_role_limit_or_failure",
            "candidate_expression_skeleton": "A_tau -> Omega_c/Omega_ref and Delta_tau -> delta_cdm, or explicit failure",
            "intended_lcdm_role": "state whether the candidate reproduces, approximates, or fails the standard source role",
            "required_input": "limit map from Tau response variables to standard comparison variables",
            "dimension_requirement": "comparison statement; every mapped variable must have a declared unit convention",
            "dimensional_precheck_status": "NOT_PRECHECKABLE_LIMIT_MAP_UNFILLED",
            "failure_mode_if_not_supplied": "no CMB no-dark or dark-sector decision can be scored",
            "blocks_no_dark_claim": "true",
        },
    ]
    return [
        {
            "candidate_row_id": f"TCMBMSC01_{index:03d}",
            "current_status": "CANDIDATE_SKELETON_DECLARED_NOT_VALIDATED",
            "lcdm_role_match_status": "LCDM_ROLE_DECLARED_NOT_MATCHED",
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
            "summary_id": "TAU_CMB_MINIMAL_SOURCE_TERM_CANDIDATE_V01",
            "candidate_components_declared": len(rows),
            "formula_skeletons_declared": sum(row["candidate_expression_skeleton"] != "" for row in rows),
            "dimensionally_precheckable_skeletons": sum(
                row["dimensional_precheck_status"].startswith("CONDITIONALLY_PRECHECKABLE") for row in rows
            ),
            "dimensional_consistency_proved_components": 0,
            "lcdm_role_matches_claimed": 0,
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "MINIMAL_SOURCE_TERM_CANDIDATE_DECLARED_NOT_VALIDATED",
            "next_required_artifact": "tau_cmb_source_term_dimensional_precheck_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_minimal_source_term_candidate_v01.md").write_text(
        """# Tau CMB Minimal Source-Term Candidate v01

**Doc class:** source-term candidate scaffold
**Status:** formula skeletons declared; no dimensional proof, no CMB likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_minimal_source_term_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_minimal_source_term_candidate_v01.csv
data/derived/tau_cmb_minimal_source_term_candidate_summary_v01.csv
```

This artifact writes the smallest useful CMB source-term candidate table for
Paper 13. It is not a Tau Core CMB solution. It exists so the later scoring
work has a concrete object to test instead of a loose verbal claim.

The candidate chain is:

```text
X_tau_CMB = Response_tau_CMB(B_tau_base_CMB, delta_M_CMB; OI, ell, h)
rho_tau_eff(a,k) = A_tau(a,k) rho_cdm_ref(a)
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
T_tau_CMB(k,a) = Transfer_tau[X_tau_CMB](k,a)
Delta_N_eff_tau <= Delta_N_eff_bound
LCDM_role_limit_or_failure
```

The Poisson-like row is a standard-form comparison slot, not a derived Tau
field equation. The density row is conditionally dimension-checkable only if
`A_tau(a,k)` is supplied as a dimensionless Tau-response amplitude rather than
a post-fit residual.

## Claim Boundary

This artifact declares a minimal source-term candidate skeleton only. It proves
no dimensional consistency result, matches no LCDM role, provides no Boltzmann
solver, provides no CMB likelihood, permits no Tau-response claim, and permits
no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_rows()
    write_csv(DERIVED / "tau_cmb_minimal_source_term_candidate_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_minimal_source_term_candidate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_MINIMAL_SOURCE_TERM_CANDIDATE_V01_BUILT")


if __name__ == "__main__":
    main()
