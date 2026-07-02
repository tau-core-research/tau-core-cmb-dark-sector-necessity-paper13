#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01.csv"
REQUEST_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01_"
    "supply_packet_only_source_artifacts_not_supplied_no_source_acceptance_no_staging_write_"
    "no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "supply_row_id",
    "source_request_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "requested_source_artifact_path",
    "requested_source_hash_path",
    "requested_source_replay_path",
    "requested_source_provenance_path",
    "requested_source_firewall_path",
    "source_artifact_present",
    "source_hash_present",
    "source_replay_present",
    "source_provenance_present",
    "source_firewall_present",
    "complete_source_bundle_present",
    "source_artifact_supplied",
    "source_bundle_supplied",
    "source_artifact_accepted",
    "staging_population_allowed",
    "payload_staging_written",
    "payload_accepted",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "supply_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def table_rows() -> list[dict[str, str]]:
    request_rows = read_csv(REQUEST_TABLE)
    rows: list[dict[str, str]] = []
    for index, request in enumerate(request_rows, start=1):
        artifact = exists(request["requested_source_artifact_path"])
        source_hash = exists(request["requested_source_hash_path"])
        replay = exists(request["requested_source_replay_path"])
        provenance = exists(request["requested_source_provenance_path"])
        firewall = exists(request["requested_source_firewall_path"])
        complete = all([artifact, source_hash, replay, provenance, firewall])
        rows.append(
            {
                "supply_row_id": f"TCMBCDIEBSASP01_{index:03d}",
                "source_request_row_id": request["request_row_id"],
                "certificate_area": request["certificate_area"],
                "checker_name": request["checker_name"],
                "file_category": request["file_category"],
                "requested_source_artifact_path": request["requested_source_artifact_path"],
                "requested_source_hash_path": request["requested_source_hash_path"],
                "requested_source_replay_path": request["requested_source_replay_path"],
                "requested_source_provenance_path": request["requested_source_provenance_path"],
                "requested_source_firewall_path": request["requested_source_firewall_path"],
                "source_artifact_present": str(artifact).lower(),
                "source_hash_present": str(source_hash).lower(),
                "source_replay_present": str(replay).lower(),
                "source_provenance_present": str(provenance).lower(),
                "source_firewall_present": str(firewall).lower(),
                "complete_source_bundle_present": str(complete).lower(),
                "source_artifact_supplied": str(artifact).lower(),
                "source_bundle_supplied": str(complete).lower(),
                "source_artifact_accepted": "false",
                "staging_population_allowed": "false",
                "payload_staging_written": "false",
                "payload_accepted": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "SOURCE_BUNDLE_PRESENT_AWAITING_ACCEPTANCE_AUDIT"
                    if complete
                    else "SOURCE_ARTIFACT_SUPPLY_PACKET_DECLARED_BUNDLE_ABSENT_OR_INCOMPLETE"
                ),
                "blocking_reason": (
                    "complete source bundle is present but not accepted"
                    if complete
                    else "endpoint-blind source artifact, hash, replay, provenance, or firewall files are absent"
                ),
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
    audit = load_json(REQUEST_AUDIT) if REQUEST_AUDIT.exists() else {}
    input_ok = (
        audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_AUDITED_NOT_SUPPLIED"
        and audit.get("failed_rows") == 0
        and REQUEST_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_request_table": rel(REQUEST_TABLE),
        "input_request_audit": rel(REQUEST_AUDIT),
        "input_chain_clean": input_ok,
        "supply_rows": len(rows),
        "source_artifact_present_rows": sum(row["source_artifact_present"] == "true" for row in rows),
        "complete_source_bundle_present_rows": sum(row["complete_source_bundle_present"] == "true" for row in rows),
        "source_artifact_supplied_rows": sum(row["source_artifact_supplied"] == "true" for row in rows),
        "source_bundle_supplied_rows": sum(row["source_bundle_supplied"] == "true" for row in rows),
        "source_artifact_accepted_rows": sum(row["source_artifact_accepted"] == "true" for row in rows),
        "staging_population_allowed_rows": sum(row["staging_population_allowed"] == "true" for row in rows),
        "payload_staging_written_rows": sum(row["payload_staging_written"] == "true" for row in rows),
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_DECLARED_BUNDLE_ABSENT"
            if input_ok and sum(row["complete_source_bundle_present"] == "true" for row in rows) == 0
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_DECLARED_AWAITING_ACCEPTANCE_AUDIT"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} source supply checks" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Supply Packet v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact supply packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet checks whether requested endpoint-blind Tau-side source artifact
bundles are present. It does not create, supply, or accept source artifacts,
populate `payload_staging/`, accept payloads, execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Supply Checks

{area_text}

## Summary

```text
supply_rows={summary["supply_rows"]}
source_artifact_present_rows={summary["source_artifact_present_rows"]}
complete_source_bundle_present_rows={summary["complete_source_bundle_present_rows"]}
source_artifact_accepted_rows={summary["source_artifact_accepted_rows"]}
staging_population_allowed_rows={summary["staging_population_allowed_rows"]}
payload_staging_written_rows={summary["payload_staging_written_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB checker input endpoint-blind source artifact supply packet.")
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
