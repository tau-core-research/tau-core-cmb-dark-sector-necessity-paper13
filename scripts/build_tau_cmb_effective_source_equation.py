#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_effective_source_equation_v01_target_only_no_cmb_solution_no_verdict"

FIELDS = [
    "equation_row_id",
    "target_component",
    "symbolic_role",
    "required_object",
    "dimension_role",
    "lcdm_role_to_match_or_fail",
    "current_status",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "equation_target",
    "components_declared",
    "lcdm_role_checks_declared",
    "dimension_roles_declared",
    "source_equation_filled",
    "cmb_likelihood_available",
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


def equation_rows() -> list[dict[str, str]]:
    rows = [
        (
            "base_carrier",
            "B_tau_base_CMB",
            "CMB-era Tau base-substrate carrier",
            "carrier_space_not_constructed",
            "carrier object; no physical field units assigned",
            "must support or explicitly fail to support the non-baryonic potential role",
            "true",
        ),
        (
            "disturbance_seed",
            "delta_M_CMB",
            "source-frozen morphology/closure disturbance entering the CMB response",
            "independent_seed_extraction_not_constructed",
            "same parent-side morphology/closure class as declared source; not an endpoint residual",
            "must be independent of CMB likelihood residuals and galaxy endpoint scores",
            "true",
        ),
        (
            "response_operator",
            "Response_tau_CMB(B_tau_base_CMB, delta_M_CMB; OI, ell, h)",
            "candidate response operator before metric handoff",
            "operator_rule_not_filled",
            "operator from carrier and disturbance data to a response state",
            "must replace or fail to replace the CDM gravitational-source role",
            "true",
        ),
        (
            "effective_density",
            "rho_tau_eff(a,k)",
            "effective density-like source readout",
            "density_mapping_not_filled",
            "mass density role; same dimensional slot as cosmological source density",
            "must confront the inferred Omega_c h^2 role",
            "true",
        ),
        (
            "effective_potential",
            "Phi_tau_eff(a,k)",
            "effective metric-potential readout",
            "metric_channel_map_not_filled",
            "dimensionless scalar-potential role in perturbation equations",
            "must confront acoustic peak phase/height and CMB lensing roles",
            "true",
        ),
        (
            "transfer_response",
            "T_tau_CMB(k,a)",
            "scale- and epoch-dependent transfer response",
            "transfer_kernel_not_filled",
            "dimensionless transfer/kernel role",
            "must confront growth-seed and CMB-lensing transfer behavior",
            "true",
        ),
        (
            "radiation_guard",
            "Delta_N_eff_tau",
            "radiation-content guard for Tau response",
            "radiation_bound_not_evaluated",
            "dimensionless effective relativistic-degree contribution",
            "must avoid overproducing damping-tail or N_eff deviations",
            "false",
        ),
        (
            "known_limit_gate",
            "LCDM_role_limit_or_failure",
            "explicit comparison to the standard source roles",
            "known_limit_not_checked",
            "comparison statement rather than a new physical variable",
            "must state whether Tau reproduces, approximates, or fails each CMB role",
            "true",
        ),
    ]
    return [
        {
            "equation_row_id": f"TCMBE01_{index:03d}",
            "target_component": component,
            "symbolic_role": symbol,
            "required_object": required,
            "dimension_role": dimension,
            "lcdm_role_to_match_or_fail": lcdm_role,
            "current_status": "DECLARED_NOT_FILLED",
            "blocks_no_dark_claim": blocks,
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (component, symbol, role, required, dimension, lcdm_role, blocks) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_EFFECTIVE_SOURCE_EQUATION_V01",
            "equation_target": "tau_cmb_effective_source_equation_v01",
            "components_declared": len(rows),
            "lcdm_role_checks_declared": sum(row["lcdm_role_to_match_or_fail"] != "" for row in rows),
            "dimension_roles_declared": sum(row["dimension_role"] != "" for row in rows),
            "source_equation_filled": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "EFFECTIVE_SOURCE_EQUATION_TARGET_DECLARED_NOT_FILLED",
            "next_required_artifact": "tau_cmb_known_limit_and_dimension_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_effective_source_equation_v01.md").write_text(
        """# Tau CMB Effective Source Equation v01

**Doc class:** equation-target scaffold
**Status:** target declared; no CMB source equation filled

Script:

```text
scripts/build_tau_cmb_effective_source_equation.py
```

Derived outputs:

```text
data/derived/tau_cmb_effective_source_equation_v01.csv
data/derived/tau_cmb_effective_source_equation_summary_v01.csv
```

This artifact converts the CMB constraint map into an equation-level target.
It does not solve the target.

The intended skeleton is:

```text
B_tau_base_CMB, delta_M_CMB, OI, ell, h
  -> Response_tau_CMB
  -> rho_tau_eff(a,k), Phi_tau_eff(a,k), T_tau_CMB(k,a)
  -> acoustic, lensing, damping, and growth role checks
```

The target is deliberately split into carrier, source, response-operator,
effective-density, effective-potential, transfer, radiation-guard, and
known-limit rows so that a future derivation cannot hide the standard CDM role
inside a fitted residual.

## Claim Boundary

This artifact declares required fields and dimensional roles only. It provides
no Boltzmann solver, no CMB likelihood, no fitted parameters, no Tau Core CMB
validation, no physical Tau dark-sector field, and no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = equation_rows()
    write_csv(DERIVED / "tau_cmb_effective_source_equation_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_effective_source_equation_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_EFFECTIVE_SOURCE_EQUATION_V01_BUILT")


if __name__ == "__main__":
    main()
