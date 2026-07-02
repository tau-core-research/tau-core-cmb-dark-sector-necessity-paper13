#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXEC_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance_audit_summary_v01.json"
IMPORT_TEMPLATE = ROOT / "role_coordinate_numeric_value_import_packets/tau_cmb_readout_role_coordinate_numeric_value_import_template_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01.md"
PACKET_PATH = ROOT / "role_coordinate_numeric_value_import_packets/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01.json"
HASH_PATH = ROOT / "role_coordinate_numeric_value_import_packets/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01.hashes.json"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01_"
    "population_contract_declared_no_values_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "population_packet_row_id",
    "source_numeric_value_cell_supply_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_artifact",
    "population_packet_json",
    "population_packet_hash_artifact",
    "required_value_field",
    "required_unit_or_convention_field",
    "required_provenance_field",
    "required_replay_field",
    "required_endpoint_blind_attestation",
    "population_contract_declared",
    "population_value_supplied",
    "population_row_accepted",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "population_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not EXEC_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(EXEC_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_EXECUTION_ACCEPTED_NOOP_RECEIPT_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01"
        and summary.get("numeric_value_import_execution_acceptance_rows") == 33
        and summary.get("execution_row_accepted_as_receipt_rows") == 33
        and summary.get("execution_row_accepted_for_score_rows") == 0
        and summary.get("cell_populated_rows") == 0
        and summary.get("cell_artifact_written_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def write_packet(rows: list[dict[str, str]]) -> None:
    packet = {
        "artifact_status": "NUMERIC_VALUE_IMPORT_POPULATION_CONTRACT_DECLARED_VALUES_ABSENT",
        "claim_boundary": CLAIM_BOUNDARY,
        "input_numeric_value_import_execution_acceptance_audit_summary": rel(EXEC_ACCEPTANCE_SUMMARY),
        "input_import_template": rel(IMPORT_TEMPLATE),
        "population_row_count": len(rows),
        "required_fields_per_row": [
            "import_numeric_value",
            "import_unit_or_convention",
            "import_provenance",
            "import_replay",
            "endpoint_blind_attestation",
        ],
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "population_values_supplied": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "blocking_reason": "population contract is declared, but no numeric population values are supplied",
    }
    write_json(PACKET_PATH, packet)
    write_json(
        HASH_PATH,
        {
            "target": rel(PACKET_PATH),
            "sha256": sha256(PACKET_PATH),
            "claim_boundary": CLAIM_BOUNDARY,
            "population_values_supplied": False,
            "score_entry_allowed": False,
            "likelihood_allowed": False,
            "dark_sector_verdict_allowed": False,
        },
    )


def table_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value import execution acceptance audit summary is not clean")
    template_rows = read_csv(IMPORT_TEMPLATE)
    if write_artifacts:
        write_packet(template_rows)
    hash_matches = HASH_PATH.exists() and PACKET_PATH.exists() and load_json(HASH_PATH).get("sha256") == sha256(PACKET_PATH)
    out: list[dict[str, str]] = []
    for index, source in enumerate(template_rows, start=1):
        out.append(
            {
                "population_packet_row_id": f"TCMBRRCNVIPP01_{index:03d}",
                "source_numeric_value_cell_supply_row_id": source["source_numeric_value_cell_supply_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_artifact": source["cell_artifact"],
                "population_packet_json": rel(PACKET_PATH),
                "population_packet_hash_artifact": rel(HASH_PATH),
                "required_value_field": "import_numeric_value",
                "required_unit_or_convention_field": "import_unit_or_convention",
                "required_provenance_field": "import_provenance",
                "required_replay_field": "import_replay",
                "required_endpoint_blind_attestation": "endpoint_blind_attestation",
                "population_contract_declared": str(hash_matches).lower(),
                "population_value_supplied": "false",
                "population_row_accepted": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "population_status": (
                    "NUMERIC_VALUE_IMPORT_POPULATION_CONTRACT_DECLARED_VALUES_ABSENT"
                    if hash_matches
                    else "NUMERIC_VALUE_IMPORT_POPULATION_PACKET_HASH_BLOCKED"
                ),
                "blocking_reason": "population contract is declared, but no numeric value payload is supplied",
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
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_import_execution_acceptance_audit_summary": rel(EXEC_ACCEPTANCE_SUMMARY),
        "input_import_template": rel(IMPORT_TEMPLATE),
        "population_packet_json": rel(PACKET_PATH),
        "population_packet_hash_artifact": rel(HASH_PATH),
        "input_chain_clean": input_chain_clean(),
        "population_packet_rows": len(rows),
        "population_contract_declared_rows": sum(row["population_contract_declared"] == "true" for row in rows),
        "population_value_supplied_rows": sum(row["population_value_supplied"] == "true" for row in rows),
        "population_row_accepted_rows": sum(row["population_row_accepted"] == "true" for row in rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_POPULATION_CONTRACT_DECLARED_VALUES_ABSENT"
            if input_chain_clean() and len(rows) == 33 and all(row["population_contract_declared"] == "true" for row in rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_POPULATION_PACKET_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Import Population Packet v01

**Doc class:** role-coordinate numeric value import population contract
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet declares the exact 33-row population contract required to turn the
numeric-value import template into populated score-input candidates. It supplies
no values.

## Summary

```text
population_packet_rows={summary["population_packet_rows"]}
population_contract_declared_rows={summary["population_contract_declared_rows"]}
population_value_supplied_rows={summary["population_value_supplied_rows"]}
population_row_accepted_rows={summary["population_row_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB numeric value import population packet.")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows(write_artifacts=args.write_artifacts)
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
