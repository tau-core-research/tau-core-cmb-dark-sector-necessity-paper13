#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance_audit_v01_"
    "acceptance_audit_candidates_rejected_role_coordinate_numeric_materialization_required_"
    "no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "physical_R_CMB_materialization_acceptance_row_id",
    "source_materialization_supply_row_id",
    "certificate_area",
    "checker_name",
    "domain_object_name",
    "materialization_artifact_supplied",
    "hash_matches",
    "domain_object_accepted",
    "role_coordinate_audits_present",
    "role_coordinates_accepted",
    "physical_R_CMB_materialized",
    "numeric_values_materialized",
    "codomain_checker_passed",
    "materialization_accepted",
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


def input_chain_clean() -> bool:
    if not SUPPLY_SUMMARY.exists():
        return False
    summary = load_json(SUPPLY_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_CANDIDATES_SUPPLIED_ROLE_COORDINATES_BLOCKED"
        and summary.get("input_chain_clean") is True
        and summary.get("physical_R_CMB_materialization_supply_rows") == 7
        and summary.get("hash_matched_rows") == 7
        and summary.get("role_coordinates_accepted_rows") == 0
        and summary.get("physical_R_CMB_materialized_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("physical R_CMB materialization supply summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(SUPPLY_TABLE), start=1):
        accepted = (
            source["hash_matches"] == "true"
            and source["domain_object_accepted"] == "true"
            and source["role_coordinate_audits_present"] == "true"
            and source["role_coordinates_accepted"] == "true"
            and source["physical_R_CMB_materialized"] == "true"
            and source["numeric_values_materialized"] == "true"
            and source["codomain_checker_passed"] == "true"
        )
        out.append(
            {
                "physical_R_CMB_materialization_acceptance_row_id": f"TCMBCDSEMPHRCMBACC01_{index:03d}",
                "source_materialization_supply_row_id": source["physical_R_CMB_materialization_supply_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "domain_object_name": source["domain_object_name"],
                "materialization_artifact_supplied": source["materialization_artifact_supplied"],
                "hash_matches": source["hash_matches"],
                "domain_object_accepted": source["domain_object_accepted"],
                "role_coordinate_audits_present": source["role_coordinate_audits_present"],
                "role_coordinates_accepted": source["role_coordinates_accepted"],
                "physical_R_CMB_materialized": source["physical_R_CMB_materialized"],
                "numeric_values_materialized": source["numeric_values_materialized"],
                "codomain_checker_passed": source["codomain_checker_passed"],
                "materialization_accepted": str(accepted).lower(),
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "PHYSICAL_R_CMB_MATERIALIZATION_ACCEPTED"
                    if accepted
                    else "PHYSICAL_R_CMB_MATERIALIZATION_REJECTED_ROLE_COORDINATE_NUMERIC_MATERIALIZATION_REQUIRED"
                ),
                "blocking_reason": (
                    "physical R_CMB materialization accepted"
                    if accepted
                    else "requires accepted role coordinates, numeric readout values, and codomain checker pass"
                ),
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
    accepted = sum(row["materialization_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_physical_R_CMB_materialization_supply_table": rel(SUPPLY_TABLE),
        "input_physical_R_CMB_materialization_supply_summary": rel(SUPPLY_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "physical_R_CMB_materialization_acceptance_rows": len(rows),
        "materialization_accepted_rows": accepted,
        "materialization_rejected_rows": len(rows) - accepted,
        "role_coordinates_accepted_rows": sum(row["role_coordinates_accepted"] == "true" for row in rows),
        "physical_R_CMB_materialized_rows": sum(row["physical_R_CMB_materialized"] == "true" for row in rows),
        "numeric_values_materialized_rows": sum(row["numeric_values_materialized"] == "true" for row in rows),
        "codomain_checker_passed_rows": sum(row["codomain_checker_passed"] == "true" for row in rows),
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_ACCEPTANCE_AUDITED_REJECTED_ROLE_COORDINATE_NUMERIC_MATERIALIZATION_REQUIRED"
            if input_chain_clean() and len(rows) == 7 and accepted == 0
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_ACCEPTANCE_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_materialization_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Physical R_CMB Materialization Acceptance Audit v01

**Doc class:** physical R_CMB materialization acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit rejects supplied materialization candidates as physical R_CMB because
role coordinates are still blocked/not numerically materialized. It keeps score,
likelihood, and dark-sector verdict closed.

## Summary

```text
physical_R_CMB_materialization_acceptance_rows={summary["physical_R_CMB_materialization_acceptance_rows"]}
materialization_accepted_rows={summary["materialization_accepted_rows"]}
role_coordinates_accepted_rows={summary["role_coordinates_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB physical R_CMB materialization acceptance.")
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
