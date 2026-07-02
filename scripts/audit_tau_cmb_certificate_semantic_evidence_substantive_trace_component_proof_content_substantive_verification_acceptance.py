#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_v01_"
    "acceptance_audit_allows_component_level_acceptance_only_no_trace_acceptance_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "substantive_verification_acceptance_row_id",
    "source_substantive_verification_supply_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "substantive_verification_artifact",
    "hash_matches",
    "component_artifact_exists",
    "proof_content_artifact_exists",
    "proof_content_hash_matches",
    "endpoint_blind_verification",
    "mechanical_checks_recorded",
    "local_derivation_replay_body_present",
    "dependency_boundary_present",
    "non_claim_boundary_present",
    "substantive_verification_accepted",
    "component_substantively_proven_after_verification",
    "component_accepted_after_verification",
    "trace_accepted_after_component",
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
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_CANDIDATES_SUPPLIED_NOT_ACCEPTED"
        and summary.get("input_chain_clean") is True
        and summary.get("substantive_verification_supply_rows") == 128
        and summary.get("substantive_verification_artifact_supplied_rows") == 128
        and summary.get("hash_matched_rows") == 128
        and summary.get("mechanical_checks_recorded_rows") == 128
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def local_derivation_replay_body_present(payload: dict[str, Any]) -> bool:
    body = payload.get("local_derivation_replay_body")
    return isinstance(body, dict) and bool(body.get("steps")) and bool(body.get("conclusion"))


def dependency_boundary_present(payload: dict[str, Any]) -> bool:
    boundary = payload.get("verification_candidate", {}).get("recorded_dependency_boundary")
    return isinstance(boundary, list) and len(boundary) > 0


def non_claim_boundary_present(payload: dict[str, Any]) -> bool:
    non_claims = payload.get("verification_candidate", {}).get("non_claims")
    return isinstance(non_claims, list) and len(non_claims) >= 5


def audit_rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("substantive verification supply summary is not clean")
    rows: list[dict[str, str]] = []
    for source in read_csv(SUPPLY_TABLE):
        index = len(rows) + 1
        artifact = ROOT / source["substantive_verification_artifact"]
        payload = load_json(artifact) if artifact.exists() else {}
        local_body = local_derivation_replay_body_present(payload)
        dependency_boundary = dependency_boundary_present(payload)
        non_claim_boundary = non_claim_boundary_present(payload)
        mechanical_ok = (
            source["hash_matches"] == "true"
            and source["component_artifact_exists"] == "true"
            and source["proof_content_artifact_exists"] == "true"
            and source["proof_content_hash_matches"] == "true"
            and source["endpoint_blind_verification"] == "true"
            and source["mechanical_checks_recorded"] == "true"
        )
        accepted = mechanical_ok and local_body and dependency_boundary and non_claim_boundary
        rows.append(
            {
                "substantive_verification_acceptance_row_id": f"TCMBCDSEMPCVERACC01_{index:03d}",
                "source_substantive_verification_supply_row_id": source["substantive_verification_supply_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "semantic_evidence_field": source["semantic_evidence_field"],
                "trace_component_name": source["trace_component_name"],
                "substantive_verification_artifact": source["substantive_verification_artifact"],
                "hash_matches": source["hash_matches"],
                "component_artifact_exists": source["component_artifact_exists"],
                "proof_content_artifact_exists": source["proof_content_artifact_exists"],
                "proof_content_hash_matches": source["proof_content_hash_matches"],
                "endpoint_blind_verification": source["endpoint_blind_verification"],
                "mechanical_checks_recorded": source["mechanical_checks_recorded"],
                "local_derivation_replay_body_present": str(local_body).lower(),
                "dependency_boundary_present": str(dependency_boundary).lower(),
                "non_claim_boundary_present": str(non_claim_boundary).lower(),
                "substantive_verification_accepted": str(accepted).lower(),
                "component_substantively_proven_after_verification": str(accepted).lower(),
                "component_accepted_after_verification": str(accepted).lower(),
                "trace_accepted_after_component": "false",
                "certificate_rule_executable_after_component": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "SUBSTANTIVE_VERIFICATION_ACCEPTED"
                    if accepted
                    else "SUBSTANTIVE_VERIFICATION_REJECTED_LOCAL_DERIVATION_REPLAY_BODY_REQUIRED"
                ),
                "blocking_reason": (
                    "accepted endpoint-blind substantive verification with local derivation/replay body"
                    if accepted
                    else "mechanical checks are recorded, but local derivation/replay body is not present or not accepted"
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
    accepted = sum(row["substantive_verification_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_substantive_verification_supply_table": rel(SUPPLY_TABLE),
        "input_substantive_verification_supply_summary": rel(SUPPLY_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "substantive_verification_acceptance_rows": len(rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "component_artifact_exists_rows": sum(row["component_artifact_exists"] == "true" for row in rows),
        "proof_content_artifact_exists_rows": sum(row["proof_content_artifact_exists"] == "true" for row in rows),
        "proof_content_hash_matches_rows": sum(row["proof_content_hash_matches"] == "true" for row in rows),
        "endpoint_blind_verification_rows": sum(row["endpoint_blind_verification"] == "true" for row in rows),
        "mechanical_checks_recorded_rows": sum(row["mechanical_checks_recorded"] == "true" for row in rows),
        "local_derivation_replay_body_present_rows": sum(row["local_derivation_replay_body_present"] == "true" for row in rows),
        "dependency_boundary_present_rows": sum(row["dependency_boundary_present"] == "true" for row in rows),
        "non_claim_boundary_present_rows": sum(row["non_claim_boundary_present"] == "true" for row in rows),
        "substantive_verification_accepted_rows": accepted,
        "substantive_verification_rejected_rows": len(rows) - accepted,
        "component_substantively_proven_after_verification_rows": accepted,
        "component_accepted_after_verification_rows": accepted,
        "trace_accepted_after_component_rows": 0,
        "certificate_rule_executable_after_component_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_ACCEPTANCE_AUDITED_REJECTED_LOCAL_DERIVATION_REPLAY_REQUIRED"
            if input_chain_clean() and len(rows) == 128 and accepted == 0
            else (
                "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_ACCEPTED_COMPONENT_LEVEL_ONLY"
                if input_chain_clean() and len(rows) == 128 and accepted == 128
                else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
            )
        ),
        "next_minimal_unblock": (
            "tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_v01"
            if accepted == 128
            else "tau_cmb_certificate_semantic_evidence_substantive_trace_component_local_derivation_replay_body_supply_v01"
        ),
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Proof Content Substantive Verification Acceptance Audit v01

**Doc class:** semantic certificate evidence substantive verification acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit separates mechanical readiness, component-level acceptance, and
downstream certificate/scoring claims. When local derivation/replay bodies are
present, this audit may accept trace components only; trace acceptance,
certificate execution, physical readout, scoring, likelihood, and verdict remain
closed.

## Summary

```text
substantive_verification_acceptance_rows={summary["substantive_verification_acceptance_rows"]}
mechanical_checks_recorded_rows={summary["mechanical_checks_recorded_rows"]}
endpoint_blind_verification_rows={summary["endpoint_blind_verification_rows"]}
local_derivation_replay_body_present_rows={summary["local_derivation_replay_body_present_rows"]}
substantive_verification_accepted_rows={summary["substantive_verification_accepted_rows"]}
component_accepted_after_verification_rows={summary["component_accepted_after_verification_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB substantive verification acceptance.")
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
