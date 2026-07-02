#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COLLAPSE_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_collapse_summary_v01.json"
COLLAPSE_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_collapse_v01.csv"
PROJECTION_OPERATOR_AUDIT = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_audit_v01.json"
LENSING_STATUS = ROOT / "data/derived/cmb_tau_lensing_scoring_status_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_lensing_bridge_candidates_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_lensing_bridge_candidates_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_endpoint_blind_lensing_bridge_candidates_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_endpoint_blind_lensing_bridge_candidates_audit_v01_"
    "bridge_audit_only_no_physical_source_acceptance_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "bridge_audit_row_id",
    "source_frontier_collapse_row_id",
    "coordinate_component",
    "formal_slot",
    "candidate_evidence_artifact",
    "candidate_evidence_status",
    "candidate_relation_to_required_slot",
    "bridge_decision",
    "physical_value_source_supplied",
    "physical_value_source_accepted",
    "explicit_fail_supply_allowed",
    "recommended_next_action",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def input_chain_clean() -> bool:
    if not COLLAPSE_SUMMARY.exists() or not COLLAPSE_TABLE.exists():
        return False
    summary = load_json(COLLAPSE_SUMMARY)
    return (
        summary.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_COLLAPSED_TO_TRIAGE_NO_SOURCES_ACCEPTED"
        and summary.get("next_minimal_unblock") == "tau_cmb_endpoint_blind_physical_value_source_bridge_audit_or_explicit_fail_supply_v01"
        and summary.get("frontier_rows") == 16
        and summary.get("physical_value_source_supplied_rows") == 0
        and summary.get("physical_value_source_accepted_rows") == 0
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def candidate_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(COLLAPSE_TABLE)
        if row["collapse_bucket"] in {
            "bridge_candidate_available_not_accepted",
            "explicit_fail_candidate_available_not_accepted",
        }
    ]


def bridge_decision(row: dict[str, str]) -> dict[str, str]:
    component = row["coordinate_component"]
    if component == "transfer_kernel":
        audit = load_json(PROJECTION_OPERATOR_AUDIT)
        explicit_fail = audit.get("explicit_operator_failure_declared") is True
        return {
            "candidate_relation_to_required_slot": "related projection-operator failure, not identical to T_tau_CMB(k,a)",
            "bridge_decision": (
                "BRIDGE_REJECTED_AUTOMATIC_PROMOTION_EXPLICIT_FAIL_EVIDENCE_REQUIRES_ROW_SPECIFIC_SUPPLY"
                if explicit_fail
                else "BRIDGE_REJECTED_NO_EXPLICIT_FAILURE_EVIDENCE"
            ),
            "physical_value_source_supplied": "false",
            "physical_value_source_accepted": "false",
            "explicit_fail_supply_allowed": str(explicit_fail).lower(),
            "recommended_next_action": "create row-specific explicit-fail supply for e_lensing.transfer_kernel or provide a true endpoint-blind T_tau_CMB operator",
        }
    if component == "amplitude_shape_response":
        status = load_json(LENSING_STATUS)
        score_accepted = status.get("physical_tau_score_output_accepted") is True
        return {
            "candidate_relation_to_required_slot": "related reduced lensing score output, not a direct S_lens_tau(L) value-source payload",
            "bridge_decision": (
                "BRIDGE_REJECTED_SCORE_OUTPUT_NOT_ACCEPTED_AS_VALUE_SOURCE_WITHOUT_ROW_SPECIFIC_ADAPTER"
                if score_accepted
                else "BRIDGE_REJECTED_NO_SCORE_OUTPUT_CANDIDATE"
            ),
            "physical_value_source_supplied": "false",
            "physical_value_source_accepted": "false",
            "explicit_fail_supply_allowed": "false",
            "recommended_next_action": "build row-specific adapter from reduced lensing score output to S_lens_tau(L), or provide explicit fail evidence",
        }
    raise KeyError(component)


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("frontier collapse summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(candidate_rows(), start=1):
        decision = bridge_decision(source)
        out.append(
            {
                "bridge_audit_row_id": f"TCMBEBLBA01_{index:03d}",
                "source_frontier_collapse_row_id": source["frontier_collapse_row_id"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "candidate_evidence_artifact": source["candidate_evidence_artifact"],
                "candidate_evidence_status": source["candidate_evidence_status"],
                **decision,
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
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
    accepted_sources = sum(row["physical_value_source_accepted"] == "true" for row in rows)
    explicit_fail_supply_allowed = sum(row["explicit_fail_supply_allowed"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_endpoint_blind_lensing_bridge_candidates_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_frontier_collapse_summary": rel(COLLAPSE_SUMMARY),
        "input_frontier_collapse_table": rel(COLLAPSE_TABLE),
        "input_chain_clean": input_chain_clean(),
        "bridge_candidate_rows": len(rows),
        "automatic_bridge_acceptance_rows": accepted_sources,
        "explicit_fail_supply_allowed_rows": explicit_fail_supply_allowed,
        "physical_value_source_supplied_rows": sum(row["physical_value_source_supplied"] == "true" for row in rows),
        "physical_value_source_accepted_rows": accepted_sources,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_ENDPOINT_BLIND_LENSING_BRIDGE_CANDIDATES_AUDITED_NO_AUTOMATIC_SOURCE_ACCEPTANCE"
            if input_chain_clean() and len(rows) == 2 and accepted_sources == 0
            else "CMB_ENDPOINT_BLIND_LENSING_BRIDGE_CANDIDATES_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_lensing_transfer_kernel_row_specific_explicit_fail_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Endpoint-Blind Lensing Bridge Candidates Audit v01

**Doc class:** bridge-candidate audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
bridge_candidate_rows={summary["bridge_candidate_rows"]}
automatic_bridge_acceptance_rows={summary["automatic_bridge_acceptance_rows"]}
explicit_fail_supply_allowed_rows={summary["explicit_fail_supply_allowed_rows"]}
physical_value_source_supplied_rows={summary["physical_value_source_supplied_rows"]}
physical_value_source_accepted_rows={summary["physical_value_source_accepted_rows"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

Related lensing artifacts are not automatically promoted into CMB value-source
rows. One row permits a row-specific explicit-fail supply; the other requires a
dedicated adapter or explicit fail evidence.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB endpoint-blind lensing bridge candidates.")
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
