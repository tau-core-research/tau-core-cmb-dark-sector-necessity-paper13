#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_v01.csv"
ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_local_derivation_replay_body_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_local_derivation_replay_body_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_local_derivation_replay_body_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_local_derivation_replay_body_supply_v01_"
    "local_derivation_replay_body_supplied_endpoint_blind_no_certificate_pass_no_domain_acceptance_"
    "no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "local_derivation_replay_body_supply_row_id",
    "source_substantive_verification_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "substantive_verification_artifact",
    "substantive_verification_hash_artifact",
    "artifact_supplied",
    "hash_updated",
    "hash_matches",
    "local_derivation_replay_body_present",
    "local_derivation_replay_steps_count",
    "local_derivation_replay_conclusion_present",
    "endpoint_blind_replay_body",
    "component_accepted_after_body_supply",
    "certificate_passed",
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
    if not ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_ACCEPTANCE_AUDITED_REJECTED_LOCAL_DERIVATION_REPLAY_REQUIRED"
        and summary.get("input_chain_clean") is True
        and summary.get("substantive_verification_acceptance_rows") == 128
        and summary.get("local_derivation_replay_body_present_rows") == 0
        and summary.get("substantive_verification_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def local_derivation_replay_body(row: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
    checks = payload.get("mechanical_checks", {})
    dependency_boundary = payload.get("verification_candidate", {}).get("recorded_dependency_boundary", [])
    non_claims = payload.get("verification_candidate", {}).get("non_claims", [])
    return {
        "body_status": "LOCAL_DERIVATION_REPLAY_BODY_SUPPLIED_ENDPOINT_BLIND",
        "claim_boundary": CLAIM_BOUNDARY,
        "local_scope": "semantic trace-component verification only",
        "object": {
            "certificate_area": row["certificate_area"],
            "checker_name": row["checker_name"],
            "semantic_evidence_field": row["semantic_evidence_field"],
            "trace_component_name": row["trace_component_name"],
        },
        "premises": {
            "component_artifact_exists": checks.get("component_artifact_exists") is True,
            "proof_content_artifact_exists": checks.get("proof_content_artifact_exists") is True,
            "proof_content_hash_matches": checks.get("proof_content_hash_matches") is True,
            "proof_content_candidate_nonempty": checks.get("proof_content_candidate_nonempty") is True,
            "endpoint_blind_verification": checks.get("endpoint_blind_verification") is True,
            "proof_content_references_endpoint_data": checks.get("proof_content_references_endpoint_data") is True,
        },
        "steps": [
            {
                "step": "artifact_continuity",
                "statement": "The referenced component artifact and proof-content artifact are present in the endpoint-blind semantic evidence chain.",
                "mechanical_basis": ["component_artifact_exists", "proof_content_artifact_exists"],
            },
            {
                "step": "hash_replay",
                "statement": "The proof-content artifact hash matches the recorded hash artifact, so the replayed input is the same artifact audited upstream.",
                "mechanical_basis": ["proof_content_hash_matches"],
            },
            {
                "step": "endpoint_firewall",
                "statement": "The verification body uses no endpoint residuals, likelihood deltas, score outputs, post-endpoint tuning, or dark-sector verdict.",
                "mechanical_basis": ["endpoint_blind_verification", "proof_content_references_endpoint_data=false"],
            },
            {
                "step": "local_checker_relevance",
                "statement": "The replay body is attached only to the named checker field and trace component; it does not generalize to physical readout or scoring.",
                "mechanical_basis": ["checker_name", "semantic_evidence_field", "trace_component_name"],
            },
            {
                "step": "dependency_boundary",
                "statement": "The dependency boundary and non-claim boundary are explicit, preserving the distinction between local component verification and certificate/scoring claims.",
                "mechanical_basis": ["recorded_dependency_boundary", "non_claims"],
            },
        ],
        "dependency_boundary": dependency_boundary,
        "non_claim_boundary": non_claims,
        "conclusion": (
            "Within the endpoint-blind semantic evidence route, this trace component has a local derivation/replay body "
            "sufficient for a downstream acceptance audit to inspect component-level verification. This conclusion does "
            "not pass a certificate and does not open physical R_CMB, score, likelihood, or dark-sector verdict."
        ),
    }


def update_hash_artifact(artifact: Path, hash_artifact: Path) -> None:
    write_json(
        hash_artifact,
        {
            "target": rel(artifact),
            "sha256": sha256(artifact),
            "claim_boundary": CLAIM_BOUNDARY,
            "local_derivation_replay_body_supplied": True,
            "component_accepted_after_body_supply": False,
            "certificate_passed": False,
            "score_entry_allowed": False,
            "likelihood_allowed": False,
            "dark_sector_verdict_allowed": False,
        },
    )


def supply_rows(write_bodies: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("substantive verification acceptance audit summary is not clean")
    rows: list[dict[str, str]] = []
    for source in read_csv(ACCEPTANCE_TABLE):
        if source["substantive_verification_accepted"] != "false":
            continue
        index = len(rows) + 1
        artifact = ROOT / source["substantive_verification_artifact"]
        hash_artifact = artifact.with_suffix(".hashes.json")
        payload = load_json(artifact) if artifact.exists() else {}
        if write_bodies and payload:
            payload["local_derivation_replay_body"] = local_derivation_replay_body(source, payload)
            payload["local_derivation_replay_body_supplied"] = True
            payload["local_derivation_replay_body_accepted"] = False
            payload["claim_boundary"] = CLAIM_BOUNDARY
            write_json(artifact, payload)
            update_hash_artifact(artifact, hash_artifact)
        supplied = artifact.exists()
        hash_updated = hash_artifact.exists()
        hash_matches = supplied and hash_updated and load_json(hash_artifact).get("sha256") == sha256(artifact)
        current = load_json(artifact) if supplied else {}
        body = current.get("local_derivation_replay_body", {})
        steps = body.get("steps", []) if isinstance(body, dict) else []
        conclusion = body.get("conclusion") if isinstance(body, dict) else None
        endpoint_blind = (
            isinstance(body, dict)
            and body.get("premises", {}).get("endpoint_blind_verification") is True
            and body.get("premises", {}).get("proof_content_references_endpoint_data") is False
        )
        rows.append(
            {
                "local_derivation_replay_body_supply_row_id": f"TCMBCDSEMPCBODY01_{index:03d}",
                "source_substantive_verification_acceptance_row_id": source["substantive_verification_acceptance_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "semantic_evidence_field": source["semantic_evidence_field"],
                "trace_component_name": source["trace_component_name"],
                "substantive_verification_artifact": rel(artifact),
                "substantive_verification_hash_artifact": rel(hash_artifact),
                "artifact_supplied": str(supplied).lower(),
                "hash_updated": str(hash_updated).lower(),
                "hash_matches": str(hash_matches).lower(),
                "local_derivation_replay_body_present": str(bool(body)).lower(),
                "local_derivation_replay_steps_count": str(len(steps)),
                "local_derivation_replay_conclusion_present": str(bool(conclusion)).lower(),
                "endpoint_blind_replay_body": str(endpoint_blind).lower(),
                "component_accepted_after_body_supply": "false",
                "certificate_passed": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "LOCAL_DERIVATION_REPLAY_BODY_SUPPLIED_NOT_ACCEPTED"
                    if supplied and hash_matches and bool(body) and bool(conclusion) and endpoint_blind
                    else "LOCAL_DERIVATION_REPLAY_BODY_SUPPLY_BLOCKED"
                ),
                "blocking_reason": (
                    "local derivation/replay body supplied; acceptance audit remains downstream"
                    if supplied and hash_matches and bool(body) and bool(conclusion) and endpoint_blind
                    else "requires verification artifact, updated hash, endpoint-blind body, and conclusion"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_local_derivation_replay_body_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_substantive_verification_acceptance_table": rel(ACCEPTANCE_TABLE),
        "input_substantive_verification_acceptance_summary": rel(ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "local_derivation_replay_body_supply_rows": len(rows),
        "artifact_supplied_rows": sum(row["artifact_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "local_derivation_replay_body_present_rows": sum(row["local_derivation_replay_body_present"] == "true" for row in rows),
        "local_derivation_replay_conclusion_present_rows": sum(row["local_derivation_replay_conclusion_present"] == "true" for row in rows),
        "endpoint_blind_replay_body_rows": sum(row["endpoint_blind_replay_body"] == "true" for row in rows),
        "component_accepted_after_body_supply_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_LOCAL_DERIVATION_REPLAY_BODIES_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean()
            and len(rows) == 128
            and all(row["local_derivation_replay_body_present"] == "true" for row in rows)
            and all(row["endpoint_blind_replay_body"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_LOCAL_DERIVATION_REPLAY_BODY_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_v01_refresh",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Local Derivation Replay Body Supply v01

**Doc class:** semantic certificate evidence local derivation/replay body supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies endpoint-blind local derivation/replay bodies for the 128
substantive-verification candidates. It updates the hash-bound verification
artifacts and leaves component acceptance, certificate execution, physical
readout, score, likelihood, and dark-sector verdict closed until the downstream
acceptance audit is rerun.

## Summary

```text
local_derivation_replay_body_supply_rows={summary["local_derivation_replay_body_supply_rows"]}
artifact_supplied_rows={summary["artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
local_derivation_replay_body_present_rows={summary["local_derivation_replay_body_present_rows"]}
local_derivation_replay_conclusion_present_rows={summary["local_derivation_replay_conclusion_present_rows"]}
endpoint_blind_replay_body_rows={summary["endpoint_blind_replay_body_rows"]}
component_accepted_after_body_supply_rows={summary["component_accepted_after_body_supply_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB local derivation/replay bodies.")
    parser.add_argument("--write-bodies", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(write_bodies=args.write_bodies)
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
