#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATERIALIZATION_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_v01.csv"
MATERIALIZATION_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_summary_v01.json"
FULFILLMENT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01.csv"
FULFILLMENT_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_audit_v01.md"

EXPECTED_AREAS = {
    "carrier_well_formedness",
    "domain_membership_rule",
    "seed_admissibility",
    "null_control_admissibility",
    "source_object_admissibility",
    "quotient_and_equivalence_survival",
    "codomain_compatibility",
    "endpoint_firewall_replay",
}

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_materialization_packet_audit_v01_"
    "audit_only_schema_clean_but_unmaterialized_no_payload_acceptance_no_checker_execution_"
    "no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def audit_row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    required = [MATERIALIZATION_TABLE, MATERIALIZATION_SUMMARY, FULFILLMENT_TABLE, FULFILLMENT_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    materialization_rows = read_csv(MATERIALIZATION_TABLE)
    fulfillment_rows = read_csv(FULFILLMENT_TABLE)
    summary = load_json(MATERIALIZATION_SUMMARY)
    fulfillment_audit = load_json(FULFILLMENT_AUDIT)
    expected_slot_count = sum(
        len(split_paths(row["requested_payload_paths"]))
        + len(split_paths(row["requested_replay_paths"]))
        + len(split_paths(row["requested_provenance_paths"]))
        + len(split_paths(row["requested_hash_paths"]))
        + len(split_paths(row["requested_firewall_paths"]))
        for row in fulfillment_rows
    )

    areas = {row.get("certificate_area") for row in materialization_rows}
    categories = {row.get("file_category") for row in materialization_rows}
    shape_ok = (
        len(materialization_rows) == expected_slot_count
        and areas == EXPECTED_AREAS
        and categories == {"payload", "replay", "provenance", "hash", "firewall"}
    )
    rows.append(audit_row(
        "materialization_row_shape",
        "PASS_EXPECTED_MATERIALIZATION_ROWS_PRESENT" if shape_ok else "FAIL_MATERIALIZATION_ROW_SHAPE",
        f"rows={len(materialization_rows)}, areas={sorted(areas)}, categories={sorted(categories)}",
        shape_ok,
        "materialization packet requires one file-slot row for every requested fulfillment path across eight areas and five file categories",
    ))

    input_ok = (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_MATERIALIZATION_PACKET_SCHEMA_DECLARED_UNMATERIALIZED"
        and summary.get("input_chain_clean") is True
        and fulfillment_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_AUDITED_INCOMPLETE_NOT_EXECUTABLE"
        and fulfillment_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_fulfillment_chain",
        "PASS_MATERIALIZATION_INPUT_CHAIN" if input_ok else "FAIL_MATERIALIZATION_INPUT_CHAIN",
        "materialization packet follows a clean audited incomplete fulfillment packet",
        input_ok,
        "materialization audit must be downstream of a clean fulfillment-packet audit",
    ))

    template_ok = all(
        row.get("required_payload_staging_path", "").startswith("payload_staging/")
        and row.get("template_artifact_path", "").startswith("payload_templates/")
        and row.get("materialization_requirement")
        for row in materialization_rows
    )
    rows.append(audit_row(
        "template_path_mapping",
        "PASS_TEMPLATE_PATH_MAPPING" if template_ok else "FAIL_TEMPLATE_PATH_MAPPING",
        "each required staging file has a declared payload_templates counterpart and materialization requirement",
        template_ok,
        "materialization packet needs staging-to-template path mapping for every required file slot",
    ))

    accounting_ok = (
        summary.get("materialization_rows") == expected_slot_count
        and summary.get("template_paths_declared") == expected_slot_count
        and summary.get("file_materialized_rows") == 0
        and summary.get("hash_bound_rows") == 0
        and summary.get("provenance_bound_rows") == 0
        and summary.get("replay_bound_rows") == 0
        and summary.get("firewall_bound_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("can_execute_after_materialization_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "materialization_accounting",
        "PASS_MATERIALIZATION_ACCOUNTING" if accounting_ok else "FAIL_MATERIALIZATION_ACCOUNTING",
        (
            f"rows={summary.get('materialization_rows')}, templates={summary.get('template_paths_declared')}, "
            f"materialized={summary.get('file_materialized_rows')}, accepted={summary.get('payload_accepted_rows')}, "
            f"executable={summary.get('can_execute_after_materialization_rows')}"
        ),
        accounting_ok,
        "schema-only materialization packet should declare all requested templates with zero materialized or accepted rows",
    ))

    firewall_ok = (
        all(row.get("file_materialized") == "false" for row in materialization_rows)
        and all(row.get("payload_accepted") == "false" for row in materialization_rows)
        and all(row.get("can_execute_after_materialization") == "false" for row in materialization_rows)
        and all(row.get("checker_executed") == "false" for row in materialization_rows)
        and all(row.get("certificate_passed") == "false" for row in materialization_rows)
        and all(row.get("domain_object_accepted") == "false" for row in materialization_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in materialization_rows)
        and all(row.get("allows_score_entry") == "false" for row in materialization_rows)
        and all(row.get("allows_likelihood") == "false" for row in materialization_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in materialization_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_MATERIALIZATION_FIREWALL_CLOSED" if firewall_ok else "FAIL_MATERIALIZATION_FIREWALL",
        "schema-only materialization packet does not open file materialization, acceptance, execution, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "materialization schema must not promote template paths to actual payload files",
    ))

    boundary_ok = all(
        "materialization_packet_schema_only" in row.get("claim_boundary", "")
        and "no_payload_files_materialized" in row.get("claim_boundary", "")
        and "no_payload_acceptance" in row.get("claim_boundary", "")
        and "no_checker_execution" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in materialization_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_MATERIALIZATION_CLAIM_BOUNDARY" if boundary_ok else "FAIL_MATERIALIZATION_CLAIM_BOUNDARY",
        "row claim boundaries mark schema-only materialization with no payload acceptance or score/verdict",
        boundary_ok,
        "materialization packet must preserve no-materialization/no-acceptance claim boundary",
    ))

    rows.append(audit_row(
        "file_materialization",
        "BLOCKED_FILES_NOT_MATERIALIZED",
        "template paths are declared but required payload-staging files are not materialized",
        False,
        "requires actual endpoint-blind payload, replay, provenance, hash, and firewall files",
    ))
    rows.append(audit_row(
        "binding_checks",
        "BLOCKED_BINDINGS_NOT_AVAILABLE",
        "hash, provenance, replay, and firewall bindings are not available",
        False,
        "requires materialized files before binding checks can pass",
    ))
    rows.append(audit_row(
        "payload_acceptance",
        "BLOCKED_ACCEPTANCE_AUDIT_NOT_AVAILABLE",
        "payloads cannot be accepted before materialized files and binding checks",
        False,
        "requires materialized file bundles and acceptance audit",
    ))
    rows.append(audit_row(
        "checker_execution_and_R_CMB",
        "BLOCKED_EXECUTION_AND_R_CMB",
        "checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream",
        False,
        "requires accepted payloads before checker execution and downstream certificates",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_materialization_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(MATERIALIZATION_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "materialization_packet_audited": clean,
        "file_materialization_allowed": False,
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_MATERIALIZATION_PACKET_AUDITED_SCHEMA_ONLY_NOT_EXECUTABLE"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_MATERIALIZATION_PACKET_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_file_materialization_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Materialization Packet Audit v01

**Doc class:** carrier/domain checker input payload materialization packet audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the schema-only materialization packet for checker input
payload files. It verifies row shape, upstream lineage, staging-to-template path
mapping, accounting, promotion-firewall closure, and claim-boundary discipline.
It does not materialize files, accept payloads, execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The materialization schema is audit-visible and internally clean, but no
required file has been materialized.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain checker input payload materialization packet.")
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
