#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LENSING_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_lensing_audit_v01.json"
GROWTH_CLOSURE = ROOT / "data/derived/tau_cmb_growth_transfer_kernel_closure_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_growth_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_growth_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_growth_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_growth_v01_coordinate_candidate_only_"
    "not_materialized_no_growth_score_no_structure_match_no_concrete_R_CMB_"
    "no_carrier_certification_no_verdict"
)

FIELDS = [
    "coordinate_row_id",
    "coordinate_component",
    "formal_slot",
    "candidate_definition",
    "source_dependency",
    "blocked_by",
    "coordinate_status",
    "dimension_role",
    "allows_coordinate_acceptance",
    "allows_growth_score",
    "allows_structure_match",
    "allows_concrete_R_CMB",
    "allows_carrier_certification",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "coordinate_component": "domain_specification",
        "formal_slot": "X_tau_CMB or (rho_tau_eff,Phi_tau_eff)",
        "candidate_definition": "growth coordinate must select an endpoint-blind input object before propagation",
        "source_dependency": "tau_cmb_growth_transfer_kernel_closure_v01",
        "blocked_by": "domain family is narrowed but no single input object is selected",
        "coordinate_status": "PARTIAL_DOMAIN_GUARD_DECLARED_NOT_SELECTED",
        "dimension_role": "domain convention role; units depend on selected input object",
    },
    {
        "coordinate_component": "codomain_specification",
        "formal_slot": "Y_growth_tau(k,a)",
        "candidate_definition": "growth coordinate must select an observable-side comparison variable and normalization",
        "source_dependency": "tau_cmb_growth_transfer_kernel_closure_v01",
        "blocked_by": "codomain family is narrowed but no comparison variable is selected",
        "coordinate_status": "PARTIAL_CODOMAIN_GUARD_DECLARED_NOT_SELECTED",
        "dimension_role": "codomain convention role; normalized only after comparison variable is fixed",
    },
    {
        "coordinate_component": "time_scale_convention",
        "formal_slot": "K_growth[k,a_initial,a_final,N_growth]",
        "candidate_definition": "growth coordinate requires k convention, scale-factor convention, epochs, and normalization point",
        "source_dependency": "tau_cmb_growth_transfer_kernel_closure_v01",
        "blocked_by": "concrete numeric convention still required before score use",
        "coordinate_status": "CONDITIONAL_TIME_SCALE_GUARD_DECLARED_NOT_NUMERIC",
        "dimension_role": "time/scale convention guard; no standalone physical unit claim",
    },
    {
        "coordinate_component": "operator_rule",
        "formal_slot": "Transfer_tau[X_tau_CMB](k,a)",
        "candidate_definition": "growth coordinate requires a lawful propagation operator, reduced evolution equation, or explicit failure",
        "source_dependency": "tau_cmb_growth_transfer_kernel_closure_v01",
        "blocked_by": "no transfer operator, reduced evolution equation, or propagation rule is supplied",
        "coordinate_status": "BLOCKED_OPERATOR_RULE_NOT_DERIVED",
        "dimension_role": "operator role; dimension depends on domain/codomain normalization",
    },
    {
        "coordinate_component": "cross_role_consistency",
        "formal_slot": "Consistent(T_tau_CMB,e_density,e_acoustic,e_lensing)",
        "candidate_definition": "growth support must not contradict density, acoustic, or lensing readout roles",
        "source_dependency": "tau_cmb_readout_role_coordinate_lensing_audit_v01; tau_cmb_growth_transfer_kernel_closure_v01",
        "blocked_by": "dependent density, acoustic, and lensing coordinates remain blocked and unmaterialized",
        "coordinate_status": "BLOCKED_DEPENDENT_ROLES_STILL_OPEN",
        "dimension_role": "consistency role; no physical units",
    },
    {
        "coordinate_component": "growth_stop_rule",
        "formal_slot": "growth_fail_if_transfer_operator_or_consistency_missing",
        "candidate_definition": "coordinate keeps a stop/fail branch if no lawful growth transfer or role-consistency route can be supplied",
        "source_dependency": "tau_cmb_known_limit_failure_map_v01",
        "blocked_by": "run reduced checks or explicitly assign FAIL after transfer evaluation",
        "coordinate_status": "STOP_RULE_DECLARED_NOT_TRIGGERED",
        "dimension_role": "decision guard; no physical units",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "coordinate_row_id": f"TCMBRRCG01_{index:03d}",
            "allows_coordinate_acceptance": "false",
            "allows_growth_score": "false",
            "allows_structure_match": "false",
            "allows_concrete_R_CMB": "false",
            "allows_carrier_certification": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(ROWS, start=1)
    ]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    lensing_audit = load_json(LENSING_AUDIT) if LENSING_AUDIT.exists() else {}
    input_ok = (
        lensing_audit.get("status") == "LENSING_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED"
        and lensing_audit.get("failed_rows") == 0
        and GROWTH_CLOSURE.exists()
    )
    return {
        "report_id": "tau_cmb_readout_role_coordinate_growth_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_lensing_coordinate_audit": rel(LENSING_AUDIT),
        "input_lensing_coordinate_audit_clean": input_ok,
        "input_growth_transfer_closure": rel(GROWTH_CLOSURE),
        "coordinate_symbol": "e_growth",
        "coordinate_rows": len(rows),
        "blocked_rows": sum(row["coordinate_status"].startswith("BLOCKED") for row in rows),
        "guard_rows": sum("GUARD" in row["coordinate_status"] or "STOP_RULE" in row["coordinate_status"] for row in rows),
        "coordinate_acceptance_allowed": False,
        "growth_score_allowed": False,
        "structure_match_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "GROWTH_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED"
            if input_ok
            else "GROWTH_ROLE_COORDINATE_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_coordinate_growth_audit_v01"
            if input_ok
            else "repair_growth_coordinate_inputs"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['coordinate_row_id']}` `{row['coordinate_component']}`: {row['coordinate_status']} | `{row['formal_slot']}`"
        for row in rows
    )
    text = f"""# Tau CMB Readout Role Coordinate Growth v01

**Doc class:** growth role-coordinate candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the candidate components of the growth readout role
coordinate `e_growth`. It is not a growth score, not a structure-growth match,
not a CMB likelihood, not a concrete `R_CMB` map, and not evidence for a
dark-sector verdict.

## Coordinate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The growth coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because no endpoint-blind domain/codomain selection,
numeric time/scale convention, lawful transfer operator, or cross-role
consistency proof is supplied in score-ready form.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB growth readout role-coordinate candidate.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
