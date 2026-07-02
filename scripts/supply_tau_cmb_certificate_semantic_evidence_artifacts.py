#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATERIALIZATION_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_materialization_v01.csv"
MATERIALIZATION_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_materialization_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_artifact_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_artifact_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_artifact_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_artifact_supply_v01_"
    "candidate_artifacts_materialized_not_accepted_not_proof_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "supply_row_id",
    "source_evidence_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "candidate_evidence_artifact",
    "candidate_hash_artifact",
    "artifact_materialized",
    "hash_materialized",
    "hash_matches",
    "endpoint_blind_candidate",
    "evidence_accepted",
    "proof_claim_allowed",
    "certificate_rule_executable",
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
    if not MATERIALIZATION_SUMMARY.exists():
        return False
    summary = load_json(MATERIALIZATION_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_MATERIALIZATION_MATRIX_DECLARED_NOT_MATERIALIZED"
        and summary.get("semantic_evidence_rows") == 28
        and summary.get("evidence_materialized_rows") == 0
        and summary.get("evidence_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def evidence_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "artifact_id": row["evidence_row_id"],
        "artifact_status": "SEMANTIC_EVIDENCE_CANDIDATE_MATERIALIZED_NOT_ACCEPTED_NOT_PROOF",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "semantic_evidence_field": row["semantic_evidence_field"],
        "required_for_predicate": row["required_for_predicate"],
        "source_materialization_row": row["evidence_row_id"],
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "evidence_role": "candidate carrier for future semantic proof/evidence acceptance",
        "semantic_assertion_value": None,
        "semantic_assertion_accepted": False,
        "proof_claim_allowed": False,
        "certificate_rule_executable": False,
        "certificate_passed": False,
        "domain_object_accepted": False,
        "physical_R_CMB_materialized": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_step": "audit and replace candidate with accepted endpoint-blind semantic proof/evidence",
    }


def supply_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("semantic evidence materialization matrix is not clean")
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(MATERIALIZATION_TABLE), start=1):
        artifact = ROOT / source["candidate_evidence_artifact"]
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, evidence_payload(source))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "evidence_accepted": False,
                    "proof_claim_allowed": False,
                    "certificate_passed": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        materialized = artifact.exists()
        hash_materialized = hash_artifact.exists()
        hash_matches = hash_materialized and load_json(hash_artifact).get("sha256") == sha256(artifact)
        rows.append(
            {
                "supply_row_id": f"TCMBCDSEMSUP01_{index:03d}",
                "source_evidence_row_id": source["evidence_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "semantic_evidence_field": source["semantic_evidence_field"],
                "candidate_evidence_artifact": rel(artifact),
                "candidate_hash_artifact": rel(hash_artifact),
                "artifact_materialized": str(materialized).lower(),
                "hash_materialized": str(hash_materialized).lower(),
                "hash_matches": str(hash_matches).lower(),
                "endpoint_blind_candidate": "true",
                "evidence_accepted": "false",
                "proof_claim_allowed": "false",
                "certificate_rule_executable": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "SEMANTIC_EVIDENCE_CANDIDATE_ARTIFACT_SUPPLIED_NOT_ACCEPTED"
                    if materialized and hash_matches
                    else "SEMANTIC_EVIDENCE_CANDIDATE_SUPPLY_BLOCKED"
                ),
                "blocking_reason": (
                    "candidate artifact exists and is hash-bound; requires evidence acceptance/replacement before certificate execution"
                    if materialized and hash_matches
                    else "requires candidate artifact and matching hash"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_artifact_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_materialization_table": rel(MATERIALIZATION_TABLE),
        "input_materialization_summary": rel(MATERIALIZATION_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "supply_rows": len(rows),
        "artifact_materialized_rows": sum(row["artifact_materialized"] == "true" for row in rows),
        "hash_materialized_rows": sum(row["hash_materialized"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_candidate_rows": sum(row["endpoint_blind_candidate"] == "true" for row in rows),
        "evidence_accepted_rows": 0,
        "proof_claim_allowed_rows": 0,
        "certificate_rule_executable_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CANDIDATE_ARTIFACTS_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean() and len(rows) == 28 and all(row["artifact_materialized"] == "true" and row["hash_matches"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_ARTIFACT_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Artifact Supply v01

**Doc class:** semantic certificate evidence artifact supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact supplies endpoint-blind candidate files for the 28 semantic
certificate evidence rows. The files are intentionally not accepted as proof.
They are hash-bound placeholders/candidates for the next evidence acceptance or
replacement step.

## Summary

```text
supply_rows={summary["supply_rows"]}
artifact_materialized_rows={summary["artifact_materialized_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
evidence_accepted_rows={summary["evidence_accepted_rows"]}
proof_claim_allowed_rows={summary["proof_claim_allowed_rows"]}
certificate_rule_executable_rows={summary["certificate_rule_executable_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB semantic evidence candidate artifacts.")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(args.write_artifacts)
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
