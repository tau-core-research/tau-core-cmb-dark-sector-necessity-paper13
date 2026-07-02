#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXEC_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_execution_v01.csv"
EXEC_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_execution_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_v01_"
    "execution_accepted_as_noop_rejected_for_score_no_populated_cells_no_concrete_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_import_execution_acceptance_row_id",
    "source_numeric_value_import_execution_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_population_attempted",
    "cell_populated",
    "cell_artifact_written",
    "execution_row_accepted_as_receipt",
    "execution_row_accepted_for_score",
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
    if not EXEC_SUMMARY.exists():
        return False
    summary = load_json(EXEC_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_EXECUTION_RAN_NO_ROWS_POPULATED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_v01"
        and summary.get("numeric_value_import_execution_rows") == 33
        and summary.get("cell_population_attempted_rows") == 33
        and summary.get("cell_populated_rows") == 0
        and summary.get("cell_artifact_written_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value import execution summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(EXEC_TABLE), start=1):
        receipt_accepted = source["cell_population_attempted"] == "true"
        score_accepted = (
            receipt_accepted
            and source["cell_populated"] == "true"
            and source["cell_artifact_written"] == "true"
        )
        out.append(
            {
                "numeric_value_import_execution_acceptance_row_id": f"TCMBRRCNVIEACC01_{index:03d}",
                "source_numeric_value_import_execution_row_id": source["numeric_value_import_execution_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_population_attempted": source["cell_population_attempted"],
                "cell_populated": source["cell_populated"],
                "cell_artifact_written": source["cell_artifact_written"],
                "execution_row_accepted_as_receipt": str(receipt_accepted).lower(),
                "execution_row_accepted_for_score": str(score_accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "NUMERIC_VALUE_IMPORT_EXECUTION_ROW_ACCEPTED_FOR_SCORE"
                    if score_accepted
                    else "NUMERIC_VALUE_IMPORT_EXECUTION_ROW_ACCEPTED_AS_NOOP_RECEIPT_ONLY"
                ),
                "blocking_reason": (
                    "execution row accepted for score"
                    if score_accepted
                    else "import execution receipt exists, but no populated cell artifact exists"
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
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_import_execution_table": rel(EXEC_TABLE),
        "input_numeric_value_import_execution_summary": rel(EXEC_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_import_execution_acceptance_rows": len(table_rows),
        "execution_row_accepted_as_receipt_rows": sum(row["execution_row_accepted_as_receipt"] == "true" for row in table_rows),
        "execution_row_accepted_for_score_rows": sum(row["execution_row_accepted_for_score"] == "true" for row in table_rows),
        "cell_populated_rows": sum(row["cell_populated"] == "true" for row in table_rows),
        "cell_artifact_written_rows": sum(row["cell_artifact_written"] == "true" for row in table_rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_EXECUTION_ACCEPTED_NOOP_RECEIPT_VALUES_ABSENT"
            if input_chain_clean()
            and len(table_rows) == 33
            and all(row["execution_row_accepted_as_receipt"] == "true" for row in table_rows)
            and all(row["execution_row_accepted_for_score"] == "false" for row in table_rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_EXECUTION_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Import Execution Acceptance Audit v01

**Doc class:** role-coordinate numeric value import execution acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the import execution only as a no-op receipt. It rejects the
execution as score input because no cell was populated and no cell artifact was
written with numeric value, unit/convention, provenance, and replay.

## Summary

```text
numeric_value_import_execution_acceptance_rows={summary["numeric_value_import_execution_acceptance_rows"]}
execution_row_accepted_as_receipt_rows={summary["execution_row_accepted_as_receipt_rows"]}
execution_row_accepted_for_score_rows={summary["execution_row_accepted_for_score_rows"]}
cell_populated_rows={summary["cell_populated_rows"]}
cell_artifact_written_rows={summary["cell_artifact_written_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB role-coordinate numeric value import execution acceptance.")
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
