#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_projection_equation_spec_scaffold_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_projection_equation_spec_scaffold_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_equation_spec_scaffold_v01.md"


ROWS = [
    {
        "row_id": "TCMBPESS01_001",
        "component": "operator_equation_form",
        "required_content": "closed equation, discrete sum, kernel table rule, or explicit failure",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "equation form is fixed before endpoint comparison and references kernel/measure/normalization artifacts",
        "failure_if": "operator form is chosen after inspecting score behavior",
    },
    {
        "row_id": "TCMBPESS01_002",
        "component": "linearity_policy",
        "required_content": "linear, affine-with-baseline, or declared zero-preserving nonlinear operator policy",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "policy is compatible with the zero-source obligation",
        "failure_if": "operator includes undeclared source-independent additive Tau term",
    },
    {
        "row_id": "TCMBPESS01_003",
        "component": "baseline_delta_policy",
        "required_content": "declare tau_PP direct output or delta_PP_tau relative to named fiducial PP",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "baseline/fiducial contribution is separated from Tau contribution",
        "failure_if": "fiducial PP and Tau contribution are mixed without a named delta convention",
    },
    {
        "row_id": "TCMBPESS01_004",
        "component": "composition_order",
        "required_content": "Phi_tau_eff -> T_tau_CMB -> Phi_lens_tau -> Projection_PP -> PP/delta_PP_tau",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "operator composition order is explicit and hash-bound",
        "failure_if": "adapter replay B_ACT @ grid is substituted for the physical projection equation",
    },
    {
        "row_id": "TCMBPESS01_005",
        "component": "materialization_rule",
        "required_content": "recipe to produce exactly 3000 finite values for L=10..3009",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "recipe can be replayed without endpoint score data",
        "failure_if": "materialization requires score output, residuals, or hand-edited endpoint fitting",
    },
    {
        "row_id": "TCMBPESS01_006",
        "component": "formula_artifact",
        "required_content": "equation/table/integral artifact with provenance, hash, and claim boundary",
        "current_status": "REQUIRED_NOT_SUPPLIED",
        "acceptance_condition": "artifact is available before score and references all dependent specs",
        "failure_if": "formula artifact is missing or generated from post-score diagnostics",
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
        "report_id": "cmb_tau_lensing_projection_equation_spec_scaffold_summary_v01",
        "claim_boundary": "projection_equation_spec_scaffold_only_no_equation_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "target": "Projection_PP[Phi_lens_tau](L)",
        "status": "PROJECTION_EQUATION_SPEC_DECLARED_NOT_FILLED",
        "rows": len(ROWS),
        "missing_or_unproved_rows": [row["row_id"] for row in ROWS],
        "minimal_scaffold_equation": (
            "tau_PP_tau_contribution(L) = N_projection_physical * "
            "Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)]"
        ),
        "blocked_shortcuts": [
            "do not use B_ACT @ grid as the physical projection equation",
            "do not hide a nonzero Tau term in the fiducial PP baseline",
            "do not choose operator form from post-score residuals",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(
        (
            f"- `{row['row_id']}` `{row['component']}`: {row['current_status']} | "
            f"required: {row['required_content']} | failure if: {row['failure_if']}"
        )
        for row in ROWS
    )
    shortcuts = "\n".join(f"- {item}" for item in summary["blocked_shortcuts"])
    text = f"""# CMB Tau Lensing Projection Equation Spec Scaffold v01

**Doc class:** projection equation spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** equation schema declared; no equation accepted; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Target

```text
{summary["target"]}
```

## Minimal Scaffold Equation

```text
{summary["minimal_scaffold_equation"]}
```

## Required Rows

{rows}

## Blocked Shortcuts

{shortcuts}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build projection equation spec scaffold.")
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
