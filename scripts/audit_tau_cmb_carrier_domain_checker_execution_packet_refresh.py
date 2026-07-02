#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REFRESH_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_v01.csv"
REFRESH_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_summary_v01.json"
PAYLOAD_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v01_"
    "audit_only_execution_readiness_refresh_no_checker_attempt_no_certificate_pass_no_domain_acceptance_"
    "no_R_CMB_no_score_no_likelihood_no_verdict"
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
    rows: list[dict[str, Any]] = []
    required = [REFRESH_TABLE, REFRESH_SUMMARY, PAYLOAD_ACCEPTANCE_SUMMARY]
    missing = [p for p in required if not p.exists()]
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    refresh_rows = read_csv(REFRESH_TABLE)
    summary = load_json(REFRESH_SUMMARY)
    payload_summary = load_json(PAYLOAD_ACCEPTANCE_SUMMARY)

    shape_ok = len(refresh_rows) == 8
    rows.append(audit_row("refresh_row_shape", "PASS_REFRESH_ROWS_PRESENT" if shape_ok else "FAIL_REFRESH_ROW_SHAPE", f"rows={len(refresh_rows)}", shape_ok, "refresh requires eight checker rows"))

    input_ok = (
        summary.get("input_chain_clean") is True
        and payload_summary.get("payload_accepted_rows") == 66
        and payload_summary.get("checker_input_available_rows") == 66
        and payload_summary.get("checker_executed_rows") == 0
    )
    rows.append(audit_row("input_payload_acceptance_chain", "PASS_REFRESH_INPUT_CHAIN" if input_ok else "FAIL_REFRESH_INPUT_CHAIN", "refresh follows accepted checker-input payloads", input_ok, "refresh requires accepted checker-input payloads"))

    readiness_ok = (
        summary.get("payload_ready_rows") == 8
        and summary.get("can_execute_after_refresh_rows") == 7
        and summary.get("blocked_by_concrete_R_CMB_candidate_rows") == 1
        and sum(row["can_execute_after_refresh"] == "true" for row in refresh_rows) == 7
        and any(row["certificate_area"] == "codomain_compatibility" and row["can_execute_after_refresh"] == "false" for row in refresh_rows)
    )
    rows.append(audit_row("readiness_accounting", "PASS_REFRESH_READINESS_ACCOUNTING" if readiness_ok else "FAIL_REFRESH_READINESS_ACCOUNTING", f"ready={summary.get('can_execute_after_refresh_rows')}, blocked_R_CMB={summary.get('blocked_by_concrete_R_CMB_candidate_rows')}", readiness_ok, "refresh should mark seven executable rows and one codomain R_CMB block"))

    firewall_ok = (
        all(row["execution_attempted"] == "false" for row in refresh_rows)
        and all(row["execution_succeeded"] == "false" for row in refresh_rows)
        and all(row["checker_output_supplied"] == "false" for row in refresh_rows)
        and all(row["certificate_passed"] == "false" for row in refresh_rows)
        and all(row["domain_object_accepted"] == "false" for row in refresh_rows)
        and all(row["allows_concrete_R_CMB"] == "false" for row in refresh_rows)
        and all(row["allows_score_entry"] == "false" for row in refresh_rows)
        and all(row["allows_likelihood"] == "false" for row in refresh_rows)
        and all(row["allows_dark_sector_verdict"] == "false" for row in refresh_rows)
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row("promotion_firewall", "PASS_REFRESH_FIREWALL_CLOSED" if firewall_ok else "FAIL_REFRESH_FIREWALL", "refresh does not execute checkers or open R_CMB/score/likelihood/verdict", firewall_ok, "refresh must not promote readiness into execution or downstream claims"))

    rows.append(audit_row("checker_execution_attempt", "BLOCKED_CHECKER_EXECUTION_NOT_ATTEMPTED", "seven checker rows are ready but not attempted", False, "requires explicit checker execution attempt packet"))
    rows.append(audit_row("codomain_R_CMB_candidate", "BLOCKED_CONCRETE_R_CMB_CANDIDATE_ABSENT", "codomain compatibility remains blocked by missing concrete R_CMB candidate", False, "requires concrete R_CMB candidate gate before codomain execution"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(r["audit_passed"]) for r in rows)
    blocked = sum(r["audit_status"].startswith("BLOCKED") for r in rows)
    failed = sum(r["audit_status"].startswith("FAIL") for r in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(REFRESH_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "execution_packet_refresh_audited": clean,
        "checker_execution_attempt_allowed_rows": 7 if clean else 0,
        "codomain_execution_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_AUDITED_PARTIAL_EXECUTION_READY_NOT_ATTEMPTED" if clean else "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_AUDIT_FAILED",
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_execution_attempt_packet_v01_or_concrete_R_CMB_candidate_gate_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{r['component']}`: {r['audit_status']} | {r['finding']}" for r in report["audit_rows"])
    text = f"""# Tau CMB Carrier Domain Checker Execution Packet Refresh Audit v01

**Doc class:** carrier/domain checker execution packet refresh audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the refreshed checker-execution readiness after input-payload
acceptance. It does not execute checkers, pass certificates, accept domain
objects, materialize `R_CMB`, open score entry, compute a likelihood, or decide
the dark-sector question.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

Seven checker rows are ready but not attempted. Codomain compatibility remains
blocked until a concrete `R_CMB` candidate exists.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker execution packet refresh.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
