#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POP_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01.csv"
POP_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_v01_"
    "contract_accepted_population_values_absent_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "population_packet_acceptance_row_id",
    "source_population_packet_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "population_contract_declared",
    "population_contract_accepted",
    "population_value_supplied",
    "population_row_accepted_for_score",
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
    if not POP_SUMMARY.exists():
        return False
    summary = load_json(POP_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_POPULATION_CONTRACT_DECLARED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_v01"
        and summary.get("population_packet_rows") == 33
        and summary.get("population_contract_declared_rows") == 33
        and summary.get("population_value_supplied_rows") == 0
        and summary.get("population_row_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value import population packet summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(POP_TABLE), start=1):
        contract_accepted = source["population_contract_declared"] == "true"
        score_accepted = contract_accepted and source["population_value_supplied"] == "true"
        out.append(
            {
                "population_packet_acceptance_row_id": f"TCMBRRCNVIPPACC01_{index:03d}",
                "source_population_packet_row_id": source["population_packet_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "population_contract_declared": source["population_contract_declared"],
                "population_contract_accepted": str(contract_accepted).lower(),
                "population_value_supplied": source["population_value_supplied"],
                "population_row_accepted_for_score": str(score_accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "POPULATION_ROW_ACCEPTED_FOR_SCORE"
                    if score_accepted
                    else "POPULATION_CONTRACT_ACCEPTED_VALUES_ABSENT"
                ),
                "blocking_reason": (
                    "population row accepted for score"
                    if score_accepted
                    else "population contract is accepted, but value payload is absent"
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
    score_rows = sum(row["population_row_accepted_for_score"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_population_packet_table": rel(POP_TABLE),
        "input_population_packet_summary": rel(POP_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "population_packet_acceptance_rows": len(rows),
        "population_contract_accepted_rows": sum(row["population_contract_accepted"] == "true" for row in rows),
        "population_value_supplied_rows": sum(row["population_value_supplied"] == "true" for row in rows),
        "population_row_accepted_for_score_rows": score_rows,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_POPULATION_CONTRACT_ACCEPTED_VALUES_ABSENT"
            if input_chain_clean() and len(rows) == 33 and score_rows == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_POPULATION_PACKET_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Import Population Packet Acceptance Audit v01

**Doc class:** role-coordinate numeric value import population contract acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the 33-row population packet only as a contract. It rejects
all rows for score entry because no populated numeric value payload is supplied.

## Summary

```text
population_packet_acceptance_rows={summary["population_packet_acceptance_rows"]}
population_contract_accepted_rows={summary["population_contract_accepted_rows"]}
population_value_supplied_rows={summary["population_value_supplied_rows"]}
population_row_accepted_for_score_rows={summary["population_row_accepted_for_score_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB numeric value import population packet acceptance.")
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
