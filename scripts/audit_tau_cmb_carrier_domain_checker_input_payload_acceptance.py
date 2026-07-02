#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STAGING_EXEC_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01.csv"
STAGING_EXEC_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_v01_"
    "payload_staging_files_accepted_as_checker_inputs_only_no_checker_execution_no_certificate_pass_"
    "no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "acceptance_row_id",
    "source_execution_row_id",
    "source_population_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "payload_staging_path",
    "payload_staging_present",
    "staging_hash_matches",
    "staging_boundary_clean",
    "endpoint_blind_firewall_clean",
    "source_artifact_trace_present",
    "payload_accepted",
    "checker_input_available",
    "checker_execution_allowed",
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


def input_chain_clean() -> bool:
    if not STAGING_EXEC_AUDIT.exists():
        return False
    audit = load_json(STAGING_EXEC_AUDIT)
    return (
        audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_AUDITED_PAYLOADS_POPULATED_NOT_ACCEPTED"
        and audit.get("failed_rows") == 0
        and audit.get("staging_population_execution_succeeded") is True
        and audit.get("payload_acceptance_allowed") is False
        and audit.get("checker_execution_allowed") is False
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def staging_boundary_clean(payload: dict[str, Any]) -> bool:
    permissions = payload.get("acceptance_permissions", {})
    return (
        payload.get("staging_status") == "POPULATED_FROM_ACCEPTED_ENDPOINT_BLIND_TAU_SIDE_SOURCE_NOT_ACCEPTED"
        and permissions.get("payload_accepted") is False
        and permissions.get("checker_execution_allowed") is False
        and permissions.get("certificate_pass_allowed") is False
        and permissions.get("domain_acceptance_allowed") is False
        and permissions.get("concrete_R_CMB_allowed") is False
        and permissions.get("score_entry_allowed") is False
        and permissions.get("likelihood_allowed") is False
        and permissions.get("dark_sector_verdict_allowed") is False
    )


def endpoint_blind_firewall_clean(payload: dict[str, Any]) -> bool:
    firewall = payload.get("endpoint_blind_firewall", {})
    return (
        firewall.get("cmb_endpoint_residuals_used") is False
        and firewall.get("act_planck_likelihood_used") is False
        and firewall.get("score_output_used") is False
        and firewall.get("post_endpoint_tuning_used") is False
        and firewall.get("dark_sector_verdict_used") is False
    )


def acceptance_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(STAGING_EXEC_TABLE), start=1):
        target = ROOT / source["target_payload_staging_path"]
        present = target.exists()
        payload = load_json(target) if present else {}
        hash_ok = present and source.get("staging_sha256") == sha256(target)
        boundary_ok = present and staging_boundary_clean(payload)
        firewall_ok = present and endpoint_blind_firewall_clean(payload)
        trace_ok = present and all(
            payload.get(key)
            for key in [
                "source_artifact_path",
                "source_hash_path",
                "source_replay_path",
                "source_provenance_path",
                "source_firewall_path",
                "acceptance_row_id",
                "population_row_id",
            ]
        )
        accepted = all([present, hash_ok, boundary_ok, firewall_ok, trace_ok])
        rows.append(
            {
                "acceptance_row_id": f"TCMBCDIPA01_{index:03d}",
                "source_execution_row_id": source["execution_row_id"],
                "source_population_row_id": source["source_population_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "file_category": source["file_category"],
                "payload_staging_path": source["target_payload_staging_path"],
                "payload_staging_present": bool_text(present),
                "staging_hash_matches": bool_text(hash_ok),
                "staging_boundary_clean": bool_text(boundary_ok),
                "endpoint_blind_firewall_clean": bool_text(firewall_ok),
                "source_artifact_trace_present": bool_text(trace_ok),
                "payload_accepted": bool_text(accepted),
                "checker_input_available": bool_text(accepted),
                "checker_execution_allowed": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "PAYLOAD_ACCEPTED_AS_CHECKER_INPUT_ONLY"
                    if accepted
                    else "PAYLOAD_ACCEPTANCE_BLOCKED"
                ),
                "blocking_reason": (
                    "payload accepted as checker input; requires refreshed execution packet before checker execution"
                    if accepted
                    else "payload failed staging presence/hash/boundary/firewall/source-trace checks"
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
    accepted_rows = sum(row["payload_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_staging_population_execution_table": rel(STAGING_EXEC_TABLE),
        "input_staging_population_execution_audit": rel(STAGING_EXEC_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "acceptance_rows": len(rows),
        "payload_staging_present_rows": sum(row["payload_staging_present"] == "true" for row in rows),
        "staging_hash_matches_rows": sum(row["staging_hash_matches"] == "true" for row in rows),
        "staging_boundary_clean_rows": sum(row["staging_boundary_clean"] == "true" for row in rows),
        "endpoint_blind_firewall_clean_rows": sum(row["endpoint_blind_firewall_clean"] == "true" for row in rows),
        "source_artifact_trace_present_rows": sum(row["source_artifact_trace_present"] == "true" for row in rows),
        "payload_accepted_rows": accepted_rows,
        "checker_input_available_rows": sum(row["checker_input_available"] == "true" for row in rows),
        "checker_execution_allowed_rows": sum(row["checker_execution_allowed"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ACCEPTANCE_AUDITED_PAYLOADS_ACCEPTED_AS_CHECKER_INPUTS_ONLY"
            if input_chain_clean() and accepted_rows == 66
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ACCEPTANCE_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_execution_packet_refresh_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} accepted checker-input files" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Acceptance Audit v01

**Doc class:** carrier/domain checker input payload acceptance audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts populated `payload_staging/` files only as checker-input
payloads. It verifies file presence, staging hash agreement, not-yet-accepted
boundary cleanliness, endpoint-blind firewall cleanliness, and source-artifact
traceability. It does not execute checkers, pass certificates, accept domain
objects, materialize `R_CMB`, open score entry, compute a likelihood, or decide
the dark-sector question.

## Acceptance Coverage

{area_text}

## Summary

```text
acceptance_rows={summary["acceptance_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
checker_input_available_rows={summary["checker_input_available_rows"]}
checker_execution_allowed_rows={summary["checker_execution_allowed_rows"]}
checker_executed_rows={summary["checker_executed_rows"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Status

```text
{summary["status"]}
```

The staging payloads are accepted as checker inputs only. Checker execution
requires a refreshed execution packet and remains downstream.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker input payload acceptance.")
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
