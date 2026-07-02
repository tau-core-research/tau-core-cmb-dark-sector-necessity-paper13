#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACQ_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_summary_v01.json"
ACQ_ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_v01.csv"
INGEST_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_summary_v01.json"
INGEST_ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_score_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_score_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_score_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_score_v01_"
    "protocol_value_readiness_score_only_no_physical_CMB_score_no_likelihood_no_verdict"
)

FIELDS = [
    "value_score_row_id",
    "source_acquisition_acceptance_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "source_acquisition_request_accepted",
    "value_source_acquired",
    "value_source_accepted",
    "value_score_component",
    "value_score_status",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
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
    if INGEST_ACCEPTANCE_SUMMARY.exists():
        summary = load_json(INGEST_ACCEPTANCE_SUMMARY)
        return (
            summary.get("status")
            in {
                "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGEST_ACCEPTED_NULL_CONTROL_PROTOCOL_ONLY",
                "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGEST_ACCEPTED_FOCUSED_PROTOCOL_ONLY",
            }
            and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_next_role_v01"
            and summary.get("source_ingest_acceptance_rows") == 33
            and 0 <= summary.get("protocol_value_component_accepted_rows", -1) <= 33
            and summary.get("physical_CMB_component_accepted_rows") == 0
            and summary.get("physical_CMB_score_allowed") is False
            and summary.get("likelihood_allowed") is False
            and summary.get("dark_sector_verdict_allowed") is False
        )
    if not ACQ_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(ACQ_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACQUISITION_REQUESTS_ACCEPTED_SOURCES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01"
        and summary.get("value_source_acquisition_acceptance_rows") == 33
        and summary.get("source_acquisition_request_accepted_rows") == 33
        and summary.get("value_source_acquired_rows") == 0
        and summary.get("value_source_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("value source acceptance input summary is not clean")
    if INGEST_ACCEPTANCE_SUMMARY.exists():
        rows: list[dict[str, str]] = []
        for index, source in enumerate(read_csv(INGEST_ACCEPTANCE_TABLE), start=1):
            component_score = 1.0 if source["protocol_value_component_accepted"] == "true" else 0.0
            rows.append(
                {
                    "value_score_row_id": f"TCMBRRCNVSC01_{index:03d}",
                    "source_acquisition_acceptance_row_id": source["source_ingest_acceptance_row_id"],
                    "role_name": source["role_name"],
                    "coordinate_symbol": source["coordinate_symbol"],
                    "coordinate_component": source["coordinate_component"],
                    "formal_slot": source["formal_slot"],
                    "source_acquisition_request_accepted": "true",
                    "value_source_acquired": source["protocol_value_component_accepted"],
                    "value_source_accepted": source["protocol_value_component_accepted"],
                    "value_score_component": f"{component_score:.6f}",
                    "value_score_status": (
                        "PROTOCOL_VALUE_SOURCE_ACCEPTED_COMPONENT_READY"
                        if component_score == 1.0
                        else "VALUE_SOURCE_ABSENT_COMPONENT_SCORE_ZERO"
                    ),
                    "allows_physical_CMB_score": "false",
                    "allows_likelihood": "false",
                    "allows_dark_sector_verdict": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        return rows
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(ACQ_ACCEPTANCE_TABLE), start=1):
        component_score = 1.0 if source["value_source_accepted"] == "true" else 0.0
        rows.append(
            {
                "value_score_row_id": f"TCMBRRCNVSC01_{index:03d}",
                "source_acquisition_acceptance_row_id": source["value_source_acquisition_acceptance_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "source_acquisition_request_accepted": source["source_acquisition_request_accepted"],
                "value_source_acquired": source["value_source_acquired"],
                "value_source_accepted": source["value_source_accepted"],
                "value_score_component": f"{component_score:.6f}",
                "value_score_status": (
                    "VALUE_SOURCE_ACCEPTED_COMPONENT_READY"
                    if component_score == 1.0
                    else "VALUE_SOURCE_ABSENT_COMPONENT_SCORE_ZERO"
                ),
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    total = len(rows)
    accepted = sum(row["value_source_accepted"] == "true" for row in rows)
    value_score = accepted / total if total else 0.0
    input_summary = INGEST_ACCEPTANCE_SUMMARY if INGEST_ACCEPTANCE_SUMMARY.exists() else ACQ_ACCEPTANCE_SUMMARY
    input_table = INGEST_ACCEPTANCE_TABLE if INGEST_ACCEPTANCE_SUMMARY.exists() else ACQ_ACCEPTANCE_TABLE
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_score_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_value_source_acceptance_summary": rel(input_summary),
        "input_value_source_acceptance_table": rel(input_table),
        "input_chain_clean": input_chain_clean(),
        "value_score_rows": total,
        "source_acquisition_request_accepted_rows": sum(row["source_acquisition_request_accepted"] == "true" for row in rows),
        "value_source_acquired_rows": sum(row["value_source_acquired"] == "true" for row in rows),
        "value_source_accepted_rows": accepted,
        "value_score_numerator": accepted,
        "value_score_denominator": total,
        "value_score": round(value_score, 6),
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_COMPUTED_FOCUSED_PROTOCOL_BATCH_ONLY"
            if input_chain_clean() and total == 33 and accepted == 17
            else
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_COMPUTED_NULL_CONTROL_BATCH_PROTOCOL_ONLY"
            if input_chain_clean() and total == 33 and accepted == 5
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_COMPUTED_ZERO_SOURCES_ABSENT"
            if input_chain_clean() and total == 33 and accepted == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_next_role_v01"
            if accepted > 0
            else "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01"
        ),
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Score v01

**Doc class:** protocol value-readiness score
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact computes a protocol value-readiness score:

```text
value_score = accepted_value_sources / required_value_sources
```

It is not a physical CMB score, not a likelihood, and not a dark-sector verdict.

## Summary

```text
value_score_rows={summary["value_score_rows"]}
value_source_accepted_rows={summary["value_source_accepted_rows"]}
value_score_numerator={summary["value_score_numerator"]}
value_score_denominator={summary["value_score_denominator"]}
value_score={summary["value_score"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB numeric value readiness score.")
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
