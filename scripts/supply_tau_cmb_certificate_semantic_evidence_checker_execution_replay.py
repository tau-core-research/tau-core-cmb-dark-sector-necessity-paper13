#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RULE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_v01.csv"
RULE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_summary_v01.json"
CHECKER_OUTPUT_ROOT = ROOT / "data/derived/tau_cmb_checker_scaffold_outputs"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_v01_"
    "checker_execution_replay_supplied_structural_scaffold_only_no_certificate_pass_no_domain_acceptance_"
    "no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "checker_execution_replay_supply_row_id",
    "source_certificate_rule_execution_refresh_row_id",
    "certificate_area",
    "checker_name",
    "checker_output_artifact",
    "checker_output_hash_artifact",
    "checker_output_artifact_exists",
    "checker_output_hash_exists",
    "checker_output_hash_matches",
    "checker_scaffold_executed",
    "checker_output_supplied",
    "checker_execution_succeeded",
    "checker_status",
    "checker_replay_present",
    "checker_replay_certificate_level",
    "certificate_passed_by_checker_output",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "supply_status",
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


def sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not RULE_SUMMARY.exists():
        return False
    summary = load_json(RULE_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_RULES_EXECUTABLE_CHECKER_REPLAY_REQUIRED"
        and summary.get("input_chain_clean") is True
        and summary.get("certificate_rule_rows") == 7
        and summary.get("certificate_rule_executable_rows") == 7
        and summary.get("checker_execution_replay_present_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def replay_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("certificate rule execution summary is not clean")
    rows: list[dict[str, str]] = []
    for rule in read_csv(RULE_TABLE):
        index = len(rows) + 1
        checker = rule["checker_name"]
        output = CHECKER_OUTPUT_ROOT / f"{checker}_scaffold_result_v01.json"
        hash_output = CHECKER_OUTPUT_ROOT / f"{checker}_scaffold_result_v01.hashes.json"
        exists = output.exists()
        hash_exists = hash_output.exists()
        hash_matches = exists and hash_exists and load_json(hash_output).get("sha256") == sha256(output)
        payload = load_json(output) if exists else {}
        replay_present = (
            exists
            and hash_matches
            and payload.get("certificate_area") == rule["certificate_area"]
            and payload.get("checker_name") == checker
            and payload.get("checker_scaffold_executed") is True
            and payload.get("checker_output_supplied") is True
        )
        certificate_level = payload.get("status") == "CHECKER_EXECUTED_CERTIFICATE_LEVEL_PASS"
        certificate_passed = payload.get("certificate_passed") is True and certificate_level
        rows.append(
            {
                "checker_execution_replay_supply_row_id": f"TCMBCDSEMCHECKREPLAY01_{index:03d}",
                "source_certificate_rule_execution_refresh_row_id": rule["certificate_rule_execution_refresh_row_id"],
                "certificate_area": rule["certificate_area"],
                "checker_name": checker,
                "checker_output_artifact": rel(output),
                "checker_output_hash_artifact": rel(hash_output),
                "checker_output_artifact_exists": str(exists).lower(),
                "checker_output_hash_exists": str(hash_exists).lower(),
                "checker_output_hash_matches": str(hash_matches).lower(),
                "checker_scaffold_executed": str(payload.get("checker_scaffold_executed") is True).lower(),
                "checker_output_supplied": str(payload.get("checker_output_supplied") is True).lower(),
                "checker_execution_succeeded": str(payload.get("execution_succeeded") is True).lower(),
                "checker_status": str(payload.get("status", "")),
                "checker_replay_present": str(replay_present).lower(),
                "checker_replay_certificate_level": str(certificate_level).lower(),
                "certificate_passed_by_checker_output": str(certificate_passed).lower(),
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "CHECKER_EXECUTION_REPLAY_SUPPLIED_STRUCTURAL_SCAFFOLD_NOT_CERTIFICATE"
                    if replay_present and not certificate_passed
                    else (
                        "CHECKER_EXECUTION_REPLAY_SUPPLIED_CERTIFICATE_LEVEL"
                        if replay_present and certificate_passed
                        else "CHECKER_EXECUTION_REPLAY_SUPPLY_BLOCKED"
                    )
                ),
                "blocking_reason": (
                    "checker replay exists, hash matches, and structural scaffold succeeded; certificate-level pass remains downstream"
                    if replay_present and not certificate_passed
                    else (
                        "certificate-level checker pass supplied"
                        if replay_present and certificate_passed
                        else "requires checker output artifact, matching hash, and checker execution replay"
                    )
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
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_certificate_rule_execution_table": rel(RULE_TABLE),
        "input_certificate_rule_execution_summary": rel(RULE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "checker_execution_replay_supply_rows": len(rows),
        "checker_replay_present_rows": sum(row["checker_replay_present"] == "true" for row in rows),
        "checker_output_hash_matched_rows": sum(row["checker_output_hash_matches"] == "true" for row in rows),
        "checker_execution_succeeded_rows": sum(row["checker_execution_succeeded"] == "true" for row in rows),
        "checker_replay_certificate_level_rows": sum(row["checker_replay_certificate_level"] == "true" for row in rows),
        "certificate_passed_by_checker_output_rows": sum(row["certificate_passed_by_checker_output"] == "true" for row in rows),
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CHECKER_EXECUTION_REPLAY_SUPPLIED_STRUCTURAL_SCAFFOLD_NOT_CERTIFICATE"
            if input_chain_clean()
            and len(rows) == 7
            and all(row["checker_replay_present"] == "true" for row in rows)
            and all(row["certificate_passed_by_checker_output"] == "false" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CHECKER_EXECUTION_REPLAY_SUPPLY_BLOCKED_OR_CERTIFICATE_LEVEL"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Checker Execution Replay Supply v01

**Doc class:** semantic evidence checker execution replay supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies hash-bound checker execution replay artifacts for the seven
executable certificate rules. The current replay artifacts are structural
scaffold outputs, not certificate-level passes.

## Summary

```text
checker_execution_replay_supply_rows={summary["checker_execution_replay_supply_rows"]}
checker_replay_present_rows={summary["checker_replay_present_rows"]}
checker_output_hash_matched_rows={summary["checker_output_hash_matched_rows"]}
checker_execution_succeeded_rows={summary["checker_execution_succeeded_rows"]}
checker_replay_certificate_level_rows={summary["checker_replay_certificate_level_rows"]}
certificate_passed_by_checker_output_rows={summary["certificate_passed_by_checker_output_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB checker execution replay artifacts.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = replay_rows()
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
