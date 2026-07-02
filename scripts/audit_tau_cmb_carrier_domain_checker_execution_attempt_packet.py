#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ATTEMPT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_attempt_packet_v01.csv"
ATTEMPT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_attempt_packet_summary_v01.json"
REFRESH_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v02.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_attempt_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_execution_attempt_packet_audit_v01.md"

EXPECTED_AREAS = [
    "carrier_well_formedness",
    "domain_membership_rule",
    "seed_admissibility",
    "null_control_admissibility",
    "source_object_admissibility",
    "quotient_and_equivalence_survival",
    "endpoint_firewall_replay",
]

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_execution_attempt_packet_audit_v01_"
    "audit_only_seven_ready_rows_blocked_by_absent_checker_implementations_"
    "no_execution_success_no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_"
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
    required = [ATTEMPT_TABLE, ATTEMPT_SUMMARY, REFRESH_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    attempt_rows = read_csv(ATTEMPT_TABLE)
    summary = load_json(ATTEMPT_SUMMARY)
    refresh_audit = load_json(REFRESH_AUDIT)
    areas = [row.get("certificate_area") for row in attempt_rows]

    shape_ok = areas == EXPECTED_AREAS
    rows.append(audit_row(
        "attempt_row_shape",
        "PASS_EXPECTED_ATTEMPT_ROWS_PRESENT" if shape_ok else "FAIL_ATTEMPT_ROW_SHAPE",
        f"certificate_areas={areas}",
        shape_ok,
        "attempt packet must contain exactly the seven v02 full-execution-ready non-codomain rows",
    ))

    input_ok = (
        summary.get("input_chain_clean") is True
        and refresh_audit.get("status") == "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_V02_AUDITED_STRUCTURAL_PRECHECK_READY"
        and refresh_audit.get("failed_rows") == 0
        and refresh_audit.get("full_checker_execution_ready_rows") == 7
    )
    rows.append(audit_row(
        "refresh_v02_input_chain",
        "PASS_REFRESH_V02_INPUT_CHAIN" if input_ok else "FAIL_REFRESH_V02_INPUT_CHAIN",
        "attempt packet follows the audited v02 refresh with seven full checker rows ready",
        input_ok,
        "execution attempt audit must be downstream of clean v02 refresh audit",
    ))

    implementation_accounting_ok = (
        summary.get("attempt_packet_rows") == 7
        and summary.get("ready_input_rows") == 7
        and summary.get("checker_implementation_present_rows") == 0
        and summary.get("checker_implementation_absent_rows") == 7
        and all(row.get("checker_implementation_present") == "false" for row in attempt_rows)
        and all(Path(ROOT / row.get("expected_checker_script", "")).exists() is False for row in attempt_rows)
    )
    rows.append(audit_row(
        "checker_implementation_accounting",
        "PASS_CHECKER_IMPLEMENTATIONS_ABSENT_ACCOUNTED" if implementation_accounting_ok else "FAIL_CHECKER_IMPLEMENTATION_ACCOUNTING",
        (
            f"present={summary.get('checker_implementation_present_rows')}, "
            f"absent={summary.get('checker_implementation_absent_rows')}"
        ),
        implementation_accounting_ok,
        "all seven expected checker implementations must be explicitly accounted for before execution can proceed",
    ))

    execution_closed_ok = (
        summary.get("execution_attempt_declared_rows") == 7
        and summary.get("execution_attempted_rows") == 0
        and summary.get("execution_succeeded_rows") == 0
        and summary.get("checker_output_supplied_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
        and all(row.get("execution_attempt_declared") == "true" for row in attempt_rows)
        and all(row.get("execution_attempted") == "false" for row in attempt_rows)
        and all(row.get("execution_succeeded") == "false" for row in attempt_rows)
        and all(row.get("certificate_passed") == "false" for row in attempt_rows)
        and all(row.get("domain_object_accepted") == "false" for row in attempt_rows)
    )
    rows.append(audit_row(
        "execution_accounting",
        "PASS_ATTEMPT_DECLARED_EXECUTION_CLOSED" if execution_closed_ok else "FAIL_ATTEMPT_EXECUTION_ACCOUNTING",
        "seven attempts are declared, zero checker executions are performed or passed",
        execution_closed_ok,
        "absent checker implementations must not be promoted into successful execution or certificates",
    ))

    firewall_ok = (
        all(row.get("allows_concrete_R_CMB") == "false" for row in attempt_rows)
        and all(row.get("allows_score_entry") == "false" for row in attempt_rows)
        and all(row.get("allows_likelihood") == "false" for row in attempt_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in attempt_rows)
        and summary.get("physical_R_CMB_materialized") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_ATTEMPT_FIREWALL_CLOSED" if firewall_ok else "FAIL_ATTEMPT_FIREWALL",
        "attempt packet does not open concrete R_CMB, score entry, likelihood, or verdict",
        firewall_ok,
        "execution-attempt packet must preserve the scoring and verdict firewall",
    ))

    rows.append(audit_row(
        "checker_execution",
        "BLOCKED_CHECKER_IMPLEMENTATIONS_ABSENT",
        "seven ready rows have no executable checker implementation files",
        False,
        "requires tau_cmb_carrier_domain_checker_implementation_scaffold_v01",
    ))
    rows.append(audit_row(
        "physical_R_CMB_materialization",
        "BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED",
        "codomain row remains outside this packet because physical R_CMB is not materialized",
        False,
        "requires physical R_CMB materialization before codomain execution",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_execution_attempt_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(ATTEMPT_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "execution_attempt_packet_audited": clean,
        "attempt_packet_rows": 7 if clean else 0,
        "checker_implementation_absent_rows": 7 if clean else 0,
        "execution_attempted_rows": 0,
        "execution_succeeded_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_EXECUTION_ATTEMPT_PACKET_AUDITED_BLOCKED_IMPLEMENTATIONS_ABSENT"
            if clean
            else "CARRIER_DOMAIN_CHECKER_EXECUTION_ATTEMPT_PACKET_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_implementation_scaffold_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Carrier Domain Checker Execution Attempt Packet Audit v01

**Doc class:** carrier/domain checker execution attempt audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that the v01 execution-attempt packet uses only the seven
v02 full-execution-ready rows, accounts for checker implementation presence,
and keeps certificate pass, domain acceptance, physical `R_CMB`, score,
likelihood, and verdict closed.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

The current narrow blocker is no longer input materialization for these seven
rows. It is the absence of executable checker implementations.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker execution attempt packet v01.")
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
