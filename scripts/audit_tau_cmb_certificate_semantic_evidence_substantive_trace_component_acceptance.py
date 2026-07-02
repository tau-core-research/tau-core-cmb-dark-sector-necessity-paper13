#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMPONENT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_v01.csv"
COMPONENT_AUDIT = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_v01_"
    "component_drafts_rejected_until_substantive_proof_content_no_trace_acceptance_"
    "no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "component_acceptance_row_id",
    "source_component_supply_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "component_artifact",
    "artifact_present",
    "hash_present",
    "hash_matches",
    "endpoint_blind_component",
    "component_content_supplied",
    "component_substantively_proven",
    "component_accepted",
    "trace_accepted_after_component",
    "semantic_assertion_acceptance_allowed",
    "certificate_rule_executable_after_component",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not COMPONENT_AUDIT.exists():
        return False
    audit = load_json(COMPONENT_AUDIT)
    return (
        audit.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUPPLY_AUDITED_DRAFT_CONTENT_NOT_ACCEPTED"
        and audit.get("failed_rows") == 0
        and audit.get("component_supply_rows", 0) > 0
        and audit.get("component_accepted_rows") == 0
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def hash_matches(artifact: Path, hash_artifact: Path) -> bool:
    if not artifact.exists() or not hash_artifact.exists():
        return False
    return load_json(hash_artifact).get("sha256") == sha256(artifact)


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(COMPONENT_TABLE), start=1):
        artifact = ROOT / source["component_artifact"]
        hash_artifact = ROOT / source["component_hash_artifact"]
        payload = load_json(artifact) if artifact.exists() else {}
        present = artifact.exists()
        hash_present = hash_artifact.exists()
        hash_ok = hash_matches(artifact, hash_artifact)
        endpoint_blind = (
            payload.get("endpoint_blind_firewall", {}).get("cmb_endpoint_residuals_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("act_planck_likelihood_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("score_output_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("post_endpoint_tuning_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("dark_sector_verdict_used") is False
        )
        content = payload.get("component_content_supplied") is True
        substantive = payload.get("component_substantively_proven") is True
        accepted = present and hash_ok and endpoint_blind and content and substantive and payload.get("component_accepted") is True
        rows.append(
            {
                "component_acceptance_row_id": f"TCMBCDSEMCOMPACC01_{index:03d}",
                "source_component_supply_row_id": source["component_supply_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "semantic_evidence_field": source["semantic_evidence_field"],
                "trace_component_name": source["trace_component_name"],
                "component_artifact": source["component_artifact"],
                "artifact_present": str(present).lower(),
                "hash_present": str(hash_present).lower(),
                "hash_matches": str(hash_ok).lower(),
                "endpoint_blind_component": str(endpoint_blind).lower(),
                "component_content_supplied": str(content).lower(),
                "component_substantively_proven": str(substantive).lower(),
                "component_accepted": str(accepted).lower(),
                "trace_accepted_after_component": "false",
                "semantic_assertion_acceptance_allowed": "false",
                "certificate_rule_executable_after_component": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "TRACE_COMPONENT_ACCEPTED_FOR_TRACE_REVIEW_ONLY"
                    if accepted
                    else "TRACE_COMPONENT_REJECTED_SUBSTANTIVE_PROOF_REQUIRED"
                ),
                "blocking_reason": (
                    "component accepted only for trace review; trace/certificate execution remains downstream"
                    if accepted
                    else "component content is draft-only and not substantively proven/accepted"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_component_supply_table": rel(COMPONENT_TABLE),
        "input_component_supply_audit": rel(COMPONENT_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "component_acceptance_rows": len(rows),
        "artifact_present_rows": sum(row["artifact_present"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_component_rows": sum(row["endpoint_blind_component"] == "true" for row in rows),
        "component_content_supplied_rows": sum(row["component_content_supplied"] == "true" for row in rows),
        "component_substantively_proven_rows": sum(row["component_substantively_proven"] == "true" for row in rows),
        "component_accepted_rows": sum(row["component_accepted"] == "true" for row in rows),
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
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_ACCEPTANCE_AUDITED_REJECTED_SUBSTANTIVE_PROOF_REQUIRED"
            if input_chain_clean() and len(rows) > 0 and all(row["component_accepted"] == "false" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_ACCEPTANCE_AUDIT_PARTIAL_OR_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Acceptance Audit v01

**Doc class:** semantic certificate evidence trace component acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether trace-component draft content can be accepted as
substantive proof content. Current components are rejected because they are
draft-only and not marked as substantively proven.

## Summary

```text
component_acceptance_rows={summary["component_acceptance_rows"]}
artifact_present_rows={summary["artifact_present_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
endpoint_blind_component_rows={summary["endpoint_blind_component_rows"]}
component_content_supplied_rows={summary["component_content_supplied_rows"]}
component_substantively_proven_rows={summary["component_substantively_proven_rows"]}
component_accepted_rows={summary["component_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB substantive trace component acceptance.")
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
