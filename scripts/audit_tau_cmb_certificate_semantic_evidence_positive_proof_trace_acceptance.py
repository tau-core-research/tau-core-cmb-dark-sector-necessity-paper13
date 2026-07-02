#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_v01.csv"
TRACE_AUDIT = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_v01_"
    "draft_traces_rejected_until_substantive_components_proven_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "acceptance_row_id",
    "source_trace_supply_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "positive_trace_artifact",
    "artifact_present",
    "hash_present",
    "hash_matches",
    "endpoint_blind_trace",
    "trace_components_declared",
    "trace_components_substantively_proven",
    "trace_accepted",
    "semantic_assertion_acceptance_allowed",
    "proof_claim_allowed",
    "certificate_rule_executable_after_trace",
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
    if not TRACE_AUDIT.exists():
        return False
    audit = load_json(TRACE_AUDIT)
    return (
        audit.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_SUPPLY_AUDITED_DRAFTS_NOT_ACCEPTED"
        and audit.get("failed_rows") == 0
        and audit.get("trace_supply_rows") == 28
        and audit.get("positive_trace_supplied_rows") == 28
        and audit.get("trace_accepted_rows") == 0
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def hash_matches(artifact: Path, hash_artifact: Path) -> bool:
    if not artifact.exists() or not hash_artifact.exists():
        return False
    return load_json(hash_artifact).get("sha256") == sha256(artifact)


def components_substantively_proven(payload: dict[str, Any]) -> bool:
    rows = payload.get("trace_component_status", [])
    return bool(rows) and all(item.get("status") == "SUBSTANTIVELY_PROVEN" for item in rows)


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(TRACE_TABLE), start=1):
        artifact = ROOT / source["positive_trace_artifact"]
        hash_artifact = ROOT / source["positive_trace_hash_artifact"]
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
        declared = bool(payload.get("required_trace_components"))
        substantive = components_substantively_proven(payload)
        accepted = present and hash_ok and endpoint_blind and declared and substantive and payload.get("trace_accepted") is True
        rows.append(
            {
                "acceptance_row_id": f"TCMBCDSEMPTRACC01_{index:03d}",
                "source_trace_supply_row_id": source["trace_supply_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "semantic_evidence_field": source["semantic_evidence_field"],
                "positive_trace_artifact": source["positive_trace_artifact"],
                "artifact_present": str(present).lower(),
                "hash_present": str(hash_present).lower(),
                "hash_matches": str(hash_ok).lower(),
                "endpoint_blind_trace": str(endpoint_blind).lower(),
                "trace_components_declared": str(declared).lower(),
                "trace_components_substantively_proven": str(substantive).lower(),
                "trace_accepted": str(accepted).lower(),
                "semantic_assertion_acceptance_allowed": "false",
                "proof_claim_allowed": "false",
                "certificate_rule_executable_after_trace": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "POSITIVE_PROOF_TRACE_ACCEPTED_FOR_SEMANTIC_ASSERTION_REVIEW_ONLY"
                    if accepted
                    else "POSITIVE_PROOF_TRACE_REJECTED_SUBSTANTIVE_COMPONENTS_REQUIRED"
                ),
                "blocking_reason": (
                    "trace accepted only for semantic assertion review; certificate execution remains downstream"
                    if accepted
                    else "draft trace components are declared but not substantively proven or accepted"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_trace_supply_table": rel(TRACE_TABLE),
        "input_trace_supply_audit": rel(TRACE_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "acceptance_rows": len(rows),
        "artifact_present_rows": sum(row["artifact_present"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_trace_rows": sum(row["endpoint_blind_trace"] == "true" for row in rows),
        "trace_components_declared_rows": sum(row["trace_components_declared"] == "true" for row in rows),
        "trace_components_substantively_proven_rows": sum(row["trace_components_substantively_proven"] == "true" for row in rows),
        "trace_accepted_rows": sum(row["trace_accepted"] == "true" for row in rows),
        "semantic_assertion_acceptance_allowed_rows": 0,
        "proof_claim_allowed_rows": 0,
        "certificate_rule_executable_after_trace_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_ACCEPTANCE_AUDITED_REJECTED_SUBSTANTIVE_COMPONENTS_REQUIRED"
            if input_chain_clean() and len(rows) == 28 and all(row["trace_accepted"] == "false" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_ACCEPTANCE_AUDIT_PARTIAL_OR_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Positive Proof Trace Acceptance Audit v01

**Doc class:** semantic certificate evidence positive proof trace acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the supplied draft positive traces can be accepted as
proof traces. Current traces are rejected because their components are declared
but not substantively proven.

## Summary

```text
acceptance_rows={summary["acceptance_rows"]}
artifact_present_rows={summary["artifact_present_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
endpoint_blind_trace_rows={summary["endpoint_blind_trace_rows"]}
trace_components_declared_rows={summary["trace_components_declared_rows"]}
trace_components_substantively_proven_rows={summary["trace_components_substantively_proven_rows"]}
trace_accepted_rows={summary["trace_accepted_rows"]}
semantic_assertion_acceptance_allowed_rows={summary["semantic_assertion_acceptance_allowed_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB positive proof trace acceptance.")
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
