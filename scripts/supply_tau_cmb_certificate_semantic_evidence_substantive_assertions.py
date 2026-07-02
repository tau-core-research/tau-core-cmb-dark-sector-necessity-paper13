#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPLACEMENT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_supply_v01.csv"
REPLACEMENT_AUDIT = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_replacement_supply_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_v01_"
    "nonnull_status_assertions_supplied_not_accepted_not_proof_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "assertion_row_id",
    "source_replacement_supply_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "replacement_artifact",
    "hash_artifact",
    "assertion_supplied",
    "semantic_assertion_value",
    "semantic_assertion_kind",
    "semantic_assertion_accepted",
    "proof_claim_allowed",
    "replacement_accepted",
    "certificate_rule_executable_after_assertion",
    "certificate_passed",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "assertion_status",
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
    if not REPLACEMENT_AUDIT.exists():
        return False
    audit = load_json(REPLACEMENT_AUDIT)
    return (
        audit.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_SUPPLY_AUDITED_DRAFTS_NOT_ACCEPTED"
        and audit.get("failed_rows") == 0
        and audit.get("replacement_supply_rows") == 28
        and audit.get("replacement_supplied_rows") == 28
        and audit.get("replacement_accepted_rows") == 0
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def update_replacement(path: Path, row: dict[str, str]) -> dict[str, Any]:
    payload = load_json(path)
    payload.update(
        {
            "artifact_status": "SEMANTIC_EVIDENCE_SUBSTANTIVE_STATUS_ASSERTION_SUPPLIED_NOT_ACCEPTED_NOT_PROOF",
            "claim_boundary": CLAIM_BOUNDARY,
            "semantic_assertion_value": False,
            "semantic_assertion_kind": "negative_status_assertion_about_current_certificate_evidence",
            "semantic_assertion_statement": (
                f"The current replacement for {row['semantic_evidence_field']} does not yet establish "
                "the required certificate predicate as accepted semantic evidence."
            ),
            "semantic_assertion_rationale": (
                "The assertion is non-null and endpoint-blind, but it is a negative status assertion: "
                "it records that substantive proof content remains absent. It must not be read as a "
                "certificate predicate pass."
            ),
            "semantic_assertion_accepted": False,
            "proof_claim_allowed": False,
            "certificate_rule_executable": False,
            "certificate_passed": False,
            "domain_object_accepted": False,
            "physical_R_CMB_materialized": False,
            "score_entry_allowed": False,
            "likelihood_allowed": False,
            "dark_sector_verdict_allowed": False,
            "next_required_step": "replace negative status assertion with accepted endpoint-blind proof trace before certificate execution",
        }
    )
    return payload


def supply_rows(write_assertions: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("replacement supply audit is not clean")
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(REPLACEMENT_TABLE), start=1):
        artifact = ROOT / source["replacement_artifact"]
        hash_artifact = ROOT / source["replacement_hash_artifact"]
        if write_assertions:
            updated = update_replacement(artifact, source)
            write_json(artifact, updated)
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "semantic_assertion_accepted": False,
                    "proof_claim_allowed": False,
                    "certificate_passed": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        payload = load_json(artifact)
        assertion_supplied = payload.get("semantic_assertion_value") is not None
        assertion_value = str(payload.get("semantic_assertion_value")).lower()
        rows.append(
            {
                "assertion_row_id": f"TCMBCDSEMSA01_{index:03d}",
                "source_replacement_supply_row_id": source["supply_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "semantic_evidence_field": source["semantic_evidence_field"],
                "replacement_artifact": rel(artifact),
                "hash_artifact": rel(hash_artifact),
                "assertion_supplied": str(assertion_supplied).lower(),
                "semantic_assertion_value": assertion_value,
                "semantic_assertion_kind": str(payload.get("semantic_assertion_kind", "")),
                "semantic_assertion_accepted": str(payload.get("semantic_assertion_accepted") is True).lower(),
                "proof_claim_allowed": str(payload.get("proof_claim_allowed") is True).lower(),
                "replacement_accepted": "false",
                "certificate_rule_executable_after_assertion": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "assertion_status": "NONNULL_NEGATIVE_STATUS_ASSERTION_SUPPLIED_NOT_ACCEPTED_NOT_PROOF",
                "blocking_reason": "requires accepted endpoint-blind proof trace before positive certificate evidence can be accepted",
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
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_replacement_supply_table": rel(REPLACEMENT_TABLE),
        "input_replacement_supply_audit": rel(REPLACEMENT_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "assertion_rows": len(rows),
        "assertion_supplied_rows": sum(row["assertion_supplied"] == "true" for row in rows),
        "negative_status_assertion_rows": sum(row["semantic_assertion_value"] == "false" for row in rows),
        "semantic_assertion_accepted_rows": 0,
        "proof_claim_allowed_rows": 0,
        "replacement_accepted_rows": 0,
        "certificate_rule_executable_after_assertion_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_NONNULL_STATUS_ASSERTIONS_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean() and len(rows) == 28 and all(row["assertion_supplied"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_SUBSTANTIVE_ASSERTION_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Assertion Supply v01

**Doc class:** semantic certificate evidence assertion supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact supplies non-null assertions inside the 28 draft replacement
files. The assertions are negative status assertions: they state that the
current replacement does not yet establish the corresponding certificate
predicate as accepted semantic evidence. They are not proof claims and do not
open certificate execution.

## Summary

```text
assertion_rows={summary["assertion_rows"]}
assertion_supplied_rows={summary["assertion_supplied_rows"]}
negative_status_assertion_rows={summary["negative_status_assertion_rows"]}
semantic_assertion_accepted_rows={summary["semantic_assertion_accepted_rows"]}
proof_claim_allowed_rows={summary["proof_claim_allowed_rows"]}
replacement_accepted_rows={summary["replacement_accepted_rows"]}
certificate_rule_executable_after_assertion_rows={summary["certificate_rule_executable_after_assertion_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply non-null status assertions for Tau CMB semantic evidence replacements.")
    parser.add_argument("--write-assertions", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(args.write_assertions)
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
