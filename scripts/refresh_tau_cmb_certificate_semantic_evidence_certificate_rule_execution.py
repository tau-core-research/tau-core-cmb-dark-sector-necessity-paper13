#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_v01.csv"
TRACE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_v01_"
    "certificate_rule_executable_from_trace_acceptance_only_no_certificate_pass_no_domain_acceptance_"
    "no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "certificate_rule_execution_refresh_row_id",
    "certificate_area",
    "checker_name",
    "trace_rows",
    "trace_accepted_rows",
    "all_traces_accepted",
    "certificate_rule_executable",
    "checker_execution_replay_present",
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
    if not TRACE_SUMMARY.exists():
        return False
    summary = load_json(TRACE_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACES_ACCEPTED_FROM_COMPONENT_ACCEPTANCE_ONLY"
        and summary.get("input_chain_clean") is True
        and summary.get("trace_acceptance_rows") == 28
        and summary.get("trace_accepted_rows") == 28
        and summary.get("certificate_passed_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def refresh_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("trace acceptance refresh summary is not clean")
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(TRACE_TABLE):
        groups[(row["certificate_area"], row["checker_name"])].append(row)

    rows: list[dict[str, str]] = []
    for index, ((area, checker), members) in enumerate(sorted(groups.items()), start=1):
        accepted_count = sum(row["trace_accepted"] == "true" for row in members)
        all_accepted = len(members) > 0 and accepted_count == len(members)
        rows.append(
            {
                "certificate_rule_execution_refresh_row_id": f"TCMBCDSEMCERTRULE01_{index:03d}",
                "certificate_area": area,
                "checker_name": checker,
                "trace_rows": str(len(members)),
                "trace_accepted_rows": str(accepted_count),
                "all_traces_accepted": str(all_accepted).lower(),
                "certificate_rule_executable": str(all_accepted).lower(),
                "checker_execution_replay_present": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "refresh_status": (
                    "CERTIFICATE_RULE_EXECUTABLE_CHECKER_REPLAY_REQUIRED"
                    if all_accepted
                    else "CERTIFICATE_RULE_BLOCKED_TRACE_ACCEPTANCE_INCOMPLETE"
                ),
                "blocking_reason": (
                    "all semantic traces accepted; requires checker execution replay before certificate pass"
                    if all_accepted
                    else "requires all semantic evidence traces accepted"
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
    executable = sum(row["certificate_rule_executable"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_trace_acceptance_table": rel(TRACE_TABLE),
        "input_trace_acceptance_summary": rel(TRACE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "certificate_rule_rows": len(rows),
        "certificate_rule_executable_rows": executable,
        "checker_execution_replay_present_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_RULES_EXECUTABLE_CHECKER_REPLAY_REQUIRED"
            if input_chain_clean() and len(rows) == 7 and executable == 7
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_RULE_EXECUTION_REFRESH_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Certificate Rule Execution Refresh v01

**Doc class:** semantic evidence certificate rule execution refresh
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This refresh marks certificate rules executable only after all semantic traces
for a checker are accepted. It does not replay checker execution, pass a
certificate, accept domain objects, materialize physical R_CMB, run scoring,
evaluate likelihoods, or decide the dark-sector question.

## Summary

```text
certificate_rule_rows={summary["certificate_rule_rows"]}
certificate_rule_executable_rows={summary["certificate_rule_executable_rows"]}
checker_execution_replay_present_rows={summary["checker_execution_replay_present_rows"]}
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
    parser = argparse.ArgumentParser(description="Refresh Tau CMB certificate rule executability.")
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
