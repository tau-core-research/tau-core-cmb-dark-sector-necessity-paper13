#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md"


ROWS = [
    {
        "row_id": "TCMBPKMSS01_001",
        "kernel_component": "domain_support",
        "required_content": "declared a,k support for Phi_lens_tau(a,k)",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "support is inherited from endpoint-blind Phi_tau_eff/T_tau_CMB artifacts and fixed before score readout",
        "failure_if": "support is selected after endpoint residual inspection",
    },
    {
        "row_id": "TCMBPKMSS01_002",
        "kernel_component": "measure_definition",
        "required_content": "dmu(a,k) or discrete sum weights",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "measure, quadrature/binning weights, and integration/sum limits are explicit and finite",
        "failure_if": "measure absorbs arbitrary amplitude or leaves normalization underdetermined",
    },
    {
        "row_id": "TCMBPKMSS01_003",
        "kernel_component": "L_mapping",
        "required_content": "mapping from a,k support to L=10..3009 output",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "each output L has a declared projection rule and exact 3000-row alignment",
        "failure_if": "L alignment is inferred from best score or bandpower residual behavior",
    },
    {
        "row_id": "TCMBPKMSS01_004",
        "kernel_component": "kernel_units_and_sign",
        "required_content": "units/sign role of K_tau_PP(L; a,k)",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "kernel times measure times Phi_lens_tau maps into selected PP/delta_PP_tau convention",
        "failure_if": "sign or units are chosen to improve fit after scoring",
    },
    {
        "row_id": "TCMBPKMSS01_005",
        "kernel_component": "integrability_bound",
        "required_content": "finite/integrable kernel-measure condition for every L",
        "current_status": "REQUIRED_NOT_PROVED",
        "acceptance_condition": "finite replay values follow from declared support, kernel, measure, and finite input field",
        "failure_if": "kernel can diverge or produce non-finite grid values without an explicit regularization rule",
    },
    {
        "row_id": "TCMBPKMSS01_006",
        "kernel_component": "kernel_artifact",
        "required_content": "equation, table, or integral artifact with hash/provenance",
        "current_status": "REQUIRED_NOT_SUPPLIED",
        "acceptance_condition": "artifact is hash-bound and produced before endpoint comparison",
        "failure_if": "kernel artifact is edited or selected using score output",
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
        "report_id": "cmb_tau_lensing_projection_kernel_measure_spec_scaffold_summary_v01",
        "claim_boundary": "projection_kernel_measure_spec_scaffold_only_no_kernel_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "status": "KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED",
        "operator_component": "K_tau_PP(L; a,k)dmu(a,k)",
        "rows": len(ROWS),
        "missing_or_unproved_rows": [row["row_id"] for row in ROWS],
        "unblocks_when": [
            "domain support is inherited from endpoint-blind Phi artifacts",
            "measure and L mapping are explicit",
            "kernel units/sign convention is dimensionally compatible with PP or delta_PP_tau",
            "integrability/finite replay condition is proved or enforced",
            "kernel artifact is hash-bound before endpoint comparison",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(
        (
            f"- `{row['row_id']}` `{row['kernel_component']}`: {row['current_status']} | "
            f"required: {row['required_content']} | failure if: {row['failure_if']}"
        )
        for row in ROWS
    )
    unblocks = "\n".join(f"- {item}" for item in summary["unblocks_when"])
    text = f"""# CMB Tau Lensing Projection Kernel/Measure Spec Scaffold v01

**Doc class:** projection kernel/measure spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** kernel/measure schema declared; no kernel accepted; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Target Component

```text
{summary["operator_component"]}
```

## Required Rows

{rows}

## Unblocks When

{unblocks}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build projection kernel/measure spec scaffold.")
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
