#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXEC_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01.csv"
EXEC_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_summary_v01.json"
ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01_"
    "audit_only_staging_files_populated_not_payload_accepted_no_checker_execution_no_certificate_pass_"
    "no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
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
    required = [EXEC_TABLE, EXEC_SUMMARY, ACCEPTANCE_SUMMARY]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    exec_rows = read_csv(EXEC_TABLE)
    summary = load_json(EXEC_SUMMARY)
    acceptance_summary = load_json(ACCEPTANCE_SUMMARY)

    shape_ok = (
        len(exec_rows) == 66
        and {row.get("file_category") for row in exec_rows} == {"payload", "replay", "provenance", "hash", "firewall"}
    )
    rows.append(audit_row(
        "execution_row_shape",
        "PASS_EXPECTED_EXECUTION_ROWS_PRESENT" if shape_ok else "FAIL_EXECUTION_ROW_SHAPE",
        f"rows={len(exec_rows)}",
        shape_ok,
        "staging population execution requires the 66 declared rows",
    ))

    input_ok = (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTED_PAYLOADS_POPULATED_NOT_ACCEPTED"
        and summary.get("input_chain_clean") is True
        and acceptance_summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACTS_ACCEPTED_FOR_STAGING_POPULATION_ONLY"
        and acceptance_summary.get("source_artifact_accepted_rows") == 66
        and acceptance_summary.get("staging_population_allowed_rows") == 66
    )
    rows.append(audit_row(
        "input_source_acceptance_chain",
        "PASS_EXECUTION_INPUT_CHAIN" if input_ok else "FAIL_EXECUTION_INPUT_CHAIN",
        "staging execution follows accepted endpoint-blind source artifacts",
        input_ok,
        "execution audit must be downstream of accepted source artifacts",
    ))

    files_ok = True
    bad_files: list[str] = []
    boundary_ok = True
    bad_boundary: list[str] = []
    for row in exec_rows:
        target = ROOT / row["target_payload_staging_path"]
        if not target.exists() or row.get("staging_sha256") != sha256(target):
            files_ok = False
            bad_files.append(row["target_payload_staging_path"])
            continue
        payload = load_json(target)
        permissions = payload.get("acceptance_permissions", {})
        if (
            payload.get("staging_status") != "POPULATED_FROM_ACCEPTED_ENDPOINT_BLIND_TAU_SIDE_SOURCE_NOT_ACCEPTED"
            or payload.get("claim_boundary") != summary.get("claim_boundary")
            or permissions.get("payload_accepted") is True
            or permissions.get("checker_execution_allowed") is True
            or permissions.get("concrete_R_CMB_allowed") is True
            or permissions.get("score_entry_allowed") is True
            or permissions.get("likelihood_allowed") is True
            or permissions.get("dark_sector_verdict_allowed") is True
        ):
            boundary_ok = False
            bad_boundary.append(row["target_payload_staging_path"])
    rows.append(audit_row(
        "staging_files_present_and_hash_bound",
        "PASS_STAGING_FILES_PRESENT_AND_HASH_BOUND" if files_ok else "FAIL_STAGING_FILE_HASH_BINDING",
        "all populated staging files exist and match recorded hashes" if files_ok else f"bad_files={bad_files[:5]}",
        files_ok,
        "populated staging files must exist and match recorded hashes",
    ))
    rows.append(audit_row(
        "staging_claim_boundary",
        "PASS_STAGING_CLAIM_BOUNDARY" if boundary_ok else "FAIL_STAGING_CLAIM_BOUNDARY",
        "all staging files remain not accepted and forbid execution/R_CMB/score/likelihood/verdict" if boundary_ok else f"bad_boundary={bad_boundary[:5]}",
        boundary_ok,
        "staging files must not promote themselves to accepted payloads or downstream claims",
    ))

    accounting_ok = (
        summary.get("execution_rows") == 66
        and summary.get("can_execute_rows") == 66
        and summary.get("execution_attempted_rows") == 66
        and summary.get("execution_succeeded_rows") == 66
        and summary.get("payload_staging_written_rows") == 66
        and summary.get("payload_staging_populated_rows") == 66
        and summary.get("payload_accepted_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "execution_accounting",
        "PASS_EXECUTION_ACCOUNTING" if accounting_ok else "FAIL_EXECUTION_ACCOUNTING",
        (
            f"rows={summary.get('execution_rows')}, attempted={summary.get('execution_attempted_rows')}, "
            f"succeeded={summary.get('execution_succeeded_rows')}, staging_written={summary.get('payload_staging_written_rows')}, "
            f"accepted={summary.get('payload_accepted_rows')}"
        ),
        accounting_ok,
        "execution should populate 66 staging files but accept zero payloads",
    ))

    firewall_ok = (
        all(row.get("payload_accepted") == "false" for row in exec_rows)
        and all(row.get("checker_executed") == "false" for row in exec_rows)
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
        "PASS_EXECUTION_FIREWALL_CLOSED" if firewall_ok else "FAIL_EXECUTION_FIREWALL",
        "staging execution does not open payload acceptance, checker execution, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "staging execution must not promote populated files to accepted payloads",
    ))

    rows.append(audit_row(
        "payload_acceptance",
        "BLOCKED_ACCEPTANCE_AUDIT_NOT_AVAILABLE",
        "payloads are populated but not accepted",
        False,
        "requires payload acceptance audit before checker execution",
    ))
    rows.append(audit_row(
        "checker_execution_and_R_CMB",
        "BLOCKED_CHECKERS_AND_R_CMB",
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
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(EXEC_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "staging_population_execution_audited": clean,
        "staging_population_execution_succeeded": clean,
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_AUDITED_PAYLOADS_POPULATED_NOT_ACCEPTED"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Staging Population Execution Audit v01

**Doc class:** carrier/domain checker input payload staging population execution audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that `payload_staging/` checker-input files were populated
from accepted endpoint-blind Tau-side source artifacts while remaining
unaccepted. It does not accept payloads, execute checkers, pass certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The staging files are populated and auditable, but payload acceptance remains
blocked.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB staging population execution.")
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
