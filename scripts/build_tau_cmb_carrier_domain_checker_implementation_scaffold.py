#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "data/derived/tau_cmb_checker_scaffold_outputs"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_implementation_scaffold_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_implementation_scaffold_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_implementation_scaffold_v01_"
    "checker_scripts_and_structural_scaffold_outputs_present_not_certificate_pass_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

CHECKERS = [
    ("carrier_well_formedness", "run_carrier_ok_checker"),
    ("domain_membership_rule", "run_dom_ok_checker"),
    ("seed_admissibility", "run_seed_admissibility_checker"),
    ("null_control_admissibility", "run_null_control_checker"),
    ("source_object_admissibility", "run_source_object_checker"),
    ("quotient_and_equivalence_survival", "run_quotient_survival_checker"),
    ("endpoint_firewall_replay", "run_endpoint_firewall_checker"),
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def checker_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for area, checker in CHECKERS:
        script = ROOT / "scripts" / f"{checker}.py"
        output = OUTPUT_ROOT / f"{checker}_scaffold_result_v01.json"
        hashes = OUTPUT_ROOT / f"{checker}_scaffold_result_v01.hashes.json"
        result = load_json(output) if output.exists() else {}
        rows.append(
            {
                "certificate_area": area,
                "checker_name": checker,
                "checker_script": rel(script),
                "checker_script_present": script.exists(),
                "scaffold_output": rel(output),
                "scaffold_output_present": output.exists(),
                "scaffold_hash_output": rel(hashes),
                "scaffold_hash_output_present": hashes.exists(),
                "scaffold_checks_passed": result.get("scaffold_checks_passed") is True,
                "execution_succeeded": result.get("execution_succeeded") is True,
                "checker_output_supplied": result.get("checker_output_supplied") is True,
                "certificate_passed": result.get("certificate_passed") is True,
                "domain_object_accepted": result.get("domain_object_accepted") is True,
                "score_entry_allowed": result.get("score_entry_allowed") is True,
                "likelihood_allowed": result.get("likelihood_allowed") is True,
                "dark_sector_verdict_allowed": result.get("dark_sector_verdict_allowed") is True,
                "status": result.get("status", "CHECKER_SCAFFOLD_OUTPUT_MISSING"),
            }
        )
    return rows


def build_report() -> dict[str, Any]:
    rows = checker_rows()
    return {
        "report_id": "tau_cmb_carrier_domain_checker_implementation_scaffold_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "checker_rows": rows,
        "checker_script_rows": len(rows),
        "checker_scripts_present_rows": sum(row["checker_script_present"] for row in rows),
        "scaffold_output_present_rows": sum(row["scaffold_output_present"] for row in rows),
        "scaffold_hash_output_present_rows": sum(row["scaffold_hash_output_present"] for row in rows),
        "scaffold_checks_passed_rows": sum(row["scaffold_checks_passed"] for row in rows),
        "execution_succeeded_rows": sum(row["execution_succeeded"] for row in rows),
        "checker_output_supplied_rows": sum(row["checker_output_supplied"] for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] for row in rows),
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_IMPLEMENTATION_SCAFFOLD_PRESENT_AND_SMOKE_EXECUTED_NOT_CERTIFICATE"
            if all(row["checker_script_present"] and row["scaffold_checks_passed"] for row in rows)
            else "CARRIER_DOMAIN_CHECKER_IMPLEMENTATION_SCAFFOLD_INCOMPLETE"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_scaffold_output_acceptance_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['certificate_area']}`: script={str(row['checker_script_present']).lower()} | output={str(row['scaffold_output_present']).lower()} | status={row['status']}"
        for row in report["checker_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Implementation Scaffold v01

**Doc class:** checker implementation scaffold manifest
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {report["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This manifest records the seven non-codomain checker scaffold scripts and their
structural scaffold outputs. These scripts perform endpoint-blind input
validation only. They do not pass carrier/domain certificates, accept domain
objects, materialize physical `R_CMB`, open score entry, compute likelihood, or
decide the dark-sector question.

## Checker Rows

{row_text}

## Summary

```text
checker_script_rows={report["checker_script_rows"]}
checker_scripts_present_rows={report["checker_scripts_present_rows"]}
scaffold_output_present_rows={report["scaffold_output_present_rows"]}
scaffold_checks_passed_rows={report["scaffold_checks_passed_rows"]}
execution_succeeded_rows={report["execution_succeeded_rows"]}
certificate_passed_rows={report["certificate_passed_rows"]}
accepted_domain_objects={report["accepted_domain_objects"]}
score_entry_allowed={report["score_entry_allowed"]}
likelihood_allowed={report["likelihood_allowed"]}
dark_sector_verdict_allowed={report["dark_sector_verdict_allowed"]}
```

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB checker implementation scaffold manifest.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
