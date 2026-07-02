#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_cosmology_derivation_spine_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_cosmology_derivation_spine_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_cosmology_derivation_spine_v01.md"


ROWS = [
    {
        "row_id": "TCMBCDS01_001",
        "layer": "tau_background",
        "symbol": "M_tau^CMB, a_tau, H_tau",
        "definition_or_target": "Declare a homogeneous readout-compatible Tau background with scale parameter a_tau and expansion rate H_tau := d ln a_tau / d t_readout.",
        "derived_status": "DEFINITION_SCAFFOLD",
        "dimension_status": "H_tau has inverse time if t_readout is supplied; a_tau dimensionless by convention.",
        "blocks": "cannot define perturbation evolution without readout time/scale convention",
    },
    {
        "row_id": "TCMBCDS01_002",
        "layer": "tau_effective_source",
        "symbol": "rho_tau_eff(a,k)",
        "definition_or_target": "rho_tau_eff(a,k) := A_tau(a,k) rho_ref(a), with A_tau dimensionless and endpoint-blind.",
        "derived_status": "CONDITIONAL_ROLE_FORMULA",
        "dimension_status": "density dimension inherited from rho_ref; A_tau must be dimensionless.",
        "blocks": "A_tau derivation and normalization are not supplied",
    },
    {
        "row_id": "TCMBCDS01_003",
        "layer": "tau_potential_constraint",
        "symbol": "Phi_tau_eff(a,k)",
        "definition_or_target": "k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k), used as a role-matching Poisson-slot target, not yet a Tau field equation.",
        "derived_status": "COMPARISON_SLOT_NOT_FIELD_EQUATION",
        "dimension_status": "dimensionless potential if k is comoving inverse length and density slot uses standard cosmological units.",
        "blocks": "Delta_tau and Tau-side field equation are not derived",
    },
    {
        "row_id": "TCMBCDS01_004",
        "layer": "tau_transfer",
        "symbol": "Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]",
        "definition_or_target": "Define the lensing-era Tau potential response as a transfer of Phi_tau_eff through endpoint-blind T_tau_CMB.",
        "derived_status": "TRANSFER_OPERATOR_REQUIRED",
        "dimension_status": "T_tau_CMB dimensionless if it maps potential to potential; otherwise units must be declared.",
        "blocks": "numeric or analytic T_tau_CMB operator is not supplied",
    },
    {
        "row_id": "TCMBCDS01_005",
        "layer": "lensing_projection_kernel",
        "symbol": "K_tau_PP(L; a,k) dmu(a,k)",
        "definition_or_target": "Project Phi_lens_tau(a,k) to a PP or delta_PP_tau L-space grid through a declared lensing window/kernel, support, measure, and L mapping.",
        "derived_status": "PROJECTION_KERNEL_REQUIRED",
        "dimension_status": "kernel-measure-normalization product must map Phi_lens_tau to selected PP/delta_PP_tau convention.",
        "blocks": "full K_tau_PP, measure, support, and normalization are not supplied",
    },
    {
        "row_id": "TCMBCDS01_006",
        "layer": "projection_formula",
        "symbol": "tau_PP(L)",
        "definition_or_target": "tau_PP(L) = N_projection_physical Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)].",
        "derived_status": "FORMULA_SCAFFOLD_NOT_ACCEPTED",
        "dimension_status": "requires finite N_projection_physical and audited PP/delta_PP_tau codomain units.",
        "blocks": "N_projection_physical, zero-source proof, dimension/sign audit, and firewall are not accepted",
    },
    {
        "row_id": "TCMBCDS01_007",
        "layer": "zero_source_limit",
        "symbol": "Phi_lens_tau -> 0 => tau_PP contribution -> 0",
        "definition_or_target": "If the operator is zero-preserving and kernel/measure/normalization are finite, the Tau contribution vanishes under zero source.",
        "derived_status": "PROOF_OBLIGATION_CONDITIONAL",
        "dimension_status": "not a dimension claim; depends on operator algebra and finite support.",
        "blocks": "cannot discharge until operator, kernel, and normalization are supplied",
    },
    {
        "row_id": "TCMBCDS01_008",
        "layer": "score_readout",
        "symbol": "L=10..3009 grid -> ACT/Planck comparison",
        "definition_or_target": "Only after the projection grid is generated endpoint-blind may a score adapter compare to CMB lensing data.",
        "derived_status": "PRESCORE_LOCKED",
        "dimension_status": "requires exact grid alignment and covariance/readout convention.",
        "blocks": "content audit blocks physical Tau-route score",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def write_table(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0].keys()))
        writer.writeheader()
        writer.writerows(ROWS)


def build_summary(table_path: Path) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_cosmology_derivation_spine_summary_v01",
        "claim_boundary": "tau_cmb_cosmology_derivation_spine_only_minimal_derivation_scaffold_no_boltzmann_solver_no_likelihood_no_dark_sector_verdict",
        "table": rel(table_path),
        "status": "DERIVATION_SPINE_DECLARED_PARTIAL_NOT_SCORE_ELIGIBLE",
        "rows": len(ROWS),
        "closed_rows": ["TCMBCDS01_001"],
        "conditional_rows": ["TCMBCDS01_002", "TCMBCDS01_003", "TCMBCDS01_007"],
        "blocked_rows": [
            "TCMBCDS01_004",
            "TCMBCDS01_005",
            "TCMBCDS01_006",
            "TCMBCDS01_008",
        ],
        "next_minimal_unblock": "derive_endpoint_blind_T_tau_CMB_and_K_tau_PP_with_N_projection_physical",
        "source_grounding_gate": "docs/tau_cmb_source_grounding_gate_v01.md",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(
        (
            f"- `{row['row_id']}` `{row['layer']}`: {row['derived_status']} | "
            f"`{row['symbol']}` | blocks: {row['blocks']}"
        )
        for row in ROWS
    )
    text = f"""# Tau CMB Cosmology Derivation Spine v01

**Doc class:** Tau-side cosmology derivation spine
**Reader role:** Paper 13 / Tau CMB implementer
**Status:** partial derivation scaffold; not a Boltzmann solver; not score eligible
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Purpose

This artifact turns the Paper 13 CMB requirement map into a minimal Tau-side
cosmology derivation chain. It does not claim that Tau Core has solved CMB
cosmology. It identifies the smallest mathematical spine that must be populated
before CMB lensing or dark-sector necessity can be tested.

## Derivation Chain

```text
Tau background/readout
-> rho_tau_eff(a,k)
-> Phi_tau_eff(a,k)
-> Phi_lens_tau(a,k) via T_tau_CMB
-> tau_PP(L) via K_tau_PP and N_projection_physical
-> endpoint-blind CMB score grid
```

## Rows

{rows}

## Minimal Formula Spine

```text
H_tau := d ln a_tau / d t_readout
rho_tau_eff(a,k) := A_tau(a,k) rho_ref(a)
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]
tau_PP(L) = N_projection_physical Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)]
```

## Status

```text
{summary["status"]}
```

The first three mathematical slots are definitions or comparison targets. The
score-critical blockers remain the endpoint-blind transfer operator
`T_tau_CMB`, the projection kernel/measure `K_tau_PP dmu`, the physical
normalization `N_projection_physical`, the zero-source proof, and the
post-population firewall.

## Source-Grounding Dependency

The effective source row `rho_tau_eff(a,k)` is not source-accepted by this
spine. It must pass the separate source-grounding gate before it can be used as
a Tau-derived CMB source:

```text
{summary["source_grounding_gate"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB cosmology derivation spine.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path)
    summary = build_summary(table_path)
    if args.write_summary:
        path = Path(args.write_summary)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(summary, Path(args.write_doc))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
