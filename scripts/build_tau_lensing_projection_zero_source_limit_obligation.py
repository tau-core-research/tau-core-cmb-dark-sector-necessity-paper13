#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_projection_zero_source_limit_obligation_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_zero_source_limit_obligation_v01.md"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def build_report() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_projection_zero_source_limit_obligation_v01",
        "claim_boundary": "projection_zero_source_limit_obligation_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "status": "PROOF_OBLIGATION_DECLARED_NOT_DISCHARGED",
        "target_statement": "Phi_lens_tau(a,k) -> 0 implies projected Tau contribution -> 0",
        "scaffold_equation": (
            "tau_PP(L) = N_projection_physical * Integral[K_tau_PP(L; a,k) "
            "Phi_lens_tau(a,k) dmu(a,k)]"
        ),
        "sufficient_conditions": [
            {
                "condition": "linearity_or_declared_zero-preserving_nonlinearity",
                "requirement": "Projection_PP[0](L)=0, or every nonlinear term contains at least one Phi_lens_tau factor and no source-independent additive term.",
                "status": "PROJECTION_EQUATION_SPEC_DECLARED_NOT_FILLED",
            },
            {
                "condition": "finite_kernel_measure",
                "requirement": "K_tau_PP(L; a,k)dmu(a,k) is finite/integrable on the declared support for each L=10..3009.",
                "status": "KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED",
            },
            {
                "condition": "finite_normalization",
                "requirement": "N_projection_physical is finite and fixed before endpoint comparison.",
                "status": "NORMALIZATION_SPEC_DECLARED_NOT_FILLED",
            },
            {
                "condition": "no_hidden_baseline",
                "requirement": "Any fiducial PP baseline is outside the Tau contribution and is not counted as nonzero Tau response.",
                "status": "DECLARED_REQUIRED",
            },
            {
                "condition": "delta_route_consistency",
                "requirement": "If using delta_PP_tau, the zero-source limit applies to delta_PP_tau(L), not to the fiducial PP baseline.",
                "status": "DECLARED_REQUIRED",
            },
        ],
        "algebraic_discharge_rule": (
            "If the supplied operator is zero-preserving and the kernel measure and normalization are finite, "
            "then substituting Phi_lens_tau=0 gives tau_PP_tau_contribution(L)=0 for every L."
        ),
        "current_result": "NOT_DISCHARGED_BECAUSE_OPERATOR_KERNEL_AND_NORMALIZATION_NOT_SUPPLIED",
        "blocked_shortcuts": [
            "do not use the synthetic zero-control route as proof of the physical projection operator",
            "do not infer zero-source behavior from a scored residual",
            "do not hide a nonzero additive Tau term inside the fiducial PP baseline",
        ],
        "source_links": [
            "docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md",
            "docs/cmb_tau_lensing_projection_equation_spec_scaffold_v01.md",
            "docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md",
            "docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md",
            "docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md",
            "docs/cmb_tau_lensing_projection_normalization_requirement_v01.md",
            "docs/cmb_tau_lensing_zero_response_control_v01.md",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    conditions = "\n".join(
        f"- `{item['condition']}`: {item['status']} | {item['requirement']}"
        for item in report["sufficient_conditions"]
    )
    shortcuts = "\n".join(f"- {item}" for item in report["blocked_shortcuts"])
    sources = "\n".join(f"- `{item}`" for item in report["source_links"])
    text = f"""# CMB Tau Lensing Projection Zero-Source Limit Obligation v01

**Doc class:** projection zero-source proof obligation
**Reader role:** Paper 13 Tau-grid implementer
**Status:** proof obligation declared; not discharged; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Target Statement

```text
{report["target_statement"]}
```

## Scaffold Equation

```text
{report["scaffold_equation"]}
```

## Sufficient Conditions

{conditions}

## Algebraic Discharge Rule

```text
{report["algebraic_discharge_rule"]}
```

## Current Result

```text
{report["current_result"]}
```

## Blocked Shortcuts

{shortcuts}

## Source Links

{sources}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build physical projection zero-source limit obligation.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(report, Path(args.write_doc))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
