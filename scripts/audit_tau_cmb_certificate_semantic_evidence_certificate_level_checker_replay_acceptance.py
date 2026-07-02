#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_v01_"
    "semantic_certificate_checker_pass_only_no_domain_acceptance_no_physical_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "certificate_level_checker_replay_acceptance_row_id",
    "source_certificate_level_checker_replay_supply_row_id",
    "certificate_area",
    "checker_name",
    "certificate_level_replay_artifact",
    "hash_matches",
    "structural_checker_replay_present",
    "structural_checker_execution_succeeded",
    "all_traces_accepted",
    "certificate_rule_executable",
    "certificate_level_replay_body_present",
    "certificate_pass_candidate",
    "certificate_level_replay_accepted",
    "certificate_passed",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "acceptance_status",
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
    if not SUPPLY_SUMMARY.exists():
        return False
    summary = load_json(SUPPLY_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_LEVEL_CHECKER_REPLAY_CANDIDATES_SUPPLIED"
        and summary.get("input_chain_clean") is True
        and summary.get("certificate_level_checker_replay_supply_rows") == 7
        and summary.get("certificate_pass_candidate_rows") == 7
        and summary.get("certificate_passed_after_supply_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def audit_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("certificate-level checker replay supply summary is not clean")
    rows: list[dict[str, str]] = []
    for source in read_csv(SUPPLY_TABLE):
        index = len(rows) + 1
        accepted = all(
            source[key] == "true"
            for key in [
                "hash_matches",
                "structural_checker_replay_present",
                "structural_checker_execution_succeeded",
                "all_traces_accepted",
                "certificate_rule_executable",
                "certificate_level_replay_body_present",
                "certificate_pass_candidate",
            ]
        )
        rows.append(
            {
                "certificate_level_checker_replay_acceptance_row_id": f"TCMBCDSEMCERTREPLAYACC01_{index:03d}",
                "source_certificate_level_checker_replay_supply_row_id": source["certificate_level_checker_replay_supply_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "certificate_level_replay_artifact": source["certificate_level_replay_artifact"],
                "hash_matches": source["hash_matches"],
                "structural_checker_replay_present": source["structural_checker_replay_present"],
                "structural_checker_execution_succeeded": source["structural_checker_execution_succeeded"],
                "all_traces_accepted": source["all_traces_accepted"],
                "certificate_rule_executable": source["certificate_rule_executable"],
                "certificate_level_replay_body_present": source["certificate_level_replay_body_present"],
                "certificate_pass_candidate": source["certificate_pass_candidate"],
                "certificate_level_replay_accepted": str(accepted).lower(),
                "certificate_passed": str(accepted).lower(),
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "SEMANTIC_CERTIFICATE_CHECKER_PASS_ACCEPTED"
                    if accepted
                    else "SEMANTIC_CERTIFICATE_CHECKER_PASS_REJECTED"
                ),
                "blocking_reason": (
                    "semantic certificate checker pass accepted; domain-object acceptance remains downstream"
                    if accepted
                    else "requires hash-matched replay body, accepted traces, executable rule, and structural checker replay"
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
    passed = sum(row["certificate_passed"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_certificate_level_checker_replay_supply_table": rel(SUPPLY_TABLE),
        "input_certificate_level_checker_replay_supply_summary": rel(SUPPLY_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "certificate_level_checker_replay_acceptance_rows": len(rows),
        "certificate_level_replay_accepted_rows": sum(row["certificate_level_replay_accepted"] == "true" for row in rows),
        "certificate_passed_rows": passed,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_LEVEL_CHECKER_REPLAYS_ACCEPTED_SEMANTIC_CERTIFICATE_PASS"
            if input_chain_clean() and len(rows) == 7 and passed == 7
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_LEVEL_CHECKER_REPLAY_ACCEPTANCE_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Certificate-Level Checker Replay Acceptance Audit v01

**Doc class:** semantic evidence certificate-level checker replay acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts semantic certificate-level checker replays only. It does not
accept domain objects, materialize physical R_CMB, open scoring, evaluate
likelihoods, or decide the dark-sector question.

## Summary

```text
certificate_level_checker_replay_acceptance_rows={summary["certificate_level_checker_replay_acceptance_rows"]}
certificate_level_replay_accepted_rows={summary["certificate_level_replay_accepted_rows"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
accepted_domain_objects={summary["accepted_domain_objects"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB certificate-level checker replay acceptance.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = audit_rows()
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
