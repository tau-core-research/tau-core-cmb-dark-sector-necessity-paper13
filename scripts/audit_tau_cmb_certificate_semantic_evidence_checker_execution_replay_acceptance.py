#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_v01_"
    "acceptance_audit_structural_replay_present_certificate_level_replay_required_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "checker_execution_replay_acceptance_row_id",
    "source_checker_execution_replay_supply_row_id",
    "certificate_area",
    "checker_name",
    "checker_replay_present",
    "checker_output_hash_matches",
    "checker_execution_succeeded",
    "checker_replay_certificate_level",
    "certificate_passed_by_checker_output",
    "checker_execution_replay_accepted",
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
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CHECKER_EXECUTION_REPLAY_SUPPLIED_STRUCTURAL_SCAFFOLD_NOT_CERTIFICATE"
        and summary.get("input_chain_clean") is True
        and summary.get("checker_execution_replay_supply_rows") == 7
        and summary.get("checker_replay_present_rows") == 7
        and summary.get("certificate_passed_by_checker_output_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def audit_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("checker execution replay supply summary is not clean")
    rows: list[dict[str, str]] = []
    for source in read_csv(SUPPLY_TABLE):
        index = len(rows) + 1
        accepted = (
            source["checker_replay_present"] == "true"
            and source["checker_output_hash_matches"] == "true"
            and source["checker_execution_succeeded"] == "true"
            and source["checker_replay_certificate_level"] == "true"
            and source["certificate_passed_by_checker_output"] == "true"
        )
        rows.append(
            {
                "checker_execution_replay_acceptance_row_id": f"TCMBCDSEMCHECKREPLAYACC01_{index:03d}",
                "source_checker_execution_replay_supply_row_id": source["checker_execution_replay_supply_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "checker_replay_present": source["checker_replay_present"],
                "checker_output_hash_matches": source["checker_output_hash_matches"],
                "checker_execution_succeeded": source["checker_execution_succeeded"],
                "checker_replay_certificate_level": source["checker_replay_certificate_level"],
                "certificate_passed_by_checker_output": source["certificate_passed_by_checker_output"],
                "checker_execution_replay_accepted": str(accepted).lower(),
                "certificate_passed": str(accepted).lower(),
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "CHECKER_EXECUTION_REPLAY_ACCEPTED_CERTIFICATE_PASSED"
                    if accepted
                    else "CHECKER_EXECUTION_REPLAY_REJECTED_CERTIFICATE_LEVEL_REPLAY_REQUIRED"
                ),
                "blocking_reason": (
                    "certificate-level checker replay accepted"
                    if accepted
                    else "structural checker replay is present, but certificate-level replay/pass is not supplied"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_checker_execution_replay_supply_table": rel(SUPPLY_TABLE),
        "input_checker_execution_replay_supply_summary": rel(SUPPLY_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "checker_execution_replay_acceptance_rows": len(rows),
        "checker_replay_present_rows": sum(row["checker_replay_present"] == "true" for row in rows),
        "checker_output_hash_matched_rows": sum(row["checker_output_hash_matches"] == "true" for row in rows),
        "checker_execution_succeeded_rows": sum(row["checker_execution_succeeded"] == "true" for row in rows),
        "checker_replay_certificate_level_rows": sum(row["checker_replay_certificate_level"] == "true" for row in rows),
        "checker_execution_replay_accepted_rows": sum(row["checker_execution_replay_accepted"] == "true" for row in rows),
        "certificate_passed_rows": passed,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CHECKER_EXECUTION_REPLAY_ACCEPTANCE_AUDITED_REJECTED_CERTIFICATE_LEVEL_REPLAY_REQUIRED"
            if input_chain_clean() and len(rows) == 7 and passed == 0
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CHECKER_EXECUTION_REPLAY_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Checker Execution Replay Acceptance Audit v01

**Doc class:** semantic evidence checker execution replay acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit confirms that checker replay artifacts are present and hash-bound,
but rejects certificate pass because the current outputs are structural
scaffold executions, not certificate-level checker replays.

## Summary

```text
checker_execution_replay_acceptance_rows={summary["checker_execution_replay_acceptance_rows"]}
checker_replay_present_rows={summary["checker_replay_present_rows"]}
checker_execution_succeeded_rows={summary["checker_execution_succeeded_rows"]}
checker_replay_certificate_level_rows={summary["checker_replay_certificate_level_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker execution replay acceptance.")
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
