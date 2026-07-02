#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_v01.csv"
REQUEST_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_summary_v01.json"
EXEC_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_request_audit_v01.md"

EXPECTED_AREAS = [
    "carrier_well_formedness",
    "domain_membership_rule",
    "seed_admissibility",
    "null_control_admissibility",
    "source_object_admissibility",
    "quotient_and_equivalence_survival",
    "codomain_compatibility",
    "endpoint_firewall_replay",
]

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_request_audit_v01_audit_only_"
    "request_clean_but_unfulfilled_no_payload_acceptance_no_checker_execution_"
    "no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
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
    areas = [row.get("certificate_area") for row in request_rows]
    shape_ok = areas == EXPECTED_AREAS
    rows.append(audit_row(
        "request_row_shape",
        "PASS_EXPECTED_REQUEST_ROWS_PRESENT" if shape_ok else "FAIL_REQUEST_ROW_SHAPE",
        f"certificate_areas={areas}",
        shape_ok,
        "checker input payload request requires the eight declared areas in order",
    ))

    input_ok = (
        summary.get("status") == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_DECLARED_NOT_FULFILLED"
        and summary.get("input_chain_clean") is True
        and exec_audit.get("status") == "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_AUDITED_BLOCKED_NOT_EXECUTABLE"
        and exec_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_execution_chain",
        "PASS_REQUEST_INPUT_CHAIN" if input_ok else "FAIL_REQUEST_INPUT_CHAIN",
        "input payload request follows the audited blocked execution packet",
        input_ok,
        "request audit must be downstream of a clean blocked execution-packet audit",
    ))

    field_ok = all(
        row.get("checker_name")
        and row.get("requested_payload_files")
        and row.get("requested_replay_files")
        and row.get("requested_provenance_files")
        and row.get("requested_hash_files")
        and row.get("requested_firewall_files")
        and row.get("minimum_acceptance_condition")
        and row.get("blocking_reason")
        for row in request_rows
    )
    rows.append(audit_row(
        "request_fields_declared",
        "PASS_REQUEST_FIELDS_DECLARED" if field_ok else "FAIL_REQUEST_FIELDS",
        "each request row declares checker, payload, replay, provenance, hash, firewall, acceptance condition, and blocker",
        field_ok,
        "request rows need checker and all requested file categories",
    ))

    accounting_ok = (
        len(request_rows) == 8
        and summary.get("request_rows") == 8
        and summary.get("requests_declared") == 8
        and summary.get("payload_supplied_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("can_execute_after_fulfillment_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "request_accounting",
        "PASS_REQUEST_ACCOUNTING" if accounting_ok else "FAIL_REQUEST_ACCOUNTING",
        (
            f"request_rows={summary.get('request_rows')}, declared={summary.get('requests_declared')}, "
            f"payload_supplied={summary.get('payload_supplied_rows')}, payload_accepted={summary.get('payload_accepted_rows')}, "
            f"can_execute_after_fulfillment={summary.get('can_execute_after_fulfillment_rows')}, "
            f"executed={summary.get('checker_executed_rows')}, passed={summary.get('certificate_passed_rows')}"
        ),
        accounting_ok,
        "request package should declare eight requests with zero supplied, accepted, executable, executed, or passed rows",
    ))

    permissions_closed = (
        all(row.get("request_declared") == "true" for row in request_rows)
        and all(row.get("payload_supplied") == "false" for row in request_rows)
        and all(row.get("replay_supplied") == "false" for row in request_rows)
        and all(row.get("provenance_supplied") == "false" for row in request_rows)
        and all(row.get("hash_supplied") == "false" for row in request_rows)
        and all(row.get("firewall_supplied") == "false" for row in request_rows)
        and all(row.get("payload_accepted") == "false" for row in request_rows)
        and all(row.get("can_execute_after_fulfillment") == "false" for row in request_rows)
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
        "PASS_REQUEST_FIREWALL_CLOSED" if permissions_closed else "FAIL_REQUEST_FIREWALL",
        "request package declares no supplied payload, accepted payload, executable checker, execution, pass, accepted domain object, concrete R_CMB, score, likelihood, or verdict",
        permissions_closed,
        "request package must not fulfill payloads or open execution/scoring",
    ))

    boundary_ok = all(
        "request_only" in row.get("claim_boundary", "")
        and "payloads_not_supplied" in row.get("claim_boundary", "")
        and "no_checker_execution" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in request_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_REQUEST_CLAIM_BOUNDARY" if boundary_ok else "FAIL_REQUEST_CLAIM_BOUNDARY",
        "row claim boundaries mark the artifact as request-only with unsupplied payloads and no score/verdict",
        boundary_ok,
        "request package must preserve request-only claim boundary",
    ))

    rows.append(audit_row(
        "payload_fulfillment",
        "BLOCKED_PAYLOADS_NOT_SUPPLIED",
        "input payloads are requested but not supplied",
        False,
        "requires checker input payload fulfillment packet",
    ))
    rows.append(audit_row(
        "payload_acceptance",
        "BLOCKED_PAYLOADS_NOT_ACCEPTED",
        "requested payloads cannot be accepted before supply, hash, provenance, replay, and firewall checks",
        False,
        "requires payload receipt/materialization and acceptance audit",
    ))
    rows.append(audit_row(
        "checker_execution",
        "BLOCKED_CHECKERS_NOT_EXECUTABLE",
        "can_execute remains false until request fulfillment is audited",
        False,
        "requires accepted payloads before checker execution",
    ))
    rows.append(audit_row(
        "certificate_domain_R_CMB",
        "BLOCKED_CERTIFICATES_DOMAIN_AND_R_CMB",
        "certificate pass, domain acceptance, and concrete R_CMB remain downstream",
        False,
        "requires checker outputs and pass audits before domain acceptance and R_CMB materialization",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_request_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(REQUEST_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "input_payload_request_audited": clean,
        "payload_fulfillment_allowed": False,
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_AUDITED_UNFULFILLED_NOT_EXECUTABLE"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Request Audit v01

**Doc class:** carrier/domain checker input payload request audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the carrier/domain checker input payload request. It verifies
row shape, upstream lineage, request field completeness, accounting, promotion
firewall closure, and claim-boundary discipline. It does not supply or accept
payloads, execute checkers, pass certificates, accept domain objects,
materialize `R_CMB`, open score entry, compute a likelihood, or decide the
dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The request is audit-visible and internally clean, but it is unfulfilled.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain checker input payload request.")
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
