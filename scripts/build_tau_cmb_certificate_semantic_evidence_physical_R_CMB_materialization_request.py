#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_v01.csv"
DOMAIN_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_summary_v01.json"
STRUCTURAL_GATE_AUDIT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_candidate_gate_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_v01_"
    "materialization_request_only_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "physical_R_CMB_materialization_request_row_id",
    "source_domain_object_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "domain_object_name",
    "domain_object_accepted",
    "structural_R_CMB_candidate_available",
    "required_materialization_artifact",
    "required_materialization_content",
    "required_endpoint_blind_firewall",
    "physical_R_CMB_materialization_requested",
    "physical_R_CMB_materialized",
    "numeric_values_materialized",
    "codomain_checker_passed",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "request_status",
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
    if not DOMAIN_SUMMARY.exists() or not STRUCTURAL_GATE_AUDIT.exists():
        return False
    domain = load_json(DOMAIN_SUMMARY)
    structural = load_json(STRUCTURAL_GATE_AUDIT)
    return (
        domain.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_DOMAIN_OBJECTS_ACCEPTED_SEMANTIC_ONLY"
        and domain.get("input_chain_clean") is True
        and domain.get("accepted_domain_objects") == 7
        and domain.get("physical_R_CMB_materialized") is False
        and structural.get("status") == "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_AUDITED_NOT_PHYSICAL"
        and structural.get("structural_candidate_available_for_codomain_precheck") is True
        and structural.get("physical_R_CMB_materialized") is False
        and domain.get("score_entry_allowed") is False
        and domain.get("likelihood_allowed") is False
        and domain.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("domain-object acceptance or structural R_CMB gate input is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(DOMAIN_TABLE), start=1):
        artifact = ROOT / "physical_R_CMB_materialization_requests" / source["certificate_area"] / f"{source['domain_object_name']}_physical_R_CMB_materialization_v01.json"
        out.append(
            {
                "physical_R_CMB_materialization_request_row_id": f"TCMBCDSEMPHRCMBREQ01_{index:03d}",
                "source_domain_object_acceptance_row_id": source["domain_object_acceptance_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "domain_object_name": source["domain_object_name"],
                "domain_object_accepted": source["domain_object_accepted"],
                "structural_R_CMB_candidate_available": "true",
                "required_materialization_artifact": rel(artifact),
                "required_materialization_content": (
                    "endpoint-blind physical/numeric R_CMB materialization payload with role-vector coordinates, "
                    "dimension/gauge replay, null-anchor compatibility, codomain typing, provenance, and hash binding"
                ),
                "required_endpoint_blind_firewall": (
                    "cmb_endpoint_residuals_used=false; act_planck_likelihood_used=false; "
                    "score_output_used=false; post_endpoint_tuning_used=false; dark_sector_verdict_used=false"
                ),
                "physical_R_CMB_materialization_requested": "true",
                "physical_R_CMB_materialized": "false",
                "numeric_values_materialized": "false",
                "codomain_checker_passed": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "request_status": "PHYSICAL_R_CMB_MATERIALIZATION_REQUESTED_NOT_SUPPLIED",
                "blocking_reason": "requires endpoint-blind physical R_CMB materialization payload before scoring can open",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_domain_object_acceptance_table": rel(DOMAIN_TABLE),
        "input_domain_object_acceptance_summary": rel(DOMAIN_SUMMARY),
        "input_structural_R_CMB_candidate_audit": rel(STRUCTURAL_GATE_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "physical_R_CMB_materialization_request_rows": len(rows),
        "physical_R_CMB_materialization_requested_rows": sum(row["physical_R_CMB_materialization_requested"] == "true" for row in rows),
        "domain_object_accepted_rows": sum(row["domain_object_accepted"] == "true" for row in rows),
        "structural_R_CMB_candidate_available_rows": sum(row["structural_R_CMB_candidate_available"] == "true" for row in rows),
        "physical_R_CMB_materialized_rows": 0,
        "numeric_values_materialized_rows": 0,
        "codomain_checker_passed_rows": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_REQUEST_DECLARED"
            if input_chain_clean() and len(rows) == 7
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_REQUEST_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Physical R_CMB Materialization Request v01

**Doc class:** physical R_CMB materialization request
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This request converts accepted semantic domain objects and the audited
structural R_CMB candidate shell into a finite physical-materialization worklist.
It does not supply physical/numeric R_CMB values, pass codomain checks, open
scoring, evaluate likelihoods, or decide the dark-sector question.

## Summary

```text
physical_R_CMB_materialization_request_rows={summary["physical_R_CMB_materialization_request_rows"]}
domain_object_accepted_rows={summary["domain_object_accepted_rows"]}
structural_R_CMB_candidate_available_rows={summary["structural_R_CMB_candidate_available_rows"]}
physical_R_CMB_materialized_rows={summary["physical_R_CMB_materialized_rows"]}
numeric_values_materialized_rows={summary["numeric_values_materialized_rows"]}
codomain_checker_passed_rows={summary["codomain_checker_passed_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB physical R_CMB materialization request.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_rows = rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, table_rows)
    if args.write_table:
        write_table(table_path, table_rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
