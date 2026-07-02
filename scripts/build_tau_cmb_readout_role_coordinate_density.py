#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACOUSTIC_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_audit_v01.json"
DENSITY_CLOSURE = ROOT / "data/derived/tau_cmb_density_amplitude_closure_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_density_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_density_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_density_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_density_v01_coordinate_candidate_only_"
    "not_materialized_no_density_score_no_omega_c_h2_match_no_concrete_R_CMB_no_carrier_certification_no_verdict"
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
    "allows_density_score",
    "allows_omega_c_h2_match",
    "allows_concrete_R_CMB",
    "allows_carrier_certification",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "coordinate_component": "density_ratio_guard",
        "formal_slot": "A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)",
        "candidate_definition": "density coordinate may use the formal ratio only under a shared density-normalization convention",
        "source_dependency": "tau_cmb_density_amplitude_closure_v01",
        "blocked_by": "shared density normalization convention still required before numerical use",
        "coordinate_status": "CONDITIONAL_RATIO_GUARD_DECLARED_NOT_NUMERIC",
        "dimension_role": "dimensionless ratio if both densities share normalization",
    },
    {
        "coordinate_component": "tau_effective_density",
        "formal_slot": "rho_tau_eff(a,k)",
        "candidate_definition": "density coordinate requires a Tau-derived effective density function",
        "source_dependency": "tau_cmb_density_amplitude_closure_v01",
        "blocked_by": "rho_tau_eff is still a source slot rather than a derived function",
        "coordinate_status": "BLOCKED_DENSITY_FORMULA_NOT_DERIVED",
        "dimension_role": "density role; units only after source formula and rho_ref convention",
    },
    {
        "coordinate_component": "endpoint_blind_amplitude",
        "formal_slot": "endpoint_blind(A_tau)",
        "candidate_definition": "A_tau must be derived before density residual fitting or likelihood tuning",
        "source_dependency": "tau_cmb_density_amplitude_closure_v01",
        "blocked_by": "no provenance rule proves independence from CMB residual fitting",
        "coordinate_status": "BLOCKED_ENDPOINT_BLIND_AMPLITUDE_MISSING",
        "dimension_role": "dimensionless amplitude role",
    },
    {
        "coordinate_component": "omega_c_h2_role_comparison",
        "formal_slot": "Omega_c h^2 comparison role",
        "candidate_definition": "density coordinate may compare to Omega_c h^2 only after numeric A_tau prediction and benchmark convention",
        "source_dependency": "tau_cmb_density_amplitude_closure_v01",
        "blocked_by": "no benchmark, likelihood, or numeric A_tau prediction",
        "coordinate_status": "BLOCKED_NO_NUMERICAL_COMPARISON",
        "dimension_role": "comparison role; not a new unit claim",
    },
    {
        "coordinate_component": "density_stop_rule",
        "formal_slot": "density_fail_if_A_tau_missing",
        "candidate_definition": "coordinate keeps a stop/fail branch if endpoint-blind A_tau cannot be derived",
        "source_dependency": "tau_cmb_scorecard_blocker_closure_plan_v01",
        "blocked_by": "derive endpoint-blind A_tau or explicitly fail the density role",
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
            "coordinate_row_id": f"TCMBRRCD01_{index:03d}",
            "allows_coordinate_acceptance": "false",
            "allows_density_score": "false",
            "allows_omega_c_h2_match": "false",
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
    acoustic_audit = load_json(ACOUSTIC_AUDIT) if ACOUSTIC_AUDIT.exists() else {}
    input_ok = (
        acoustic_audit.get("status") == "ACOUSTIC_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED"
        and acoustic_audit.get("failed_rows") == 0
        and DENSITY_CLOSURE.exists()
    )
    return {
        "report_id": "tau_cmb_readout_role_coordinate_density_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_acoustic_coordinate_audit": rel(ACOUSTIC_AUDIT),
        "input_acoustic_coordinate_audit_clean": input_ok,
        "coordinate_symbol": "e_density",
        "coordinate_rows": len(rows),
        "blocked_rows": sum(row["coordinate_status"].startswith("BLOCKED") for row in rows),
        "guard_rows": sum("GUARD" in row["coordinate_status"] or "STOP_RULE" in row["coordinate_status"] for row in rows),
        "coordinate_acceptance_allowed": False,
        "density_score_allowed": False,
        "omega_c_h2_match_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "DENSITY_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED"
            if input_ok
            else "DENSITY_ROLE_COORDINATE_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_coordinate_density_audit_v01"
            if input_ok
            else "repair_density_coordinate_inputs"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['coordinate_row_id']}` `{row['coordinate_component']}`: {row['coordinate_status']} | `{row['formal_slot']}`"
        for row in rows
    )
    text = f"""# Tau CMB Readout Role Coordinate Density v01

**Doc class:** density role-coordinate candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the candidate components of the density readout role
coordinate `e_density`. It is not a density score, not an `Omega_c h^2` match,
not a CMB likelihood, not a concrete `R_CMB` map, and not evidence for a
dark-sector verdict.

## Coordinate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The density coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because `rho_tau_eff(a,k)`, endpoint-blind `A_tau(a,k)`,
and a numerical `Omega_c h^2` comparison are not supplied.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB density readout role-coordinate candidate.")
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
