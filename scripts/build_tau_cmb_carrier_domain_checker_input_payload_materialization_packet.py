#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FULFILLMENT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01.csv"
FULFILLMENT_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_materialization_packet_v01_"
    "materialization_packet_schema_only_no_payload_files_materialized_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "materialization_row_id",
    "source_fulfillment_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "required_payload_staging_path",
    "template_artifact_path",
    "materialization_requirement",
    "template_status",
    "materialization_status",
    "file_materialized",
    "hash_bound",
    "provenance_bound",
    "replay_bound",
    "firewall_bound",
    "payload_accepted",
    "can_execute_after_materialization",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "blocking_reason",
    "claim_boundary",
]

CATEGORIES = [
    ("payload", "requested_payload_paths", "materialize endpoint-blind checker payload file with required fields and stable content hash"),
    ("replay", "requested_replay_paths", "materialize deterministic replay trace or command without endpoint target access"),
    ("provenance", "requested_provenance_paths", "materialize source provenance, freeze record, and construction rationale"),
    ("hash", "requested_hash_paths", "materialize hash manifest binding payload, replay, provenance, and firewall objects"),
    ("firewall", "requested_firewall_paths", "materialize endpoint-blind firewall attestation and access exclusion log"),
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def template_path_for(staging_path: str) -> str:
    path = Path(staging_path)
    parts = list(path.parts)
    if parts and parts[0] == "payload_staging":
        parts[0] = "payload_templates"
    return str(Path(*parts))


def table_rows() -> list[dict[str, str]]:
    fulfillment_rows = read_csv(FULFILLMENT_TABLE)
    rows: list[dict[str, str]] = []
    counter = 1
    for fulfillment in fulfillment_rows:
        for category, source_field, requirement in CATEGORIES:
            for required_path in split_paths(fulfillment[source_field]):
                rows.append(
                    {
                        "materialization_row_id": f"TCMBCDIMP01_{counter:03d}",
                        "source_fulfillment_row_id": fulfillment["fulfillment_row_id"],
                        "certificate_area": fulfillment["certificate_area"],
                        "checker_name": fulfillment["checker_name"],
                        "file_category": category,
                        "required_payload_staging_path": required_path,
                        "template_artifact_path": template_path_for(required_path),
                        "materialization_requirement": requirement,
                        "template_status": "TEMPLATE_PATH_DECLARED_UNPOPULATED",
                        "materialization_status": "REQUIRED_FILE_NOT_MATERIALIZED",
                        "file_materialized": "false",
                        "hash_bound": "false",
                        "provenance_bound": "false",
                        "replay_bound": "false",
                        "firewall_bound": "false",
                        "payload_accepted": "false",
                        "can_execute_after_materialization": "false",
                        "checker_executed": "false",
                        "certificate_passed": "false",
                        "domain_object_accepted": "false",
                        "allows_concrete_R_CMB": "false",
                        "allows_score_entry": "false",
                        "allows_likelihood": "false",
                        "allows_dark_sector_verdict": "false",
                        "blocking_reason": "template path is declared but the required file is not materialized",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
                counter += 1
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    audit = load_json(FULFILLMENT_AUDIT) if FULFILLMENT_AUDIT.exists() else {}
    input_ok = (
        audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_AUDITED_INCOMPLETE_NOT_EXECUTABLE"
        and audit.get("failed_rows") == 0
        and FULFILLMENT_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_materialization_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_fulfillment_table": rel(FULFILLMENT_TABLE),
        "input_fulfillment_audit": rel(FULFILLMENT_AUDIT),
        "input_chain_clean": input_ok,
        "materialization_rows": len(rows),
        "template_paths_declared": sum(row["template_status"] == "TEMPLATE_PATH_DECLARED_UNPOPULATED" for row in rows),
        "file_materialized_rows": sum(row["file_materialized"] == "true" for row in rows),
        "hash_bound_rows": sum(row["hash_bound"] == "true" for row in rows),
        "provenance_bound_rows": sum(row["provenance_bound"] == "true" for row in rows),
        "replay_bound_rows": sum(row["replay_bound"] == "true" for row in rows),
        "firewall_bound_rows": sum(row["firewall_bound"] == "true" for row in rows),
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "can_execute_after_materialization_rows": sum(row["can_execute_after_materialization"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_MATERIALIZATION_PACKET_SCHEMA_DECLARED_UNMATERIALIZED"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_MATERIALIZATION_PACKET_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_materialization_packet_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    by_area: dict[str, int] = {}
    for row in rows:
        by_area[row["certificate_area"]] = by_area.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} required file slots" for area, count in by_area.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Materialization Packet v01

**Doc class:** carrier/domain checker input payload materialization packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the file-slot level materialization schema for the
carrier/domain checker inputs. It maps every requested payload, replay,
provenance, hash, and firewall file to a template path. It does not materialize
the files, accept payloads, execute checkers, pass certificates, accept domain
objects, materialize `R_CMB`, open score entry, compute a likelihood, or decide
the dark-sector question.

## Slot Counts

{area_text}

## Summary

```text
materialization_rows={summary["materialization_rows"]}
template_paths_declared={summary["template_paths_declared"]}
file_materialized_rows={summary["file_materialized_rows"]}
hash_bound_rows={summary["hash_bound_rows"]}
provenance_bound_rows={summary["provenance_bound_rows"]}
replay_bound_rows={summary["replay_bound_rows"]}
firewall_bound_rows={summary["firewall_bound_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
can_execute_after_materialization_rows={summary["can_execute_after_materialization_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain checker input payload materialization packet.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    summary = build_summary(table_path, rows)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
