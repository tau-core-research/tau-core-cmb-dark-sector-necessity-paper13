#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_projection_normalization_spec_scaffold_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md"


ROWS = [
    {
        "row_id": "TCMBPNSS01_001",
        "component": "normalization_role",
        "required_content": "state whether N_projection_physical is fixed by operator convention or is a pre-score diagnostic parameter",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "role is declared before endpoint comparison",
        "failure_if": "normalization role is chosen after seeing alpha_star, residuals, or chi2",
    },
    {
        "row_id": "TCMBPNSS01_002",
        "component": "finite_value_or_range",
        "required_content": "finite exact value or finite prior/range",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "value/range is finite and endpoint-blind",
        "failure_if": "normalization is unbounded, NaN/inf, or post-score fitted",
    },
    {
        "row_id": "TCMBPNSS01_003",
        "component": "unit_dimension_role",
        "required_content": "units or dimensionless convention for N_projection_physical",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "units close with Phi_lens_tau, kernel-measure, and PP/delta_PP_tau codomain",
        "failure_if": "normalization silently absorbs unresolved unit mismatch",
    },
    {
        "row_id": "TCMBPNSS01_004",
        "component": "sign_convention",
        "required_content": "sign role of positive/negative Tau contribution",
        "current_status": "REQUIRED_NOT_FILLED",
        "acceptance_condition": "sign convention follows operator/domain definitions before score",
        "failure_if": "sign is selected to improve endpoint fit",
    },
    {
        "row_id": "TCMBPNSS01_005",
        "component": "zero_source_compatibility",
        "required_content": "finite normalization participates in zero-source limit proof",
        "current_status": "REQUIRED_NOT_PROVED",
        "acceptance_condition": "Phi_lens_tau=0 gives zero Tau contribution under finite N_projection_physical",
        "failure_if": "normalization introduces a source-independent additive term",
    },
    {
        "row_id": "TCMBPNSS01_006",
        "component": "provenance_firewall",
        "required_content": "hash/provenance/firewall record for normalization choice",
        "current_status": "REQUIRED_NOT_SUPPLIED",
        "acceptance_condition": "record shows no score output, residual, or verdict preference was used",
        "failure_if": "normalization cites endpoint score products or derived post-score alpha",
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
        "report_id": "cmb_tau_lensing_projection_normalization_spec_scaffold_summary_v01",
        "claim_boundary": "projection_normalization_spec_scaffold_only_no_numeric_normalization_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "target": "N_projection_physical",
        "status": "NORMALIZATION_SPEC_DECLARED_NOT_FILLED",
        "rows": len(ROWS),
        "missing_or_unproved_rows": [row["row_id"] for row in ROWS],
        "allowed_value_forms": [
            "operator-implied exact finite value",
            "endpoint-blind finite diagnostic prior/range",
            "explicit failure if no lawful normalization exists",
        ],
        "forbidden_sources": [
            "post-score alpha_star",
            "ACT/Planck residual minimization",
            "reduced chi2 tuning",
            "dark-sector verdict preference",
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
    allowed = "\n".join(f"- {item}" for item in summary["allowed_value_forms"])
    forbidden = "\n".join(f"- {item}" for item in summary["forbidden_sources"])
    text = f"""# CMB Tau Lensing Projection Normalization Spec Scaffold v01

**Doc class:** projection normalization spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** normalization schema declared; no numeric normalization accepted; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_normalization_requirement_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Target

```text
{summary["target"]}
```

## Required Rows

{rows}

## Allowed Value Forms

{allowed}

## Forbidden Sources

{forbidden}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build projection normalization spec scaffold.")
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
