#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_v01.csv"
REQUEST_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_v01_"
    "draft_positive_traces_supplied_not_accepted_no_evidence_acceptance_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "trace_supply_row_id",
    "source_trace_request_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "positive_trace_artifact",
    "positive_trace_hash_artifact",
    "positive_trace_supplied",
    "hash_supplied",
    "hash_matches",
    "trace_components_declared",
    "endpoint_blind_trace",
    "trace_accepted",
    "semantic_assertion_acceptance_allowed",
    "proof_claim_allowed",
    "certificate_rule_executable_after_trace",
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
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_REQUEST_DECLARED"
        and summary.get("trace_request_rows") == 28
        and summary.get("positive_trace_requested_rows") == 28
        and summary.get("positive_trace_supplied_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def trace_payload(row: dict[str, str]) -> dict[str, Any]:
    components = [item.strip() for item in row["required_trace_components"].split(";") if item.strip()]
    return {
        "artifact_id": row["trace_request_row_id"],
        "artifact_status": "POSITIVE_PROOF_TRACE_DRAFT_SUPPLIED_NOT_ACCEPTED_NOT_PROOF",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "semantic_evidence_field": row["semantic_evidence_field"],
        "replacement_artifact": row["replacement_artifact"],
        "required_trace_components": components,
        "trace_component_status": [
            {
                "component": component,
                "status": "DECLARED_NOT_SUBSTANTIVELY_PROVEN",
                "endpoint_blind": True,
            }
            for component in components
        ],
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "trace_accepted": False,
        "semantic_assertion_acceptance_allowed": False,
        "proof_claim_allowed": False,
        "certificate_rule_executable": False,
        "certificate_passed": False,
        "domain_object_accepted": False,
        "physical_R_CMB_materialized": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_step": "audit and replace draft component declarations with substantive endpoint-blind proof trace content",
    }


def supply_rows(write_traces: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("positive proof trace request summary is not clean")
    rows: list[dict[str, str]] = []
    for index, request in enumerate(read_csv(REQUEST_TABLE), start=1):
        artifact = ROOT / request["required_positive_trace_artifact"]
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_traces:
            write_json(artifact, trace_payload(request))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "trace_accepted": False,
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
        components_declared = bool(payload.get("required_trace_components"))
        endpoint_blind = (
            payload.get("endpoint_blind_firewall", {}).get("cmb_endpoint_residuals_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("act_planck_likelihood_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("score_output_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("post_endpoint_tuning_used") is False
            and payload.get("endpoint_blind_firewall", {}).get("dark_sector_verdict_used") is False
        )
        rows.append(
            {
                "trace_supply_row_id": f"TCMBCDSEMPTRSUP01_{index:03d}",
                "source_trace_request_row_id": request["trace_request_row_id"],
                "certificate_area": request["certificate_area"],
                "checker_name": request["checker_name"],
                "semantic_evidence_field": request["semantic_evidence_field"],
                "positive_trace_artifact": rel(artifact),
                "positive_trace_hash_artifact": rel(hash_artifact),
                "positive_trace_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "trace_components_declared": str(components_declared).lower(),
                "endpoint_blind_trace": str(endpoint_blind).lower(),
                "trace_accepted": "false",
                "semantic_assertion_acceptance_allowed": "false",
                "proof_claim_allowed": "false",
                "certificate_rule_executable_after_trace": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "POSITIVE_PROOF_TRACE_DRAFT_SUPPLIED_NOT_ACCEPTED"
                    if supplied and hash_matches and components_declared
                    else "POSITIVE_PROOF_TRACE_SUPPLY_BLOCKED"
                ),
                "blocking_reason": (
                    "draft trace exists and declares required components; substantive proof content remains unaccepted"
                    if supplied and hash_matches and components_declared
                    else "requires trace artifact, matching hash, and declared trace components"
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
        "report_id": "tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_trace_request_table": rel(REQUEST_TABLE),
        "input_trace_request_summary": rel(REQUEST_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "trace_supply_rows": len(rows),
        "positive_trace_supplied_rows": sum(row["positive_trace_supplied"] == "true" for row in rows),
        "hash_supplied_rows": sum(row["hash_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "trace_components_declared_rows": sum(row["trace_components_declared"] == "true" for row in rows),
        "endpoint_blind_trace_rows": sum(row["endpoint_blind_trace"] == "true" for row in rows),
        "trace_accepted_rows": 0,
        "semantic_assertion_acceptance_allowed_rows": 0,
        "proof_claim_allowed_rows": 0,
        "certificate_rule_executable_after_trace_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_DRAFTS_SUPPLIED_NOT_ACCEPTED"
            if input_chain_clean() and len(rows) == 28 and all(row["positive_trace_supplied"] == "true" and row["hash_matches"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Positive Proof Trace Supply v01

**Doc class:** semantic certificate evidence positive proof trace supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact supplies 28 draft positive-proof-trace files. The files declare
the required trace components and endpoint-blind firewall status, but they are
not accepted proof traces and do not open semantic assertion acceptance,
certificate execution, or scoring.

## Summary

```text
trace_supply_rows={summary["trace_supply_rows"]}
positive_trace_supplied_rows={summary["positive_trace_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
trace_components_declared_rows={summary["trace_components_declared_rows"]}
endpoint_blind_trace_rows={summary["endpoint_blind_trace_rows"]}
trace_accepted_rows={summary["trace_accepted_rows"]}
semantic_assertion_acceptance_allowed_rows={summary["semantic_assertion_acceptance_allowed_rows"]}
proof_claim_allowed_rows={summary["proof_claim_allowed_rows"]}
certificate_rule_executable_after_trace_rows={summary["certificate_rule_executable_after_trace_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB positive proof trace drafts.")
    parser.add_argument("--write-traces", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(args.write_traces)
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
