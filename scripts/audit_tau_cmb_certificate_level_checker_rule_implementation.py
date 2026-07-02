#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RULE_TABLE = ROOT / "data/derived/tau_cmb_certificate_level_checker_rule_implementation_v01.csv"
RULE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_level_checker_rule_implementation_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_certificate_level_checker_rule_implementation_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_level_checker_rule_implementation_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_level_checker_rule_implementation_audit_v01_"
    "audit_only_rules_declared_semantic_evidence_absent_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
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
    missing = [path for path in [RULE_TABLE, RULE_SUMMARY] if not path.exists()]
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    table = read_csv(RULE_TABLE)
    summary = load_json(RULE_SUMMARY)
    shape_ok = len(table) == 7 and summary.get("rule_rows") == 7
    rows.append(audit_row("rule_row_shape", "PASS_SEVEN_RULE_ROWS_PRESENT" if shape_ok else "FAIL_RULE_ROW_SHAPE", f"rows={len(table)}", shape_ok, "rule implementation must cover seven non-codomain checker families"))

    declaration_ok = summary.get("rule_implementation_declared_rows") == 7 and all(row["rule_implementation_declared"] == "true" for row in table)
    rows.append(audit_row("rule_declarations", "PASS_RULE_IMPLEMENTATIONS_DECLARED" if declaration_ok else "FAIL_RULE_DECLARATIONS", f"declared={summary.get('rule_implementation_declared_rows')}", declaration_ok, "each checker family must declare certificate-level predicates"))

    evidence_accounting_ok = (
        summary.get("scaffold_output_accepted_rows") == 7
        and summary.get("semantic_evidence_fields_present_rows") == 0
        and summary.get("certificate_rule_executable_rows") == 0
        and all(row["semantic_evidence_fields_present"] == "false" for row in table)
        and all(row["certificate_rule_executable"] == "false" for row in table)
    )
    rows.append(audit_row("semantic_evidence_accounting", "PASS_SEMANTIC_EVIDENCE_BLOCK_ACCOUNTED" if evidence_accounting_ok else "FAIL_SEMANTIC_EVIDENCE_ACCOUNTING", f"semantic={summary.get('semantic_evidence_fields_present_rows')}, executable={summary.get('certificate_rule_executable_rows')}", evidence_accounting_ok, "certificate rules must not be executable until semantic proof/evidence fields are present"))

    firewall_ok = (
        summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
        and summary.get("physical_R_CMB_materialized") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
        and all(row["certificate_passed"] == "false" for row in table)
        and all(row["domain_object_accepted"] == "false" for row in table)
        and all(row["allows_score_entry"] == "false" for row in table)
        and all(row["allows_likelihood"] == "false" for row in table)
        and all(row["allows_dark_sector_verdict"] == "false" for row in table)
    )
    rows.append(audit_row("promotion_firewall", "PASS_RULE_FIREWALL_CLOSED" if firewall_ok else "FAIL_RULE_FIREWALL", "rules do not open certificate/domain/readout/score/likelihood/verdict claims", firewall_ok, "rule implementation must not promote missing semantic evidence into certificates or scoring"))

    rows.append(audit_row("semantic_certificate_evidence", "BLOCKED_SEMANTIC_CERTIFICATE_EVIDENCE_ABSENT", "certificate predicates are implemented but required semantic evidence fields are absent", False, "requires tau_cmb_certificate_semantic_evidence_materialization_v01"))
    rows.append(audit_row("physical_R_CMB_materialization", "BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED", "codomain and physical CMB readout remain downstream", False, "requires physical R_CMB materialization before codomain and scoring"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_certificate_level_checker_rule_implementation_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(RULE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "rule_implementation_audited": clean,
        "rule_implementation_declared_rows": 7 if clean else 0,
        "semantic_evidence_fields_present_rows": 0,
        "certificate_rule_executable_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_LEVEL_CHECKER_RULE_IMPLEMENTATION_AUDITED_BLOCKED_BY_SEMANTIC_EVIDENCE"
            if clean
            else "CMB_CERTIFICATE_LEVEL_CHECKER_RULE_IMPLEMENTATION_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_materialization_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Certificate-Level Checker Rule Implementation Audit v01

**Doc class:** certificate-level checker rule implementation audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that certificate-level predicates have been declared for
the seven non-codomain checker families and that the current staging payloads
do not yet contain the semantic evidence fields needed to execute certificate
passes.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

The route has moved from implementation absence to semantic certificate
evidence materialization. Scoring remains closed.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB certificate-level checker rule implementation.")
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
