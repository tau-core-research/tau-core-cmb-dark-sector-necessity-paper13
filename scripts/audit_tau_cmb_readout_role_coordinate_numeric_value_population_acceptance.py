#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POPULATION_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_v01.csv"
POPULATION_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_population_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_population_acceptance_audit_v01_"
    "cell_table_rejected_for_score_values_units_provenance_replay_absent_"
    "no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_population_acceptance_row_id",
    "source_numeric_value_population_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "numeric_value_present",
    "unit_or_convention_present",
    "provenance_present",
    "replay_present",
    "endpoint_blind_cell",
    "cell_accepted_for_coordinate",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "acceptance_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def input_chain_clean() -> bool:
    if not POPULATION_SUMMARY.exists():
        return False
    summary = load_json(POPULATION_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_POPULATION_TABLE_DECLARED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_population_acceptance_audit_v01"
        and summary.get("numeric_value_population_rows", 0) > 0
        and summary.get("numeric_value_present_rows") == 0
        and summary.get("unit_or_convention_present_rows") == 0
        and summary.get("provenance_present_rows") == 0
        and summary.get("replay_present_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value population summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(POPULATION_TABLE), start=1):
        accepted = (
            source["numeric_value_present"] == "true"
            and source["unit_or_convention_present"] == "true"
            and source["provenance_present"] == "true"
            and source["replay_present"] == "true"
            and source["endpoint_blind_cell"] == "true"
        )
        out.append(
            {
                "numeric_value_population_acceptance_row_id": f"TCMBRRCNVPACC01_{index:03d}",
                "source_numeric_value_population_row_id": source["numeric_value_population_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "numeric_value_present": source["numeric_value_present"],
                "unit_or_convention_present": source["unit_or_convention_present"],
                "provenance_present": source["provenance_present"],
                "replay_present": source["replay_present"],
                "endpoint_blind_cell": source["endpoint_blind_cell"],
                "cell_accepted_for_coordinate": str(accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "NUMERIC_VALUE_CELL_ACCEPTED_FOR_COORDINATE"
                    if accepted
                    else "NUMERIC_VALUE_CELL_REJECTED_VALUE_UNIT_PROVENANCE_REPLAY_REQUIRED"
                ),
                "blocking_reason": (
                    "numeric cell accepted"
                    if accepted
                    else "numeric value, unit/convention, provenance, and replay are all required before coordinate acceptance"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    accepted = sum(row["cell_accepted_for_coordinate"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_population_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_population_table": rel(POPULATION_TABLE),
        "input_numeric_value_population_summary": rel(POPULATION_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_population_acceptance_rows": len(rows),
        "cell_accepted_for_coordinate_rows": accepted,
        "cell_rejected_for_coordinate_rows": len(rows) - accepted,
        "numeric_value_present_rows": sum(row["numeric_value_present"] == "true" for row in rows),
        "unit_or_convention_present_rows": sum(row["unit_or_convention_present"] == "true" for row in rows),
        "provenance_present_rows": sum(row["provenance_present"] == "true" for row in rows),
        "replay_present_rows": sum(row["replay_present"] == "true" for row in rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_POPULATION_ACCEPTANCE_AUDITED_REJECTED_VALUES_ABSENT"
            if input_chain_clean() and len(rows) > 0 and accepted == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_POPULATION_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_cell_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Population Acceptance Audit v01

**Doc class:** role-coordinate numeric value population acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit rejects the cell-level population table for score entry because the
numeric values, unit/convention declarations, provenance records, and replay
records are absent.

## Summary

```text
numeric_value_population_acceptance_rows={summary["numeric_value_population_acceptance_rows"]}
cell_accepted_for_coordinate_rows={summary["cell_accepted_for_coordinate_rows"]}
cell_rejected_for_coordinate_rows={summary["cell_rejected_for_coordinate_rows"]}
numeric_value_present_rows={summary["numeric_value_present_rows"]}
unit_or_convention_present_rows={summary["unit_or_convention_present_rows"]}
provenance_present_rows={summary["provenance_present_rows"]}
replay_present_rows={summary["replay_present_rows"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB role-coordinate numeric value population acceptance.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_rows = rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, table_rows)
    if args.write_table:
        write_table(table_path, table_rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
