#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IMPORT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01.csv"
IMPORT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_v01_"
    "template_packet_accepted_import_rows_rejected_values_absent_no_concrete_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_import_packet_acceptance_row_id",
    "source_numeric_value_import_packet_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "import_template_row_declared",
    "template_packet_accepted",
    "import_numeric_value_present",
    "import_unit_or_convention_present",
    "import_provenance_present",
    "import_replay_present",
    "endpoint_blind_attestation",
    "import_row_accepted",
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
    if not IMPORT_SUMMARY.exists():
        return False
    summary = load_json(IMPORT_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_PACKET_TEMPLATE_SUPPLIED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_v01"
        and summary.get("numeric_value_import_packet_rows") == 33
        and summary.get("import_template_row_declared_rows") == 33
        and summary.get("import_packet_hash_matched") is True
        and summary.get("import_value_supplied_rows") == 0
        and summary.get("import_row_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def present(value: str) -> bool:
    return bool(value.strip())


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value import packet summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(IMPORT_TABLE), start=1):
        template_accepted = source["import_template_row_declared"] == "true"
        value_present = present(source["import_numeric_value"])
        unit_present = present(source["import_unit_or_convention"])
        provenance_present = present(source["import_provenance"])
        replay_present = present(source["import_replay"])
        endpoint_blind = source["endpoint_blind_attestation"] == "true"
        accepted = template_accepted and value_present and unit_present and provenance_present and replay_present and endpoint_blind
        out.append(
            {
                "numeric_value_import_packet_acceptance_row_id": f"TCMBRRCNVIPACC01_{index:03d}",
                "source_numeric_value_import_packet_row_id": source["numeric_value_import_packet_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "import_template_row_declared": source["import_template_row_declared"],
                "template_packet_accepted": str(template_accepted).lower(),
                "import_numeric_value_present": str(value_present).lower(),
                "import_unit_or_convention_present": str(unit_present).lower(),
                "import_provenance_present": str(provenance_present).lower(),
                "import_replay_present": str(replay_present).lower(),
                "endpoint_blind_attestation": source["endpoint_blind_attestation"],
                "import_row_accepted": str(accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "NUMERIC_VALUE_IMPORT_ROW_ACCEPTED"
                    if accepted
                    else "NUMERIC_VALUE_IMPORT_ROW_REJECTED_VALUES_ABSENT"
                ),
                "blocking_reason": (
                    "numeric import row accepted"
                    if accepted
                    else "template packet is accepted, but import value, unit/convention, provenance, and replay are absent"
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
    accepted = sum(row["import_row_accepted"] == "true" for row in table_rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_import_packet_table": rel(IMPORT_TABLE),
        "input_numeric_value_import_packet_summary": rel(IMPORT_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_import_packet_acceptance_rows": len(table_rows),
        "template_packet_accepted_rows": sum(row["template_packet_accepted"] == "true" for row in table_rows),
        "import_row_accepted_rows": accepted,
        "import_row_rejected_rows": len(table_rows) - accepted,
        "import_numeric_value_present_rows": sum(row["import_numeric_value_present"] == "true" for row in table_rows),
        "import_unit_or_convention_present_rows": sum(row["import_unit_or_convention_present"] == "true" for row in table_rows),
        "import_provenance_present_rows": sum(row["import_provenance_present"] == "true" for row in table_rows),
        "import_replay_present_rows": sum(row["import_replay_present"] == "true" for row in table_rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_PACKET_ACCEPTED_TEMPLATE_VALUES_ABSENT"
            if input_chain_clean() and len(table_rows) == 33 and accepted == 0
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_PACKET_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_import_execution_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Import Packet Acceptance Audit v01

**Doc class:** role-coordinate numeric value import packet acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the import packet only as a template packet. It rejects all
33 import rows as score inputs because the numeric values, unit/convention
records, provenance records, and replay records are still absent.

## Summary

```text
numeric_value_import_packet_acceptance_rows={summary["numeric_value_import_packet_acceptance_rows"]}
template_packet_accepted_rows={summary["template_packet_accepted_rows"]}
import_row_accepted_rows={summary["import_row_accepted_rows"]}
import_row_rejected_rows={summary["import_row_rejected_rows"]}
import_numeric_value_present_rows={summary["import_numeric_value_present_rows"]}
import_unit_or_convention_present_rows={summary["import_unit_or_convention_present_rows"]}
import_provenance_present_rows={summary["import_provenance_present_rows"]}
import_replay_present_rows={summary["import_replay_present_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB role-coordinate numeric value import packet acceptance.")
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
