#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REFRESH_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_v02.csv"
REFRESH_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_summary_v02.json"
STRUCTURAL_R_CMB_AUDIT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_candidate_gate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v02.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v02.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v02_"
    "audit_only_structural_R_CMB_visible_for_codomain_precheck_no_checker_attempt_no_certificate_pass_"
    "no_physical_R_CMB_no_score_no_likelihood_no_verdict"
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
    required = [REFRESH_TABLE, REFRESH_SUMMARY, STRUCTURAL_R_CMB_AUDIT]
    missing = [path for path in required if not path.exists()]
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    refresh_rows = read_csv(REFRESH_TABLE)
    summary = load_json(REFRESH_SUMMARY)
    structural = load_json(STRUCTURAL_R_CMB_AUDIT)

    shape_ok = len(refresh_rows) == 8
    rows.append(audit_row("refresh_row_shape", "PASS_REFRESH_V02_ROWS_PRESENT" if shape_ok else "FAIL_REFRESH_V02_ROW_SHAPE", f"rows={len(refresh_rows)}", shape_ok, "refresh v02 requires eight checker rows"))

    input_ok = (
        summary.get("input_chain_clean") is True
        and structural.get("status") == "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_AUDITED_NOT_PHYSICAL"
        and structural.get("structural_candidate_available_for_codomain_precheck") is True
        and structural.get("failed_rows") == 0
    )
    rows.append(audit_row("structural_R_CMB_input_chain", "PASS_STRUCTURAL_R_CMB_INPUT_CHAIN" if input_ok else "FAIL_STRUCTURAL_R_CMB_INPUT_CHAIN", "refresh v02 follows audited structural R_CMB candidate gate", input_ok, "refresh v02 requires clean structural R_CMB candidate gate"))

    accounting_ok = (
        summary.get("payload_ready_rows") == 8
        and summary.get("structural_precheck_ready_rows") == 8
        and summary.get("full_checker_execution_ready_rows") == 7
        and summary.get("codomain_structural_precheck_ready_rows") == 1
        and summary.get("blocked_by_physical_R_CMB_rows") == 1
        and any(
            row["certificate_area"] == "codomain_compatibility"
            and row["structural_precheck_ready"] == "true"
            and row["full_checker_execution_ready"] == "false"
            for row in refresh_rows
        )
    )
    rows.append(audit_row("readiness_accounting", "PASS_REFRESH_V02_READINESS_ACCOUNTING" if accounting_ok else "FAIL_REFRESH_V02_READINESS_ACCOUNTING", f"structural={summary.get('structural_precheck_ready_rows')}, full={summary.get('full_checker_execution_ready_rows')}, physical_R_CMB_blocked={summary.get('blocked_by_physical_R_CMB_rows')}", accounting_ok, "refresh v02 should expose 8 structural prechecks, 7 full execution-ready rows, and 1 physical R_CMB block"))

    firewall_ok = (
        all(row["execution_attempted"] == "false" for row in refresh_rows)
        and all(row["execution_succeeded"] == "false" for row in refresh_rows)
        and all(row["certificate_passed"] == "false" for row in refresh_rows)
        and all(row["domain_object_accepted"] == "false" for row in refresh_rows)
        and all(row["allows_concrete_R_CMB"] == "false" for row in refresh_rows)
        and all(row["allows_score_entry"] == "false" for row in refresh_rows)
        and all(row["allows_likelihood"] == "false" for row in refresh_rows)
        and all(row["allows_dark_sector_verdict"] == "false" for row in refresh_rows)
        and summary.get("physical_R_CMB_materialized") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row("promotion_firewall", "PASS_REFRESH_V02_FIREWALL_CLOSED" if firewall_ok else "FAIL_REFRESH_V02_FIREWALL", "refresh v02 does not execute checkers or open physical R_CMB/score/likelihood/verdict", firewall_ok, "refresh v02 must not promote structural precheck into physical readout or scoring"))

    rows.append(audit_row("checker_execution_attempt", "BLOCKED_CHECKER_EXECUTION_NOT_ATTEMPTED", "seven full checker rows are ready but not attempted", False, "requires explicit execution-attempt packet"))
    rows.append(audit_row("physical_R_CMB_materialization", "BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED", "codomain row has structural shell only, not physical R_CMB", False, "requires physical R_CMB materialization gate"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v02",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(REFRESH_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "execution_packet_refresh_v02_audited": clean,
        "structural_precheck_ready_rows": 8 if clean else 0,
        "full_checker_execution_ready_rows": 7 if clean else 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_V02_AUDITED_STRUCTURAL_PRECHECK_READY"
            if clean
            else "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_V02_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_execution_attempt_packet_v01_for_7_ready_rows_or_physical_R_CMB_materialization_gate_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Carrier Domain Checker Execution Packet Refresh Audit v02

**Doc class:** carrier/domain checker execution packet refresh audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the refresh state after the structural `R_CMB` candidate shell
is visible to the codomain route. It does not execute checkers, pass
certificates, accept domain objects, materialize physical `R_CMB`, open score
entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

Eight structural prechecks are ready, seven full checker executions are ready
but not attempted, and physical `R_CMB` materialization remains blocked.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker execution refresh v02.")
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
