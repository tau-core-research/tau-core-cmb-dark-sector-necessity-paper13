#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_implementation_scaffold_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_implementation_scaffold_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_implementation_scaffold_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_implementation_scaffold_audit_v01_"
    "audit_only_checker_scaffolds_smoke_executed_not_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


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
    if not SCAFFOLD_REPORT.exists():
        rows.append(audit_row(rel(SCAFFOLD_REPORT), "FAIL_MISSING_ARTIFACT", "implementation scaffold report is absent", False, "audit package incomplete"))
        return finalize(rows)

    report = load_json(SCAFFOLD_REPORT)
    checker_rows = report.get("checker_rows", [])
    shape_ok = len(checker_rows) == 7
    rows.append(audit_row("checker_row_shape", "PASS_SEVEN_CHECKER_ROWS_PRESENT" if shape_ok else "FAIL_CHECKER_ROW_SHAPE", f"rows={len(checker_rows)}", shape_ok, "implementation scaffold must cover seven non-codomain checker rows"))

    scripts_ok = report.get("checker_scripts_present_rows") == 7 and all(row.get("checker_script_present") is True for row in checker_rows)
    rows.append(audit_row("checker_scripts", "PASS_CHECKER_SCRIPTS_PRESENT" if scripts_ok else "FAIL_CHECKER_SCRIPTS_MISSING", f"present={report.get('checker_scripts_present_rows')}", scripts_ok, "all seven checker scripts must be present"))

    outputs_ok = (
        report.get("scaffold_output_present_rows") == 7
        and report.get("scaffold_hash_output_present_rows") == 7
        and report.get("scaffold_checks_passed_rows") == 7
        and report.get("execution_succeeded_rows") == 7
    )
    rows.append(audit_row("scaffold_outputs", "PASS_SCAFFOLD_OUTPUTS_PRESENT_AND_PASSED" if outputs_ok else "FAIL_SCAFFOLD_OUTPUTS", f"outputs={report.get('scaffold_output_present_rows')}, passed={report.get('scaffold_checks_passed_rows')}", outputs_ok, "all seven checker scaffold outputs and hashes must exist and pass structural input checks"))

    firewall_ok = (
        report.get("certificate_passed_rows") == 0
        and report.get("accepted_domain_objects") == 0
        and report.get("physical_R_CMB_materialized") is False
        and report.get("concrete_R_CMB_allowed") is False
        and report.get("score_entry_allowed") is False
        and report.get("likelihood_allowed") is False
        and report.get("dark_sector_verdict_allowed") is False
        and all(row.get("certificate_passed") is False for row in checker_rows)
        and all(row.get("domain_object_accepted") is False for row in checker_rows)
        and all(row.get("score_entry_allowed") is False for row in checker_rows)
        and all(row.get("likelihood_allowed") is False for row in checker_rows)
        and all(row.get("dark_sector_verdict_allowed") is False for row in checker_rows)
    )
    rows.append(audit_row("promotion_firewall", "PASS_SCAFFOLD_FIREWALL_CLOSED" if firewall_ok else "FAIL_SCAFFOLD_FIREWALL", "scaffold outputs do not open certificate/domain/score/likelihood/verdict claims", firewall_ok, "implementation scaffold must not promote structural smoke checks into scientific certificates or scoring"))

    rows.append(audit_row("certificate_acceptance", "BLOCKED_CERTIFICATE_ACCEPTANCE_NOT_YET_AUDITED", "structural scaffold outputs exist, but certificate acceptance remains downstream", False, "requires tau_cmb_carrier_domain_checker_scaffold_output_acceptance_audit_v01"))
    rows.append(audit_row("physical_R_CMB_materialization", "BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED", "codomain/physical readout remains outside the seven scaffold rows", False, "requires physical R_CMB materialization before codomain execution"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_implementation_scaffold_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_report": rel(SCAFFOLD_REPORT),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "checker_implementation_scaffold_audited": clean,
        "checker_scripts_present_rows": 7 if clean else 0,
        "scaffold_execution_succeeded_rows": 7 if clean else 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_IMPLEMENTATION_SCAFFOLD_AUDITED_SMOKE_EXECUTED_NOT_CERTIFICATE"
            if clean
            else "CARRIER_DOMAIN_CHECKER_IMPLEMENTATION_SCAFFOLD_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_scaffold_output_acceptance_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Carrier Domain Checker Implementation Scaffold Audit v01

**Doc class:** checker implementation scaffold audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that the seven non-codomain checker scaffold scripts exist,
their structural smoke outputs are present, and no downstream scientific or
scoring claim has been opened.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

The current narrow blocker has moved from missing checker implementations to
acceptance/auditing of scaffold outputs as non-certifying checker outputs.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker implementation scaffold.")
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
