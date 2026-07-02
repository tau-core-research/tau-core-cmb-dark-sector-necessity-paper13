#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FULFILLMENT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01.csv"
FULFILLMENT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_summary_v01.json"
REQUEST_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_audit_v01.md"

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
    "tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_audit_v01_"
    "audit_only_fulfillment_packet_clean_but_incomplete_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_"
    "no_score_no_likelihood_no_verdict"
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
    required = [FULFILLMENT_TABLE, FULFILLMENT_SUMMARY, REQUEST_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    fulfillment_rows = read_csv(FULFILLMENT_TABLE)
    summary = load_json(FULFILLMENT_SUMMARY)
    request_audit = load_json(REQUEST_AUDIT)

    areas = [row.get("certificate_area") for row in fulfillment_rows]
    shape_ok = areas == EXPECTED_AREAS
    rows.append(audit_row(
        "fulfillment_row_shape",
        "PASS_EXPECTED_FULFILLMENT_ROWS_PRESENT" if shape_ok else "FAIL_FULFILLMENT_ROW_SHAPE",
        f"certificate_areas={areas}",
        shape_ok,
        "fulfillment packet requires the eight carrier/domain checker areas in order",
    ))

    input_ok = (
        summary.get("status") == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_DECLARED_INCOMPLETE"
        and summary.get("input_chain_clean") is True
        and request_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_AUDITED_UNFULFILLED_NOT_EXECUTABLE"
        and request_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_request_chain",
        "PASS_FULFILLMENT_INPUT_CHAIN" if input_ok else "FAIL_FULFILLMENT_INPUT_CHAIN",
        "fulfillment packet follows a clean audited input-payload request",
        input_ok,
        "fulfillment audit must be downstream of a clean request audit",
    ))

    path_fields_ok = all(
        row.get("payload_bundle_root")
        and row.get("requested_payload_paths")
        and row.get("requested_replay_paths")
        and row.get("requested_provenance_paths")
        and row.get("requested_hash_paths")
        and row.get("requested_firewall_paths")
        for row in fulfillment_rows
    )
    rows.append(audit_row(
        "fulfillment_paths_declared",
        "PASS_FULFILLMENT_PATHS_DECLARED" if path_fields_ok else "FAIL_FULFILLMENT_PATHS",
        "each row declares concrete staging paths for payload, replay, provenance, hash, and firewall files",
        path_fields_ok,
        "fulfillment packet needs concrete staging paths for all requested file categories",
    ))

    accounting_ok = (
        len(fulfillment_rows) == 8
        and summary.get("fulfillment_rows") == 8
        and summary.get("fulfillment_packets_declared") == 8
        and summary.get("complete_file_bundle_rows") == 0
        and summary.get("fully_supplied_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("can_execute_after_fulfillment_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "fulfillment_accounting",
        "PASS_FULFILLMENT_ACCOUNTING" if accounting_ok else "FAIL_FULFILLMENT_ACCOUNTING",
        (
            f"rows={summary.get('fulfillment_rows')}, declared={summary.get('fulfillment_packets_declared')}, "
            f"complete={summary.get('complete_file_bundle_rows')}, supplied={summary.get('fully_supplied_rows')}, "
            f"accepted={summary.get('payload_accepted_rows')}, executable={summary.get('can_execute_after_fulfillment_rows')}"
        ),
        accounting_ok,
        "incomplete fulfillment packet should declare eight rows with zero complete, supplied, accepted, executable, executed, or passed rows",
    ))

    firewall_ok = (
        all(row.get("fulfillment_packet_declared") == "true" for row in fulfillment_rows)
        and all(row.get("all_required_files_present") == "false" for row in fulfillment_rows)
        and all(row.get("payload_accepted") == "false" for row in fulfillment_rows)
        and all(row.get("can_execute_after_fulfillment") == "false" for row in fulfillment_rows)
        and all(row.get("checker_executed") == "false" for row in fulfillment_rows)
        and all(row.get("certificate_passed") == "false" for row in fulfillment_rows)
        and all(row.get("domain_object_accepted") == "false" for row in fulfillment_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in fulfillment_rows)
        and all(row.get("allows_score_entry") == "false" for row in fulfillment_rows)
        and all(row.get("allows_likelihood") == "false" for row in fulfillment_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in fulfillment_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_FULFILLMENT_FIREWALL_CLOSED" if firewall_ok else "FAIL_FULFILLMENT_FIREWALL",
        "incomplete fulfillment packet does not open acceptance, execution, certificate pass, domain acceptance, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "fulfillment packet must not promote incomplete files to accepted/executable status",
    ))

    boundary_ok = all(
        "fulfillment_packet_only" in row.get("claim_boundary", "")
        and "payloads_not_accepted" in row.get("claim_boundary", "")
        and "no_checker_execution" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in fulfillment_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_FULFILLMENT_CLAIM_BOUNDARY" if boundary_ok else "FAIL_FULFILLMENT_CLAIM_BOUNDARY",
        "row claim boundaries mark the artifact as fulfillment-packet-only with no acceptance or score/verdict",
        boundary_ok,
        "fulfillment packet must preserve no-acceptance claim boundary",
    ))

    rows.append(audit_row(
        "file_bundle_materialization",
        "BLOCKED_FILE_BUNDLES_INCOMPLETE",
        "the concrete payload-staging file bundles are absent or incomplete",
        False,
        "requires materialized payload, replay, provenance, hash, and firewall files for all eight checker areas",
    ))
    rows.append(audit_row(
        "payload_acceptance",
        "BLOCKED_ACCEPTANCE_AUDIT_NOT_AVAILABLE",
        "payloads cannot be accepted before complete file bundles and acceptance audit",
        False,
        "requires complete file bundles and payload acceptance audit",
    ))
    rows.append(audit_row(
        "checker_execution",
        "BLOCKED_CHECKERS_NOT_EXECUTABLE",
        "checkers remain non-executable until accepted fulfillment exists",
        False,
        "requires accepted payload bundles before checker execution",
    ))
    rows.append(audit_row(
        "certificate_domain_R_CMB",
        "BLOCKED_CERTIFICATES_DOMAIN_AND_R_CMB",
        "certificate pass, domain acceptance, and concrete R_CMB remain downstream",
        False,
        "requires checker outputs and certificate/domain pass audits",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(FULFILLMENT_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "fulfillment_packet_audited": clean,
        "file_bundle_materialization_allowed": False,
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_AUDITED_INCOMPLETE_NOT_EXECUTABLE"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_materialization_packet_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Fulfillment Packet Audit v01

**Doc class:** carrier/domain checker input payload fulfillment packet audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the fulfillment packet that maps checker requests to concrete
payload-staging paths. It verifies row shape, upstream lineage, path
declaration, accounting, promotion-firewall closure, and claim-boundary
discipline. It does not materialize files, accept payloads, execute checkers,
pass certificates, accept domain objects, materialize `R_CMB`, open score
entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The fulfillment packet is audit-visible and internally clean, but the required
file bundles are incomplete.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain checker input payload fulfillment packet.")
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
