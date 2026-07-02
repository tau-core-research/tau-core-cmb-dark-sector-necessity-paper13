#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DENSITY_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_density_audit_v01.json"
LENSING_REDUCED_EVALUATION = ROOT / "data/derived/tau_cmb_lensing_transfer_reduced_evaluation_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_lensing_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_lensing_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_lensing_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_lensing_v01_coordinate_candidate_only_"
    "not_materialized_no_lensing_score_no_act_planck_match_no_concrete_R_CMB_"
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
    "allows_lensing_score",
    "allows_act_planck_match",
    "allows_concrete_R_CMB",
    "allows_carrier_certification",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "coordinate_component": "lensing_potential_source",
        "formal_slot": "Phi_tau_eff(a,k)",
        "candidate_definition": "lensing coordinate requires a potential-like Tau source over the lensing-relevant scale and epoch range",
        "source_dependency": "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "blocked_by": "Phi_tau_eff remains a target slot rather than a derived lensing-era source",
        "coordinate_status": "BLOCKED_POTENTIAL_SOURCE_NOT_DERIVED",
        "dimension_role": "potential-source role; units only after metric handoff and normalization",
    },
    {
        "coordinate_component": "transfer_kernel",
        "formal_slot": "T_tau_CMB(k,a)",
        "candidate_definition": "lensing coordinate requires a transfer kernel from CMB-era response to lensing-era readout",
        "source_dependency": "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "blocked_by": "transfer operator domain, codomain, time/scale convention, and normalization are not specified",
        "coordinate_status": "BLOCKED_TRANSFER_KERNEL_NOT_SPECIFIED",
        "dimension_role": "operator role; convention-dependent until transfer law is supplied",
    },
    {
        "coordinate_component": "projection_geometry_guard",
        "formal_slot": "G_lens[line_of_sight,distance,kernel]",
        "candidate_definition": "projection geometry must be declared before any amplitude or shape comparison",
        "source_dependency": "tau_cmb_lensing_transfer_benchmark_v01",
        "blocked_by": "concrete numeric projection convention still required before score use",
        "coordinate_status": "CONDITIONAL_PROJECTION_GEOMETRY_GUARD_DECLARED_NOT_NUMERIC",
        "dimension_role": "geometry/convention guard; no standalone physical unit claim",
    },
    {
        "coordinate_component": "amplitude_shape_response",
        "formal_slot": "S_lens_tau(L) or delta S_lens_tau(L)",
        "candidate_definition": "lensing coordinate needs endpoint-blind amplitude/shape response before ACT/Planck comparison",
        "source_dependency": "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "blocked_by": "no reduced amplitude/shape tendency has been computed from Tau source plus transfer kernel",
        "coordinate_status": "BLOCKED_AMPLITUDE_SHAPE_NOT_EVALUATED",
        "dimension_role": "lensing-response role; codomain convention must be locked before numeric use",
    },
    {
        "coordinate_component": "cross_readout_consistency",
        "formal_slot": "Consistent(A_tau,Phi_tau_eff,T_tau_CMB,e_acoustic,e_density)",
        "candidate_definition": "lensing support must not contradict density or acoustic readout roles",
        "source_dependency": "tau_cmb_readout_role_coordinate_density_audit_v01; tau_cmb_readout_role_coordinate_acoustic_audit_v01",
        "blocked_by": "density and acoustic role coordinates remain blocked and unmaterialized",
        "coordinate_status": "BLOCKED_CROSS_READOUT_NOT_AVAILABLE",
        "dimension_role": "consistency role; no physical units",
    },
    {
        "coordinate_component": "lensing_stop_rule",
        "formal_slot": "lensing_fail_if_source_transfer_projection_or_shape_missing",
        "candidate_definition": "coordinate keeps a stop/fail branch if endpoint-blind lensing source, transfer, projection, or shape response cannot be supplied",
        "source_dependency": "tau_cmb_known_limit_failure_map_v01",
        "blocked_by": "run reduced checks or explicitly assign FAIL after source/transfer/projection evaluation",
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
            "coordinate_row_id": f"TCMBRRCL01_{index:03d}",
            "allows_coordinate_acceptance": "false",
            "allows_lensing_score": "false",
            "allows_act_planck_match": "false",
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
    density_audit = load_json(DENSITY_AUDIT) if DENSITY_AUDIT.exists() else {}
    input_ok = (
        density_audit.get("status") == "DENSITY_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED"
        and density_audit.get("failed_rows") == 0
        and LENSING_REDUCED_EVALUATION.exists()
    )
    return {
        "report_id": "tau_cmb_readout_role_coordinate_lensing_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_density_coordinate_audit": rel(DENSITY_AUDIT),
        "input_density_coordinate_audit_clean": input_ok,
        "input_lensing_reduced_evaluation": rel(LENSING_REDUCED_EVALUATION),
        "coordinate_symbol": "e_lensing",
        "coordinate_rows": len(rows),
        "blocked_rows": sum(row["coordinate_status"].startswith("BLOCKED") for row in rows),
        "guard_rows": sum("GUARD" in row["coordinate_status"] or "STOP_RULE" in row["coordinate_status"] for row in rows),
        "coordinate_acceptance_allowed": False,
        "lensing_score_allowed": False,
        "act_planck_match_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "LENSING_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED"
            if input_ok
            else "LENSING_ROLE_COORDINATE_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_coordinate_lensing_audit_v01"
            if input_ok
            else "repair_lensing_coordinate_inputs"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['coordinate_row_id']}` `{row['coordinate_component']}`: {row['coordinate_status']} | `{row['formal_slot']}`"
        for row in rows
    )
    text = f"""# Tau CMB Readout Role Coordinate Lensing v01

**Doc class:** lensing role-coordinate candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the candidate components of the lensing readout role
coordinate `e_lensing`. It is not a lensing score, not an ACT/Planck match,
not a CMB likelihood, not a concrete `R_CMB` map, and not evidence for a
dark-sector verdict.

## Coordinate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The lensing coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because `Phi_tau_eff(a,k)`, `T_tau_CMB(k,a)`,
endpoint-blind amplitude/shape response, and cross-readout consistency are not
supplied in score-ready form.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB lensing readout role-coordinate candidate.")
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
