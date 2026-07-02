#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMPONENT_ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_v01.csv"
COMPONENT_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_v01_"
    "trace_acceptance_from_component_acceptance_only_no_certificate_pass_no_domain_acceptance_"
    "no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "trace_acceptance_refresh_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "component_rows",
    "component_accepted_rows",
    "all_components_accepted",
    "trace_accepted",
    "semantic_assertion_acceptance_allowed",
    "certificate_rule_executable_after_trace",
    "certificate_passed",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "refresh_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_chain_clean() -> bool:
    if not COMPONENT_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(COMPONENT_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_ACCEPTED_COMPONENT_LEVEL_ONLY"
        and summary.get("input_chain_clean") is True
        and summary.get("substantive_verification_acceptance_rows") == 128
        and summary.get("substantive_verification_accepted_rows") == 128
        and summary.get("component_accepted_after_verification_rows") == 128
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def refresh_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("component acceptance summary is not clean")
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(COMPONENT_ACCEPTANCE_TABLE):
        groups[(row["certificate_area"], row["checker_name"], row["semantic_evidence_field"])].append(row)

    rows: list[dict[str, str]] = []
    for index, ((area, checker, field), members) in enumerate(sorted(groups.items()), start=1):
        accepted_count = sum(row["component_accepted_after_verification"] == "true" for row in members)
        all_accepted = len(members) > 0 and accepted_count == len(members)
        rows.append(
            {
                "trace_acceptance_refresh_row_id": f"TCMBCDSEMTRACEACCREF01_{index:03d}",
                "certificate_area": area,
                "checker_name": checker,
                "semantic_evidence_field": field,
                "component_rows": str(len(members)),
                "component_accepted_rows": str(accepted_count),
                "all_components_accepted": str(all_accepted).lower(),
                "trace_accepted": str(all_accepted).lower(),
                "semantic_assertion_acceptance_allowed": str(all_accepted).lower(),
                "certificate_rule_executable_after_trace": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "refresh_status": (
                    "TRACE_ACCEPTED_COMPONENTS_COMPLETE"
                    if all_accepted
                    else "TRACE_BLOCKED_COMPONENT_ACCEPTANCE_INCOMPLETE"
                ),
                "blocking_reason": (
                    "trace accepted at semantic-evidence level; certificate rule execution remains downstream"
                    if all_accepted
                    else "requires all trace components accepted"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    accepted = sum(row["trace_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_component_acceptance_table": rel(COMPONENT_ACCEPTANCE_TABLE),
        "input_component_acceptance_summary": rel(COMPONENT_ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "trace_acceptance_rows": len(rows),
        "trace_accepted_rows": accepted,
        "trace_rejected_rows": len(rows) - accepted,
        "component_rows_total": sum(int(row["component_rows"]) for row in rows),
        "component_accepted_rows_total": sum(int(row["component_accepted_rows"]) for row in rows),
        "semantic_assertion_acceptance_allowed_rows": sum(row["semantic_assertion_acceptance_allowed"] == "true" for row in rows),
        "certificate_rule_executable_after_trace_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACES_ACCEPTED_FROM_COMPONENT_ACCEPTANCE_ONLY"
            if input_chain_clean() and len(rows) == 28 and accepted == 28
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_ACCEPTANCE_REFRESH_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Trace Acceptance Refresh v01

**Doc class:** semantic evidence trace acceptance refresh
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This refresh promotes semantic evidence traces only when all local trace
components are accepted. It does not execute certificate rules, accept domain
objects, materialize physical R_CMB, run scoring, evaluate likelihoods, or decide
the dark-sector question.

## Summary

```text
trace_acceptance_rows={summary["trace_acceptance_rows"]}
trace_accepted_rows={summary["trace_accepted_rows"]}
component_rows_total={summary["component_rows_total"]}
component_accepted_rows_total={summary["component_accepted_rows_total"]}
certificate_rule_executable_after_trace_rows={summary["certificate_rule_executable_after_trace_rows"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh Tau CMB trace acceptance from component acceptance.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = refresh_rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, rows)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
