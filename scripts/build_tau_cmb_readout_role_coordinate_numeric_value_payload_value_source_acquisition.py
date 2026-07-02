#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_acceptance_audit_summary_v01.json"
PAYLOAD_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_v01_"
    "source_acquisition_requests_declared_no_sources_acquired_no_concrete_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "value_source_acquisition_row_id",
    "source_population_value_payload_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "value_payload_artifact",
    "source_acquisition_artifact",
    "source_acquisition_hash_artifact",
    "source_acquisition_request_declared",
    "source_acquisition_hash_matches",
    "required_numeric_value_source",
    "required_unit_or_convention_source",
    "required_provenance_source",
    "required_replay_source",
    "endpoint_blind_attestation_required",
    "value_source_acquired",
    "value_source_accepted",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "acquisition_status",
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
    if not PAYLOAD_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(PAYLOAD_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_POPULATION_VALUE_PAYLOAD_TARGETS_ACCEPTED_VALUES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_v01"
        and summary.get("population_value_payload_acceptance_rows") == 33
        and summary.get("payload_target_accepted_rows") == 33
        and summary.get("numeric_value_supplied_rows") == 0
        and summary.get("payload_accepted_for_score_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def acquisition_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "artifact_status": "VALUE_SOURCE_ACQUISITION_REQUEST_DECLARED_NO_SOURCE_ACQUIRED",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_population_value_payload_row_id": row["population_value_payload_row_id"],
        "role_name": row["role_name"],
        "coordinate_symbol": row["coordinate_symbol"],
        "coordinate_component": row["coordinate_component"],
        "formal_slot": row["formal_slot"],
        "value_payload_artifact": row["value_payload_artifact"],
        "required_sources": {
            "numeric_value_source": "endpoint-blind numeric source for the formal slot",
            "unit_or_convention_source": "unit, normalization, or convention replay source",
            "provenance_source": "source provenance record independent of endpoint residuals",
            "replay_source": "local replay command or artifact that regenerates the value",
            "endpoint_blind_attestation": "attestation excluding endpoint residuals, likelihood outputs, post-endpoint tuning, and verdict labels",
        },
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "value_source_acquired": False,
        "value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "blocking_reason": "source acquisition request is declared, but no endpoint-blind value source is acquired",
    }


def table_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("population value payload acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(PAYLOAD_TABLE), start=1):
        artifact = ROOT / "role_coordinate_numeric_value_source_acquisition" / source["coordinate_symbol"] / f"{source['population_value_payload_row_id']}_source_acquisition_v01.json"
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, acquisition_payload(source))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "value_source_acquired": False,
                    "value_source_accepted": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_matches = supplied and hash_artifact.exists() and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        out.append(
            {
                "value_source_acquisition_row_id": f"TCMBRRCNVVSACQ01_{index:03d}",
                "source_population_value_payload_row_id": source["population_value_payload_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "value_payload_artifact": source["value_payload_artifact"],
                "source_acquisition_artifact": rel(artifact),
                "source_acquisition_hash_artifact": rel(hash_artifact),
                "source_acquisition_request_declared": str(supplied).lower(),
                "source_acquisition_hash_matches": str(hash_matches).lower(),
                "required_numeric_value_source": "true",
                "required_unit_or_convention_source": "true",
                "required_provenance_source": "true",
                "required_replay_source": "true",
                "endpoint_blind_attestation_required": "true",
                "value_source_acquired": str(payload.get("value_source_acquired") is True).lower(),
                "value_source_accepted": str(payload.get("value_source_accepted") is True).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acquisition_status": (
                    "VALUE_SOURCE_ACQUISITION_REQUEST_DECLARED_NO_SOURCE_ACQUIRED"
                    if supplied and hash_matches
                    else "VALUE_SOURCE_ACQUISITION_REQUEST_BLOCKED"
                ),
                "blocking_reason": "source acquisition request declared, but value source is not acquired",
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
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_population_value_payload_acceptance_audit_summary": rel(PAYLOAD_ACCEPTANCE_SUMMARY),
        "input_population_value_payload_table": rel(PAYLOAD_TABLE),
        "input_chain_clean": input_chain_clean(),
        "value_source_acquisition_rows": len(rows),
        "source_acquisition_request_declared_rows": sum(row["source_acquisition_request_declared"] == "true" for row in rows),
        "source_acquisition_hash_matched_rows": sum(row["source_acquisition_hash_matches"] == "true" for row in rows),
        "value_source_acquired_rows": sum(row["value_source_acquired"] == "true" for row in rows),
        "value_source_accepted_rows": sum(row["value_source_accepted"] == "true" for row in rows),
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACQUISITION_REQUESTS_DECLARED_NO_SOURCES_ACQUIRED"
            if input_chain_clean() and len(rows) == 33 and all(row["source_acquisition_hash_matches"] == "true" for row in rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACQUISITION_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Payload Value Source Acquisition v01

**Doc class:** role-coordinate numeric value source acquisition request
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step declares one endpoint-blind source-acquisition request for each of
the 33 value-payload targets. It does not acquire numeric sources.

## Summary

```text
value_source_acquisition_rows={summary["value_source_acquisition_rows"]}
source_acquisition_request_declared_rows={summary["source_acquisition_request_declared_rows"]}
source_acquisition_hash_matched_rows={summary["source_acquisition_hash_matched_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB numeric value source acquisition requests.")
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
