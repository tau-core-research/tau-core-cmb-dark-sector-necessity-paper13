#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_v01.md"


ROWS = [
    {
        "row_id": "TCMBPPFSS01_001",
        "component": "operator_artifact_firewall",
        "required_content": "operator/equation artifact created without score, residual, or verdict inputs",
        "current_status": "REQUIRED_AFTER_VALUES",
        "acceptance_condition": "artifact provenance predates endpoint comparison and excludes score products",
        "failure_if": "operator artifact cites alpha_star, chi2, residuals, or score outputs",
    },
    {
        "row_id": "TCMBPPFSS01_002",
        "component": "kernel_measure_firewall",
        "required_content": "kernel/measure artifact created without endpoint fit feedback",
        "current_status": "REQUIRED_AFTER_VALUES",
        "acceptance_condition": "kernel support, measure, and L mapping are fixed endpoint-blind",
        "failure_if": "kernel choices are selected to improve bandpower agreement",
    },
    {
        "row_id": "TCMBPPFSS01_003",
        "component": "normalization_firewall",
        "required_content": "N_projection_physical value/range provenance excludes post-score scaling",
        "current_status": "REQUIRED_AFTER_VALUES",
        "acceptance_condition": "normalization is operator-implied or pre-score diagnostic range",
        "failure_if": "normalization is set from post-score alpha_star or residual minimization",
    },
    {
        "row_id": "TCMBPPFSS01_004",
        "component": "output_grid_firewall",
        "required_content": "3000-row grid replay excludes score outputs and hand-fit edits",
        "current_status": "REQUIRED_AFTER_VALUES",
        "acceptance_condition": "grid is replayed from hash-bound physical projection inputs",
        "failure_if": "grid values are edited after score or selected from endpoint performance",
    },
    {
        "row_id": "TCMBPPFSS01_005",
        "component": "route_choice_firewall",
        "required_content": "direct PP versus delta route chosen before endpoint score",
        "current_status": "REQUIRED_AFTER_VALUES",
        "acceptance_condition": "route choice matches equation baseline/delta policy and is predeclared",
        "failure_if": "route choice is switched after comparing score outcomes",
    },
    {
        "row_id": "TCMBPPFSS01_006",
        "component": "score_separation_firewall",
        "required_content": "physical projection replay completed before guarded score execution",
        "current_status": "REQUIRED_AFTER_VALUES",
        "acceptance_condition": "score receipt timestamp/hash follows accepted projection replay packet",
        "failure_if": "score execution precedes or participates in projection construction",
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
        "report_id": "cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_summary_v01",
        "claim_boundary": "projection_post_population_firewall_spec_scaffold_only_no_firewall_pass_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "status": "POST_POPULATION_FIREWALL_SPEC_DECLARED_NOT_RUN",
        "rows": len(ROWS),
        "pending_rows": [row["row_id"] for row in ROWS],
        "scope": "firewall requirements after operator, kernel, normalization, and output grid values are populated",
        "not_a_certificate": "current skeleton PASS_FOR_CURRENT_SKELETON_ONLY remains separate",
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
    text = f"""# CMB Tau Lensing Projection Post-Population Firewall Spec Scaffold v01

**Doc class:** projection post-population firewall spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** firewall schema declared; not run; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Scope

```text
{summary["scope"]}
```

This is not the current skeleton certificate:

```text
{summary["not_a_certificate"]}
```

## Required Rows

{rows}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build projection post-population firewall spec scaffold.")
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
