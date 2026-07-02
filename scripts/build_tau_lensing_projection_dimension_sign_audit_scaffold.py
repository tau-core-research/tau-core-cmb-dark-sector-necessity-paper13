#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md"


ROWS = [
    {
        "audit_row_id": "TCMBPDSAS01_001",
        "component": "Phi_lens_tau_domain",
        "required_declaration": "dimension and sign convention for Phi_lens_tau(a,k)",
        "current_status": "DECLARED_REQUIRED_NOT_FILLED",
        "acceptance_condition": "Phi_lens_tau convention is inherited from endpoint-blind Phi_tau_eff and T_tau_CMB without endpoint residual input.",
        "failure_if": "potential sign or dimension is chosen after seeing ACT/Planck score behavior",
    },
    {
        "audit_row_id": "TCMBPDSAS01_002",
        "component": "kernel_measure",
        "required_declaration": "dimension of K_tau_PP(L; a,k) dmu(a,k)",
        "current_status": "KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED",
        "acceptance_condition": "kernel times measure maps Phi_lens_tau into the selected PP/delta_PP_tau codomain with declared units; tracked in docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md.",
        "failure_if": "kernel absorbs an arbitrary post-score amplitude or has unspecified integration/sum measure",
    },
    {
        "audit_row_id": "TCMBPDSAS01_003",
        "component": "N_projection_physical",
        "required_declaration": "unit/sign role of N_projection_physical",
        "current_status": "NORMALIZATION_SPEC_DECLARED_NOT_FILLED",
        "acceptance_condition": "normalization is implied by the operator convention or declared as a pre-score diagnostic parameter range; tracked in docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md.",
        "failure_if": "normalization is set from alpha_star, chi2 minimization, or residual matching",
    },
    {
        "audit_row_id": "TCMBPDSAS01_004",
        "component": "PP_codomain",
        "required_declaration": "PP versus delta_PP_tau convention and L=10..3009 alignment",
        "current_status": "CODOMAIN_CONTRACT_LOCKED_NO_VALUES",
        "acceptance_condition": "output convention matches the reduced adapter route before materialization.",
        "failure_if": "tau_PP and delta_PP_tau are mixed without an explicit fiducial PP reference",
    },
    {
        "audit_row_id": "TCMBPDSAS01_005",
        "component": "zero_source_limit",
        "required_declaration": "Phi_lens_tau -> 0 implies projection contribution -> 0",
        "current_status": "PROOF_OBLIGATION_DECLARED_NOT_DISCHARGED",
        "acceptance_condition": "zero-source limit follows algebraically from the supplied operator and normalization; tracked in docs/cmb_tau_lensing_projection_zero_source_limit_obligation_v01.md.",
        "failure_if": "operator has an additive nonzero term not declared as a separate baseline/fiducial contribution",
    },
    {
        "audit_row_id": "TCMBPDSAS01_006",
        "component": "endpoint_firewall",
        "required_declaration": "no endpoint score quantities used in convention choices",
        "current_status": "REQUIRED_AFTER_VALUES",
        "acceptance_condition": "firewall reruns after operator, normalization, and replay are populated.",
        "failure_if": "any convention row cites score outputs, residuals, or dark-sector verdict preference",
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
        "report_id": "cmb_tau_lensing_projection_dimension_sign_audit_scaffold_summary_v01",
        "claim_boundary": "projection_dimension_sign_audit_scaffold_only_no_operator_acceptance_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "status": "AUDIT_SCHEMA_DECLARED_NOT_FILLED",
        "rows": len(ROWS),
        "accepted_rows": [
            row["audit_row_id"]
            for row in ROWS
            if row["current_status"].startswith("CODOMAIN_CONTRACT_LOCKED")
        ],
        "blocked_or_unproved_rows": [
            row["audit_row_id"]
            for row in ROWS
            if not row["current_status"].startswith("CODOMAIN_CONTRACT_LOCKED")
        ],
        "unblocks_when": [
            "each declaration row is filled from endpoint-blind operator evidence",
            "zero-source limit is proved from the supplied operator",
            "post-population endpoint firewall passes",
            "N_projection_physical is derived or declared as a pre-score diagnostic parameter range",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(
        (
            f"- `{row['audit_row_id']}` `{row['component']}`: {row['current_status']} | "
            f"required: {row['required_declaration']} | failure if: {row['failure_if']}"
        )
        for row in ROWS
    )
    unblocks = "\n".join(f"- {item}" for item in summary["unblocks_when"])
    text = f"""# CMB Tau Lensing Projection Dimension/Sign Audit Scaffold v01

**Doc class:** projection dimension/sign audit scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** audit schema declared; values not filled; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Purpose

This table narrows the `dimension_and_sign_audit` blocker in the projection
operator formula-spec scaffold. It does not accept a physical projection
operator and does not populate `N_projection_physical`.

## Audit Rows

{rows}

## Unblocks When

{unblocks}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build projection dimension/sign audit scaffold.")
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
