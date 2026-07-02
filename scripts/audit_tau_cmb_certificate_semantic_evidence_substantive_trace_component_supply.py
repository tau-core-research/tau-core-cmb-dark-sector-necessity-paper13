#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_audit_v01_"
    "audit_only_component_draft_content_supplied_not_accepted_no_certificate_pass_"
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
    missing = [path for path in [SUPPLY_TABLE, SUPPLY_SUMMARY] if not path.exists()]
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)
    table = read_csv(SUPPLY_TABLE)
    summary = load_json(SUPPLY_SUMMARY)

    shape_ok = len(table) == summary.get("component_supply_rows") and len(table) > 0
    rows.append(audit_row("component_row_shape", "PASS_COMPONENT_ROWS_PRESENT" if shape_ok else "FAIL_COMPONENT_ROW_SHAPE", f"rows={len(table)}", shape_ok, "component supply must include every declared trace component"))

    supplied_ok = (
        summary.get("component_artifact_supplied_rows") == len(table)
        and summary.get("hash_matched_rows") == len(table)
        and summary.get("endpoint_blind_component_rows") == len(table)
        and summary.get("component_content_supplied_rows") == len(table)
        and all(row["component_artifact_supplied"] == "true" for row in table)
        and all(row["hash_matches"] == "true" for row in table)
    )
    rows.append(audit_row("component_drafts", "PASS_COMPONENT_DRAFTS_HASH_BOUND" if supplied_ok else "FAIL_COMPONENT_DRAFTS", f"supplied={summary.get('component_artifact_supplied_rows')}, hash_matched={summary.get('hash_matched_rows')}", supplied_ok, "all component draft files must exist, be hash-bound, and remain endpoint-blind"))

    not_proof_ok = (
        summary.get("component_substantively_proven_rows") == 0
        and summary.get("component_accepted_rows") == 0
        and summary.get("trace_accepted_after_component_rows") == 0
        and summary.get("certificate_rule_executable_after_component_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and all(row["component_substantively_proven"] == "false" for row in table)
        and all(row["component_accepted"] == "false" for row in table)
        and all(row["certificate_passed"] == "false" for row in table)
    )
    rows.append(audit_row("not_proof_boundary", "PASS_COMPONENTS_NOT_ACCEPTED_NOT_PROOF" if not_proof_ok else "FAIL_COMPONENT_PROOF_BOUNDARY", "component drafts do not open component acceptance, trace acceptance, or certificate execution", not_proof_ok, "component draft supply must not promote draft content into proof"))

    firewall_ok = (
        summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
        and all(row["allows_score_entry"] == "false" for row in table)
        and all(row["allows_likelihood"] == "false" for row in table)
        and all(row["allows_dark_sector_verdict"] == "false" for row in table)
    )
    rows.append(audit_row("promotion_firewall", "PASS_COMPONENT_FIREWALL_CLOSED" if firewall_ok else "FAIL_COMPONENT_FIREWALL", "component supply does not open score, likelihood, or verdict", firewall_ok, "component supply must preserve scoring firewall"))

    rows.append(audit_row("component_acceptance", "BLOCKED_COMPONENT_ACCEPTANCE_NOT_PERFORMED", "component drafts are supplied but not accepted as substantive proof components", False, "requires substantive trace component acceptance audit"))
    rows.append(audit_row("trace_acceptance", "BLOCKED_TRACE_ACCEPTANCE_NOT_ALLOWED", "traces remain unaccepted until all required components are accepted", False, "requires accepted substantive trace components"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(SUPPLY_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "component_supply_audited": clean,
        "component_supply_rows": load_json(SUPPLY_SUMMARY).get("component_supply_rows", 0) if SUPPLY_SUMMARY.exists() and clean else 0,
        "component_content_supplied_rows": load_json(SUPPLY_SUMMARY).get("component_content_supplied_rows", 0) if SUPPLY_SUMMARY.exists() and clean else 0,
        "component_substantively_proven_rows": 0,
        "component_accepted_rows": 0,
        "trace_accepted_after_component_rows": 0,
        "certificate_rule_executable_after_component_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUPPLY_AUDITED_DRAFT_CONTENT_NOT_ACCEPTED"
            if clean
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUPPLY_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Supply Audit v01

**Doc class:** semantic certificate evidence trace component supply audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that trace-component draft content exists and remains
non-certifying.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

The route has moved from missing component files to component acceptance.
Scoring remains closed.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB substantive trace component supply.")
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
