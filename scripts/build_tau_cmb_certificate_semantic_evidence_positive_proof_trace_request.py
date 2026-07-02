#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSERTION_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_v01.csv"
ASSERTION_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_v01_"
    "positive_trace_request_only_no_trace_supplied_no_evidence_acceptance_no_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "trace_request_row_id",
    "source_assertion_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "replacement_artifact",
    "required_positive_trace_artifact",
    "required_trace_components",
    "required_assertion_update",
    "required_endpoint_blind_firewall",
    "positive_trace_requested",
    "positive_trace_supplied",
    "positive_trace_accepted",
    "semantic_assertion_acceptance_allowed",
    "certificate_rule_executable_after_trace",
    "certificate_passed",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "request_status",
    "blocking_reason",
    "claim_boundary",
]


TRACE_COMPONENTS = {
    "carrier_well_formedness": "source files; role-basis replay; role-bundle closure trace; hash comparison; endpoint-blind provenance",
    "domain_membership_rule": "parent-side object witness; support witness; normalization replay; domain replay; firewall trace",
    "seed_admissibility": "seed descriptor witness; activation witness; quotient survival trace; equivalence replay; endpoint firewall trace",
    "null_control_admissibility": "null readout witness; no-response proof trace; zero-control replay; null-coordinate replay; same-domain convention trace",
    "source_object_admissibility": "endpoint-blind derivation transcript; known-limit check; dimension/gauge replay; source firewall trace",
    "quotient_and_equivalence_survival": "equivalence relation proof; null-class identification; representative independence proof; non-null witness",
    "endpoint_firewall_replay": "endpoint access log; score access log; post-endpoint tuning denial; provenance lock replay",
}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_chain_clean() -> bool:
    if not ASSERTION_SUMMARY.exists():
        return False
    summary = load_json(ASSERTION_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_NONNULL_STATUS_ASSERTIONS_SUPPLIED_NOT_ACCEPTED"
        and summary.get("assertion_rows") == 28
        and summary.get("assertion_supplied_rows") == 28
        and summary.get("negative_status_assertion_rows") == 28
        and summary.get("semantic_assertion_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(ASSERTION_TABLE):
        index = len(rows) + 1
        trace_artifact = ROOT / "semantic_evidence_positive_traces" / row["certificate_area"] / f"{row['semantic_evidence_field']}_positive_trace_request_v01.json"
        rows.append(
            {
                "trace_request_row_id": f"TCMBCDSEMPTR01_{index:03d}",
                "source_assertion_row_id": row["assertion_row_id"],
                "certificate_area": row["certificate_area"],
                "checker_name": row["checker_name"],
                "semantic_evidence_field": row["semantic_evidence_field"],
                "replacement_artifact": row["replacement_artifact"],
                "required_positive_trace_artifact": rel(trace_artifact),
                "required_trace_components": TRACE_COMPONENTS.get(row["certificate_area"], "endpoint-blind proof trace"),
                "required_assertion_update": "semantic_assertion_value=true; semantic_assertion_accepted=true; proof_claim_allowed=true only after trace audit",
                "required_endpoint_blind_firewall": "cmb_endpoint_residuals_used=false; act_planck_likelihood_used=false; score_output_used=false; post_endpoint_tuning_used=false; dark_sector_verdict_used=false",
                "positive_trace_requested": "true",
                "positive_trace_supplied": "false",
                "positive_trace_accepted": "false",
                "semantic_assertion_acceptance_allowed": "false",
                "certificate_rule_executable_after_trace": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "request_status": "POSITIVE_PROOF_TRACE_REQUESTED_NOT_SUPPLIED",
                "blocking_reason": "requires endpoint-blind positive proof trace before semantic assertion acceptance can be allowed",
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
        "report_id": "tau_cmb_certificate_semantic_evidence_positive_proof_trace_request_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_assertion_table": rel(ASSERTION_TABLE),
        "input_assertion_summary": rel(ASSERTION_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "trace_request_rows": len(rows),
        "positive_trace_requested_rows": sum(row["positive_trace_requested"] == "true" for row in rows),
        "positive_trace_supplied_rows": 0,
        "positive_trace_accepted_rows": 0,
        "semantic_assertion_acceptance_allowed_rows": 0,
        "certificate_rule_executable_after_trace_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_REQUEST_DECLARED"
            if input_chain_clean() and len(rows) == 28
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_POSITIVE_PROOF_TRACE_REQUEST_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Positive Proof Trace Request v01

**Doc class:** semantic certificate evidence positive proof trace request
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This request converts the 28 non-null negative status assertions into a finite
positive-proof-trace worklist. It does not supply traces, accept semantic
evidence, execute certificate rules, or open scoring.

## Summary

```text
trace_request_rows={summary["trace_request_rows"]}
positive_trace_requested_rows={summary["positive_trace_requested_rows"]}
positive_trace_supplied_rows={summary["positive_trace_supplied_rows"]}
positive_trace_accepted_rows={summary["positive_trace_accepted_rows"]}
semantic_assertion_acceptance_allowed_rows={summary["semantic_assertion_acceptance_allowed_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB positive proof trace request.")
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
