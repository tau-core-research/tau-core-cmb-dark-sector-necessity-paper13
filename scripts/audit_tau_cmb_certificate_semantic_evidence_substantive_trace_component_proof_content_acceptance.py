#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_v01_"
    "acceptance_audit_only_candidates_rejected_no_component_acceptance_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "proof_content_acceptance_row_id",
    "source_proof_content_supply_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "proof_content_artifact",
    "proof_content_artifact_supplied",
    "hash_matches",
    "endpoint_blind_proof_content",
    "proof_content_candidate_nonempty",
    "proof_content_has_substantive_verification",
    "proof_content_references_endpoint_data",
    "proof_content_accepted",
    "component_substantively_proven_after_audit",
    "component_accepted_after_audit",
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


def input_chain_clean() -> bool:
    if not SUPPLY_SUMMARY.exists():
        return False
    summary = load_json(SUPPLY_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_CANDIDATES_SUPPLIED_NOT_ACCEPTED"
        and summary.get("input_chain_clean") is True
        and summary.get("proof_content_supply_rows") == 128
        and summary.get("proof_content_supplied_rows") == 128
        and summary.get("hash_matched_rows") == 128
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def has_endpoint_data(payload: dict[str, Any]) -> bool:
    firewall = payload.get("endpoint_blind_firewall", {})
    return any(bool(firewall.get(key)) for key in [
        "cmb_endpoint_residuals_used",
        "act_planck_likelihood_used",
        "score_output_used",
        "post_endpoint_tuning_used",
        "dark_sector_verdict_used",
    ])


def has_substantive_verification(payload: dict[str, Any]) -> bool:
    return (
        payload.get("artifact_status") == "TRACE_COMPONENT_PROOF_CONTENT_ACCEPTED_SUBSTANTIVE"
        and payload.get("component_substantively_proven_after_supply") is True
        and payload.get("component_accepted_after_supply") is True
    )


def audit_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("proof-content supply summary is not clean")
    rows: list[dict[str, str]] = []
    for supply in read_csv(SUPPLY_TABLE):
        index = len(rows) + 1
        artifact = ROOT / supply["proof_content_artifact"]
        payload = load_json(artifact) if artifact.exists() else {}
        substantive = has_substantive_verification(payload)
        endpoint_data = has_endpoint_data(payload)
        base_ok = (
            supply["proof_content_artifact_supplied"] == "true"
            and supply["hash_matches"] == "true"
            and supply["endpoint_blind_proof_content"] == "true"
            and supply["proof_content_candidate_nonempty"] == "true"
            and not endpoint_data
        )
        accepted = base_ok and substantive
        rows.append(
            {
                "proof_content_acceptance_row_id": f"TCMBCDSEMPCACC01_{index:03d}",
                "source_proof_content_supply_row_id": supply["proof_content_supply_row_id"],
                "certificate_area": supply["certificate_area"],
                "checker_name": supply["checker_name"],
                "semantic_evidence_field": supply["semantic_evidence_field"],
                "trace_component_name": supply["trace_component_name"],
                "proof_content_artifact": supply["proof_content_artifact"],
                "proof_content_artifact_supplied": supply["proof_content_artifact_supplied"],
                "hash_matches": supply["hash_matches"],
                "endpoint_blind_proof_content": supply["endpoint_blind_proof_content"],
                "proof_content_candidate_nonempty": supply["proof_content_candidate_nonempty"],
                "proof_content_has_substantive_verification": str(substantive).lower(),
                "proof_content_references_endpoint_data": str(endpoint_data).lower(),
                "proof_content_accepted": str(accepted).lower(),
                "component_substantively_proven_after_audit": str(accepted).lower(),
                "component_accepted_after_audit": str(accepted).lower(),
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
                    "TRACE_COMPONENT_PROOF_CONTENT_ACCEPTED"
                    if accepted
                    else "TRACE_COMPONENT_PROOF_CONTENT_REJECTED_SUBSTANTIVE_VERIFICATION_REQUIRED"
                ),
                "blocking_reason": (
                    "accepted endpoint-blind substantive verification present"
                    if accepted
                    else "candidate content is supplied and endpoint-blind, but does not mark or demonstrate accepted substantive verification"
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
    accepted = sum(row["proof_content_accepted"] == "true" for row in rows)
    rejected = len(rows) - accepted
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_proof_content_supply_table": rel(SUPPLY_TABLE),
        "input_proof_content_supply_summary": rel(SUPPLY_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "proof_content_acceptance_rows": len(rows),
        "proof_content_artifact_supplied_rows": sum(row["proof_content_artifact_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_proof_content_rows": sum(row["endpoint_blind_proof_content"] == "true" for row in rows),
        "proof_content_candidate_nonempty_rows": sum(row["proof_content_candidate_nonempty"] == "true" for row in rows),
        "proof_content_has_substantive_verification_rows": sum(row["proof_content_has_substantive_verification"] == "true" for row in rows),
        "proof_content_references_endpoint_data_rows": sum(row["proof_content_references_endpoint_data"] == "true" for row in rows),
        "proof_content_accepted_rows": accepted,
        "proof_content_rejected_rows": rejected,
        "component_substantively_proven_after_audit_rows": accepted,
        "component_accepted_after_audit_rows": accepted,
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
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_ACCEPTANCE_AUDITED_REJECTED_SUBSTANTIVE_VERIFICATION_REQUIRED"
            if input_chain_clean() and len(rows) == 128 and accepted == 0
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Proof Content Acceptance Audit v01

**Doc class:** semantic certificate evidence proof-content acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether supplied proof-content candidates can be promoted into
accepted substantive trace-component proof content. Candidate content is not
accepted unless it carries accepted endpoint-blind substantive verification.

## Summary

```text
proof_content_acceptance_rows={summary["proof_content_acceptance_rows"]}
proof_content_artifact_supplied_rows={summary["proof_content_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
endpoint_blind_proof_content_rows={summary["endpoint_blind_proof_content_rows"]}
proof_content_candidate_nonempty_rows={summary["proof_content_candidate_nonempty_rows"]}
proof_content_has_substantive_verification_rows={summary["proof_content_has_substantive_verification_rows"]}
proof_content_accepted_rows={summary["proof_content_accepted_rows"]}
proof_content_rejected_rows={summary["proof_content_rejected_rows"]}
component_accepted_after_audit_rows={summary["component_accepted_after_audit_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB trace-component proof-content acceptance.")
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
