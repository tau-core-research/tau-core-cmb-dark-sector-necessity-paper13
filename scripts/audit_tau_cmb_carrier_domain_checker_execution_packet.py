#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXEC_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_v01.csv"
EXEC_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_summary_v01.json"
PAYLOAD_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_execution_packet_audit_v01.md"

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
    "tau_cmb_carrier_domain_checker_execution_packet_audit_v01_audit_only_"
    "execution_envelope_clean_but_not_executable_no_checker_attempt_no_certificate_pass_"
    "no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
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
    required = [EXEC_TABLE, EXEC_SUMMARY, PAYLOAD_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    exec_rows = read_csv(EXEC_TABLE)
    summary = load_json(EXEC_SUMMARY)
    payload_audit = load_json(PAYLOAD_AUDIT)
    areas = [row.get("certificate_area") for row in exec_rows]
    shape_ok = areas == EXPECTED_AREAS
    rows.append(audit_row(
        "execution_row_shape",
        "PASS_EXPECTED_EXECUTION_ROWS_PRESENT" if shape_ok else "FAIL_EXECUTION_ROW_SHAPE",
        f"certificate_areas={areas}",
        shape_ok,
        "checker execution packet requires the eight declared areas in order",
    ))

    input_ok = (
        summary.get("status") == "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_DECLARED_BLOCKED_NOT_EXECUTED"
        and summary.get("input_chain_clean") is True
        and payload_audit.get("status") == "CARRIER_DOMAIN_PROOF_CHECKER_PAYLOAD_PACKET_AUDITED_NOT_EXECUTED_NOT_SCORE_READY"
        and payload_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_payload_chain",
        "PASS_EXECUTION_INPUT_CHAIN" if input_ok else "FAIL_EXECUTION_INPUT_CHAIN",
        "execution packet follows the audited proof/checker payload packet",
        input_ok,
        "execution audit must be downstream of a clean payload-packet audit",
    ))

    field_ok = all(
        row.get("checker_name")
        and row.get("execution_command_template")
        and row.get("execution_prerequisite_rule")
        and row.get("required_input_artifacts")
        and row.get("required_output_artifacts")
        and row.get("expected_pass_condition")
        and row.get("blocking_reason")
        for row in exec_rows
    )
    rows.append(audit_row(
        "execution_fields_declared",
        "PASS_EXECUTION_FIELDS_DECLARED" if field_ok else "FAIL_EXECUTION_FIELDS",
        "each execution row declares checker name, command template, prerequisites, inputs, outputs, pass condition, and blocker",
        field_ok,
        "execution rows need checker name, command, prerequisites, inputs, outputs, and blocking reason",
    ))

    accounting_ok = (
        len(exec_rows) == 8
        and summary.get("execution_rows") == 8
        and summary.get("execution_packet_declared_rows") == 8
        and summary.get("can_execute_rows") == 0
        and summary.get("execution_attempted_rows") == 0
        and summary.get("execution_succeeded_rows") == 0
        and summary.get("checker_output_supplied_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "execution_accounting",
        "PASS_EXECUTION_ACCOUNTING" if accounting_ok else "FAIL_EXECUTION_ACCOUNTING",
        (
            f"execution_rows={summary.get('execution_rows')}, declared={summary.get('execution_packet_declared_rows')}, "
            f"can_execute={summary.get('can_execute_rows')}, attempted={summary.get('execution_attempted_rows')}, "
            f"succeeded={summary.get('execution_succeeded_rows')}, passed={summary.get('certificate_passed_rows')}, "
            f"accepted_domain_objects={summary.get('accepted_domain_objects')}"
        ),
        accounting_ok,
        "execution packet should declare eight rows with zero executable, attempted, succeeded, passed, or accepted rows",
    ))

    permissions_closed = (
        all(row.get("execution_packet_declared") == "true" for row in exec_rows)
        and all(row.get("can_execute") == "false" for row in exec_rows)
        and all(row.get("execution_attempted") == "false" for row in exec_rows)
        and all(row.get("execution_succeeded") == "false" for row in exec_rows)
        and all(row.get("checker_output_supplied") == "false" for row in exec_rows)
        and all(row.get("certificate_passed") == "false" for row in exec_rows)
        and all(row.get("domain_object_accepted") == "false" for row in exec_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in exec_rows)
        and all(row.get("allows_score_entry") == "false" for row in exec_rows)
        and all(row.get("allows_likelihood") == "false" for row in exec_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in exec_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_EXECUTION_FIREWALL_CLOSED" if permissions_closed else "FAIL_EXECUTION_FIREWALL",
        "execution packet declares no executable checker, no attempt, no success, no pass, no accepted domain object, no concrete R_CMB, no score, no likelihood, and no verdict",
        permissions_closed,
        "execution packet must not execute checkers or open downstream claims",
    ))

    boundary_ok = all(
        "execution_envelope_only" in row.get("claim_boundary", "")
        and "can_execute_false" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in exec_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_EXECUTION_CLAIM_BOUNDARY" if boundary_ok else "FAIL_EXECUTION_CLAIM_BOUNDARY",
        "row claim boundaries mark the artifact as execution-envelope-only with can_execute false and no score/verdict",
        boundary_ok,
        "execution packet must preserve execution-envelope-only claim boundary",
    ))

    rows.append(audit_row(
        "checker_inputs",
        "BLOCKED_CHECKER_INPUTS_ABSENT",
        "checker command templates exist but required input artifacts are absent",
        False,
        "requires checker input payload request/fulfillment before execution can be allowed",
    ))
    rows.append(audit_row(
        "checker_execution",
        "BLOCKED_CHECKERS_NOT_EXECUTABLE",
        "can_execute remains false for every checker",
        False,
        "requires populated inputs and replay artifacts before execution",
    ))
    rows.append(audit_row(
        "certificate_and_domain_acceptance",
        "BLOCKED_CERTIFICATES_AND_DOMAIN_ACCEPTANCE",
        "no certificate pass or domain-object acceptance is possible without checker outputs",
        False,
        "requires checker output audit before certificate pass and domain acceptance",
    ))
    rows.append(audit_row(
        "concrete_R_CMB",
        "BLOCKED_R_CMB_NOT_MATERIALIZED",
        "concrete R_CMB remains downstream of checker execution and accepted domain objects",
        False,
        "requires concrete R_CMB materialization candidate after accepted domain objects",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_execution_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(EXEC_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "execution_packet_audited": clean,
        "checker_execution_allowed": False,
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "domain_object_acceptance_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_AUDITED_BLOCKED_NOT_EXECUTABLE"
            if clean
            else "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_request_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Execution Packet Audit v01

**Doc class:** carrier/domain checker execution packet audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the carrier/domain checker execution packet. It verifies row
shape, upstream lineage, execution field completeness, accounting, promotion
firewall closure, and claim-boundary discipline. It does not execute checkers,
pass certificates, accept domain objects, materialize `R_CMB`, open score
entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The execution packet is audit-visible and internally clean, but it is not
executable because checker inputs are absent.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain checker execution packet.")
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
