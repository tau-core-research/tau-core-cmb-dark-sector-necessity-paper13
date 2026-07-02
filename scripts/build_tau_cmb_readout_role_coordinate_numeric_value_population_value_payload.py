#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POP_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance_audit_summary_v01.json"
POP_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_v01_"
    "payload_targets_supplied_values_absent_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "population_value_payload_row_id",
    "source_population_packet_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "cell_artifact",
    "value_payload_artifact",
    "value_payload_hash_artifact",
    "payload_target_supplied",
    "hash_supplied",
    "hash_matches",
    "numeric_value_supplied",
    "unit_or_convention_supplied",
    "provenance_supplied",
    "replay_supplied",
    "endpoint_blind_attestation",
    "payload_accepted_for_score",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "payload_status",
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
    if not POP_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(POP_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_IMPORT_POPULATION_CONTRACT_ACCEPTED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_v01"
        and summary.get("population_packet_acceptance_rows") == 33
        and summary.get("population_contract_accepted_rows") == 33
        and summary.get("population_value_supplied_rows") == 0
        and summary.get("population_row_accepted_for_score_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def payload_for(row: dict[str, str]) -> dict[str, Any]:
    return {
        "artifact_status": "POPULATION_VALUE_PAYLOAD_TARGET_SUPPLIED_VALUES_ABSENT",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_population_packet_row_id": row["population_packet_row_id"],
        "role_name": row["role_name"],
        "coordinate_symbol": row["coordinate_symbol"],
        "coordinate_component": row["coordinate_component"],
        "formal_slot": row["formal_slot"],
        "cell_artifact": row["cell_artifact"],
        "required_payload": {
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
        "endpoint_blind_attestation": True,
        "payload_accepted_for_score": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "blocking_reason": "payload target exists, but numeric value, unit/convention, provenance, and replay are absent",
    }


def table_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric value population packet acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(POP_TABLE), start=1):
        artifact = ROOT / "role_coordinate_numeric_value_payloads" / source["coordinate_symbol"] / f"{source['population_packet_row_id']}_value_payload_v01.json"
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, payload_for(source))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "numeric_value_supplied": False,
                    "payload_accepted_for_score": False,
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
                "population_value_payload_row_id": f"TCMBRRCNVPPAY01_{index:03d}",
                "source_population_packet_row_id": source["population_packet_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "cell_artifact": source["cell_artifact"],
                "value_payload_artifact": rel(artifact),
                "value_payload_hash_artifact": rel(hash_artifact),
                "payload_target_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "numeric_value_supplied": str(payload.get("numeric_value_supplied") is True).lower(),
                "unit_or_convention_supplied": str(payload.get("unit_or_convention_supplied") is True).lower(),
                "provenance_supplied": str(payload.get("provenance_supplied") is True).lower(),
                "replay_supplied": str(payload.get("replay_supplied") is True).lower(),
                "endpoint_blind_attestation": str(payload.get("endpoint_blind_attestation") is True).lower(),
                "payload_accepted_for_score": str(payload.get("payload_accepted_for_score") is True).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "payload_status": (
                    "POPULATION_VALUE_PAYLOAD_TARGET_SUPPLIED_VALUES_ABSENT"
                    if supplied and hash_matches
                    else "POPULATION_VALUE_PAYLOAD_TARGET_BLOCKED"
                ),
                "blocking_reason": "payload target supplied, but value fields are absent",
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
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_population_packet_acceptance_audit_summary": rel(POP_ACCEPTANCE_SUMMARY),
        "input_population_packet_table": rel(POP_TABLE),
        "input_chain_clean": input_chain_clean(),
        "population_value_payload_rows": len(rows),
        "payload_target_supplied_rows": sum(row["payload_target_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "numeric_value_supplied_rows": sum(row["numeric_value_supplied"] == "true" for row in rows),
        "unit_or_convention_supplied_rows": sum(row["unit_or_convention_supplied"] == "true" for row in rows),
        "provenance_supplied_rows": sum(row["provenance_supplied"] == "true" for row in rows),
        "replay_supplied_rows": sum(row["replay_supplied"] == "true" for row in rows),
        "payload_accepted_for_score_rows": sum(row["payload_accepted_for_score"] == "true" for row in rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_POPULATION_VALUE_PAYLOAD_TARGETS_SUPPLIED_VALUES_ABSENT"
            if input_chain_clean() and len(rows) == 33 and all(row["hash_matches"] == "true" for row in rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_POPULATION_VALUE_PAYLOAD_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Population Value Payload v01

**Doc class:** role-coordinate numeric value payload target
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies one hash-bound value-payload target for each of the 33
population rows. It does not supply numeric values.

## Summary

```text
population_value_payload_rows={summary["population_value_payload_rows"]}
payload_target_supplied_rows={summary["payload_target_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
numeric_value_supplied_rows={summary["numeric_value_supplied_rows"]}
payload_accepted_for_score_rows={summary["payload_accepted_for_score_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB numeric value population value payload targets.")
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
