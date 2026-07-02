#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_acceptance_audit_v01.csv"
ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_request_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_request_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_replacement_request_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_replacement_request_v01_"
    "replacement_request_only_no_replacement_supplied_no_evidence_acceptance_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "replacement_row_id",
    "source_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "rejected_candidate_artifact",
    "required_replacement_artifact",
    "required_semantic_assertion_value",
    "required_acceptance_flags",
    "required_endpoint_blind_firewall",
    "replacement_supplied",
    "replacement_accepted",
    "certificate_rule_executable_after_replacement",
    "certificate_passed",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "request_status",
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
    if not ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_ACCEPTANCE_AUDITED_REPLACEMENT_REQUIRED"
        and summary.get("acceptance_rows") == 28
        and summary.get("replacement_required_rows") == 28
        and summary.get("accepted_as_semantic_evidence_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(ACCEPTANCE_TABLE):
        if row["replacement_required"] != "true":
            continue
        index = len(rows) + 1
        replacement = ROOT / "semantic_evidence_replacements" / row["certificate_area"] / f"{row['semantic_evidence_field']}_accepted_evidence_v01.json"
        rows.append(
            {
                "replacement_row_id": f"TCMBCDSEMREP01_{index:03d}",
                "source_acceptance_row_id": row["acceptance_row_id"],
                "certificate_area": row["certificate_area"],
                "checker_name": row["checker_name"],
                "semantic_evidence_field": row["semantic_evidence_field"],
                "rejected_candidate_artifact": row["candidate_evidence_artifact"],
                "required_replacement_artifact": rel(replacement),
                "required_semantic_assertion_value": "non-null boolean true/false with reasoned endpoint-blind proof trace",
                "required_acceptance_flags": "semantic_assertion_accepted=true; proof_claim_allowed=true; certificate_rule_executable may be evaluated only after all fields in the certificate family are accepted",
                "required_endpoint_blind_firewall": "cmb_endpoint_residuals_used=false; act_planck_likelihood_used=false; score_output_used=false; post_endpoint_tuning_used=false; dark_sector_verdict_used=false",
                "replacement_supplied": "false",
                "replacement_accepted": "false",
                "certificate_rule_executable_after_replacement": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "request_status": "SEMANTIC_EVIDENCE_REPLACEMENT_REQUESTED_NOT_SUPPLIED",
                "blocking_reason": "requires accepted endpoint-blind semantic assertion artifact replacing the candidate-only file",
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
        "report_id": "tau_cmb_certificate_semantic_evidence_replacement_request_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_acceptance_table": rel(ACCEPTANCE_TABLE),
        "input_acceptance_summary": rel(ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "replacement_request_rows": len(rows),
        "replacement_supplied_rows": 0,
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
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_REQUEST_DECLARED"
            if input_chain_clean() and len(rows) == 28
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_REQUEST_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_replacement_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Replacement Request v01

**Doc class:** semantic certificate evidence replacement request
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This request converts the rejected candidate evidence artifacts into a finite
replacement list. Each replacement must provide a non-null semantic assertion,
an endpoint-blind proof trace, and explicit acceptance/proof flags. This request
does not supply replacements, accept evidence, execute certificate rules, or
open scoring.

## Summary

```text
replacement_request_rows={summary["replacement_request_rows"]}
replacement_supplied_rows={summary["replacement_supplied_rows"]}
replacement_accepted_rows={summary["replacement_accepted_rows"]}
certificate_rule_executable_after_replacement_rows={summary["certificate_rule_executable_after_replacement_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB semantic evidence replacement request.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
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
