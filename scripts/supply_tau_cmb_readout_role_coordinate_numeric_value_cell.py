#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POPULATION_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_acceptance_audit_summary_v01.json"
POPULATION_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_cell_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_cell_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_cell_supply_v01_"
    "cell_templates_supplied_values_absent_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_cell_supply_row_id",
    "source_numeric_value_population_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_artifact",
    "cell_hash_artifact",
    "cell_template_supplied",
    "hash_supplied",
    "hash_matches",
    "numeric_value_supplied",
    "unit_or_convention_supplied",
    "provenance_supplied",
    "replay_supplied",
    "endpoint_blind_cell",
    "cell_value_accepted",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "supply_status",
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
    if not POPULATION_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(POPULATION_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_POPULATION_ACCEPTANCE_AUDITED_REJECTED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_cell_supply_v01"
        and summary.get("numeric_value_population_acceptance_rows", 0) > 0
        and summary.get("cell_accepted_for_coordinate_rows") == 0
        and summary.get("numeric_value_present_rows") == 0
        and summary.get("unit_or_convention_present_rows") == 0
        and summary.get("provenance_present_rows") == 0
        and summary.get("replay_present_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def cell_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "artifact_status": "NUMERIC_VALUE_CELL_TEMPLATE_SUPPLIED_VALUE_ABSENT",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_numeric_value_population_row_id": row["numeric_value_population_row_id"],
        "role_name": row["role_name"],
        "coordinate_symbol": row["coordinate_symbol"],
        "coordinate_row_id": row["coordinate_row_id"],
        "coordinate_component": row["coordinate_component"],
        "formal_slot": row["formal_slot"],
        "source_dependency": row["source_dependency"],
        "blocked_by": row["blocked_by"],
        "dimension_role": row["dimension_role"],
        "required_fields_for_acceptance": {
            "numeric_value": None,
            "unit_or_convention": None,
            "provenance": None,
            "replay": None,
            "endpoint_blind_attestation": True,
        },
        "numeric_value_supplied": False,
        "unit_or_convention_supplied": False,
        "provenance_supplied": False,
        "replay_supplied": False,
        "endpoint_blind_cell": True,
        "cell_value_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "blocking_reason": "cell template is supplied, but numeric value, unit/convention, provenance, and replay are absent",
        "next_required_step": "populate this cell from an endpoint-blind numeric value import packet",
    }


def rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value population acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(POPULATION_TABLE), start=1):
        artifact = ROOT / "role_coordinate_numeric_value_cells" / source["coordinate_symbol"] / f"{source['numeric_value_population_row_id']}_cell_v01.json"
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, cell_payload(source))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "numeric_value_supplied": False,
                    "cell_value_accepted": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_supplied = hash_artifact.exists()
        hash_matches = supplied and hash_supplied and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        out.append(
            {
                "numeric_value_cell_supply_row_id": f"TCMBRRCNVCSUP01_{index:03d}",
                "source_numeric_value_population_row_id": source["numeric_value_population_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_artifact": rel(artifact),
                "cell_hash_artifact": rel(hash_artifact),
                "cell_template_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "numeric_value_supplied": str(payload.get("numeric_value_supplied") is True).lower(),
                "unit_or_convention_supplied": str(payload.get("unit_or_convention_supplied") is True).lower(),
                "provenance_supplied": str(payload.get("provenance_supplied") is True).lower(),
                "replay_supplied": str(payload.get("replay_supplied") is True).lower(),
                "endpoint_blind_cell": str(payload.get("endpoint_blind_cell") is True).lower(),
                "cell_value_accepted": str(payload.get("cell_value_accepted") is True).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "NUMERIC_VALUE_CELL_TEMPLATE_SUPPLIED_VALUE_ABSENT"
                    if supplied and hash_matches
                    else "NUMERIC_VALUE_CELL_SUPPLY_BLOCKED"
                ),
                "blocking_reason": "cell template supplied, but value fields are absent",
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
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_cell_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_value_population_acceptance_audit_summary": rel(POPULATION_ACCEPTANCE_SUMMARY),
        "input_numeric_value_population_table": rel(POPULATION_TABLE),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_cell_supply_rows": len(table_rows),
        "cell_template_supplied_rows": sum(row["cell_template_supplied"] == "true" for row in table_rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in table_rows),
        "numeric_value_supplied_rows": sum(row["numeric_value_supplied"] == "true" for row in table_rows),
        "unit_or_convention_supplied_rows": sum(row["unit_or_convention_supplied"] == "true" for row in table_rows),
        "provenance_supplied_rows": sum(row["provenance_supplied"] == "true" for row in table_rows),
        "replay_supplied_rows": sum(row["replay_supplied"] == "true" for row in table_rows),
        "cell_value_accepted_rows": sum(row["cell_value_accepted"] == "true" for row in table_rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_CELL_TEMPLATES_SUPPLIED_VALUES_ABSENT"
            if input_chain_clean() and len(table_rows) == 33 and all(row["hash_matches"] == "true" for row in table_rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_CELL_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Cell Supply v01

**Doc class:** role-coordinate numeric value cell supply template
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies one hash-bound cell template for each of the 33
role-coordinate numeric value slots. These are import targets, not values.

## Summary

```text
numeric_value_cell_supply_rows={summary["numeric_value_cell_supply_rows"]}
cell_template_supplied_rows={summary["cell_template_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
numeric_value_supplied_rows={summary["numeric_value_supplied_rows"]}
unit_or_convention_supplied_rows={summary["unit_or_convention_supplied_rows"]}
provenance_supplied_rows={summary["provenance_supplied_rows"]}
replay_supplied_rows={summary["replay_supplied_rows"]}
cell_value_accepted_rows={summary["cell_value_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB role-coordinate numeric value cell templates.")
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
