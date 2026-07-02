#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FILE_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_v01.csv"
FILE_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_summary_v01.json"
MATERIALIZATION_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_file_materialization_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_file_materialization_audit_v01_"
    "audit_only_template_files_clean_payload_staging_absent_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    required = [FILE_TABLE, FILE_SUMMARY, MATERIALIZATION_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    file_rows = read_csv(FILE_TABLE)
    summary = load_json(FILE_SUMMARY)
    materialization_audit = load_json(MATERIALIZATION_AUDIT)

    shape_ok = (
        len(file_rows) == 66
        and {row.get("file_category") for row in file_rows} == {"payload", "replay", "provenance", "hash", "firewall"}
    )
    rows.append(audit_row(
        "file_materialization_row_shape",
        "PASS_EXPECTED_FILE_MATERIALIZATION_ROWS_PRESENT" if shape_ok else "FAIL_FILE_MATERIALIZATION_ROW_SHAPE",
        f"rows={len(file_rows)}",
        shape_ok,
        "file materialization requires the 66 declared template-file rows",
    ))

    input_ok = (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_TEMPLATE_FILES_MATERIALIZED_PAYLOADS_NOT_MATERIALIZED"
        and summary.get("input_chain_clean") is True
        and materialization_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_MATERIALIZATION_PACKET_AUDITED_SCHEMA_ONLY_NOT_EXECUTABLE"
        and materialization_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_materialization_chain",
        "PASS_FILE_MATERIALIZATION_INPUT_CHAIN" if input_ok else "FAIL_FILE_MATERIALIZATION_INPUT_CHAIN",
        "file materialization follows a clean audited schema-only materialization packet",
        input_ok,
        "file materialization audit must be downstream of a clean materialization-packet audit",
    ))

    template_files_ok = True
    bad_templates: list[str] = []
    for row in file_rows:
        path = ROOT / row["template_artifact_path"]
        if not path.exists() or row["template_sha256"] != sha256(path):
            template_files_ok = False
            bad_templates.append(row["template_artifact_path"])
    rows.append(audit_row(
        "template_file_hash_binding",
        "PASS_TEMPLATE_FILES_HASH_BOUND" if template_files_ok else "FAIL_TEMPLATE_FILE_HASH_BINDING",
        "all template files exist and match recorded sha256" if template_files_ok else f"bad_templates={bad_templates[:5]}",
        template_files_ok,
        "template files must exist and match recorded hashes",
    ))

    template_content_ok = True
    bad_content: list[str] = []
    for row in file_rows:
        path = ROOT / row["template_artifact_path"]
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            template_content_ok = False
            bad_content.append(row["template_artifact_path"])
            continue
        if (
            content.get("template_status") != "UNPOPULATED_TEMPLATE_NOT_PAYLOAD"
            or content.get("claim_boundary") != row["claim_boundary"]
            or content.get("acceptance_permissions", {}).get("payload_accepted") is not False
            or content.get("acceptance_permissions", {}).get("score_entry_allowed") is not False
        ):
            template_content_ok = False
            bad_content.append(row["template_artifact_path"])
    rows.append(audit_row(
        "template_content_boundary",
        "PASS_TEMPLATE_CONTENT_BOUNDARY" if template_content_ok else "FAIL_TEMPLATE_CONTENT_BOUNDARY",
        "all template files are explicitly unpopulated and non-accepting" if template_content_ok else f"bad_content={bad_content[:5]}",
        template_content_ok,
        "template files must remain unpopulated and non-accepting",
    ))

    accounting_ok = (
        summary.get("file_materialization_rows") == 66
        and summary.get("template_files_written") == 66
        and summary.get("payload_staging_files_written") == 0
        and summary.get("payload_file_materialized_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("can_execute_after_file_materialization_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "file_materialization_accounting",
        "PASS_FILE_MATERIALIZATION_ACCOUNTING" if accounting_ok else "FAIL_FILE_MATERIALIZATION_ACCOUNTING",
        (
            f"rows={summary.get('file_materialization_rows')}, templates={summary.get('template_files_written')}, "
            f"staging={summary.get('payload_staging_files_written')}, accepted={summary.get('payload_accepted_rows')}"
        ),
        accounting_ok,
        "template-only file materialization should write 66 templates with zero staging payloads or accepted rows",
    ))

    firewall_ok = (
        all(row.get("template_file_written") == "true" for row in file_rows)
        and all(row.get("payload_staging_file_written") == "false" for row in file_rows)
        and all(row.get("payload_file_materialized") == "false" for row in file_rows)
        and all(row.get("payload_accepted") == "false" for row in file_rows)
        and all(row.get("can_execute_after_file_materialization") == "false" for row in file_rows)
        and all(row.get("checker_executed") == "false" for row in file_rows)
        and all(row.get("certificate_passed") == "false" for row in file_rows)
        and all(row.get("domain_object_accepted") == "false" for row in file_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in file_rows)
        and all(row.get("allows_score_entry") == "false" for row in file_rows)
        and all(row.get("allows_likelihood") == "false" for row in file_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in file_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_FILE_MATERIALIZATION_FIREWALL_CLOSED" if firewall_ok else "FAIL_FILE_MATERIALIZATION_FIREWALL",
        "template file materialization does not open payload staging, acceptance, execution, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "template materialization must not promote templates to accepted payloads",
    ))

    rows.append(audit_row(
        "payload_staging_population",
        "BLOCKED_PAYLOAD_STAGING_FILES_ABSENT",
        "payload_staging files are still absent",
        False,
        "requires endpoint-blind population of payload_staging files from Tau-side sources",
    ))
    rows.append(audit_row(
        "binding_checks",
        "BLOCKED_BINDINGS_NOT_AVAILABLE",
        "hash, provenance, replay, and firewall bindings cannot pass without populated staging payloads",
        False,
        "requires populated staging payload files and binding audit",
    ))
    rows.append(audit_row(
        "payload_acceptance",
        "BLOCKED_ACCEPTANCE_AUDIT_NOT_AVAILABLE",
        "payloads cannot be accepted from templates alone",
        False,
        "requires populated staging payloads and acceptance audit",
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
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_file_materialization_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(FILE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "file_materialization_audited": clean,
        "payload_staging_population_allowed": False,
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_TEMPLATE_FILES_AUDITED_PAYLOADS_NOT_MATERIALIZED"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FILE_MATERIALIZATION_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload File Materialization Audit v01

**Doc class:** carrier/domain checker input payload template-file materialization audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that the declared checker-input template files exist and
are hash-bound while remaining unpopulated and non-accepting. It does not
populate `payload_staging/`, accept payloads, execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The template files are materialized and auditable, but actual staging payloads
are still absent.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain checker input payload file materialization.")
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
