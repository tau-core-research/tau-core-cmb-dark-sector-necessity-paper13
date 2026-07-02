#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01.csv"
REQUEST_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_summary_v01.json"
EXEC_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01_"
    "audit_only_request_clean_but_unsupplied_no_source_acceptance_no_staging_write_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    required = [REQUEST_TABLE, REQUEST_SUMMARY, EXEC_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    request_rows = read_csv(REQUEST_TABLE)
    summary = load_json(REQUEST_SUMMARY)
    exec_audit = load_json(EXEC_AUDIT)

    shape_ok = len(request_rows) == 66 and {row.get("file_category") for row in request_rows} == {"payload", "replay", "provenance", "hash", "firewall"}
    rows.append(audit_row(
        "request_row_shape",
        "PASS_EXPECTED_SOURCE_REQUEST_ROWS_PRESENT" if shape_ok else "FAIL_SOURCE_REQUEST_ROW_SHAPE",
        f"rows={len(request_rows)}",
        shape_ok,
        "source artifact request requires 66 rows across the five file categories",
    ))

    input_ok = (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_DECLARED_NOT_SUPPLIED"
        and summary.get("input_chain_clean") is True
        and exec_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_AUDITED_BLOCKED_NOT_EXECUTED"
        and exec_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_execution_chain",
        "PASS_SOURCE_REQUEST_INPUT_CHAIN" if input_ok else "FAIL_SOURCE_REQUEST_INPUT_CHAIN",
        "source artifact request follows a clean audited blocked staging-population execution envelope",
        input_ok,
        "source artifact request audit must be downstream of a clean execution-envelope audit",
    ))

    request_fields_ok = all(
        row.get("requested_source_artifact_path", "").startswith("payload_sources/")
        and row.get("requested_source_hash_path", "").endswith(".hashes.json")
        and row.get("requested_source_replay_path", "").endswith(".replay.json")
        and row.get("requested_source_provenance_path", "").endswith(".provenance.json")
        and row.get("requested_source_firewall_path", "").endswith(".firewall.json")
        and "endpoint-blind Tau-side source artifact" in row.get("minimum_source_acceptance_condition", "")
        for row in request_rows
    )
    rows.append(audit_row(
        "source_request_fields",
        "PASS_SOURCE_REQUEST_FIELDS_DECLARED" if request_fields_ok else "FAIL_SOURCE_REQUEST_FIELDS",
        "each row declares source artifact, hash, replay, provenance, firewall, and endpoint-blind acceptance condition",
        request_fields_ok,
        "source requests must declare all required source-side files and acceptance conditions",
    ))

    accounting_ok = (
        summary.get("request_rows") == 66
        and summary.get("source_artifact_requests_declared") == 66
        and summary.get("source_artifacts_supplied_rows") == 0
        and summary.get("source_hash_supplied_rows") == 0
        and summary.get("source_replay_supplied_rows") == 0
        and summary.get("source_provenance_supplied_rows") == 0
        and summary.get("source_firewall_supplied_rows") == 0
        and summary.get("source_artifact_accepted_rows") == 0
        and summary.get("staging_population_allowed_rows") == 0
        and summary.get("payload_staging_written_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "source_request_accounting",
        "PASS_SOURCE_REQUEST_ACCOUNTING" if accounting_ok else "FAIL_SOURCE_REQUEST_ACCOUNTING",
        (
            f"rows={summary.get('request_rows')}, declared={summary.get('source_artifact_requests_declared')}, "
            f"supplied={summary.get('source_artifacts_supplied_rows')}, accepted={summary.get('source_artifact_accepted_rows')}, "
            f"staging_allowed={summary.get('staging_population_allowed_rows')}"
        ),
        accounting_ok,
        "request-only source artifact package should declare 66 requests with zero supplied, accepted, or staging-allowed rows",
    ))

    firewall_ok = (
        all(row.get("source_artifact_request_declared") == "true" for row in request_rows)
        and all(row.get("source_artifact_supplied") == "false" for row in request_rows)
        and all(row.get("source_artifact_accepted") == "false" for row in request_rows)
        and all(row.get("staging_population_allowed") == "false" for row in request_rows)
        and all(row.get("payload_staging_written") == "false" for row in request_rows)
        and all(row.get("payload_accepted") == "false" for row in request_rows)
        and all(row.get("checker_executed") == "false" for row in request_rows)
        and all(row.get("certificate_passed") == "false" for row in request_rows)
        and all(row.get("domain_object_accepted") == "false" for row in request_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in request_rows)
        and all(row.get("allows_score_entry") == "false" for row in request_rows)
        and all(row.get("allows_likelihood") == "false" for row in request_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in request_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_SOURCE_REQUEST_FIREWALL_CLOSED" if firewall_ok else "FAIL_SOURCE_REQUEST_FIREWALL",
        "source request does not open source acceptance, staging population, payload acceptance, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "source artifact request must not promote unsupplied artifacts to accepted/staging status",
    ))

    boundary_ok = all(
        "request_only" in row.get("claim_boundary", "")
        and "no_source_artifact_supplied" in row.get("claim_boundary", "")
        and "no_staging_write" in row.get("claim_boundary", "")
        and "no_payload_acceptance" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in request_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_SOURCE_REQUEST_CLAIM_BOUNDARY" if boundary_ok else "FAIL_SOURCE_REQUEST_CLAIM_BOUNDARY",
        "row claim boundaries mark request-only source artifacts with no staging/write/score/verdict",
        boundary_ok,
        "source request must preserve request-only no-acceptance boundary",
    ))

    rows.append(audit_row("source_artifact_supply", "BLOCKED_SOURCE_ARTIFACTS_NOT_SUPPLIED", "endpoint-blind Tau-side source artifacts are requested but absent", False, "requires source artifact supply packet"))
    rows.append(audit_row("source_artifact_acceptance", "BLOCKED_SOURCE_ACCEPTANCE_NOT_AVAILABLE", "source artifacts cannot be accepted before supply, hash, replay, provenance, and firewall checks", False, "requires source artifact receipt and acceptance audit"))
    rows.append(audit_row("staging_population", "BLOCKED_STAGING_POPULATION_NOT_ALLOWED", "staging population remains blocked until source artifacts are accepted", False, "requires accepted endpoint-blind source artifacts before staging population"))
    rows.append(audit_row("checker_execution_and_R_CMB", "BLOCKED_CHECKERS_AND_R_CMB", "checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream", False, "requires accepted payloads before checker execution and downstream certificates"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(REQUEST_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "source_artifact_request_audited": clean,
        "source_artifact_supply_allowed": False,
        "source_artifact_acceptance_allowed": False,
        "staging_population_allowed": False,
        "payload_acceptance_allowed": False,
        "checker_execution_allowed": False,
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "domain_object_acceptance_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_AUDITED_NOT_SUPPLIED"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Request Audit v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact request audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks that the endpoint-blind source artifact request is complete
and still unsupplied. It does not supply or accept source artifacts, populate
`payload_staging/`, accept payloads, execute checkers, pass certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The request is auditable, but the required endpoint-blind Tau-side source
artifacts are absent.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker input endpoint-blind source artifact request.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
