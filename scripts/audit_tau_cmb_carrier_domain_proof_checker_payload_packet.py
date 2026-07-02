#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_v01.csv"
PAYLOAD_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_summary_v01.json"
CANDIDATE_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_proof_checker_payload_packet_audit_v01.md"

EXPECTED_AREAS = [
    "carrier_well_formedness",
    "domain_membership_rule",
    "seed_admissibility",
    "null_control_admissibility",
    "source_object_admissibility",
    "quotient_and_equivalence_survival",
    "codomain_compatibility",
    "endpoint_firewall_replay",
]

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_proof_checker_payload_packet_audit_v01_audit_only_"
    "payload_specs_clean_but_not_executed_no_certificate_pass_no_domain_acceptance_"
    "no_R_CMB_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    required = [PAYLOAD_TABLE, PAYLOAD_SUMMARY, CANDIDATE_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    payload_rows = read_csv(PAYLOAD_TABLE)
    summary = load_json(PAYLOAD_SUMMARY)
    candidate_audit = load_json(CANDIDATE_AUDIT)
    areas = [row.get("certificate_area") for row in payload_rows]
    shape_ok = areas == EXPECTED_AREAS
    rows.append(audit_row(
        "payload_row_shape",
        "PASS_EXPECTED_PAYLOAD_ROWS_PRESENT" if shape_ok else "FAIL_PAYLOAD_ROW_SHAPE",
        f"certificate_areas={areas}",
        shape_ok,
        "proof/checker payload packet requires the eight declared areas in order",
    ))

    input_ok = (
        summary.get("status") == "CARRIER_DOMAIN_PROOF_CHECKER_PAYLOAD_PACKET_DECLARED_NOT_EXECUTED"
        and summary.get("input_chain_clean") is True
        and candidate_audit.get("status") == "CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_AUDITED_UNPASSED_NOT_SCORE_READY"
        and candidate_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_candidate_chain",
        "PASS_PAYLOAD_INPUT_CHAIN" if input_ok else "FAIL_PAYLOAD_INPUT_CHAIN",
        "payload packet follows the audited unpassed certificate candidate",
        input_ok,
        "payload audit must be downstream of a clean unpassed certificate-candidate audit",
    ))

    field_ok = all(
        row.get("target_candidate_object")
        and row.get("payload_kind")
        and row.get("minimal_payload_spec")
        and row.get("checker_input_contract")
        and row.get("checker_output_contract")
        and row.get("required_replay")
        and row.get("blocking_reason")
        for row in payload_rows
    )
    rows.append(audit_row(
        "payload_fields_declared",
        "PASS_PAYLOAD_FIELDS_DECLARED" if field_ok else "FAIL_PAYLOAD_FIELDS",
        "each payload row declares target object, kind, minimal spec, input/output contracts, replay, and blocker",
        field_ok,
        "payload rows need target object, payload spec, contracts, replay, and blocking reason",
    ))

    accounting_ok = (
        len(payload_rows) == 8
        and summary.get("payload_rows") == 8
        and summary.get("payload_specs_declared") == 8
        and summary.get("checkers_executed") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "payload_accounting",
        "PASS_PAYLOAD_ACCOUNTING" if accounting_ok else "FAIL_PAYLOAD_ACCOUNTING",
        (
            f"payload_rows={summary.get('payload_rows')}, specs={summary.get('payload_specs_declared')}, "
            f"executed={summary.get('checkers_executed')}, passed={summary.get('certificate_passed_rows')}, "
            f"accepted_domain_objects={summary.get('accepted_domain_objects')}"
        ),
        accounting_ok,
        "payload packet should declare eight specs with zero executions, passes, and accepted domain objects",
    ))

    permissions_closed = (
        all(row.get("payload_spec_declared") == "true" for row in payload_rows)
        and all(row.get("checker_executed") == "false" for row in payload_rows)
        and all(row.get("certificate_passed") == "false" for row in payload_rows)
        and all(row.get("domain_object_accepted") == "false" for row in payload_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in payload_rows)
        and all(row.get("allows_score_entry") == "false" for row in payload_rows)
        and all(row.get("allows_likelihood") == "false" for row in payload_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in payload_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_PAYLOAD_FIREWALL_CLOSED" if permissions_closed else "FAIL_PAYLOAD_FIREWALL",
        "payload packet declares no checker execution, no pass, no accepted domain object, no concrete R_CMB, no score, no likelihood, and no verdict",
        permissions_closed,
        "payload packet must not execute checkers or open scoring",
    ))

    boundary_ok = all(
        "payload_spec_only" in row.get("claim_boundary", "")
        and "no_checker_execution" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in payload_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_PAYLOAD_CLAIM_BOUNDARY" if boundary_ok else "FAIL_PAYLOAD_CLAIM_BOUNDARY",
        "row claim boundaries mark the artifact as payload-spec-only with no execution, score, likelihood, or verdict",
        boundary_ok,
        "payload packet must preserve payload-spec-only claim boundary",
    ))

    rows.append(audit_row(
        "checker_execution",
        "BLOCKED_CHECKERS_NOT_EXECUTED",
        "proof/checker contracts exist but no checker or proof transcript has been executed",
        False,
        "requires execution packet or proof transcript for all payload rows",
    ))
    rows.append(audit_row(
        "certificate_passes",
        "BLOCKED_CERTIFICATES_NOT_PASSED",
        "no carrier/domain certificate pass follows from the payload specs alone",
        False,
        "requires audited checker outputs before certificate pass records",
    ))
    rows.append(audit_row(
        "domain_acceptance",
        "BLOCKED_DOMAIN_OBJECTS_NOT_ACCEPTED",
        "no seed, null, or source domain object is accepted",
        False,
        "requires domain-object acceptance record after certificate passes",
    ))
    rows.append(audit_row(
        "concrete_R_CMB",
        "BLOCKED_R_CMB_NOT_MATERIALIZED",
        "concrete R_CMB remains downstream of checker execution, certificate passes, and domain acceptance",
        False,
        "requires concrete R_CMB materialization candidate after accepted domain objects",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_proof_checker_payload_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(PAYLOAD_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "payload_packet_audited": clean,
        "checker_execution_allowed": False,
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "domain_object_acceptance_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_PROOF_CHECKER_PAYLOAD_PACKET_AUDITED_NOT_EXECUTED_NOT_SCORE_READY"
            if clean
            else "CARRIER_DOMAIN_PROOF_CHECKER_PAYLOAD_PACKET_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_execution_packet_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Proof Checker Payload Packet Audit v01

**Doc class:** carrier/domain proof/checker payload packet audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the carrier/domain proof/checker payload packet. It verifies
row shape, upstream lineage, payload field completeness, accounting, promotion
firewall closure, and claim-boundary discipline. It does not execute checkers,
pass certificates, accept domain objects, materialize `R_CMB`, open score
entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The payload packet is audit-visible and internally clean, but no proof/checker
has been executed. The next object should be an execution packet or proof
transcript package.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain proof/checker payload packet.")
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
