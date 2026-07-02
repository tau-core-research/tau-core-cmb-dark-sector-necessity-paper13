#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CELL_SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_supply_v01.csv"
CELL_SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_v01_"
    "templates_accepted_cells_rejected_values_absent_no_concrete_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_cell_acceptance_row_id",
    "source_numeric_value_cell_supply_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_template_supplied",
    "hash_matches",
    "template_accepted",
    "numeric_value_supplied",
    "unit_or_convention_supplied",
    "provenance_supplied",
    "replay_supplied",
    "endpoint_blind_cell",
    "cell_value_accepted",
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
    if not CELL_SUPPLY_SUMMARY.exists():
        return False
    summary = load_json(CELL_SUPPLY_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_CELL_TEMPLATES_SUPPLIED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_v01"
        and summary.get("numeric_value_cell_supply_rows") == 33
        and summary.get("cell_template_supplied_rows") == 33
        and summary.get("hash_matched_rows") == 33
        and summary.get("numeric_value_supplied_rows") == 0
        and summary.get("unit_or_convention_supplied_rows") == 0
        and summary.get("provenance_supplied_rows") == 0
        and summary.get("replay_supplied_rows") == 0
        and summary.get("cell_value_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value cell supply summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(CELL_SUPPLY_TABLE), start=1):
        template_accepted = source["cell_template_supplied"] == "true" and source["hash_matches"] == "true"
        value_accepted = (
            template_accepted
            and source["numeric_value_supplied"] == "true"
            and source["unit_or_convention_supplied"] == "true"
            and source["provenance_supplied"] == "true"
            and source["replay_supplied"] == "true"
            and source["endpoint_blind_cell"] == "true"
        )
        out.append(
            {
                "numeric_value_cell_acceptance_row_id": f"TCMBRRCNVCACC01_{index:03d}",
                "source_numeric_value_cell_supply_row_id": source["numeric_value_cell_supply_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_template_supplied": source["cell_template_supplied"],
                "hash_matches": source["hash_matches"],
                "template_accepted": str(template_accepted).lower(),
                "numeric_value_supplied": source["numeric_value_supplied"],
                "unit_or_convention_supplied": source["unit_or_convention_supplied"],
                "provenance_supplied": source["provenance_supplied"],
                "replay_supplied": source["replay_supplied"],
                "endpoint_blind_cell": source["endpoint_blind_cell"],
                "cell_value_accepted": str(value_accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "NUMERIC_VALUE_CELL_ACCEPTED_FOR_SCORE_INPUT"
                    if value_accepted
                    else "NUMERIC_VALUE_CELL_TEMPLATE_ACCEPTED_VALUE_REJECTED_ABSENT"
                ),
                "blocking_reason": (
                    "numeric value cell accepted for score input"
                    if value_accepted
                    else "template is present, but numeric value, unit/convention, provenance, and replay are absent"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def write_table(path: Path, table_rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(table_rows)


def build_summary(table_path: Path, table_rows: list[dict[str, str]]) -> dict[str, Any]:
    accepted = sum(row["cell_value_accepted"] == "true" for row in table_rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_cell_supply_table": rel(CELL_SUPPLY_TABLE),
        "input_numeric_value_cell_supply_summary": rel(CELL_SUPPLY_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_cell_acceptance_rows": len(table_rows),
        "template_accepted_rows": sum(row["template_accepted"] == "true" for row in table_rows),
        "cell_value_accepted_rows": accepted,
        "cell_value_rejected_rows": len(table_rows) - accepted,
        "numeric_value_supplied_rows": sum(row["numeric_value_supplied"] == "true" for row in table_rows),
        "unit_or_convention_supplied_rows": sum(row["unit_or_convention_supplied"] == "true" for row in table_rows),
        "provenance_supplied_rows": sum(row["provenance_supplied"] == "true" for row in table_rows),
        "replay_supplied_rows": sum(row["replay_supplied"] == "true" for row in table_rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_CELL_TEMPLATES_ACCEPTED_VALUES_ABSENT"
            if input_chain_clean() and len(table_rows) == 33 and accepted == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_CELL_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Cell Acceptance Audit v01

**Doc class:** role-coordinate numeric value cell acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the 33 cell artifacts only as templates. It rejects them as
score inputs because the actual numeric values, units/conventions, provenance,
and replay records are absent.

## Summary

```text
numeric_value_cell_acceptance_rows={summary["numeric_value_cell_acceptance_rows"]}
template_accepted_rows={summary["template_accepted_rows"]}
cell_value_accepted_rows={summary["cell_value_accepted_rows"]}
cell_value_rejected_rows={summary["cell_value_rejected_rows"]}
numeric_value_supplied_rows={summary["numeric_value_supplied_rows"]}
unit_or_convention_supplied_rows={summary["unit_or_convention_supplied_rows"]}
provenance_supplied_rows={summary["provenance_supplied_rows"]}
replay_supplied_rows={summary["replay_supplied_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB role-coordinate numeric value cell acceptance.")
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
