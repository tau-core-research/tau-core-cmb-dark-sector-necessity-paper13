#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALUE_SCORE_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_score_v01.csv"
VALUE_SCORE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_score_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_score_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_score_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_score_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_score_acceptance_audit_v01_"
    "protocol_value_score_accepted_no_physical_CMB_score_no_likelihood_no_verdict"
)

FIELDS = [
    "value_score_acceptance_row_id",
    "source_value_score_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "value_source_accepted",
    "value_score_component",
    "protocol_value_score_component_accepted",
    "physical_CMB_score_component_accepted",
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
    if not VALUE_SCORE_SUMMARY.exists():
        return False
    summary = load_json(VALUE_SCORE_SUMMARY)
    return (
        summary.get("status")
        in {
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_COMPUTED_ZERO_SOURCES_ABSENT",
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_COMPUTED_NULL_CONTROL_BATCH_PROTOCOL_ONLY",
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_COMPUTED_FOCUSED_PROTOCOL_BATCH_ONLY",
        }
        and summary.get("value_score_rows") == 33
        and 0 <= summary.get("value_source_accepted_rows", -1) <= 33
        and summary.get("value_source_accepted_rows") == summary.get("value_score_numerator")
        and summary.get("value_score_denominator") == 33
        and summary.get("value_score") == round(summary.get("value_score_numerator", -1) / 33, 6)
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("numeric value score summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(VALUE_SCORE_TABLE), start=1):
        protocol_accepted = source["value_score_component"] in {"0.000000", "1.000000"}
        physical_accepted = False
        out.append(
            {
                "value_score_acceptance_row_id": f"TCMBRRCNVSCACC01_{index:03d}",
                "source_value_score_row_id": source["value_score_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "value_source_accepted": source["value_source_accepted"],
                "value_score_component": source["value_score_component"],
                "protocol_value_score_component_accepted": str(protocol_accepted).lower(),
                "physical_CMB_score_component_accepted": str(physical_accepted).lower(),
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "PROTOCOL_VALUE_SCORE_COMPONENT_ACCEPTED_PHYSICAL_COMPONENT_BLOCKED"
                ),
                "blocking_reason": (
                    "protocol value score component accepted; physical CMB score component remains blocked"
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
    physical_ready = sum(row["physical_CMB_score_component_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_score_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_value_score_table": rel(VALUE_SCORE_TABLE),
        "input_value_score_summary": rel(VALUE_SCORE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "value_score_acceptance_rows": len(rows),
        "protocol_value_score_component_accepted_rows": sum(row["protocol_value_score_component_accepted"] == "true" for row in rows),
        "physical_CMB_score_component_accepted_rows": physical_ready,
        "protocol_value_score_accepted": True,
        "protocol_value_score": load_json(VALUE_SCORE_SUMMARY).get("value_score"),
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_ACCEPTED_PROTOCOL_FOCUSED_BATCH_PHYSICAL_SCORE_BLOCKED"
            if input_chain_clean()
            and len(rows) == 33
            and physical_ready == 0
            and load_json(VALUE_SCORE_SUMMARY).get("value_score") == 0.515152
            else
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_ACCEPTED_PROTOCOL_NULL_CONTROL_BATCH_PHYSICAL_SCORE_BLOCKED"
            if input_chain_clean()
            and len(rows) == 33
            and physical_ready == 0
            and load_json(VALUE_SCORE_SUMMARY).get("value_score") == 0.151515
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_ACCEPTED_PROTOCOL_ZERO_PHYSICAL_SCORE_BLOCKED"
            if input_chain_clean() and len(rows) == 33 and physical_ready == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SCORE_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": load_json(VALUE_SCORE_SUMMARY).get("next_minimal_unblock"),
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Score Acceptance Audit v01

**Doc class:** protocol value-readiness score acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the value score as a protocol-readiness score only. It does
not accept any physical CMB score component, likelihood, or verdict.

## Summary

```text
value_score_acceptance_rows={summary["value_score_acceptance_rows"]}
protocol_value_score_component_accepted_rows={summary["protocol_value_score_component_accepted_rows"]}
physical_CMB_score_component_accepted_rows={summary["physical_CMB_score_component_accepted_rows"]}
protocol_value_score={summary["protocol_value_score"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB numeric value readiness score acceptance.")
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
