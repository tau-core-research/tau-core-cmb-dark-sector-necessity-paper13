#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SATURATION_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_summary_v01.json"
SATURATION_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_endpoint_blind_physical_value_source_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_endpoint_blind_physical_value_source_packet_v01_"
    "physical_source_packet_declared_sources_not_supplied_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "physical_value_source_packet_row_id",
    "source_protocol_saturation_row_id",
    "source_ingest_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "frontier_class",
    "required_next_source",
    "packet_artifact",
    "packet_hash_artifact",
    "packet_declared",
    "packet_hash_matches",
    "requires_numeric_value_or_explicit_fail",
    "requires_unit_or_convention",
    "requires_provenance",
    "requires_replay",
    "requires_endpoint_blind_attestation",
    "requires_forbidden_input_attestation",
    "physical_value_source_supplied",
    "physical_value_source_accepted",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "packet_status",
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
    if not SATURATION_SUMMARY.exists() or not SATURATION_TABLE.exists():
        return False
    summary = load_json(SATURATION_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_PROTOCOL_SATURATION_ACCEPTED_PHYSICAL_VALUE_SOURCES_REQUIRED"
        and summary.get("next_minimal_unblock") == "tau_cmb_endpoint_blind_physical_value_source_packet_v01"
        and summary.get("accepted_protocol_value_sources") == 17
        and summary.get("remaining_frontier_rows") == 16
        and summary.get("protocol_only_frontier_closed") is True
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def packet_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "artifact_status": "ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_DECLARED_SOURCE_NOT_SUPPLIED",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_protocol_saturation_row_id": row["protocol_saturation_row_id"],
        "source_ingest_row_id": row["source_ingest_row_id"],
        "role_name": row["role_name"],
        "coordinate_symbol": row["coordinate_symbol"],
        "coordinate_component": row["coordinate_component"],
        "formal_slot": row["formal_slot"],
        "frontier_class": row["frontier_class"],
        "required_next_source": row["required_next_source"],
        "supply_contract": {
            "numeric_value_or_explicit_fail": "required",
            "unit_or_convention": "required",
            "provenance": "required",
            "local_replay": "required",
            "endpoint_blind_attestation": "required",
            "forbidden_input_attestation": "required",
        },
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "physical_value_source_supplied": False,
        "physical_value_source_accepted": False,
        "allows_physical_CMB_score": False,
        "allows_likelihood": False,
        "allows_dark_sector_verdict": False,
        "blocking_reason": "endpoint-blind physical value source or explicit fail evidence is required but not supplied",
    }


def table_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("protocol saturation audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(SATURATION_TABLE), start=1):
        artifact = ROOT / "endpoint_blind_physical_value_source_packets" / source["coordinate_symbol"] / f"{source['protocol_saturation_row_id']}_physical_value_source_packet_v01.json"
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, packet_payload(source))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "physical_value_source_supplied": False,
                    "physical_value_source_accepted": False,
                    "allows_physical_CMB_score": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_matches = supplied and hash_artifact.exists() and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        out.append(
            {
                "physical_value_source_packet_row_id": f"TCMBEBPVSP01_{index:03d}",
                "source_protocol_saturation_row_id": source["protocol_saturation_row_id"],
                "source_ingest_row_id": source["source_ingest_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "frontier_class": source["frontier_class"],
                "required_next_source": source["required_next_source"],
                "packet_artifact": rel(artifact),
                "packet_hash_artifact": rel(hash_artifact),
                "packet_declared": str(supplied).lower(),
                "packet_hash_matches": str(hash_matches).lower(),
                "requires_numeric_value_or_explicit_fail": "true",
                "requires_unit_or_convention": "true",
                "requires_provenance": "true",
                "requires_replay": "true",
                "requires_endpoint_blind_attestation": "true",
                "requires_forbidden_input_attestation": "true",
                "physical_value_source_supplied": str(payload.get("physical_value_source_supplied") is True).lower(),
                "physical_value_source_accepted": str(payload.get("physical_value_source_accepted") is True).lower(),
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "packet_status": (
                    "ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_DECLARED_SOURCE_NOT_SUPPLIED"
                    if supplied and hash_matches
                    else "ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_BLOCKED"
                ),
                "blocking_reason": "endpoint-blind physical value source or explicit fail evidence is not supplied",
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
    class_counts: dict[str, int] = {}
    for row in rows:
        class_counts[row["frontier_class"]] = class_counts.get(row["frontier_class"], 0) + 1
    return {
        "report_id": "tau_cmb_endpoint_blind_physical_value_source_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_protocol_saturation_summary": rel(SATURATION_SUMMARY),
        "input_protocol_saturation_table": rel(SATURATION_TABLE),
        "input_chain_clean": input_chain_clean(),
        "physical_value_source_packet_rows": len(rows),
        "packet_declared_rows": sum(row["packet_declared"] == "true" for row in rows),
        "packet_hash_matched_rows": sum(row["packet_hash_matches"] == "true" for row in rows),
        "physical_value_source_supplied_rows": sum(row["physical_value_source_supplied"] == "true" for row in rows),
        "physical_value_source_accepted_rows": sum(row["physical_value_source_accepted"] == "true" for row in rows),
        "frontier_class_counts": class_counts,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_DECLARED_SOURCES_NOT_SUPPLIED"
            if input_chain_clean()
            and len(rows) == 16
            and all(row["packet_hash_matches"] == "true" for row in rows)
            and all(row["physical_value_source_accepted"] == "false" for row in rows)
            else "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_endpoint_blind_physical_value_source_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Endpoint-Blind Physical Value Source Packet v01

**Doc class:** endpoint-blind physical value-source packet
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet turns the 16 post-saturation frontier rows into concrete
endpoint-blind supply contracts. It does not supply or accept physical values.

Each row requires a numeric value or explicit fail evidence, unit/convention,
provenance, replay, endpoint-blind attestation, and forbidden-input attestation.

## Summary

```text
physical_value_source_packet_rows={summary["physical_value_source_packet_rows"]}
packet_declared_rows={summary["packet_declared_rows"]}
packet_hash_matched_rows={summary["packet_hash_matched_rows"]}
physical_value_source_supplied_rows={summary["physical_value_source_supplied_rows"]}
physical_value_source_accepted_rows={summary["physical_value_source_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB endpoint-blind physical value-source packet.")
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
