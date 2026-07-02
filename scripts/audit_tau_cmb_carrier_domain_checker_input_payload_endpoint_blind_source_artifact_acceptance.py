#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_summary_v01.json"
SUPPLY_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_audit_v01.json"
MATERIALIZATION_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_v01_"
    "source_artifact_candidates_accepted_for_staging_population_only_no_staging_write_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "acceptance_row_id",
    "supply_row_id",
    "source_request_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "source_artifact_path",
    "source_hash_path",
    "source_replay_path",
    "source_provenance_path",
    "source_firewall_path",
    "complete_source_bundle_present",
    "hash_binding_valid",
    "source_inventory_complete",
    "provenance_complete",
    "replay_complete",
    "firewall_endpoint_blind",
    "candidate_boundary_clean",
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
    "acceptance_status",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bool_text(value: bool) -> str:
    return str(value).lower()


def bundle_paths(row: dict[str, str]) -> dict[str, Path]:
    return {
        "artifact": ROOT / row["requested_source_artifact_path"],
        "hash": ROOT / row["requested_source_hash_path"],
        "replay": ROOT / row["requested_source_replay_path"],
        "provenance": ROOT / row["requested_source_provenance_path"],
        "firewall": ROOT / row["requested_source_firewall_path"],
    }


def hash_binding_valid(hash_path: Path) -> bool:
    if not hash_path.exists():
        return False
    hash_doc = load_json(hash_path)
    files = hash_doc.get("files", {})
    if not files:
        return False
    for raw_path, expected_hash in files.items():
        path = Path(raw_path)
        if not path.exists() or sha256(path) != expected_hash:
            return False
    return True


def candidate_boundary_clean(payloads: list[dict[str, Any]]) -> bool:
    for payload in payloads:
        if payload.get("source_artifact_accepted") is True:
            return False
        if payload.get("staging_population_allowed") is True:
            return False
        permissions = payload.get("acceptance_permissions", {})
        if permissions:
            if permissions.get("payload_accepted") is True:
                return False
            if permissions.get("checker_execution_allowed") is True:
                return False
            if permissions.get("concrete_R_CMB_allowed") is True:
                return False
            if permissions.get("score_entry_allowed") is True:
                return False
            if permissions.get("likelihood_allowed") is True:
                return False
            if permissions.get("dark_sector_verdict_allowed") is True:
                return False
    return True


def source_inventory_complete(artifact: dict[str, Any], provenance: dict[str, Any]) -> bool:
    inventory = artifact.get("source_inventory", [])
    if not inventory:
        return False
    if any(not item.get("exists") for item in inventory):
        return False
    if provenance.get("missing_source_references"):
        return False
    return True


def acceptance_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, supply in enumerate(read_csv(SUPPLY_TABLE), start=1):
        paths = bundle_paths(supply)
        complete = all(path.exists() for path in paths.values()) and supply.get("complete_source_bundle_present") == "true"
        artifact = load_json(paths["artifact"]) if paths["artifact"].exists() else {}
        provenance = load_json(paths["provenance"]) if paths["provenance"].exists() else {}
        replay = load_json(paths["replay"]) if paths["replay"].exists() else {}
        firewall = load_json(paths["firewall"]) if paths["firewall"].exists() else {}
        hash_doc = load_json(paths["hash"]) if paths["hash"].exists() else {}
        payloads = [artifact, provenance, replay, firewall, hash_doc]

        hash_ok = complete and hash_binding_valid(paths["hash"])
        inventory_ok = complete and source_inventory_complete(artifact, provenance)
        provenance_ok = complete and provenance.get("construction_method") == "local endpoint-blind source inventory materialization"
        replay_ok = complete and "materialization-packet" in replay.get("replay_command", "")
        firewall_ok = complete and firewall.get("endpoint_blind_attestation") is True and firewall.get("source_artifact_accepted") is False
        boundary_ok = complete and candidate_boundary_clean(payloads)
        accepted = all([complete, hash_ok, inventory_ok, provenance_ok, replay_ok, firewall_ok, boundary_ok])
        rows.append(
            {
                "acceptance_row_id": f"TCMBCDIEBSAA01_{index:03d}",
                "supply_row_id": supply["supply_row_id"],
                "source_request_row_id": supply["source_request_row_id"],
                "certificate_area": supply["certificate_area"],
                "checker_name": supply["checker_name"],
                "file_category": supply["file_category"],
                "source_artifact_path": supply["requested_source_artifact_path"],
                "source_hash_path": supply["requested_source_hash_path"],
                "source_replay_path": supply["requested_source_replay_path"],
                "source_provenance_path": supply["requested_source_provenance_path"],
                "source_firewall_path": supply["requested_source_firewall_path"],
                "complete_source_bundle_present": bool_text(complete),
                "hash_binding_valid": bool_text(hash_ok),
                "source_inventory_complete": bool_text(inventory_ok),
                "provenance_complete": bool_text(provenance_ok),
                "replay_complete": bool_text(replay_ok),
                "firewall_endpoint_blind": bool_text(firewall_ok),
                "candidate_boundary_clean": bool_text(boundary_ok),
                "source_artifact_accepted": bool_text(accepted),
                "staging_population_allowed": bool_text(accepted),
                "payload_staging_written": "false",
                "payload_accepted": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "SOURCE_ARTIFACT_ACCEPTED_FOR_STAGING_POPULATION_ONLY"
                    if accepted
                    else "SOURCE_ARTIFACT_ACCEPTANCE_BLOCKED"
                ),
                "blocking_reason": (
                    "accepted source artifact may be used by the staging population step"
                    if accepted
                    else "source bundle failed presence/hash/provenance/replay/firewall/boundary acceptance checks"
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
    supply_summary = load_json(SUPPLY_SUMMARY) if SUPPLY_SUMMARY.exists() else {}
    supply_audit = load_json(SUPPLY_AUDIT) if SUPPLY_AUDIT.exists() else {}
    materialization_audit = load_json(MATERIALIZATION_AUDIT) if MATERIALIZATION_AUDIT.exists() else {}
    input_ok = (
        supply_summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_DECLARED_AWAITING_ACCEPTANCE_AUDIT"
        and supply_summary.get("complete_source_bundle_present_rows") == 66
        and supply_audit.get("status") == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_AUDITED"
        and supply_audit.get("failed_rows") == 0
        and materialization_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_MATERIALIZATION_AUDITED_NOT_ACCEPTED"
        and materialization_audit.get("failed_rows") == 0
    )
    accepted_rows = sum(row["source_artifact_accepted"] == "true" for row in rows)
    staging_allowed_rows = sum(row["staging_population_allowed"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_supply_summary": rel(SUPPLY_SUMMARY),
        "input_supply_audit": rel(SUPPLY_AUDIT),
        "input_materialization_audit": rel(MATERIALIZATION_AUDIT),
        "input_chain_clean": input_ok,
        "acceptance_rows": len(rows),
        "complete_source_bundle_present_rows": sum(row["complete_source_bundle_present"] == "true" for row in rows),
        "hash_binding_valid_rows": sum(row["hash_binding_valid"] == "true" for row in rows),
        "source_inventory_complete_rows": sum(row["source_inventory_complete"] == "true" for row in rows),
        "provenance_complete_rows": sum(row["provenance_complete"] == "true" for row in rows),
        "replay_complete_rows": sum(row["replay_complete"] == "true" for row in rows),
        "firewall_endpoint_blind_rows": sum(row["firewall_endpoint_blind"] == "true" for row in rows),
        "candidate_boundary_clean_rows": sum(row["candidate_boundary_clean"] == "true" for row in rows),
        "source_artifact_accepted_rows": accepted_rows,
        "staging_population_allowed_rows": staging_allowed_rows,
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACTS_ACCEPTED_FOR_STAGING_POPULATION_ONLY"
            if input_ok and accepted_rows == 66 and staging_allowed_rows == 66
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_ACCEPTANCE_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} accepted source rows" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Acceptance v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact acceptance audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts endpoint-blind Tau-side source artifact candidate bundles
only for the next staging-population step. Acceptance here means that the
candidate bundle is present, hash-bound, provenance/replay/firewall accompanied,
endpoint-blind, and locally source-inventory complete. It does not write
`payload_staging/`, accept payloads, execute checkers, pass certificates, accept
domain objects, materialize `R_CMB`, open score entry, compute a likelihood, or
decide the dark-sector question.

## Acceptance Coverage

{area_text}

## Summary

```text
acceptance_rows={summary["acceptance_rows"]}
source_artifact_accepted_rows={summary["source_artifact_accepted_rows"]}
staging_population_allowed_rows={summary["staging_population_allowed_rows"]}
payload_staging_written_rows={summary["payload_staging_written_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
checker_executed_rows={summary["checker_executed_rows"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Status

```text
{summary["status"]}
```

The source artifacts are accepted only as source inputs for the staging
population step. Downstream physical-readout and scoring claims remain closed.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB endpoint-blind source artifact acceptance.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = acceptance_rows()
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
