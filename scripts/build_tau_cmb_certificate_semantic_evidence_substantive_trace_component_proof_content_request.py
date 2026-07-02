#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_v01.csv"
ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_v01_"
    "proof_content_request_only_no_content_supplied_no_component_acceptance_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "proof_content_request_row_id",
    "source_component_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "rejected_component_artifact",
    "required_proof_content_artifact",
    "required_proof_content",
    "required_acceptance_flags",
    "required_endpoint_blind_firewall",
    "proof_content_requested",
    "proof_content_supplied",
    "component_substantively_proven_after_supply",
    "component_accepted_after_supply",
    "trace_accepted_after_component",
    "semantic_assertion_acceptance_allowed",
    "certificate_rule_executable_after_component",
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


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


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
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_ACCEPTANCE_AUDITED_REJECTED_SUBSTANTIVE_PROOF_REQUIRED"
        and summary.get("component_acceptance_rows", 0) > 0
        and summary.get("component_accepted_rows") == 0
        and summary.get("component_substantively_proven_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(ACCEPTANCE_TABLE):
        if row["component_accepted"] != "false":
            continue
        index = len(rows) + 1
        artifact = (
            ROOT
            / "semantic_evidence_trace_component_proof_content"
            / row["certificate_area"]
            / row["semantic_evidence_field"]
            / f"{slug(row['trace_component_name'])}_proof_content_v01.json"
        )
        rows.append(
            {
                "proof_content_request_row_id": f"TCMBCDSEMPCREQ01_{index:03d}",
                "source_component_acceptance_row_id": row["component_acceptance_row_id"],
                "certificate_area": row["certificate_area"],
                "checker_name": row["checker_name"],
                "semantic_evidence_field": row["semantic_evidence_field"],
                "trace_component_name": row["trace_component_name"],
                "rejected_component_artifact": row["component_artifact"],
                "required_proof_content_artifact": rel(artifact),
                "required_proof_content": "endpoint-blind substantive proof content that verifies this trace component without endpoint residuals, score outputs, likelihood deltas, or dark-sector verdicts",
                "required_acceptance_flags": "component_substantively_proven=true; component_accepted=true only after proof-content audit",
                "required_endpoint_blind_firewall": "cmb_endpoint_residuals_used=false; act_planck_likelihood_used=false; score_output_used=false; post_endpoint_tuning_used=false; dark_sector_verdict_used=false",
                "proof_content_requested": "true",
                "proof_content_supplied": "false",
                "component_substantively_proven_after_supply": "false",
                "component_accepted_after_supply": "false",
                "trace_accepted_after_component": "false",
                "semantic_assertion_acceptance_allowed": "false",
                "certificate_rule_executable_after_component": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "request_status": "TRACE_COMPONENT_PROOF_CONTENT_REQUESTED_NOT_SUPPLIED",
                "blocking_reason": "requires endpoint-blind substantive proof content before component acceptance can be reconsidered",
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
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_component_acceptance_table": rel(ACCEPTANCE_TABLE),
        "input_component_acceptance_summary": rel(ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "proof_content_request_rows": len(rows),
        "proof_content_requested_rows": sum(row["proof_content_requested"] == "true" for row in rows),
        "proof_content_supplied_rows": 0,
        "component_substantively_proven_after_supply_rows": 0,
        "component_accepted_after_supply_rows": 0,
        "trace_accepted_after_component_rows": 0,
        "semantic_assertion_acceptance_allowed_rows": 0,
        "certificate_rule_executable_after_component_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_REQUEST_DECLARED"
            if input_chain_clean() and len(rows) > 0
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_REQUEST_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Proof Content Request v01

**Doc class:** semantic certificate evidence trace component proof-content request
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This request converts rejected trace-component drafts into a finite proof-content
worklist. It does not supply proof content, accept components, accept traces,
execute certificates, or open scoring.

## Summary

```text
proof_content_request_rows={summary["proof_content_request_rows"]}
proof_content_requested_rows={summary["proof_content_requested_rows"]}
proof_content_supplied_rows={summary["proof_content_supplied_rows"]}
component_substantively_proven_after_supply_rows={summary["component_substantively_proven_after_supply_rows"]}
component_accepted_after_supply_rows={summary["component_accepted_after_supply_rows"]}
trace_accepted_after_component_rows={summary["trace_accepted_after_component_rows"]}
certificate_rule_executable_after_component_rows={summary["certificate_rule_executable_after_component_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB trace component proof-content request.")
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
