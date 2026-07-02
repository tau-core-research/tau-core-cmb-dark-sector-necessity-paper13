#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_implementation_scaffold_v01.json"
SCAFFOLD_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_implementation_scaffold_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_scaffold_output_acceptance_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_scaffold_output_acceptance_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_scaffold_output_acceptance_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_scaffold_output_acceptance_v01_"
    "structural_checker_outputs_accepted_for_certificate_implementation_development_only_"
    "no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "acceptance_row_id",
    "certificate_area",
    "checker_name",
    "scaffold_output",
    "scaffold_hash_output",
    "output_present",
    "hash_present",
    "hash_matches",
    "scaffold_checks_passed",
    "execution_succeeded",
    "checker_output_supplied",
    "certificate_passed",
    "domain_object_accepted",
    "accepted_as_scaffold_output",
    "accepted_for_certificate_implementation_development",
    "allows_certificate_pass",
    "allows_domain_acceptance",
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not SCAFFOLD_AUDIT.exists():
        return False
    audit = load_json(SCAFFOLD_AUDIT)
    return (
        audit.get("status") == "CARRIER_DOMAIN_CHECKER_IMPLEMENTATION_SCAFFOLD_AUDITED_SMOKE_EXECUTED_NOT_CERTIFICATE"
        and audit.get("failed_rows") == 0
        and audit.get("checker_scripts_present_rows") == 7
        and audit.get("scaffold_execution_succeeded_rows") == 7
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def hash_matches(output: Path, hash_output: Path) -> bool:
    if not output.exists() or not hash_output.exists():
        return False
    payload = load_json(hash_output)
    return payload.get("sha256") == sha256(output)


def table_rows() -> list[dict[str, str]]:
    report = load_json(SCAFFOLD_REPORT)
    rows: list[dict[str, str]] = []
    for index, checker in enumerate(report.get("checker_rows", []), start=1):
        output = ROOT / checker["scaffold_output"]
        hash_output = ROOT / checker["scaffold_hash_output"]
        result = load_json(output) if output.exists() else {}
        output_ok = (
            output.exists()
            and hash_output.exists()
            and hash_matches(output, hash_output)
            and result.get("scaffold_checks_passed") is True
            and result.get("execution_succeeded") is True
            and result.get("checker_output_supplied") is True
            and result.get("certificate_passed") is False
            and result.get("domain_object_accepted") is False
            and result.get("score_entry_allowed") is False
            and result.get("likelihood_allowed") is False
            and result.get("dark_sector_verdict_allowed") is False
        )
        rows.append(
            {
                "acceptance_row_id": f"TCMBCDCSOA01_{index:03d}",
                "certificate_area": checker["certificate_area"],
                "checker_name": checker["checker_name"],
                "scaffold_output": checker["scaffold_output"],
                "scaffold_hash_output": checker["scaffold_hash_output"],
                "output_present": str(output.exists()).lower(),
                "hash_present": str(hash_output.exists()).lower(),
                "hash_matches": str(hash_matches(output, hash_output)).lower(),
                "scaffold_checks_passed": str(result.get("scaffold_checks_passed") is True).lower(),
                "execution_succeeded": str(result.get("execution_succeeded") is True).lower(),
                "checker_output_supplied": str(result.get("checker_output_supplied") is True).lower(),
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "accepted_as_scaffold_output": str(output_ok).lower(),
                "accepted_for_certificate_implementation_development": str(output_ok).lower(),
                "allows_certificate_pass": "false",
                "allows_domain_acceptance": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "SCAFFOLD_OUTPUT_ACCEPTED_FOR_CERTIFICATE_IMPLEMENTATION_DEVELOPMENT_ONLY"
                    if output_ok
                    else "SCAFFOLD_OUTPUT_ACCEPTANCE_BLOCKED"
                ),
                "blocking_reason": (
                    "accepted only as non-certifying scaffold output for developing certificate-level checker logic"
                    if output_ok
                    else "requires present output, matching hash, passed scaffold checks, and closed downstream permissions"
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
        "report_id": "tau_cmb_carrier_domain_checker_scaffold_output_acceptance_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_scaffold_report": rel(SCAFFOLD_REPORT),
        "input_scaffold_audit": rel(SCAFFOLD_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "acceptance_rows": len(rows),
        "accepted_as_scaffold_output_rows": sum(row["accepted_as_scaffold_output"] == "true" for row in rows),
        "accepted_for_certificate_implementation_development_rows": sum(row["accepted_for_certificate_implementation_development"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
        "checker_output_supplied_rows": sum(row["checker_output_supplied"] == "true" for row in rows),
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_SCAFFOLD_OUTPUTS_ACCEPTED_FOR_CERTIFICATE_IMPLEMENTATION_DEVELOPMENT_ONLY"
            if input_chain_clean() and len(rows) == 7 and all(row["accepted_as_scaffold_output"] == "true" for row in rows)
            else "CARRIER_DOMAIN_CHECKER_SCAFFOLD_OUTPUT_ACCEPTANCE_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_level_checker_rule_implementation_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['certificate_area']}`: {row['acceptance_status']} | hash={row['hash_matches']} | scaffold={row['accepted_as_scaffold_output']}"
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Checker Scaffold Output Acceptance v01

**Doc class:** checker scaffold output acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit accepts the seven structural checker scaffold outputs only as inputs
for developing certificate-level checker implementations. It does not pass
certificates, accept domain objects, materialize physical `R_CMB`, open score
entry, compute likelihood, or decide the dark-sector question.

## Acceptance Rows

{row_text}

## Summary

```text
acceptance_rows={summary["acceptance_rows"]}
accepted_as_scaffold_output_rows={summary["accepted_as_scaffold_output_rows"]}
accepted_for_certificate_implementation_development_rows={summary["accepted_for_certificate_implementation_development_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
execution_succeeded_rows={summary["execution_succeeded_rows"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
accepted_domain_objects={summary["accepted_domain_objects"]}
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
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker scaffold output acceptance.")
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
