#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_ACCEPTANCE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_v01.csv"
PAYLOAD_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_summary_v01.json"
STRUCTURAL_R_CMB_AUDIT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_candidate_gate_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_v02.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_summary_v02.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_execution_packet_refresh_v02.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_execution_packet_refresh_v02_"
    "structural_R_CMB_candidate_visible_for_codomain_precheck_no_checker_attempt_no_certificate_pass_"
    "no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "refresh_row_id",
    "certificate_area",
    "checker_name",
    "accepted_input_rows",
    "required_input_rows",
    "payload_inputs_ready",
    "requires_R_CMB_candidate",
    "structural_R_CMB_candidate_available",
    "physical_R_CMB_materialized",
    "structural_precheck_ready",
    "full_checker_execution_ready",
    "execution_attempted",
    "execution_succeeded",
    "checker_output_supplied",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "refresh_status",
    "blocking_reason",
    "claim_boundary",
]

CHECKERS = [
    ("carrier_well_formedness", "run_carrier_ok_checker", 6, False),
    ("domain_membership_rule", "run_dom_ok_checker", 7, False),
    ("seed_admissibility", "run_seed_admissibility_checker", 9, False),
    ("null_control_admissibility", "run_null_control_checker", 9, False),
    ("source_object_admissibility", "run_source_object_checker", 8, False),
    ("quotient_and_equivalence_survival", "run_quotient_survival_checker", 10, False),
    ("codomain_compatibility", "run_codomain_ok_checker", 9, True),
    ("endpoint_firewall_replay", "run_endpoint_firewall_checker", 8, False),
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def payload_chain_clean() -> bool:
    if not PAYLOAD_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(PAYLOAD_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ACCEPTANCE_AUDITED_PAYLOADS_ACCEPTED_AS_CHECKER_INPUTS_ONLY"
        and summary.get("input_chain_clean") is True
        and summary.get("payload_accepted_rows") == 66
        and summary.get("checker_input_available_rows") == 66
        and summary.get("checker_execution_allowed_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def structural_candidate_clean() -> bool:
    if not STRUCTURAL_R_CMB_AUDIT.exists():
        return False
    audit = load_json(STRUCTURAL_R_CMB_AUDIT)
    return (
        audit.get("status") == "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_AUDITED_NOT_PHYSICAL"
        and audit.get("failed_rows") == 0
        and audit.get("structural_candidate_available_for_codomain_precheck") is True
        and audit.get("physical_R_CMB_materialized") is False
        and audit.get("score_entry_allowed") is False
        and audit.get("likelihood_allowed") is False
        and audit.get("dark_sector_verdict_allowed") is False
    )


def table_rows() -> list[dict[str, str]]:
    accepted_by_area: dict[str, int] = defaultdict(int)
    for row in read_csv(PAYLOAD_ACCEPTANCE):
        if row["payload_accepted"] == "true" and row["checker_input_available"] == "true":
            accepted_by_area[row["certificate_area"]] += 1

    structural_ok = structural_candidate_clean()
    rows: list[dict[str, str]] = []
    for index, (area, checker, required, needs_r_cmb) in enumerate(CHECKERS, start=1):
        accepted = accepted_by_area[area]
        payload_ready = accepted == required
        structural_ready = payload_ready and (not needs_r_cmb or structural_ok)
        full_ready = payload_ready and (not needs_r_cmb)
        rows.append(
            {
                "refresh_row_id": f"TCMBCDCEPR02_{index:03d}",
                "certificate_area": area,
                "checker_name": checker,
                "accepted_input_rows": str(accepted),
                "required_input_rows": str(required),
                "payload_inputs_ready": str(payload_ready).lower(),
                "requires_R_CMB_candidate": str(needs_r_cmb).lower(),
                "structural_R_CMB_candidate_available": str(structural_ok if needs_r_cmb else False).lower(),
                "physical_R_CMB_materialized": "false",
                "structural_precheck_ready": str(structural_ready).lower(),
                "full_checker_execution_ready": str(full_ready).lower(),
                "execution_attempted": "false",
                "execution_succeeded": "false",
                "checker_output_supplied": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "refresh_status": (
                    "CHECKER_FULL_EXECUTION_READY_NOT_ATTEMPTED"
                    if full_ready
                    else "CODOMAIN_STRUCTURAL_PRECHECK_READY_PHYSICAL_R_CMB_BLOCKED"
                    if structural_ready and needs_r_cmb
                    else "CHECKER_REFRESH_BLOCKED_BY_INPUTS"
                ),
                "blocking_reason": (
                    "checker input payloads are accepted; execution is a downstream explicit step"
                    if full_ready
                    else "structural R_CMB candidate is visible, but physical R_CMB materialization is still absent"
                    if structural_ready and needs_r_cmb
                    else "accepted checker-input payloads or structural R_CMB candidate are incomplete"
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
        "report_id": "tau_cmb_carrier_domain_checker_execution_packet_refresh_summary_v02",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_payload_acceptance_table": rel(PAYLOAD_ACCEPTANCE),
        "input_payload_acceptance_summary": rel(PAYLOAD_ACCEPTANCE_SUMMARY),
        "input_structural_R_CMB_candidate_audit": rel(STRUCTURAL_R_CMB_AUDIT),
        "input_chain_clean": payload_chain_clean() and structural_candidate_clean(),
        "refresh_rows": len(rows),
        "payload_ready_rows": sum(row["payload_inputs_ready"] == "true" for row in rows),
        "structural_precheck_ready_rows": sum(row["structural_precheck_ready"] == "true" for row in rows),
        "full_checker_execution_ready_rows": sum(row["full_checker_execution_ready"] == "true" for row in rows),
        "codomain_structural_precheck_ready_rows": sum(row["refresh_status"] == "CODOMAIN_STRUCTURAL_PRECHECK_READY_PHYSICAL_R_CMB_BLOCKED" for row in rows),
        "blocked_by_physical_R_CMB_rows": sum(row["requires_R_CMB_candidate"] == "true" and row["physical_R_CMB_materialized"] == "false" for row in rows),
        "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
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
            "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_V02_AUDIT_INPUTS_DECLARED_STRUCTURAL_PRECHECK_READY"
            if payload_chain_clean() and structural_candidate_clean()
            else "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_V02_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_execution_attempt_packet_v01_for_7_ready_rows_or_physical_R_CMB_materialization_gate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['certificate_area']}`: {row['refresh_status']} | structural_precheck={row['structural_precheck_ready']} | full_execution={row['full_checker_execution_ready']}"
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Checker Execution Packet Refresh v02

**Doc class:** carrier/domain checker execution packet refresh
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This refresh includes the audited structural `R_CMB` candidate shell in the
codomain-readiness accounting. It does not execute checkers, pass certificates,
accept domain objects, materialize physical `R_CMB`, open score entry, compute
a likelihood, or decide the dark-sector question.

## Refresh Rows

{row_text}

## Summary

```text
refresh_rows={summary["refresh_rows"]}
payload_ready_rows={summary["payload_ready_rows"]}
structural_precheck_ready_rows={summary["structural_precheck_ready_rows"]}
full_checker_execution_ready_rows={summary["full_checker_execution_ready_rows"]}
codomain_structural_precheck_ready_rows={summary["codomain_structural_precheck_ready_rows"]}
blocked_by_physical_R_CMB_rows={summary["blocked_by_physical_R_CMB_rows"]}
execution_attempted_rows={summary["execution_attempted_rows"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Status

```text
{summary["status"]}
```

The codomain row has a structural precheck target, but physical `R_CMB`
materialization remains absent.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB checker execution refresh v02 with structural R_CMB candidate.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
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
