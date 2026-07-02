#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQ_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_v01.csv"
REQ_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_summary_v01.json"
PREDICATE_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_audit_v01.json"
SINGLE_PASS = ROOT / "data/derived/tau_cmb_single_pass_derivation_spine_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_certificate_requirements_audit_v01.md"

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
    "tau_cmb_carrier_domain_certificate_requirements_audit_v01_audit_only_"
    "requirements_clean_but_carrier_not_certified_domain_not_certified_"
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
    required = [REQ_TABLE, REQ_SUMMARY, PREDICATE_AUDIT, SINGLE_PASS]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    req_rows = read_csv(REQ_TABLE)
    summary = load_json(REQ_SUMMARY)
    predicate = load_json(PREDICATE_AUDIT)
    single_pass = load_json(SINGLE_PASS)
    areas = [row.get("certificate_area") for row in req_rows]
    shape_ok = areas == EXPECTED_AREAS
    rows.append(audit_row(
        "requirement_row_shape",
        "PASS_EXPECTED_REQUIREMENT_ROWS_PRESENT" if shape_ok else "FAIL_REQUIREMENT_ROW_SHAPE",
        f"certificate_areas={areas}",
        shape_ok,
        "carrier/domain certificate requirements require the eight declared areas in order",
    ))

    input_ok = (
        summary.get("status") == "CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED"
        and summary.get("input_chain_clean") is True
        and predicate.get("status") == "CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDITED_BLOCKED_NOT_SCORE_READY"
        and predicate.get("failed_rows") == 0
        and single_pass.get("status") == "SINGLE_PASS_DERIVATION_SPINE_DECLARED_ROUTE_BLOCKED_NOT_SCORE_READY"
        and single_pass.get("input_chain_consistent_with_blocked_route") is True
    )
    rows.append(audit_row(
        "input_chain",
        "PASS_REQUIREMENTS_INPUT_CHAIN" if input_ok else "FAIL_REQUIREMENTS_INPUT_CHAIN",
        "requirements follow the predicate audit and single-pass blocked route",
        input_ok,
        "requirements audit must be downstream of the blocked predicate audit and single-pass spine",
    ))

    field_ok = all(
        row.get("formal_requirement")
        and row.get("acceptance_condition")
        and row.get("required_evidence")
        and row.get("current_evidence")
        and row.get("blocking_reason")
        for row in req_rows
    )
    rows.append(audit_row(
        "requirement_fields_declared",
        "PASS_REQUIREMENT_FIELDS_DECLARED" if field_ok else "FAIL_REQUIREMENT_FIELDS",
        "each requirement row declares formal requirement, acceptance condition, evidence, and blocker",
        field_ok,
        "requirements need formal statement, acceptance condition, evidence, and blocking reason",
    ))

    accounting_ok = (
        len(req_rows) == 8
        and summary.get("requirement_rows") == 8
        and summary.get("blocked_requirement_rows") == 8
    )
    rows.append(audit_row(
        "requirement_accounting",
        "PASS_REQUIREMENT_ACCOUNTING" if accounting_ok else "FAIL_REQUIREMENT_ACCOUNTING",
        f"requirement_rows={summary.get('requirement_rows')}, blocked_requirement_rows={summary.get('blocked_requirement_rows')}",
        accounting_ok,
        "requirements package should contain eight blocked requirement rows",
    ))

    permissions_closed = (
        all(row.get("allows_carrier_certificate") == "false" for row in req_rows)
        and all(row.get("allows_domain_certificate") == "false" for row in req_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in req_rows)
        and all(row.get("allows_score_entry") == "false" for row in req_rows)
        and all(row.get("allows_likelihood") == "false" for row in req_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in req_rows)
        and summary.get("carrier_certificate_allowed") is False
        and summary.get("domain_certificate_allowed") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_REQUIREMENTS_FIREWALL_CLOSED" if permissions_closed else "FAIL_REQUIREMENTS_FIREWALL",
        "carrier, domain, concrete R_CMB, score, likelihood, and verdict permissions remain closed",
        permissions_closed,
        "requirements artifact must not certify carrier/domain or open score entry",
    ))

    boundary_ok = all(
        "requirements_only" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in req_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_REQUIREMENTS_CLAIM_BOUNDARY" if boundary_ok else "FAIL_REQUIREMENTS_CLAIM_BOUNDARY",
        "row claim boundaries mark the artifact as requirements-only with no score and no verdict",
        boundary_ok,
        "requirements must preserve requirements-only claim boundary",
    ))

    rows.append(audit_row(
        "carrier_and_domain_certificate",
        "BLOCKED_CARRIER_AND_DOMAIN_CERTIFICATES_NOT_BUILT",
        "CarrierOK and DomOK are finite requirements but no certificate object is built",
        False,
        "requires a carrier/domain certificate candidate with proof/checker payloads",
    ))
    rows.append(audit_row(
        "seed_null_source_admissibility",
        "BLOCKED_ADMISSIBILITY_OBJECTS_NOT_ACCEPTED",
        "seed, null control, and source objects remain admissibility requirements rather than accepted domain elements",
        False,
        "requires accepted seed/null/source domain objects and replay evidence",
    ))
    rows.append(audit_row(
        "quotient_and_codomain",
        "BLOCKED_QUOTIENT_SURVIVAL_AND_CODOMAIN_OUTPUT",
        "non-null quotient survival and concrete role-codomain output are not yet proved",
        False,
        "requires quotient survival certificate and concrete codomain output typing",
    ))
    rows.append(audit_row(
        "concrete_R_CMB_and_firewall",
        "BLOCKED_R_CMB_MATERIALIZATION_AND_FIREWALL",
        "concrete R_CMB materialization and post-population endpoint firewall remain downstream",
        False,
        "requires concrete R_CMB candidate followed by firewall replay",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_certificate_requirements_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(REQ_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "requirements_audited": clean,
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED_NOT_SCORE_READY"
            if clean
            else "CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_certificate_candidate_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Certificate Requirements Audit v01

**Doc class:** carrier/domain certificate requirements audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the finite carrier/domain certificate requirement set. It
verifies row shape, upstream lineage, field completeness, accounting, promotion
firewall closure, and claim-boundary discipline. It does not certify the
carrier, certify `Dom(R_CMB)`, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The requirement set is audit-visible and internally clean, but still blocked.
The next object may be a certificate candidate; it still cannot open scoring.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain certificate requirements.")
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
