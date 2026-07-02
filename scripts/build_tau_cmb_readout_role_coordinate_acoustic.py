#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASIS_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_space_basis_audit_v01.json"
ACOUSTIC_EVAL = ROOT / "data/derived/tau_cmb_acoustic_reduced_evaluation_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_acoustic_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_acoustic_v01_coordinate_candidate_only_"
    "not_materialized_no_acoustic_score_no_likelihood_no_concrete_R_CMB_no_carrier_certification_no_verdict"
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
    "allows_acoustic_score",
    "allows_concrete_R_CMB",
    "allows_carrier_certification",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "coordinate_component": "potential_source_presence",
        "formal_slot": "Phi_tau_eff(a,k)|recombination",
        "candidate_definition": "acoustic coordinate may reference a pre-recombination potential-source slot only after endpoint-blind handoff",
        "source_dependency": "tau_cmb_acoustic_reduced_evaluation_v01",
        "blocked_by": "Phi_tau_eff remains a target slot rather than a derived pre-recombination source",
        "coordinate_status": "BLOCKED_SOURCE_NOT_DERIVED",
        "dimension_role": "potential role; dimensionless only after convention replay",
    },
    {
        "coordinate_component": "phase_support",
        "formal_slot": "phase_tau_acoustic",
        "candidate_definition": "phase coordinate requires a reduced photon-baryon oscillator response with Tau source timing/sign",
        "source_dependency": "tau_cmb_acoustic_reduced_evaluation_v01",
        "blocked_by": "oscillator response is not evaluated",
        "coordinate_status": "BLOCKED_OSCILLATOR_RESPONSE_NOT_EVALUATED",
        "dimension_role": "dimensionless phase role",
    },
    {
        "coordinate_component": "relative_peak_height",
        "formal_slot": "height_ratio_tau_acoustic",
        "candidate_definition": "relative-height coordinate requires endpoint-blind A_tau and potential normalization",
        "source_dependency": "tau_cmb_acoustic_reduced_evaluation_v01",
        "blocked_by": "A_tau is only a formal ratio and endpoint-blind amplitude is unavailable",
        "coordinate_status": "BLOCKED_AMPLITUDE_NOT_AVAILABLE",
        "dimension_role": "dimensionless relative-height role",
    },
    {
        "coordinate_component": "baryon_loading_coupling",
        "formal_slot": "coupling_sign_tau_baryon",
        "candidate_definition": "coordinate must state Tau source coupling sign relative to baryon loading before phase/height comparison",
        "source_dependency": "tau_cmb_acoustic_reduced_evaluation_v01",
        "blocked_by": "source-coupling sign and baryon-loading convention are missing",
        "coordinate_status": "BLOCKED_COUPLING_SIGN_MISSING",
        "dimension_role": "sign/convention role",
    },
    {
        "coordinate_component": "scale_horizon_guard",
        "formal_slot": "(k,a_rec,r_s)_convention",
        "candidate_definition": "coordinate must use declared k, scale-factor, recombination epoch, and sound-horizon conventions",
        "source_dependency": "tau_cmb_acoustic_reduced_evaluation_v01",
        "blocked_by": "numeric convention still required for future evaluation",
        "coordinate_status": "CONVENTION_GUARD_DECLARED_NOT_NUMERIC",
        "dimension_role": "mixed convention guard; not a score coordinate",
    },
    {
        "coordinate_component": "failure_branch",
        "formal_slot": "acoustic_fail_if_missing_required_inputs",
        "candidate_definition": "coordinate keeps an explicit FAIL branch if source, phase, or height checks cannot be supplied",
        "source_dependency": "tau_cmb_known_limit_failure_map_v01",
        "blocked_by": "reduced checks are not run and no acoustic decision is assigned",
        "coordinate_status": "FAILURE_BRANCH_READY_NOT_TRIGGERED",
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
            "coordinate_row_id": f"TCMBRRCA01_{index:03d}",
            "allows_coordinate_acceptance": "false",
            "allows_acoustic_score": "false",
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
    basis_audit = load_json(BASIS_AUDIT) if BASIS_AUDIT.exists() else {}
    input_ok = (
        basis_audit.get("status") == "CMB_READOUT_ROLE_SPACE_BASIS_AUDITED_BLOCKED_NOT_CERTIFIED"
        and basis_audit.get("failed_rows") == 0
        and ACOUSTIC_EVAL.exists()
    )
    return {
        "report_id": "tau_cmb_readout_role_coordinate_acoustic_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_basis_audit": rel(BASIS_AUDIT),
        "input_basis_audit_clean": input_ok,
        "coordinate_symbol": "e_acoustic",
        "coordinate_rows": len(rows),
        "blocked_rows": sum(row["coordinate_status"].startswith("BLOCKED") for row in rows),
        "guard_rows": sum("GUARD" in row["coordinate_status"] or "FAILURE_BRANCH" in row["coordinate_status"] for row in rows),
        "coordinate_acceptance_allowed": False,
        "acoustic_score_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "ACOUSTIC_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED"
            if input_ok
            else "ACOUSTIC_ROLE_COORDINATE_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_coordinate_acoustic_audit_v01"
            if input_ok
            else "repair_acoustic_coordinate_inputs"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['coordinate_row_id']}` `{row['coordinate_component']}`: {row['coordinate_status']} | `{row['formal_slot']}`"
        for row in rows
    )
    text = f"""# Tau CMB Readout Role Coordinate Acoustic v01

**Doc class:** acoustic role-coordinate candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the candidate components of the acoustic readout role
coordinate `e_acoustic`. It is not an acoustic fit, not a CMB likelihood, not a
concrete `R_CMB` map, and not evidence for a dark-sector verdict.

## Coordinate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The acoustic coordinate is now explicit as a blocked role-coordinate candidate.
It remains unmaterialized because the Tau pre-recombination source, oscillator
response, endpoint-blind amplitude, and coupling sign are not supplied.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB acoustic readout role-coordinate candidate.")
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
