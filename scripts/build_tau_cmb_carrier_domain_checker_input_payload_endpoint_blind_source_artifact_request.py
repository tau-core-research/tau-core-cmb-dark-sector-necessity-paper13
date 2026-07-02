#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXEC_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01.csv"
EXEC_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01_"
    "request_only_no_source_artifact_supplied_no_staging_write_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "request_row_id",
    "source_execution_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "target_payload_staging_path",
    "requested_source_artifact_path",
    "requested_source_hash_path",
    "requested_source_replay_path",
    "requested_source_provenance_path",
    "requested_source_firewall_path",
    "minimum_source_acceptance_condition",
    "source_artifact_request_declared",
    "source_artifact_supplied",
    "source_hash_supplied",
    "source_replay_supplied",
    "source_provenance_supplied",
    "source_firewall_supplied",
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
    "request_status",
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


def source_base(area: str, category: str, row_id: str) -> str:
    return f"payload_sources/tau_cmb_carrier_domain_checker_input_payloads/{area}/{row_id}_{category}_source"


def table_rows() -> list[dict[str, str]]:
    exec_rows = read_csv(EXEC_TABLE)
    rows: list[dict[str, str]] = []
    for index, source in enumerate(exec_rows, start=1):
        base = source_base(source["certificate_area"], source["file_category"], source["source_population_row_id"])
        rows.append(
            {
                "request_row_id": f"TCMBCDIEBSAR01_{index:03d}",
                "source_execution_row_id": source["execution_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "file_category": source["file_category"],
                "target_payload_staging_path": source["target_payload_staging_path"],
                "requested_source_artifact_path": f"{base}.json",
                "requested_source_hash_path": f"{base}.hashes.json",
                "requested_source_replay_path": f"{base}.replay.json",
                "requested_source_provenance_path": f"{base}.provenance.json",
                "requested_source_firewall_path": f"{base}.firewall.json",
                "minimum_source_acceptance_condition": (
                    "endpoint-blind Tau-side source artifact, hash, replay, provenance, and firewall "
                    "must be supplied and mutually consistent before staging population can execute"
                ),
                "source_artifact_request_declared": "true",
                "source_artifact_supplied": "false",
                "source_hash_supplied": "false",
                "source_replay_supplied": "false",
                "source_provenance_supplied": "false",
                "source_firewall_supplied": "false",
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
                "request_status": "ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_DECLARED_NOT_SUPPLIED",
                "blocking_reason": "endpoint-blind Tau-side source artifact bundle is absent",
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
    audit = load_json(EXEC_AUDIT) if EXEC_AUDIT.exists() else {}
    input_ok = (
        audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_AUDITED_BLOCKED_NOT_EXECUTED"
        and audit.get("failed_rows") == 0
        and EXEC_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_execution_table": rel(EXEC_TABLE),
        "input_execution_audit": rel(EXEC_AUDIT),
        "input_chain_clean": input_ok,
        "request_rows": len(rows),
        "source_artifact_requests_declared": sum(row["source_artifact_request_declared"] == "true" for row in rows),
        "source_artifacts_supplied_rows": sum(row["source_artifact_supplied"] == "true" for row in rows),
        "source_hash_supplied_rows": sum(row["source_hash_supplied"] == "true" for row in rows),
        "source_replay_supplied_rows": sum(row["source_replay_supplied"] == "true" for row in rows),
        "source_provenance_supplied_rows": sum(row["source_provenance_supplied"] == "true" for row in rows),
        "source_firewall_supplied_rows": sum(row["source_firewall_supplied"] == "true" for row in rows),
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_DECLARED_NOT_SUPPLIED"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} source artifact requests" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Request v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact request
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This request names the endpoint-blind Tau-side source artifacts required before
staging-population execution can become possible. It does not supply or accept
source artifacts, write `payload_staging/`, accept payloads, execute checkers,
pass certificates, accept domain objects, materialize `R_CMB`, open score
entry, compute a likelihood, or decide the dark-sector question.

## Request Counts

{area_text}

## Summary

```text
request_rows={summary["request_rows"]}
source_artifact_requests_declared={summary["source_artifact_requests_declared"]}
source_artifacts_supplied_rows={summary["source_artifacts_supplied_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB checker input endpoint-blind source artifact request.")
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
