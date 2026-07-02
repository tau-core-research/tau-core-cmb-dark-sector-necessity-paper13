#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RADIATION_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_audit_v01.json"
ZERO_CONTROL_AUDIT = ROOT / "data/derived/tau_cmb_seed_zero_control_audit_v01.json"
QUOTIENT_AUDIT = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_null_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_null_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_null_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_null_v01_control_candidate_only_"
    "null_not_accepted_no_physical_response_no_quotient_proof_no_concrete_R_CMB_"
    "no_carrier_certification_no_score_no_verdict"
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
    "allows_physical_response",
    "allows_quotient_proof",
    "allows_concrete_R_CMB",
    "allows_carrier_certification",
    "allows_score_entry",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "coordinate_component": "null_seed_anchor",
        "formal_slot": "null_seed_tau_CMB",
        "candidate_definition": "null coordinate requires a same-domain null seed anchor for readout comparison",
        "source_dependency": "tau_cmb_seed_zero_control_audit_v01",
        "blocked_by": "zero-control is audited but not accepted as a readout-domain member",
        "coordinate_status": "BLOCKED_NULL_SEED_NOT_ACCEPTED",
        "dimension_role": "control object; no physical units",
    },
    {
        "coordinate_component": "null_readout_anchor",
        "formal_slot": "R_CMB(null_seed_tau_CMB) := null_readout",
        "candidate_definition": "null coordinate requires a declared null readout anchor for quotient comparison",
        "source_dependency": "tau_cmb_seed_zero_control_audit_v01",
        "blocked_by": "null readout role is declared but concrete R_CMB is not materialized",
        "coordinate_status": "BLOCKED_NULL_READOUT_NOT_MATERIALIZED",
        "dimension_role": "readout-control role; no source amplitude",
    },
    {
        "coordinate_component": "quotient_relation_hook",
        "formal_slot": "R_CMB(seed) ~ R_CMB(null_seed)",
        "candidate_definition": "null coordinate provides the anchor side of the future quotient/null comparison",
        "source_dependency": "tau_cmb_seed_readout_quotient_relation_candidate_audit_v01",
        "blocked_by": "equivalence relation, quotient map, and survival condition are not proved",
        "coordinate_status": "BLOCKED_QUOTIENT_RELATION_NOT_PROVED",
        "dimension_role": "relation role; no physical units",
    },
    {
        "coordinate_component": "zero_source_consistency",
        "formal_slot": "zero_source -> zero Tau readout contribution",
        "candidate_definition": "null coordinate requires zero-control consistency without substituting it for a physical zero-source proof",
        "source_dependency": "tau_cmb_seed_zero_control_audit_v01; cmb_tau_lensing_projection_zero_source_limit_obligation_v01",
        "blocked_by": "zero-control exists as a control candidate but does not prove physical zero-source behavior",
        "coordinate_status": "GUARD_ZERO_SOURCE_CONTROL_DECLARED_NOT_PHYSICAL_PROOF",
        "dimension_role": "control/known-limit guard; no physical units",
    },
    {
        "coordinate_component": "forbidden_promotion",
        "formal_slot": "null_seed != physical Tau response",
        "candidate_definition": "null coordinate forbids promoting the null control into physical response or score evidence",
        "source_dependency": "tau_cmb_seed_zero_control_audit_v01",
        "blocked_by": "promotion remains forbidden until a separate non-null source route is accepted",
        "coordinate_status": "PROMOTION_FORBIDDEN_DECLARED",
        "dimension_role": "claim-boundary guard; no physical units",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "coordinate_row_id": f"TCMBRRCN01_{index:03d}",
            "allows_coordinate_acceptance": "false",
            "allows_physical_response": "false",
            "allows_quotient_proof": "false",
            "allows_concrete_R_CMB": "false",
            "allows_carrier_certification": "false",
            "allows_score_entry": "false",
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
    radiation_audit = load_json(RADIATION_AUDIT) if RADIATION_AUDIT.exists() else {}
    zero_audit = load_json(ZERO_CONTROL_AUDIT) if ZERO_CONTROL_AUDIT.exists() else {}
    quotient_audit = load_json(QUOTIENT_AUDIT) if QUOTIENT_AUDIT.exists() else {}
    input_ok = (
        radiation_audit.get("status") == "RADIATION_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED"
        and radiation_audit.get("failed_rows") == 0
        and zero_audit.get("status") == "SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED"
        and zero_audit.get("failed_rows") == 0
        and quotient_audit.get("status") == "SEED_READOUT_QUOTIENT_RELATION_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED"
        and quotient_audit.get("failed_rows") == 0
    )
    return {
        "report_id": "tau_cmb_readout_role_coordinate_null_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_radiation_coordinate_audit": rel(RADIATION_AUDIT),
        "input_zero_control_audit": rel(ZERO_CONTROL_AUDIT),
        "input_quotient_relation_candidate_audit": rel(QUOTIENT_AUDIT),
        "input_control_chain_clean": input_ok,
        "coordinate_symbol": "e_null",
        "coordinate_rows": len(rows),
        "blocked_rows": sum(row["coordinate_status"].startswith("BLOCKED") for row in rows),
        "guard_rows": sum("GUARD" in row["coordinate_status"] or "FORBIDDEN" in row["coordinate_status"] for row in rows),
        "coordinate_acceptance_allowed": False,
        "physical_response_allowed": False,
        "quotient_proof_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "NULL_ROLE_COORDINATE_CONTROL_CANDIDATE_DECLARED_BLOCKED_NOT_ACCEPTED"
            if input_ok
            else "NULL_ROLE_COORDINATE_CONTROL_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_coordinate_null_audit_v01"
            if input_ok
            else "repair_null_coordinate_inputs"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['coordinate_row_id']}` `{row['coordinate_component']}`: {row['coordinate_status']} | `{row['formal_slot']}`"
        for row in rows
    )
    text = f"""# Tau CMB Readout Role Coordinate Null v01

**Doc class:** null/control role-coordinate candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the candidate components of the null/control readout
role coordinate `e_null`. It is not a physical Tau response, not a quotient
proof, not a concrete `R_CMB` map, not carrier certification, not a score
entry, and not evidence for a dark-sector verdict.

## Coordinate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The null coordinate is explicit as a blocked control candidate. It anchors the
future null side of readout comparison, while preserving the rule that
zero-control is not physical response evidence and cannot be used as a
zero-source proof for a physical projection operator.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB null readout role-coordinate candidate.")
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
