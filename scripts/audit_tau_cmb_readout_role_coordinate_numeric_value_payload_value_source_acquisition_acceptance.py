#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACQ_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_v01.csv"
ACQ_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_v01_"
    "requests_accepted_sources_absent_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "value_source_acquisition_acceptance_row_id",
    "source_value_source_acquisition_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "source_acquisition_request_declared",
    "source_acquisition_hash_matches",
    "source_acquisition_request_accepted",
    "value_source_acquired",
    "value_source_accepted",
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
    if not ACQ_SUMMARY.exists():
        return False
    summary = load_json(ACQ_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACQUISITION_REQUESTS_DECLARED_NO_SOURCES_ACQUIRED"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_v01"
        and summary.get("value_source_acquisition_rows") == 33
        and summary.get("source_acquisition_request_declared_rows") == 33
        and summary.get("source_acquisition_hash_matched_rows") == 33
        and summary.get("value_source_acquired_rows") == 0
        and summary.get("value_source_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("value source acquisition summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(ACQ_TABLE), start=1):
        request_accepted = source["source_acquisition_request_declared"] == "true" and source["source_acquisition_hash_matches"] == "true"
        value_accepted = request_accepted and source["value_source_acquired"] == "true" and source["value_source_accepted"] == "true"
        out.append(
            {
                "value_source_acquisition_acceptance_row_id": f"TCMBRRCNVVSACQACC01_{index:03d}",
                "source_value_source_acquisition_row_id": source["value_source_acquisition_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "source_acquisition_request_declared": source["source_acquisition_request_declared"],
                "source_acquisition_hash_matches": source["source_acquisition_hash_matches"],
                "source_acquisition_request_accepted": str(request_accepted).lower(),
                "value_source_acquired": source["value_source_acquired"],
                "value_source_accepted": str(value_accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "VALUE_SOURCE_ACCEPTED_FOR_SCORE_INPUT"
                    if value_accepted
                    else "VALUE_SOURCE_ACQUISITION_REQUEST_ACCEPTED_SOURCE_ABSENT"
                ),
                "blocking_reason": (
                    "value source accepted"
                    if value_accepted
                    else "source acquisition request is accepted, but endpoint-blind value source is absent"
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
    value_rows = sum(row["value_source_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_value_source_acquisition_table": rel(ACQ_TABLE),
        "input_value_source_acquisition_summary": rel(ACQ_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "value_source_acquisition_acceptance_rows": len(rows),
        "source_acquisition_request_accepted_rows": sum(row["source_acquisition_request_accepted"] == "true" for row in rows),
        "value_source_acquired_rows": sum(row["value_source_acquired"] == "true" for row in rows),
        "value_source_accepted_rows": value_rows,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACQUISITION_REQUESTS_ACCEPTED_SOURCES_ABSENT"
            if input_chain_clean() and len(rows) == 33 and value_rows == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACQUISITION_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Payload Value Source Acquisition Acceptance Audit v01

**Doc class:** role-coordinate numeric value source acquisition acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the source-acquisition rows only as requests. It rejects
them as score inputs because no endpoint-blind value source has been acquired.

## Summary

```text
value_source_acquisition_acceptance_rows={summary["value_source_acquisition_acceptance_rows"]}
source_acquisition_request_accepted_rows={summary["source_acquisition_request_accepted_rows"]}
value_source_acquired_rows={summary["value_source_acquired_rows"]}
value_source_accepted_rows={summary["value_source_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB numeric value source acquisition acceptance.")
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
