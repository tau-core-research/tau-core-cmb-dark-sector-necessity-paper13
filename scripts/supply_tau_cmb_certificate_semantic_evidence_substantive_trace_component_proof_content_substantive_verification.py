#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_v01.csv"
ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_v01_"
    "substantive_verification_candidate_supplied_mechanical_checks_recorded_not_accepted_"
    "no_component_acceptance_no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "substantive_verification_supply_row_id",
    "source_proof_content_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "proof_content_artifact",
    "substantive_verification_artifact",
    "substantive_verification_hash_artifact",
    "substantive_verification_artifact_supplied",
    "hash_supplied",
    "hash_matches",
    "component_artifact_exists",
    "proof_content_artifact_exists",
    "proof_content_hash_matches",
    "endpoint_blind_verification",
    "mechanical_checks_recorded",
    "substantive_verification_candidate_supplied",
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
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_PROOF_CONTENT_ACCEPTANCE_AUDITED_REJECTED_SUBSTANTIVE_VERIFICATION_REQUIRED"
        and summary.get("input_chain_clean") is True
        and summary.get("proof_content_acceptance_rows") == 128
        and summary.get("proof_content_accepted_rows") == 0
        and summary.get("proof_content_rejected_rows") == 128
        and summary.get("proof_content_references_endpoint_data_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def proof_content_hash_matches(path: Path) -> bool:
    hash_path = path.with_suffix(".hashes.json")
    return path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(path)


def rejected_component_path(proof_content_path: Path) -> Path | None:
    if not proof_content_path.exists():
        return None
    payload = load_json(proof_content_path)
    component = payload.get("rejected_component_artifact")
    if not component:
        return None
    return ROOT / str(component)


def verification_artifact_for(row: dict[str, str]) -> Path:
    proof_path = Path(row["proof_content_artifact"])
    return ROOT / "semantic_evidence_trace_component_substantive_verifications" / proof_path.parent.relative_to("semantic_evidence_trace_component_proof_content") / proof_path.name.replace("_proof_content_v01.json", "_substantive_verification_v01.json")


def verification_payload(row: dict[str, str]) -> dict[str, Any]:
    proof_path = ROOT / row["proof_content_artifact"]
    component_path = rejected_component_path(proof_path)
    component_exists = bool(component_path and component_path.exists())
    proof_exists = proof_path.exists()
    proof_hash_ok = proof_content_hash_matches(proof_path)
    return {
        "artifact_id": row["proof_content_acceptance_row_id"],
        "artifact_status": "SUBSTANTIVE_VERIFICATION_CANDIDATE_SUPPLIED_NOT_ACCEPTED",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "semantic_evidence_field": row["semantic_evidence_field"],
        "trace_component_name": row["trace_component_name"],
        "proof_content_artifact": row["proof_content_artifact"],
        "referenced_component_artifact": rel(component_path) if component_path else None,
        "mechanical_checks": {
            "component_artifact_exists": component_exists,
            "proof_content_artifact_exists": proof_exists,
            "proof_content_hash_matches": proof_hash_ok,
            "proof_content_candidate_nonempty": row["proof_content_candidate_nonempty"] == "true",
            "proof_content_references_endpoint_data": row["proof_content_references_endpoint_data"] == "true",
            "endpoint_blind_verification": True,
        },
        "verification_candidate": {
            "local_object": row["trace_component_name"],
            "local_scope": "trace-component proof-content acceptance only",
            "verification_standard": (
                "accept only if mechanical checks are true, endpoint data is absent, and a later audit "
                "finds a substantive local derivation or replay tying the component to the named checker field"
            ),
            "recorded_dependency_boundary": [
                "component draft artifact",
                "proof-content candidate artifact",
                "matching proof-content hash",
                "endpoint-blind firewall flags",
            ],
            "non_claims": [
                "not a physical R_CMB readout",
                "not a CMB likelihood evaluation",
                "not a score",
                "not a dark-sector verdict",
                "not accepted substantive proof until audited",
            ],
        },
        "substantive_verification_candidate_supplied": True,
        "substantive_verification_accepted": False,
        "component_substantively_proven_after_verification": False,
        "component_accepted_after_verification": False,
        "certificate_passed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_step": "audit substantive verification candidates against the local derivation/replay standard",
    }


def supply_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("proof-content acceptance audit summary is not clean")
    rows: list[dict[str, str]] = []
    for source in read_csv(ACCEPTANCE_TABLE):
        if source["proof_content_accepted"] != "false":
            continue
        index = len(rows) + 1
        artifact = verification_artifact_for(source)
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, verification_payload(source))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "substantive_verification_candidate_supplied": True,
                    "substantive_verification_accepted": False,
                    "component_accepted_after_verification": False,
                    "certificate_passed": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_supplied = hash_artifact.exists()
        hash_matches = supplied and hash_supplied and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        checks = payload.get("mechanical_checks", {})
        rows.append(
            {
                "substantive_verification_supply_row_id": f"TCMBCDSEMPCVER01_{index:03d}",
                "source_proof_content_acceptance_row_id": source["proof_content_acceptance_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "semantic_evidence_field": source["semantic_evidence_field"],
                "trace_component_name": source["trace_component_name"],
                "proof_content_artifact": source["proof_content_artifact"],
                "substantive_verification_artifact": rel(artifact),
                "substantive_verification_hash_artifact": rel(hash_artifact),
                "substantive_verification_artifact_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "component_artifact_exists": str(checks.get("component_artifact_exists") is True).lower(),
                "proof_content_artifact_exists": str(checks.get("proof_content_artifact_exists") is True).lower(),
                "proof_content_hash_matches": str(checks.get("proof_content_hash_matches") is True).lower(),
                "endpoint_blind_verification": str(checks.get("endpoint_blind_verification") is True and checks.get("proof_content_references_endpoint_data") is False).lower(),
                "mechanical_checks_recorded": str(bool(checks)).lower(),
                "substantive_verification_candidate_supplied": str(payload.get("substantive_verification_candidate_supplied") is True).lower(),
                "substantive_verification_accepted": "false",
                "component_substantively_proven_after_verification": "false",
                "component_accepted_after_verification": "false",
                "trace_accepted_after_component": "false",
                "certificate_rule_executable_after_component": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "SUBSTANTIVE_VERIFICATION_CANDIDATE_SUPPLIED_NOT_ACCEPTED"
                    if supplied and hash_matches and payload.get("substantive_verification_candidate_supplied") is True
                    else "SUBSTANTIVE_VERIFICATION_SUPPLY_BLOCKED"
                ),
                "blocking_reason": (
                    "verification candidate supplied with mechanical checks; acceptance audit remains downstream"
                    if supplied and hash_matches and payload.get("substantive_verification_candidate_supplied") is True
                    else "requires verification artifact, matching hash, and recorded mechanical checks"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_proof_content_acceptance_table": rel(ACCEPTANCE_TABLE),
        "input_proof_content_acceptance_summary": rel(ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "substantive_verification_supply_rows": len(rows),
        "substantive_verification_artifact_supplied_rows": sum(row["substantive_verification_artifact_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "component_artifact_exists_rows": sum(row["component_artifact_exists"] == "true" for row in rows),
        "proof_content_artifact_exists_rows": sum(row["proof_content_artifact_exists"] == "true" for row in rows),
        "proof_content_hash_matches_rows": sum(row["proof_content_hash_matches"] == "true" for row in rows),
        "endpoint_blind_verification_rows": sum(row["endpoint_blind_verification"] == "true" for row in rows),
        "mechanical_checks_recorded_rows": sum(row["mechanical_checks_recorded"] == "true" for row in rows),
        "substantive_verification_candidate_supplied_rows": sum(row["substantive_verification_candidate_supplied"] == "true" for row in rows),
        "substantive_verification_accepted_rows": 0,
        "component_substantively_proven_after_verification_rows": 0,
        "component_accepted_after_verification_rows": 0,
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
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_CANDIDATES_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean()
            and len(rows) == 128
            and all(row["substantive_verification_candidate_supplied"] == "true" for row in rows)
            and all(row["hash_matches"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUBSTANTIVE_VERIFICATION_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Proof Content Substantive Verification Supply v01

**Doc class:** semantic certificate evidence substantive verification supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies endpoint-blind substantive-verification candidates and records
mechanical checks for the 128 proof-content candidates. It does not accept those
verifications, components, traces, certificates, domain objects, physical
readouts, scores, likelihoods, or dark-sector verdicts.

## Summary

```text
substantive_verification_supply_rows={summary["substantive_verification_supply_rows"]}
substantive_verification_artifact_supplied_rows={summary["substantive_verification_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
component_artifact_exists_rows={summary["component_artifact_exists_rows"]}
proof_content_artifact_exists_rows={summary["proof_content_artifact_exists_rows"]}
proof_content_hash_matches_rows={summary["proof_content_hash_matches_rows"]}
endpoint_blind_verification_rows={summary["endpoint_blind_verification_rows"]}
mechanical_checks_recorded_rows={summary["mechanical_checks_recorded_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB substantive verification candidates.")
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
