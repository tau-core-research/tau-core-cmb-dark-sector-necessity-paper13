#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_v01.csv"
CANDIDATE_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_summary_v01.json"
REQ_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_certificate_candidate_audit_v01.md"

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
    "tau_cmb_carrier_domain_certificate_candidate_audit_v01_audit_only_"
    "candidate_shape_clean_but_certificates_unpassed_domain_unaccepted_"
    "R_CMB_not_materialized_no_score_no_likelihood_no_verdict"
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
    required = [CANDIDATE_TABLE, CANDIDATE_SUMMARY, REQ_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    candidate_rows = read_csv(CANDIDATE_TABLE)
    summary = load_json(CANDIDATE_SUMMARY)
    req_audit = load_json(REQ_AUDIT)
    areas = [row.get("certificate_area") for row in candidate_rows]
    shape_ok = areas == EXPECTED_AREAS
    rows.append(audit_row(
        "candidate_row_shape",
        "PASS_EXPECTED_CANDIDATE_ROWS_PRESENT" if shape_ok else "FAIL_CANDIDATE_ROW_SHAPE",
        f"certificate_areas={areas}",
        shape_ok,
        "carrier/domain certificate candidate requires the eight declared areas in order",
    ))

    input_ok = (
        summary.get("status") == "CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_DECLARED_UNPASSED"
        and summary.get("input_chain_clean") is True
        and req_audit.get("status") == "CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED_NOT_SCORE_READY"
        and req_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_requirements_chain",
        "PASS_CANDIDATE_INPUT_CHAIN" if input_ok else "FAIL_CANDIDATE_INPUT_CHAIN",
        "candidate follows the audited carrier/domain certificate requirements",
        input_ok,
        "candidate audit must be downstream of a clean blocked requirements audit",
    ))

    field_ok = all(
        row.get("candidate_certificate_object")
        and row.get("candidate_certificate_content")
        and row.get("required_payload")
        and row.get("current_payload")
        and row.get("acceptance_blocker")
        for row in candidate_rows
    )
    rows.append(audit_row(
        "candidate_fields_declared",
        "PASS_CANDIDATE_FIELDS_DECLARED" if field_ok else "FAIL_CANDIDATE_FIELDS",
        "each candidate row declares object, content, required payload, current payload, and blocker",
        field_ok,
        "candidate rows need certificate object, payload, and acceptance blocker",
    ))

    accounting_ok = (
        len(candidate_rows) == 8
        and summary.get("candidate_rows") == 8
        and summary.get("declared_candidate_rows") == 8
        and summary.get("carrier_certificate_passed_rows") == 0
        and summary.get("domain_certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "candidate_accounting",
        "PASS_CANDIDATE_ACCOUNTING" if accounting_ok else "FAIL_CANDIDATE_ACCOUNTING",
        (
            f"candidate_rows={summary.get('candidate_rows')}, "
            f"declared={summary.get('declared_candidate_rows')}, "
            f"carrier_passed={summary.get('carrier_certificate_passed_rows')}, "
            f"domain_passed={summary.get('domain_certificate_passed_rows')}, "
            f"accepted_domain_objects={summary.get('accepted_domain_objects')}"
        ),
        accounting_ok,
        "candidate package should declare eight rows with zero passed certificates and zero accepted domain objects",
    ))

    permissions_closed = (
        all(row.get("certificate_candidate_declared") == "true" for row in candidate_rows)
        and all(row.get("carrier_certificate_passed") == "false" for row in candidate_rows)
        and all(row.get("domain_certificate_passed") == "false" for row in candidate_rows)
        and all(row.get("domain_object_accepted") == "false" for row in candidate_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in candidate_rows)
        and all(row.get("allows_score_entry") == "false" for row in candidate_rows)
        and all(row.get("allows_likelihood") == "false" for row in candidate_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in candidate_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_CANDIDATE_FIREWALL_CLOSED" if permissions_closed else "FAIL_CANDIDATE_FIREWALL",
        "candidate declares no pass, no accepted domain object, no concrete R_CMB, no score, no likelihood, and no verdict",
        permissions_closed,
        "certificate candidate must not pass certificates or open scoring",
    ))

    boundary_ok = all(
        "candidate_only" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in candidate_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_CANDIDATE_CLAIM_BOUNDARY" if boundary_ok else "FAIL_CANDIDATE_CLAIM_BOUNDARY",
        "row claim boundaries mark the artifact as candidate-only with no score, no likelihood, and no verdict",
        boundary_ok,
        "certificate candidate must preserve candidate-only claim boundary",
    ))

    rows.append(audit_row(
        "proof_checker_payloads",
        "BLOCKED_PROOF_CHECKER_PAYLOADS_MISSING",
        "CarrierOK, DomOK, admissibility, quotient, codomain, and firewall candidates lack proof/checker payloads",
        False,
        "requires a proof/checker payload packet for all candidate objects",
    ))
    rows.append(audit_row(
        "certificate_passes",
        "BLOCKED_CERTIFICATES_UNPASSED",
        "no carrier or domain certificate pass is recorded",
        False,
        "requires audited pass records before any domain object can be accepted",
    ))
    rows.append(audit_row(
        "domain_acceptance",
        "BLOCKED_DOMAIN_OBJECTS_UNACCEPTED",
        "seed, null, and source domain objects remain unaccepted",
        False,
        "requires accepted domain-object records after certificate passes",
    ))
    rows.append(audit_row(
        "concrete_R_CMB",
        "BLOCKED_R_CMB_NOT_MATERIALIZED",
        "no concrete R_CMB can be materialized until certificates pass and domain objects are accepted",
        False,
        "requires concrete R_CMB materialization candidate after accepted carrier/domain certificates",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_certificate_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(CANDIDATE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "candidate_audited": clean,
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "domain_object_acceptance_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_AUDITED_UNPASSED_NOT_SCORE_READY"
            if clean
            else "CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_proof_checker_payload_packet_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Certificate Candidate Audit v01

**Doc class:** carrier/domain certificate candidate audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the carrier/domain certificate candidate. It verifies row
shape, upstream lineage, payload-slot completeness, accounting, promotion
firewall closure, and claim-boundary discipline. It does not pass certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The candidate is audit-visible and internally clean, but no certificate has
passed. The next object should provide proof/checker payloads for the named
candidate certificates.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain certificate candidate.")
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
