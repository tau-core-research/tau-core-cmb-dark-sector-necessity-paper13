#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IMPORT_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_summary_v01.json"
IMPORT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_execution_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_execution_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_import_execution_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_import_execution_v01_"
    "execution_receipt_no_rows_populated_values_absent_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_import_execution_row_id",
    "source_numeric_value_import_packet_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_artifact",
    "import_numeric_value_present",
    "import_unit_or_convention_present",
    "import_provenance_present",
    "import_replay_present",
    "endpoint_blind_attestation",
    "cell_population_attempted",
    "cell_populated",
    "cell_artifact_written",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "execution_status",
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


def present(value: str) -> bool:
    return bool(value.strip())


def input_chain_clean() -> bool:
    if not IMPORT_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(IMPORT_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_PACKET_ACCEPTED_TEMPLATE_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_import_execution_v01"
        and summary.get("numeric_value_import_packet_acceptance_rows") == 33
        and summary.get("template_packet_accepted_rows") == 33
        and summary.get("import_row_accepted_rows") == 0
        and summary.get("import_numeric_value_present_rows") == 0
        and summary.get("import_unit_or_convention_present_rows") == 0
        and summary.get("import_provenance_present_rows") == 0
        and summary.get("import_replay_present_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value import packet acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(IMPORT_TABLE), start=1):
        value_present = present(source["import_numeric_value"])
        unit_present = present(source["import_unit_or_convention"])
        provenance_present = present(source["import_provenance"])
        replay_present = present(source["import_replay"])
        endpoint_blind = source["endpoint_blind_attestation"] == "true"
        populated = value_present and unit_present and provenance_present and replay_present and endpoint_blind
        out.append(
            {
                "numeric_value_import_execution_row_id": f"TCMBRRCNVIEXE01_{index:03d}",
                "source_numeric_value_import_packet_row_id": source["numeric_value_import_packet_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_artifact": source["cell_artifact"],
                "import_numeric_value_present": str(value_present).lower(),
                "import_unit_or_convention_present": str(unit_present).lower(),
                "import_provenance_present": str(provenance_present).lower(),
                "import_replay_present": str(replay_present).lower(),
                "endpoint_blind_attestation": source["endpoint_blind_attestation"],
                "cell_population_attempted": "true",
                "cell_populated": str(populated).lower(),
                "cell_artifact_written": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "execution_status": (
                    "NUMERIC_VALUE_IMPORT_ROW_POPULATED"
                    if populated
                    else "NUMERIC_VALUE_IMPORT_ROW_NOT_POPULATED_VALUES_ABSENT"
                ),
                "blocking_reason": (
                    "cell populated from endpoint-blind import row"
                    if populated
                    else "import execution ran, but numeric value, unit/convention, provenance, or replay is absent"
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
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_import_execution_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_import_packet_acceptance_audit_summary": rel(IMPORT_ACCEPTANCE_SUMMARY),
        "input_numeric_value_import_packet_table": rel(IMPORT_TABLE),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_import_execution_rows": len(rows),
        "cell_population_attempted_rows": sum(row["cell_population_attempted"] == "true" for row in rows),
        "cell_populated_rows": sum(row["cell_populated"] == "true" for row in rows),
        "cell_artifact_written_rows": sum(row["cell_artifact_written"] == "true" for row in rows),
        "import_numeric_value_present_rows": sum(row["import_numeric_value_present"] == "true" for row in rows),
        "import_unit_or_convention_present_rows": sum(row["import_unit_or_convention_present"] == "true" for row in rows),
        "import_provenance_present_rows": sum(row["import_provenance_present"] == "true" for row in rows),
        "import_replay_present_rows": sum(row["import_replay_present"] == "true" for row in rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_EXECUTION_RAN_NO_ROWS_POPULATED_VALUES_ABSENT"
            if input_chain_clean() and len(rows) == 33 and all(row["cell_populated"] == "false" for row in rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_EXECUTION_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Import Execution v01

**Doc class:** role-coordinate numeric value import execution receipt
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step executes the import packet mechanically. With the current empty
template, it records a no-op execution receipt: all 33 rows are attempted, but
no cell is populated.

## Summary

```text
numeric_value_import_execution_rows={summary["numeric_value_import_execution_rows"]}
cell_population_attempted_rows={summary["cell_population_attempted_rows"]}
cell_populated_rows={summary["cell_populated_rows"]}
cell_artifact_written_rows={summary["cell_artifact_written_rows"]}
import_numeric_value_present_rows={summary["import_numeric_value_present_rows"]}
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
    parser = argparse.ArgumentParser(description="Execute Tau CMB role-coordinate numeric value import.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, rows)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
