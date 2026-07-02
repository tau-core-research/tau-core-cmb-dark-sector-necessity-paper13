#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_artifact_supply_v01.csv"
SUPPLY_AUDIT = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_artifact_supply_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_acceptance_audit_v01_"
    "candidate_evidence_rejected_until_nonnull_accepted_semantic_assertions_"
    "no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "acceptance_row_id",
    "source_supply_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "candidate_evidence_artifact",
    "artifact_present",
    "hash_present",
    "hash_matches",
    "endpoint_blind_candidate",
    "semantic_assertion_nonnull",
    "semantic_assertion_accepted_in_artifact",
    "proof_claim_allowed_in_artifact",
    "accepted_as_semantic_evidence",
    "replacement_required",
    "certificate_rule_executable_after_acceptance",
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
    if not SUPPLY_AUDIT.exists():
        return False
    audit = load_json(SUPPLY_AUDIT)
    return (
        audit.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_ARTIFACT_SUPPLY_AUDITED_CANDIDATES_NOT_ACCEPTED"
        and audit.get("failed_rows") == 0
        and audit.get("supply_rows") == 28
        and audit.get("artifact_materialized_rows") == 28
        and audit.get("evidence_accepted_rows") == 0
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
    for index, supply in enumerate(read_csv(SUPPLY_TABLE), start=1):
        artifact = ROOT / supply["candidate_evidence_artifact"]
        hash_artifact = ROOT / supply["candidate_hash_artifact"]
        payload = load_json(artifact) if artifact.exists() else {}
        artifact_present = artifact.exists()
        hash_present = hash_artifact.exists()
        hash_ok = hash_matches(artifact, hash_artifact)
        endpoint_blind = (
            payload.get("endpoint_blind_firewall", {}).get("cmb_endpoint_residuals_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("act_planck_likelihood_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("score_output_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("post_endpoint_tuning_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("dark_sector_verdict_used") is False
        )
        assertion_nonnull = payload.get("semantic_assertion_value") is not None
        assertion_accepted = payload.get("semantic_assertion_accepted") is True
        proof_allowed = payload.get("proof_claim_allowed") is True
        accepted = artifact_present and hash_present and hash_ok and endpoint_blind and assertion_nonnull and assertion_accepted and proof_allowed
        rows.append(
            {
                "acceptance_row_id": f"TCMBCDSEMACC01_{index:03d}",
                "source_supply_row_id": supply["supply_row_id"],
                "certificate_area": supply["certificate_area"],
                "checker_name": supply["checker_name"],
                "semantic_evidence_field": supply["semantic_evidence_field"],
                "candidate_evidence_artifact": supply["candidate_evidence_artifact"],
                "artifact_present": str(artifact_present).lower(),
                "hash_present": str(hash_present).lower(),
                "hash_matches": str(hash_ok).lower(),
                "endpoint_blind_candidate": str(endpoint_blind).lower(),
                "semantic_assertion_nonnull": str(assertion_nonnull).lower(),
                "semantic_assertion_accepted_in_artifact": str(assertion_accepted).lower(),
                "proof_claim_allowed_in_artifact": str(proof_allowed).lower(),
                "accepted_as_semantic_evidence": str(accepted).lower(),
                "replacement_required": str(not accepted).lower(),
                "certificate_rule_executable_after_acceptance": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "SEMANTIC_EVIDENCE_ACCEPTED_FOR_CERTIFICATE_RULE_INPUT_ONLY"
                    if accepted
                    else "SEMANTIC_EVIDENCE_REJECTED_REPLACEMENT_REQUIRED"
                ),
                "blocking_reason": (
                    "accepted only as semantic evidence input; certificate execution remains downstream"
                    if accepted
                    else "candidate lacks non-null accepted semantic assertion and proof-claim permission"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_supply_table": rel(SUPPLY_TABLE),
        "input_supply_audit": rel(SUPPLY_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "acceptance_rows": len(rows),
        "artifact_present_rows": sum(row["artifact_present"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_candidate_rows": sum(row["endpoint_blind_candidate"] == "true" for row in rows),
        "semantic_assertion_nonnull_rows": sum(row["semantic_assertion_nonnull"] == "true" for row in rows),
        "semantic_assertion_accepted_rows": sum(row["semantic_assertion_accepted_in_artifact"] == "true" for row in rows),
        "proof_claim_allowed_rows": sum(row["proof_claim_allowed_in_artifact"] == "true" for row in rows),
        "accepted_as_semantic_evidence_rows": sum(row["accepted_as_semantic_evidence"] == "true" for row in rows),
        "replacement_required_rows": sum(row["replacement_required"] == "true" for row in rows),
        "certificate_rule_executable_after_acceptance_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_ACCEPTANCE_AUDITED_REPLACEMENT_REQUIRED"
            if input_chain_clean() and len(rows) == 28 and all(row["replacement_required"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_ACCEPTANCE_AUDIT_PARTIAL_OR_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_replacement_request_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Acceptance Audit v01

**Doc class:** semantic certificate evidence acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the supplied candidate evidence artifacts can be
accepted as semantic evidence for certificate-level checker execution. The
current candidates are intentionally not proof: their semantic assertion values
are null, and proof-claim permission remains false.

## Summary

```text
acceptance_rows={summary["acceptance_rows"]}
artifact_present_rows={summary["artifact_present_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
endpoint_blind_candidate_rows={summary["endpoint_blind_candidate_rows"]}
semantic_assertion_nonnull_rows={summary["semantic_assertion_nonnull_rows"]}
semantic_assertion_accepted_rows={summary["semantic_assertion_accepted_rows"]}
proof_claim_allowed_rows={summary["proof_claim_allowed_rows"]}
accepted_as_semantic_evidence_rows={summary["accepted_as_semantic_evidence_rows"]}
replacement_required_rows={summary["replacement_required_rows"]}
certificate_rule_executable_after_acceptance_rows={summary["certificate_rule_executable_after_acceptance_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB semantic evidence acceptance.")
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
