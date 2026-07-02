#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_v01.csv"
REQUEST_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_v01_"
    "proof_content_candidate_supplied_not_accepted_no_component_acceptance_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "proof_content_supply_row_id",
    "source_proof_content_request_row_id",
    "source_component_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "rejected_component_artifact",
    "proof_content_artifact",
    "proof_content_hash_artifact",
    "proof_content_artifact_supplied",
    "hash_supplied",
    "hash_matches",
    "endpoint_blind_proof_content",
    "proof_content_supplied",
    "proof_content_candidate_nonempty",
    "required_acceptance_flags_repeated",
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not REQUEST_SUMMARY.exists():
        return False
    summary = load_json(REQUEST_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_REQUEST_DECLARED"
        and summary.get("input_chain_clean") is True
        and summary.get("proof_content_request_rows") == 128
        and summary.get("proof_content_requested_rows") == 128
        and summary.get("proof_content_supplied_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def proof_content_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "artifact_id": row["proof_content_request_row_id"],
        "artifact_status": "TRACE_COMPONENT_PROOF_CONTENT_CANDIDATE_SUPPLIED_NOT_ACCEPTED",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "semantic_evidence_field": row["semantic_evidence_field"],
        "trace_component_name": row["trace_component_name"],
        "rejected_component_artifact": row["rejected_component_artifact"],
        "proof_content_role": (
            "Endpoint-blind candidate proof content for a previously rejected trace component. "
            "It is supplied so that a later acceptance audit has concrete material to inspect."
        ),
        "substantive_content_candidate": {
            "object_to_verify": row["trace_component_name"],
            "local_verification_standard": row["required_proof_content"],
            "acceptance_flags_required": row["required_acceptance_flags"],
            "minimal_checks_expected": [
                "the referenced component artifact exists and is the component named by this row",
                "the component claim is checked using only upstream/domain material",
                "endpoint residuals, score outputs, likelihood deltas, and dark-sector verdicts are absent",
                "the component can be replayed as a local premise for the named checker",
                "the proof content states its dependency boundary and known non-claims",
            ],
            "non_claims": [
                "this candidate does not prove the component",
                "this candidate does not accept the component",
                "this candidate does not accept the trace",
                "this candidate does not execute or pass a certificate",
                "this candidate does not open physical R_CMB, score, likelihood, or verdict",
            ],
        },
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "proof_content_supplied": True,
        "proof_content_candidate_nonempty": True,
        "component_substantively_proven_after_supply": False,
        "component_accepted_after_supply": False,
        "trace_accepted_after_component": False,
        "semantic_assertion_acceptance_allowed": False,
        "certificate_rule_executable_after_component": False,
        "certificate_passed": False,
        "domain_object_accepted": False,
        "physical_R_CMB_materialized": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_step": "audit supplied proof-content candidates for substantive component acceptance",
    }


def supply_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("proof-content request summary is not clean")
    rows: list[dict[str, str]] = []
    for request in read_csv(REQUEST_TABLE):
        if request["proof_content_requested"] != "true":
            continue
        index = len(rows) + 1
        artifact = ROOT / request["required_proof_content_artifact"]
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, proof_content_payload(request))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "proof_content_supplied": True,
                    "component_substantively_proven_after_supply": False,
                    "component_accepted_after_supply": False,
                    "certificate_passed": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_supplied = hash_artifact.exists()
        hash_matches = hash_supplied and supplied and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        content_supplied = payload.get("proof_content_supplied") is True
        candidate_nonempty = bool(payload.get("substantive_content_candidate"))
        rows.append(
            {
                "proof_content_supply_row_id": f"TCMBCDSEMPCSUP01_{index:03d}",
                "source_proof_content_request_row_id": request["proof_content_request_row_id"],
                "source_component_acceptance_row_id": request["source_component_acceptance_row_id"],
                "certificate_area": request["certificate_area"],
                "checker_name": request["checker_name"],
                "semantic_evidence_field": request["semantic_evidence_field"],
                "trace_component_name": request["trace_component_name"],
                "rejected_component_artifact": request["rejected_component_artifact"],
                "proof_content_artifact": rel(artifact),
                "proof_content_hash_artifact": rel(hash_artifact),
                "proof_content_artifact_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "endpoint_blind_proof_content": "true",
                "proof_content_supplied": str(content_supplied).lower(),
                "proof_content_candidate_nonempty": str(candidate_nonempty).lower(),
                "required_acceptance_flags_repeated": request["required_acceptance_flags"],
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
                "supply_status": (
                    "TRACE_COMPONENT_PROOF_CONTENT_CANDIDATE_SUPPLIED_NOT_ACCEPTED"
                    if supplied and hash_matches and content_supplied and candidate_nonempty
                    else "TRACE_COMPONENT_PROOF_CONTENT_SUPPLY_BLOCKED"
                ),
                "blocking_reason": (
                    "proof-content candidate exists and is hash-bound; substantive acceptance remains downstream"
                    if supplied and hash_matches and content_supplied and candidate_nonempty
                    else "requires proof-content artifact, matching hash, and nonempty candidate content"
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
    all_supplied = len(rows) > 0 and all(
        row["proof_content_artifact_supplied"] == "true"
        and row["hash_matches"] == "true"
        and row["proof_content_supplied"] == "true"
        and row["proof_content_candidate_nonempty"] == "true"
        for row in rows
    )
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_proof_content_request_table": rel(REQUEST_TABLE),
        "input_proof_content_request_summary": rel(REQUEST_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "proof_content_supply_rows": len(rows),
        "proof_content_artifact_supplied_rows": sum(row["proof_content_artifact_supplied"] == "true" for row in rows),
        "hash_supplied_rows": sum(row["hash_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_proof_content_rows": sum(row["endpoint_blind_proof_content"] == "true" for row in rows),
        "proof_content_supplied_rows": sum(row["proof_content_supplied"] == "true" for row in rows),
        "proof_content_candidate_nonempty_rows": sum(row["proof_content_candidate_nonempty"] == "true" for row in rows),
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
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_CANDIDATES_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean() and all_supplied
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Proof Content Supply v01

**Doc class:** semantic certificate evidence trace component proof-content supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This supply step materializes endpoint-blind proof-content candidates for the
finite 128-row trace-component worklist. It does not accept any proof content,
component, trace, certificate, domain object, physical readout, score,
likelihood, or dark-sector verdict.

## Summary

```text
proof_content_supply_rows={summary["proof_content_supply_rows"]}
proof_content_artifact_supplied_rows={summary["proof_content_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
endpoint_blind_proof_content_rows={summary["endpoint_blind_proof_content_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB trace-component proof-content candidates.")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(write_artifacts=args.write_artifacts)
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
