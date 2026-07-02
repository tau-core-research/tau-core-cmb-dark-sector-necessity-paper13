#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_request_v01.csv"
REQUEST_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_request_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_replacement_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_replacement_supply_v01_"
    "draft_replacements_supplied_not_accepted_no_proof_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "supply_row_id",
    "source_replacement_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "replacement_artifact",
    "replacement_hash_artifact",
    "replacement_supplied",
    "hash_supplied",
    "hash_matches",
    "endpoint_blind_replacement",
    "semantic_assertion_nonnull",
    "semantic_assertion_accepted",
    "proof_claim_allowed",
    "replacement_accepted",
    "certificate_rule_executable_after_replacement",
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
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_REQUEST_DECLARED"
        and summary.get("replacement_request_rows") == 28
        and summary.get("replacement_supplied_rows") == 0
        and summary.get("replacement_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def replacement_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "artifact_id": row["replacement_row_id"],
        "artifact_status": "SEMANTIC_EVIDENCE_DRAFT_REPLACEMENT_SUPPLIED_NOT_ACCEPTED_NOT_PROOF",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "semantic_evidence_field": row["semantic_evidence_field"],
        "replaces_candidate_artifact": row["rejected_candidate_artifact"],
        "required_semantic_assertion_value": row["required_semantic_assertion_value"],
        "required_acceptance_flags": row["required_acceptance_flags"],
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "semantic_assertion_value": None,
        "semantic_assertion_rationale": "draft replacement shell only; substantive endpoint-blind proof trace not supplied in this artifact",
        "semantic_assertion_accepted": False,
        "proof_claim_allowed": False,
        "certificate_rule_executable": False,
        "certificate_passed": False,
        "domain_object_accepted": False,
        "physical_R_CMB_materialized": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_step": "supply substantive endpoint-blind proof trace and set semantic assertion only after audit",
    }


def supply_rows(write_replacements: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("semantic evidence replacement request is not clean")
    rows: list[dict[str, str]] = []
    for index, request in enumerate(read_csv(REQUEST_TABLE), start=1):
        artifact = ROOT / request["required_replacement_artifact"]
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_replacements:
            write_json(artifact, replacement_payload(request))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "replacement_accepted": False,
                    "proof_claim_allowed": False,
                    "certificate_passed": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_supplied = hash_artifact.exists()
        hash_matches = hash_supplied and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        assertion_nonnull = payload.get("semantic_assertion_value") is not None
        assertion_accepted = payload.get("semantic_assertion_accepted") is True
        proof_allowed = payload.get("proof_claim_allowed") is True
        accepted = supplied and hash_matches and assertion_nonnull and assertion_accepted and proof_allowed
        rows.append(
            {
                "supply_row_id": f"TCMBCDSEMRSUP01_{index:03d}",
                "source_replacement_row_id": request["replacement_row_id"],
                "certificate_area": request["certificate_area"],
                "checker_name": request["checker_name"],
                "semantic_evidence_field": request["semantic_evidence_field"],
                "replacement_artifact": rel(artifact),
                "replacement_hash_artifact": rel(hash_artifact),
                "replacement_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "endpoint_blind_replacement": "true",
                "semantic_assertion_nonnull": str(assertion_nonnull).lower(),
                "semantic_assertion_accepted": str(assertion_accepted).lower(),
                "proof_claim_allowed": str(proof_allowed).lower(),
                "replacement_accepted": str(accepted).lower(),
                "certificate_rule_executable_after_replacement": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "SEMANTIC_EVIDENCE_DRAFT_REPLACEMENT_SUPPLIED_NOT_ACCEPTED"
                    if supplied and hash_matches
                    else "SEMANTIC_EVIDENCE_REPLACEMENT_SUPPLY_BLOCKED"
                ),
                "blocking_reason": (
                    "draft replacement exists and is hash-bound; substantive semantic assertion/proof trace remains absent"
                    if supplied and hash_matches
                    else "requires replacement artifact and matching hash"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_replacement_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_replacement_request_table": rel(REQUEST_TABLE),
        "input_replacement_request_summary": rel(REQUEST_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "replacement_supply_rows": len(rows),
        "replacement_supplied_rows": sum(row["replacement_supplied"] == "true" for row in rows),
        "hash_supplied_rows": sum(row["hash_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_replacement_rows": sum(row["endpoint_blind_replacement"] == "true" for row in rows),
        "semantic_assertion_nonnull_rows": sum(row["semantic_assertion_nonnull"] == "true" for row in rows),
        "semantic_assertion_accepted_rows": sum(row["semantic_assertion_accepted"] == "true" for row in rows),
        "proof_claim_allowed_rows": sum(row["proof_claim_allowed"] == "true" for row in rows),
        "replacement_accepted_rows": sum(row["replacement_accepted"] == "true" for row in rows),
        "certificate_rule_executable_after_replacement_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_DRAFT_REPLACEMENTS_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean() and len(rows) == 28 and all(row["replacement_supplied"] == "true" and row["hash_matches"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_replacement_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Replacement Supply v01

**Doc class:** semantic certificate evidence replacement supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact supplies draft replacement files for all 28 rejected semantic
evidence candidates. These replacements are hash-bound shells only: they do not
contain accepted non-null semantic assertions or proof claims.

## Summary

```text
replacement_supply_rows={summary["replacement_supply_rows"]}
replacement_supplied_rows={summary["replacement_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
semantic_assertion_nonnull_rows={summary["semantic_assertion_nonnull_rows"]}
semantic_assertion_accepted_rows={summary["semantic_assertion_accepted_rows"]}
proof_claim_allowed_rows={summary["proof_claim_allowed_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB semantic evidence draft replacements.")
    parser.add_argument("--write-replacements", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(args.write_replacements)
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
