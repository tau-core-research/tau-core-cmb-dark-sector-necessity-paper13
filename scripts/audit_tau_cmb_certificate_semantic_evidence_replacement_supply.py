#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_supply_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_supply_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_replacement_supply_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_replacement_supply_audit_v01_"
    "audit_only_draft_replacements_supplied_not_accepted_no_proof_no_certificate_pass_"
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
    shape_ok = len(table) == 28 and summary.get("replacement_supply_rows") == 28
    rows.append(audit_row("replacement_row_shape", "PASS_28_REPLACEMENT_ROWS_PRESENT" if shape_ok else "FAIL_REPLACEMENT_ROW_SHAPE", f"rows={len(table)}", shape_ok, "replacement supply must cover all 28 requested replacements"))

    supplied_ok = (
        summary.get("replacement_supplied_rows") == 28
        and summary.get("hash_supplied_rows") == 28
        and summary.get("hash_matched_rows") == 28
        and all(row["replacement_supplied"] == "true" for row in table)
        and all(row["hash_matches"] == "true" for row in table)
    )
    rows.append(audit_row("draft_replacements", "PASS_DRAFT_REPLACEMENTS_HASH_BOUND" if supplied_ok else "FAIL_DRAFT_REPLACEMENTS", f"supplied={summary.get('replacement_supplied_rows')}, hash_matched={summary.get('hash_matched_rows')}", supplied_ok, "all draft replacement files must exist and be hash-bound"))

    not_accepted_ok = (
        summary.get("semantic_assertion_nonnull_rows") == 0
        and summary.get("semantic_assertion_accepted_rows") == 0
        and summary.get("proof_claim_allowed_rows") == 0
        and summary.get("replacement_accepted_rows") == 0
        and summary.get("certificate_rule_executable_after_replacement_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and all(row["replacement_accepted"] == "false" for row in table)
        and all(row["proof_claim_allowed"] == "false" for row in table)
        and all(row["certificate_passed"] == "false" for row in table)
    )
    rows.append(audit_row("not_accepted_boundary", "PASS_REPLACEMENTS_NOT_ACCEPTED_NOT_PROOF" if not_accepted_ok else "FAIL_REPLACEMENT_PROOF_BOUNDARY", "draft replacements contain no accepted semantic assertions or proof claims", not_accepted_ok, "replacement supply must not promote draft shells into accepted evidence"))

    firewall_ok = (
        summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
        and all(row["allows_score_entry"] == "false" for row in table)
        and all(row["allows_likelihood"] == "false" for row in table)
        and all(row["allows_dark_sector_verdict"] == "false" for row in table)
    )
    rows.append(audit_row("promotion_firewall", "PASS_REPLACEMENT_FIREWALL_CLOSED" if firewall_ok else "FAIL_REPLACEMENT_FIREWALL", "replacement supply does not open score, likelihood, or verdict", firewall_ok, "replacement supply must preserve scoring firewall"))

    rows.append(audit_row("semantic_assertions", "BLOCKED_SUBSTANTIVE_SEMANTIC_ASSERTIONS_ABSENT", "draft replacements are present but semantic assertions remain null", False, "requires substantive endpoint-blind proof traces and non-null accepted assertions"))
    rows.append(audit_row("certificate_execution", "BLOCKED_CERTIFICATE_EXECUTION_NOT_ALLOWED", "certificate rules remain non-executable until replacements are accepted", False, "requires replacement acceptance audit after substantive assertions are supplied"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_replacement_supply_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(SUPPLY_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "replacement_supply_audited": clean,
        "replacement_supply_rows": 28 if clean else 0,
        "replacement_supplied_rows": 28 if clean else 0,
        "replacement_accepted_rows": 0,
        "certificate_rule_executable_after_replacement_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_SUPPLY_AUDITED_DRAFTS_NOT_ACCEPTED"
            if clean
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_SUPPLY_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Certificate Semantic Evidence Replacement Supply Audit v01

**Doc class:** semantic certificate evidence replacement supply audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that the 28 draft replacement files exist and are
hash-bound, while remaining unaccepted and non-proof.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

The route has moved from missing replacement files to missing substantive
semantic assertions. Scoring remains closed.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB semantic evidence draft replacement supply.")
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
