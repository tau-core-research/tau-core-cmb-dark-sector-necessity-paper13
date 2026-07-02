#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CELL_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_summary_v01.json"
CELL_SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_supply_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01.md"
PACKET_DIR = ROOT / "role_coordinate_numeric_value_import_packets"
PACKET_JSON = PACKET_DIR / "tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01.json"
PACKET_CSV = PACKET_DIR / "tau_cmb_readout_role_coordinate_numeric_value_import_template_v01.csv"
PACKET_HASH = PACKET_DIR / "tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01.hashes.json"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01_"
    "import_template_supplied_values_absent_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_import_packet_row_id",
    "source_numeric_value_cell_supply_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_artifact",
    "import_packet_json",
    "import_template_csv",
    "import_packet_hash_artifact",
    "import_template_row_declared",
    "import_numeric_value",
    "import_unit_or_convention",
    "import_provenance",
    "import_replay",
    "endpoint_blind_attestation",
    "import_value_supplied",
    "import_row_accepted",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "import_status",
    "blocking_reason",
    "claim_boundary",
]

IMPORT_FIELDS = [
    "source_numeric_value_cell_supply_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_artifact",
    "import_numeric_value",
    "import_unit_or_convention",
    "import_provenance",
    "import_replay",
    "endpoint_blind_attestation",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not CELL_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(CELL_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_CELL_TEMPLATES_ACCEPTED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_import_packet_v01"
        and summary.get("numeric_value_cell_acceptance_rows") == 33
        and summary.get("template_accepted_rows") == 33
        and summary.get("cell_value_accepted_rows") == 0
        and summary.get("numeric_value_supplied_rows") == 0
        and summary.get("unit_or_convention_supplied_rows") == 0
        and summary.get("provenance_supplied_rows") == 0
        and summary.get("replay_supplied_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def import_template_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in read_csv(CELL_SUPPLY_TABLE):
        rows.append(
            {
                "source_numeric_value_cell_supply_row_id": source["numeric_value_cell_supply_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_artifact": source["cell_artifact"],
                "import_numeric_value": "",
                "import_unit_or_convention": "",
                "import_provenance": "",
                "import_replay": "",
                "endpoint_blind_attestation": "true",
            }
        )
    return rows


def write_import_template(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=IMPORT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_packet_artifacts() -> None:
    rows = import_template_rows()
    write_import_template(PACKET_CSV, rows)
    packet = {
        "artifact_status": "NUMERIC_VALUE_IMPORT_PACKET_TEMPLATE_SUPPLIED_VALUES_ABSENT",
        "claim_boundary": CLAIM_BOUNDARY,
        "input_numeric_value_cell_acceptance_audit_summary": rel(CELL_ACCEPTANCE_SUMMARY),
        "input_numeric_value_cell_supply_table": rel(CELL_SUPPLY_TABLE),
        "import_template_csv": rel(PACKET_CSV),
        "import_row_count": len(rows),
        "required_import_fields": IMPORT_FIELDS,
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "numeric_values_supplied": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "blocking_reason": "import packet schema and template are supplied, but numeric values are absent",
        "next_required_step": "execute endpoint-blind numeric value import by filling all 33 import rows with value, unit/convention, provenance, and replay",
    }
    write_json(PACKET_JSON, packet)
    write_json(
        PACKET_HASH,
        {
            "claim_boundary": CLAIM_BOUNDARY,
            "hash_scope": "numeric_value_import_packet_template_bundle",
            "files": {
                rel(PACKET_JSON): sha256(PACKET_JSON),
                rel(PACKET_CSV): sha256(PACKET_CSV),
            },
            "numeric_values_supplied": False,
            "score_entry_allowed": False,
            "likelihood_allowed": False,
            "dark_sector_verdict_allowed": False,
        },
    )


def rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value cell acceptance audit summary is not clean")
    if write_artifacts:
        write_packet_artifacts()
    out: list[dict[str, str]] = []
    hash_payload = load_json(PACKET_HASH) if PACKET_HASH.exists() else {}
    hash_matches = (
        PACKET_JSON.exists()
        and PACKET_CSV.exists()
        and PACKET_HASH.exists()
        and hash_payload.get("files", {}).get(rel(PACKET_JSON)) == sha256(PACKET_JSON)
        and hash_payload.get("files", {}).get(rel(PACKET_CSV)) == sha256(PACKET_CSV)
    )
    for index, source in enumerate(read_csv(CELL_SUPPLY_TABLE), start=1):
        out.append(
            {
                "numeric_value_import_packet_row_id": f"TCMBRRCNVIP01_{index:03d}",
                "source_numeric_value_cell_supply_row_id": source["numeric_value_cell_supply_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_artifact": source["cell_artifact"],
                "import_packet_json": rel(PACKET_JSON),
                "import_template_csv": rel(PACKET_CSV),
                "import_packet_hash_artifact": rel(PACKET_HASH),
                "import_template_row_declared": "true",
                "import_numeric_value": "",
                "import_unit_or_convention": "",
                "import_provenance": "",
                "import_replay": "",
                "endpoint_blind_attestation": "true",
                "import_value_supplied": "false",
                "import_row_accepted": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "import_status": (
                    "NUMERIC_VALUE_IMPORT_TEMPLATE_ROW_DECLARED_VALUE_ABSENT"
                    if hash_matches
                    else "NUMERIC_VALUE_IMPORT_PACKET_HASH_BLOCKED"
                ),
                "blocking_reason": "import row is declared, but numeric value, unit/convention, provenance, and replay are absent",
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
    hash_matched = all(row["import_status"] == "NUMERIC_VALUE_IMPORT_TEMPLATE_ROW_DECLARED_VALUE_ABSENT" for row in table_rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_import_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_cell_acceptance_audit_summary": rel(CELL_ACCEPTANCE_SUMMARY),
        "input_numeric_value_cell_supply_table": rel(CELL_SUPPLY_TABLE),
        "import_packet_json": rel(PACKET_JSON),
        "import_template_csv": rel(PACKET_CSV),
        "import_packet_hash_artifact": rel(PACKET_HASH),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_import_packet_rows": len(table_rows),
        "import_template_row_declared_rows": sum(row["import_template_row_declared"] == "true" for row in table_rows),
        "import_packet_hash_matched": hash_matched,
        "import_value_supplied_rows": sum(row["import_value_supplied"] == "true" for row in table_rows),
        "import_row_accepted_rows": sum(row["import_row_accepted"] == "true" for row in table_rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_PACKET_TEMPLATE_SUPPLIED_VALUES_ABSENT"
            if input_chain_clean() and len(table_rows) == 33 and hash_matched
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_PACKET_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Import Packet v01

**Doc class:** role-coordinate numeric value import packet template
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies a single endpoint-blind import packet template for the 33
numeric-value cell templates. It defines the import schema and hash-binds the
packet, but supplies no numeric values.

## Summary

```text
numeric_value_import_packet_rows={summary["numeric_value_import_packet_rows"]}
import_template_row_declared_rows={summary["import_template_row_declared_rows"]}
import_packet_hash_matched={summary["import_packet_hash_matched"]}
import_value_supplied_rows={summary["import_value_supplied_rows"]}
import_row_accepted_rows={summary["import_row_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB role-coordinate numeric value import packet.")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_rows = rows(write_artifacts=args.write_artifacts)
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
