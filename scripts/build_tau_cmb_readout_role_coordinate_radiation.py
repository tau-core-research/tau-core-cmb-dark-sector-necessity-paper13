#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GROWTH_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_growth_audit_v01.json"
RADIATION_EVALUATION = ROOT / "data/derived/tau_cmb_radiation_guard_evaluation_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_radiation_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_radiation_v01_coordinate_candidate_only_"
    "not_materialized_no_radiation_score_no_neff_bound_eval_no_concrete_R_CMB_"
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
    "allows_radiation_score",
    "allows_neff_bound_eval",
    "allows_concrete_R_CMB",
    "allows_carrier_certification",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "coordinate_component": "tau_radiation_like_contribution",
        "formal_slot": "Delta_N_eff_tau",
        "candidate_definition": "radiation coordinate requires a Tau-derived dimensionless radiation-like contribution under the adopted convention",
        "source_dependency": "tau_cmb_radiation_guard_evaluation_v01",
        "blocked_by": "Delta_N_eff_tau is declared as a slot but not derived from Tau response",
        "coordinate_status": "BLOCKED_TAU_DELTA_NEFF_NOT_DERIVED",
        "dimension_role": "dimensionless effective relativistic-degree contribution after convention lock",
    },
    {
        "coordinate_component": "external_bound_convention",
        "formal_slot": "Delta_N_eff_bound",
        "candidate_definition": "radiation coordinate requires the external Neff/damping-tail convention and dataset family before comparison",
        "source_dependency": "tau_cmb_radiation_guard_bound_check_v01",
        "blocked_by": "concrete numeric bound and provenance are not selected",
        "coordinate_status": "CONDITIONAL_BOUND_CONVENTION_GUARD_DECLARED_NOT_NUMERIC",
        "dimension_role": "dimensionless bound convention guard",
    },
    {
        "coordinate_component": "damping_tail_inequality",
        "formal_slot": "Delta_N_eff_tau <= Delta_N_eff_bound",
        "candidate_definition": "radiation coordinate requires numerical evaluation of the Tau contribution against the adopted bound",
        "source_dependency": "tau_cmb_radiation_guard_evaluation_v01",
        "blocked_by": "no numerical left-hand side or selected bound is evaluated",
        "coordinate_status": "BLOCKED_BOUND_INEQUALITY_NOT_EVALUATED",
        "dimension_role": "dimensionless inequality under shared convention",
    },
    {
        "coordinate_component": "cross_role_consistency",
        "formal_slot": "Consistent(Delta_N_eff_tau,A_tau,Phi_tau_eff,T_tau_CMB)",
        "candidate_definition": "radiation guard must not contradict density, acoustic, lensing, or growth readout roles",
        "source_dependency": "tau_cmb_readout_role_coordinate_growth_audit_v01; tau_cmb_radiation_guard_evaluation_v01",
        "blocked_by": "dependent density, acoustic, lensing, and growth coordinates remain blocked and unmaterialized",
        "coordinate_status": "BLOCKED_DEPENDENT_ROLES_STILL_OPEN",
        "dimension_role": "consistency role; no physical units",
    },
    {
        "coordinate_component": "radiation_stop_rule",
        "formal_slot": "radiation_fail_if_delta_neff_missing_or_bound_violated",
        "candidate_definition": "coordinate keeps a stop/fail branch if Tau contribution cannot be defined or exceeds the adopted bound",
        "source_dependency": "tau_cmb_known_limit_failure_map_v01",
        "blocked_by": "run the guard or explicitly assign FAIL after convention and contribution evaluation",
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
            "coordinate_row_id": f"TCMBRRCR01_{index:03d}",
            "allows_coordinate_acceptance": "false",
            "allows_radiation_score": "false",
            "allows_neff_bound_eval": "false",
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
    growth_audit = load_json(GROWTH_AUDIT) if GROWTH_AUDIT.exists() else {}
    input_ok = (
        growth_audit.get("status") == "GROWTH_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED"
        and growth_audit.get("failed_rows") == 0
        and RADIATION_EVALUATION.exists()
    )
    return {
        "report_id": "tau_cmb_readout_role_coordinate_radiation_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_growth_coordinate_audit": rel(GROWTH_AUDIT),
        "input_growth_coordinate_audit_clean": input_ok,
        "input_radiation_guard_evaluation": rel(RADIATION_EVALUATION),
        "coordinate_symbol": "e_radiation",
        "coordinate_rows": len(rows),
        "blocked_rows": sum(row["coordinate_status"].startswith("BLOCKED") for row in rows),
        "guard_rows": sum("GUARD" in row["coordinate_status"] or "STOP_RULE" in row["coordinate_status"] for row in rows),
        "coordinate_acceptance_allowed": False,
        "radiation_score_allowed": False,
        "neff_bound_eval_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "RADIATION_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED"
            if input_ok
            else "RADIATION_ROLE_COORDINATE_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_coordinate_radiation_audit_v01"
            if input_ok
            else "repair_radiation_coordinate_inputs"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['coordinate_row_id']}` `{row['coordinate_component']}`: {row['coordinate_status']} | `{row['formal_slot']}`"
        for row in rows
    )
    text = f"""# Tau CMB Readout Role Coordinate Radiation v01

**Doc class:** radiation role-coordinate candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the candidate components of the radiation/damping-tail
readout role coordinate `e_radiation`. It is not a radiation score, not a
numerical `Delta_N_eff` bound evaluation, not a CMB likelihood, not a concrete
`R_CMB` map, and not evidence for a dark-sector verdict.

## Coordinate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The radiation coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because `Delta_N_eff_tau`, the selected external bound,
the damping-tail inequality, and cross-role consistency are not supplied in
score-ready form.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB radiation readout role-coordinate candidate.")
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
