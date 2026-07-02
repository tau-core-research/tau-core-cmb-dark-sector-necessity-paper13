#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_source_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_source_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_source_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_source_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_source_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_source_acceptance_audit_v01_"
    "requirement_worklist_accepted_as_worklist_only_numeric_values_absent_"
    "no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_source_acceptance_row_id",
    "source_numeric_value_source_supply_row_id",
    "role_name",
    "coordinate_symbol",
    "source_requirement_artifact_supplied",
    "hash_matches",
    "source_requirement_rows",
    "requirement_worklist_accepted",
    "numeric_value_source_supplied",
    "numeric_values_materialized",
    "role_coordinate_acceptance_allowed",
    "concrete_R_CMB_allowed",
    "numeric_value_source_accepted",
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
    if not SUPPLY_SUMMARY.exists():
        return False
    summary = load_json(SUPPLY_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_REQUIREMENT_WORKLIST_SUPPLIED_NOT_NUMERIC"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_source_acceptance_audit_v01"
        and summary.get("numeric_value_source_supply_rows") == 6
        and summary.get("source_requirement_artifact_supplied_rows") == 6
        and summary.get("hash_matched_rows") == 6
        and summary.get("source_requirement_rows", 0) > 0
        and summary.get("numeric_value_source_supplied_rows") == 0
        and summary.get("numeric_values_materialized_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value-source supply summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(SUPPLY_TABLE), start=1):
        worklist_accepted = (
            source["source_requirement_artifact_supplied"] == "true"
            and source["hash_matches"] == "true"
            and int(source["source_requirement_rows"]) > 0
        )
        source_accepted = (
            worklist_accepted
            and source["numeric_value_source_supplied"] == "true"
            and source["numeric_values_materialized"] == "true"
            and source["role_coordinate_acceptance_allowed"] == "true"
            and source["concrete_R_CMB_allowed"] == "true"
        )
        out.append(
            {
                "numeric_value_source_acceptance_row_id": f"TCMBRRCNVSACC01_{index:03d}",
                "source_numeric_value_source_supply_row_id": source["numeric_value_source_supply_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "source_requirement_artifact_supplied": source["source_requirement_artifact_supplied"],
                "hash_matches": source["hash_matches"],
                "source_requirement_rows": source["source_requirement_rows"],
                "requirement_worklist_accepted": str(worklist_accepted).lower(),
                "numeric_value_source_supplied": source["numeric_value_source_supplied"],
                "numeric_values_materialized": source["numeric_values_materialized"],
                "role_coordinate_acceptance_allowed": source["role_coordinate_acceptance_allowed"],
                "concrete_R_CMB_allowed": source["concrete_R_CMB_allowed"],
                "numeric_value_source_accepted": str(source_accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACCEPTED"
                    if source_accepted
                    else "ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_REJECTED_VALUES_ABSENT_WORKLIST_ONLY"
                ),
                "blocking_reason": (
                    "numeric value source accepted"
                    if source_accepted
                    else "requirement worklist is accepted only as a worklist; numeric values and concrete R_CMB allowance are absent"
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
    source_accepted = sum(row["numeric_value_source_accepted"] == "true" for row in table_rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_source_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_source_supply_table": rel(SUPPLY_TABLE),
        "input_numeric_value_source_supply_summary": rel(SUPPLY_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_source_acceptance_rows": len(table_rows),
        "requirement_worklist_accepted_rows": sum(row["requirement_worklist_accepted"] == "true" for row in table_rows),
        "source_requirement_rows": sum(int(row["source_requirement_rows"]) for row in table_rows),
        "numeric_value_source_accepted_rows": source_accepted,
        "numeric_value_source_rejected_rows": len(table_rows) - source_accepted,
        "numeric_values_materialized_rows": sum(row["numeric_values_materialized"] == "true" for row in table_rows),
        "role_coordinate_acceptance_allowed_rows": sum(row["role_coordinate_acceptance_allowed"] == "true" for row in table_rows),
        "concrete_R_CMB_allowed_rows": sum(row["concrete_R_CMB_allowed"] == "true" for row in table_rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_REQUIREMENT_WORKLIST_ACCEPTED_VALUES_ABSENT"
            if input_chain_clean() and len(table_rows) == 6 and source_accepted == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_population_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Source Acceptance Audit v01

**Doc class:** role-coordinate numeric value-source acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the supplied artifacts only as a finite numeric-source
worklist. It rejects them as numeric value sources because no actual
endpoint-blind numeric values, unit/convention replay, or concrete `R_CMB`
allowance has been supplied.

## Summary

```text
numeric_value_source_acceptance_rows={summary["numeric_value_source_acceptance_rows"]}
requirement_worklist_accepted_rows={summary["requirement_worklist_accepted_rows"]}
source_requirement_rows={summary["source_requirement_rows"]}
numeric_value_source_accepted_rows={summary["numeric_value_source_accepted_rows"]}
numeric_values_materialized_rows={summary["numeric_values_materialized_rows"]}
concrete_R_CMB_allowed_rows={summary["concrete_R_CMB_allowed_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB role-coordinate numeric value-source acceptance.")
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
