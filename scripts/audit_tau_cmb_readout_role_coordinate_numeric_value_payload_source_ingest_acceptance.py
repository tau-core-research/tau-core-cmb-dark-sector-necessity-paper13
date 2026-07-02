#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INGEST_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01.csv"
INGEST_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_v01_"
    "focused_protocol_sources_accepted_no_physical_CMB_score_no_likelihood_no_verdict"
)

FIELDS = [
    "source_ingest_acceptance_row_id",
    "source_source_ingest_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "source_ingested",
    "value_source_accepted",
    "protocol_value_component_accepted",
    "physical_CMB_component_accepted",
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
    if not INGEST_SUMMARY.exists():
        return False
    summary = load_json(INGEST_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGESTED_FOCUSED_PROTOCOL_BATCH_ONLY"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_v01"
        and summary.get("source_ingest_rows") == 33
        and summary.get("source_ingest_attempted_rows") == 17
        and summary.get("source_ingested_rows") == 17
        and summary.get("value_source_accepted_rows") == 17
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("source ingest summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(INGEST_TABLE), start=1):
        protocol_accepted = source["value_source_accepted"] == "true"
        physical_accepted = False
        out.append(
            {
                "source_ingest_acceptance_row_id": f"TCMBRRCNVSIACC01_{index:03d}",
                "source_source_ingest_row_id": source["source_ingest_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "source_ingested": source["source_ingested"],
                "value_source_accepted": source["value_source_accepted"],
                "protocol_value_component_accepted": str(protocol_accepted).lower(),
                "physical_CMB_component_accepted": str(physical_accepted).lower(),
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "FOCUSED_PROTOCOL_VALUE_SOURCE_ACCEPTED"
                    if protocol_accepted
                    else "VALUE_SOURCE_NOT_ACCEPTED_IN_THIS_BATCH"
                ),
                "blocking_reason": (
                    "focused protocol value accepted; physical score still closed"
                    if protocol_accepted
                    else "not ingested in this focused batch"
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
    protocol = sum(row["protocol_value_component_accepted"] == "true" for row in rows)
    physical = sum(row["physical_CMB_component_accepted"] == "true" for row in rows)
    total = len(rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_source_ingest_table": rel(INGEST_TABLE),
        "input_source_ingest_summary": rel(INGEST_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "source_ingest_acceptance_rows": total,
        "protocol_value_component_accepted_rows": protocol,
        "physical_CMB_component_accepted_rows": physical,
        "protocol_value_score_numerator": protocol,
        "protocol_value_score_denominator": total,
        "protocol_value_score": round(protocol / total, 6) if total else 0.0,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGEST_ACCEPTED_FOCUSED_PROTOCOL_ONLY"
            if input_chain_clean() and protocol == 17 and physical == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGEST_ACCEPTANCE_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_next_role_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Payload Source Ingest Acceptance Audit v01

**Doc class:** focused protocol source ingest acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
protocol_value_component_accepted_rows={summary["protocol_value_component_accepted_rows"]}
physical_CMB_component_accepted_rows={summary["physical_CMB_component_accepted_rows"]}
protocol_value_score={summary["protocol_value_score"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB focused source ingest acceptance.")
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
