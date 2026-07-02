#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REFRESH_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_v02.csv"
REFRESH_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v02.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_attempt_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_attempt_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_execution_attempt_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_execution_attempt_packet_v01_"
    "seven_ready_rows_attempt_audited_but_checker_implementations_absent_"
    "no_execution_success_no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "attempt_row_id",
    "source_refresh_row_id",
    "certificate_area",
    "checker_name",
    "expected_checker_script",
    "input_payload_ready",
    "full_checker_execution_ready",
    "checker_implementation_present",
    "execution_attempt_declared",
    "execution_attempted",
    "execution_succeeded",
    "checker_output_supplied",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "attempt_status",
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


def script_for(checker_name: str) -> Path:
    return ROOT / "scripts" / f"{checker_name}.py"


def refresh_chain_clean() -> bool:
    if not REFRESH_AUDIT.exists():
        return False
    audit = load_json(REFRESH_AUDIT)
    return (
        audit.get("status") == "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_V02_AUDITED_STRUCTURAL_PRECHECK_READY"
        and audit.get("failed_rows") == 0
        and audit.get("full_checker_execution_ready_rows") == 7
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    refresh_rows = read_csv(REFRESH_TABLE)
    ready_rows = [row for row in refresh_rows if row.get("full_checker_execution_ready") == "true"]
    rows: list[dict[str, str]] = []
    for index, row in enumerate(ready_rows, start=1):
        checker_name = row["checker_name"]
        checker_script = script_for(checker_name)
        present = checker_script.exists()
        rows.append(
            {
                "attempt_row_id": f"TCMBCDCEAP01_{index:03d}",
                "source_refresh_row_id": row["refresh_row_id"],
                "certificate_area": row["certificate_area"],
                "checker_name": checker_name,
                "expected_checker_script": rel(checker_script),
                "input_payload_ready": row["payload_inputs_ready"],
                "full_checker_execution_ready": row["full_checker_execution_ready"],
                "checker_implementation_present": str(present).lower(),
                "execution_attempt_declared": "true",
                "execution_attempted": str(present).lower(),
                "execution_succeeded": "false",
                "checker_output_supplied": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "attempt_status": (
                    "CHECKER_EXECUTION_ATTEMPT_DECLARED_IMPLEMENTATION_PRESENT_NOT_RUN_BY_PACKET"
                    if present
                    else "CHECKER_EXECUTION_ATTEMPT_BLOCKED_IMPLEMENTATION_ABSENT"
                ),
                "blocking_reason": (
                    "checker implementation exists but this packet only declares attempt eligibility; a separate runner must execute and hash outputs"
                    if present
                    else f"missing executable checker implementation: {rel(checker_script)}"
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
    present = sum(row["checker_implementation_present"] == "true" for row in rows)
    attempted = sum(row["execution_attempted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_carrier_domain_checker_execution_attempt_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_refresh_table": rel(REFRESH_TABLE),
        "input_refresh_audit": rel(REFRESH_AUDIT),
        "input_chain_clean": refresh_chain_clean(),
        "attempt_packet_rows": len(rows),
        "ready_input_rows": sum(row["full_checker_execution_ready"] == "true" for row in rows),
        "checker_implementation_present_rows": present,
        "checker_implementation_absent_rows": len(rows) - present,
        "execution_attempt_declared_rows": sum(row["execution_attempt_declared"] == "true" for row in rows),
        "execution_attempted_rows": attempted,
        "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
        "checker_output_supplied_rows": sum(row["checker_output_supplied"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_EXECUTION_ATTEMPT_PACKET_DECLARED_BLOCKED_IMPLEMENTATIONS_ABSENT"
            if refresh_chain_clean() and len(rows) == 7 and present == 0
            else "CARRIER_DOMAIN_CHECKER_EXECUTION_ATTEMPT_PACKET_DECLARED_PARTIAL_IMPLEMENTATION_PRESENT"
            if refresh_chain_clean() and len(rows) == 7
            else "CARRIER_DOMAIN_CHECKER_EXECUTION_ATTEMPT_PACKET_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_implementation_scaffold_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['certificate_area']}`: {row['attempt_status']} | implementation={row['checker_implementation_present']} | `{row['expected_checker_script']}`"
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Checker Execution Attempt Packet v01

**Doc class:** carrier/domain checker execution attempt packet
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet is the first explicit execution-attempt layer after the v02 checker
refresh. It includes only rows that were already full-checker-execution-ready
in v02. It does not include the codomain row, because physical
`R_CMB` materialization is still absent.

## Attempt Rows

{row_text}

## Summary

```text
attempt_packet_rows={summary["attempt_packet_rows"]}
ready_input_rows={summary["ready_input_rows"]}
checker_implementation_present_rows={summary["checker_implementation_present_rows"]}
checker_implementation_absent_rows={summary["checker_implementation_absent_rows"]}
execution_attempt_declared_rows={summary["execution_attempt_declared_rows"]}
execution_attempted_rows={summary["execution_attempted_rows"]}
execution_succeeded_rows={summary["execution_succeeded_rows"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
accepted_domain_objects={summary["accepted_domain_objects"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Status

```text
{summary["status"]}
```

The route has now reached executable-checker implementation as the narrow
blocker for the seven non-codomain checker rows.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB checker execution attempt packet v01.")
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
