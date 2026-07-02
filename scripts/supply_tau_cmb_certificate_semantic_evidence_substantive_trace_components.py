#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_v01.csv"
TRACE_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_v01_"
    "component_draft_content_supplied_not_accepted_not_proof_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "component_supply_row_id",
    "source_trace_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "trace_component_name",
    "positive_trace_artifact",
    "component_artifact",
    "component_hash_artifact",
    "component_artifact_supplied",
    "hash_supplied",
    "hash_matches",
    "endpoint_blind_component",
    "component_content_supplied",
    "component_substantively_proven",
    "component_accepted",
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


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


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
    if not TRACE_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(TRACE_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_ACCEPTANCE_AUDITED_REJECTED_SUBSTANTIVE_COMPONENTS_REQUIRED"
        and summary.get("acceptance_rows") == 28
        and summary.get("trace_components_declared_rows") == 28
        and summary.get("trace_components_substantively_proven_rows") == 0
        and summary.get("trace_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def component_payload(row: dict[str, str], component: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": row["acceptance_row_id"],
        "artifact_status": "TRACE_COMPONENT_DRAFT_CONTENT_SUPPLIED_NOT_ACCEPTED_NOT_PROOF",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "semantic_evidence_field": row["semantic_evidence_field"],
        "positive_trace_artifact": row["positive_trace_artifact"],
        "trace_component_name": component.get("component"),
        "component_statement": (
            "This component is required by the positive proof trace and is "
            "represented as endpoint-blind draft content. It is not yet a "
            "substantive proof and must not be promoted to certificate evidence."
        ),
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "component_content_supplied": True,
        "component_substantively_proven": False,
        "component_accepted": False,
        "trace_accepted_after_component": False,
        "semantic_assertion_acceptance_allowed": False,
        "proof_claim_allowed": False,
        "certificate_rule_executable": False,
        "certificate_passed": False,
        "domain_object_accepted": False,
        "physical_R_CMB_materialized": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_step": "replace draft component content with accepted endpoint-blind substantive proof content",
    }


def supply_rows(write_components: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("positive proof trace acceptance audit summary is not clean")
    rows: list[dict[str, str]] = []
    for trace_row in read_csv(TRACE_ACCEPTANCE_TABLE):
        trace_path = ROOT / trace_row["positive_trace_artifact"]
        trace_payload = load_json(trace_path)
        for component in trace_payload.get("trace_component_status", []):
            index = len(rows) + 1
            component_name = str(component.get("component"))
            artifact = (
                ROOT
                / "semantic_evidence_trace_components"
                / trace_row["certificate_area"]
                / trace_row["semantic_evidence_field"]
                / f"{slug(component_name)}_component_draft_v01.json"
            )
            hash_artifact = artifact.with_suffix(".hashes.json")
            if write_components:
                write_json(artifact, component_payload(trace_row, component))
                write_json(
                    hash_artifact,
                    {
                        "target": rel(artifact),
                        "sha256": sha256(artifact),
                        "claim_boundary": CLAIM_BOUNDARY,
                        "component_accepted": False,
                        "component_substantively_proven": False,
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
            rows.append(
                {
                    "component_supply_row_id": f"TCMBCDSEMCOMP01_{index:03d}",
                    "source_trace_acceptance_row_id": trace_row["acceptance_row_id"],
                    "certificate_area": trace_row["certificate_area"],
                    "checker_name": trace_row["checker_name"],
                    "semantic_evidence_field": trace_row["semantic_evidence_field"],
                    "trace_component_name": component_name,
                    "positive_trace_artifact": trace_row["positive_trace_artifact"],
                    "component_artifact": rel(artifact),
                    "component_hash_artifact": rel(hash_artifact),
                    "component_artifact_supplied": str(supplied).lower(),
                    "hash_supplied": str(hash_supplied).lower(),
                    "hash_matches": str(hash_matches).lower(),
                    "endpoint_blind_component": "true",
                    "component_content_supplied": str(payload.get("component_content_supplied") is True).lower(),
                    "component_substantively_proven": str(payload.get("component_substantively_proven") is True).lower(),
                    "component_accepted": str(payload.get("component_accepted") is True).lower(),
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
                        "TRACE_COMPONENT_DRAFT_CONTENT_SUPPLIED_NOT_ACCEPTED"
                        if supplied and hash_matches and payload.get("component_content_supplied") is True
                        else "TRACE_COMPONENT_SUPPLY_BLOCKED"
                    ),
                    "blocking_reason": (
                        "component draft content exists and is hash-bound; substantive proof acceptance remains downstream"
                        if supplied and hash_matches and payload.get("component_content_supplied") is True
                        else "requires component artifact, matching hash, and component draft content"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_trace_acceptance_table": rel(TRACE_ACCEPTANCE_TABLE),
        "input_trace_acceptance_summary": rel(TRACE_ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "component_supply_rows": len(rows),
        "component_artifact_supplied_rows": sum(row["component_artifact_supplied"] == "true" for row in rows),
        "hash_supplied_rows": sum(row["hash_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "endpoint_blind_component_rows": sum(row["endpoint_blind_component"] == "true" for row in rows),
        "component_content_supplied_rows": sum(row["component_content_supplied"] == "true" for row in rows),
        "component_substantively_proven_rows": 0,
        "component_accepted_rows": 0,
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
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_DRAFT_CONTENT_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean() and len(rows) > 0 and all(row["component_content_supplied"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Substantive Trace Component Supply v01

**Doc class:** semantic certificate evidence trace component supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact supplies draft component-content files for the positive proof
traces. The component files are endpoint-blind and hash-bound, but they are not
accepted as substantive proof and do not open trace acceptance, certificate
execution, or scoring.

## Summary

```text
component_supply_rows={summary["component_supply_rows"]}
component_artifact_supplied_rows={summary["component_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
component_content_supplied_rows={summary["component_content_supplied_rows"]}
component_substantively_proven_rows={summary["component_substantively_proven_rows"]}
component_accepted_rows={summary["component_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB substantive trace component draft content.")
    parser.add_argument("--write-components", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(args.write_components)
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
