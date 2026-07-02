#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RULE_TABLE = ROOT / "data/derived/tau_cmb_certificate_level_checker_rule_implementation_v01.csv"
RULE_AUDIT = ROOT / "data/derived/tau_cmb_certificate_level_checker_rule_implementation_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_materialization_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_materialization_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_materialization_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_materialization_v01_"
    "missing_semantic_certificate_evidence_matrix_only_no_evidence_materialized_"
    "no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "evidence_row_id",
    "certificate_area",
    "checker_name",
    "semantic_evidence_field",
    "required_for_predicate",
    "candidate_evidence_artifact",
    "evidence_materialized",
    "evidence_accepted",
    "certificate_rule_executable_after_materialization",
    "certificate_passed",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "materialization_status",
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
    if not RULE_AUDIT.exists():
        return False
    audit = load_json(RULE_AUDIT)
    return (
        audit.get("status") == "CMB_CERTIFICATE_LEVEL_CHECKER_RULE_IMPLEMENTATION_AUDITED_BLOCKED_BY_SEMANTIC_EVIDENCE"
        and audit.get("failed_rows") == 0
        and audit.get("rule_implementation_declared_rows") == 7
        and audit.get("semantic_evidence_fields_present_rows") == 0
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rule in read_csv(RULE_TABLE):
        fields = [item.strip() for item in rule["required_semantic_evidence_fields"].split(";") if item.strip()]
        for field in fields:
            index = len(rows) + 1
            artifact = ROOT / "semantic_evidence" / rule["certificate_area"] / f"{field}_evidence_v01.json"
            rows.append(
                {
                    "evidence_row_id": f"TCMBCDSEM01_{index:03d}",
                    "certificate_area": rule["certificate_area"],
                    "checker_name": rule["checker_name"],
                    "semantic_evidence_field": field,
                    "required_for_predicate": rule["certificate_rule_predicates"],
                    "candidate_evidence_artifact": rel(artifact),
                    "evidence_materialized": "false",
                    "evidence_accepted": "false",
                    "certificate_rule_executable_after_materialization": "false",
                    "certificate_passed": "false",
                    "domain_object_accepted": "false",
                    "allows_physical_R_CMB": "false",
                    "allows_score_entry": "false",
                    "allows_likelihood": "false",
                    "allows_dark_sector_verdict": "false",
                    "materialization_status": "SEMANTIC_EVIDENCE_REQUIRED_NOT_MATERIALIZED",
                    "blocking_reason": "requires endpoint-blind semantic proof/evidence artifact before certificate rule execution",
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
    areas = sorted({row["certificate_area"] for row in rows})
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_materialization_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_rule_table": rel(RULE_TABLE),
        "input_rule_audit": rel(RULE_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "certificate_areas": areas,
        "certificate_area_count": len(areas),
        "semantic_evidence_rows": len(rows),
        "evidence_materialized_rows": sum(row["evidence_materialized"] == "true" for row in rows),
        "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
        "certificate_rule_executable_after_materialization_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_MATERIALIZATION_MATRIX_DECLARED_NOT_MATERIALIZED"
            if input_chain_clean() and len(rows) > 0
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_MATERIALIZATION_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_artifact_supply_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    by_area: dict[str, int] = {}
    for row in rows:
        by_area[row["certificate_area"]] = by_area.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} required semantic evidence fields" for area, count in by_area.items())
    text = f"""# Tau CMB Certificate Semantic Evidence Materialization v01

**Doc class:** semantic certificate evidence materialization matrix
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact converts the certificate-level checker rule blockers into a
field-level materialization matrix. It does not materialize or accept the
evidence. It identifies the endpoint-blind semantic evidence artifacts that
must exist before certificate execution can be attempted.

## Evidence Rows By Area

{area_text}

## Summary

```text
semantic_evidence_rows={summary["semantic_evidence_rows"]}
evidence_materialized_rows={summary["evidence_materialized_rows"]}
evidence_accepted_rows={summary["evidence_accepted_rows"]}
certificate_rule_executable_after_materialization_rows={summary["certificate_rule_executable_after_materialization_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB certificate semantic evidence materialization matrix.")
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
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
