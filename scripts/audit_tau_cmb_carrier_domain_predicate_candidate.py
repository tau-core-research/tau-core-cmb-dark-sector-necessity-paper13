#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_v01.csv"
CANDIDATE_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_summary_v01.json"
CERT_AUDIT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_predicate_candidate_audit_v01.md"

EXPECTED_COMPONENTS = [
    "carrier_membership",
    "domain_membership",
    "null_control_admissibility",
    "source_object_admissibility",
    "forbidden_endpoint_dependency",
]

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_predicate_candidate_audit_v01_audit_only_"
    "predicate_shape_clean_but_carrier_not_certified_domain_not_certified_"
    "R_CMB_not_materialized_no_score_no_verdict"
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
    required = [CANDIDATE_TABLE, CANDIDATE_SUMMARY, CERT_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    candidate_rows = read_csv(CANDIDATE_TABLE)
    summary = load_json(CANDIDATE_SUMMARY)
    cert_audit = load_json(CERT_AUDIT)
    components = [row.get("predicate_component") for row in candidate_rows]
    shape_ok = components == EXPECTED_COMPONENTS
    rows.append(audit_row(
        "predicate_row_shape",
        "PASS_EXPECTED_PREDICATE_ROWS_PRESENT" if shape_ok else "FAIL_PREDICATE_ROW_SHAPE",
        f"predicate_components={components}",
        shape_ok,
        "carrier/domain predicate candidate requires the five declared predicate components",
    ))

    input_ok = (
        summary.get("status") == "CARRIER_DOMAIN_PREDICATE_CANDIDATE_DECLARED_NOT_CERTIFIED"
        and summary.get("input_chain_clean") is True
        and cert_audit.get("status") == "CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED"
        and cert_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_certificate_chain",
        "PASS_CERTIFICATE_AUDIT_CHAIN" if input_ok else "FAIL_CERTIFICATE_AUDIT_CHAIN",
        "predicate candidate follows the audited concrete R_CMB carrier-certificate requirements",
        input_ok,
        "carrier/domain predicate audit must be downstream of a clean blocked carrier-certificate audit",
    ))

    field_ok = all(
        row.get("formal_predicate")
        and row.get("candidate_rule")
        and row.get("required_evidence")
        and row.get("current_evidence")
        and row.get("blocking_reason")
        for row in candidate_rows
    )
    rows.append(audit_row(
        "predicate_fields_declared",
        "PASS_PREDICATE_FIELDS_DECLARED" if field_ok else "FAIL_PREDICATE_FIELDS",
        "each predicate row declares formal predicate, candidate rule, evidence, and blocker",
        field_ok,
        "predicate rows need formal predicate, rule, evidence, and blocking reason",
    ))

    accounting_ok = (
        len(candidate_rows) == 5
        and summary.get("predicate_rows") == 5
        and summary.get("candidate_rows") == 4
        and summary.get("firewall_rows") == 1
    )
    rows.append(audit_row(
        "candidate_accounting",
        "PASS_CANDIDATE_ACCOUNTING" if accounting_ok else "FAIL_CANDIDATE_ACCOUNTING",
        f"predicate_rows={summary.get('predicate_rows')}, candidate_rows={summary.get('candidate_rows')}, firewall_rows={summary.get('firewall_rows')}",
        accounting_ok,
        "predicate candidate should contain four candidate rows and one firewall row",
    ))

    permissions_closed = (
        all(row.get("allows_carrier_certificate") == "false" for row in candidate_rows)
        and all(row.get("allows_domain_certificate") == "false" for row in candidate_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in candidate_rows)
        and all(row.get("allows_score_entry") == "false" for row in candidate_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in candidate_rows)
        and summary.get("carrier_certificate_allowed") is False
        and summary.get("domain_certificate_allowed") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_PREDICATE_FIREWALL_CLOSED" if permissions_closed else "FAIL_PREDICATE_FIREWALL",
        "carrier, domain, concrete R_CMB, score, and verdict permissions remain closed",
        permissions_closed,
        "predicate candidate must not certify carrier/domain or open score entry",
    ))

    claim_boundary_ok = all(
        "candidate_only" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in candidate_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_CANDIDATE_CLAIM_BOUNDARY" if claim_boundary_ok else "FAIL_CANDIDATE_CLAIM_BOUNDARY",
        "row claim boundaries mark the artifact as candidate-only with no score and no verdict",
        claim_boundary_ok,
        "predicate candidate must preserve candidate-only claim boundary",
    ))

    rows.append(audit_row(
        "carrier_certificate",
        "BLOCKED_CARRIER_PREDICATE_NOT_PROVED",
        "WellFormedRoleRepresentative_CMB is declared but not proved as a carrier certificate",
        False,
        "requires proof or executable checker for carrier membership",
    ))
    rows.append(audit_row(
        "domain_certificate",
        "BLOCKED_DOMAIN_RULE_NOT_CERTIFIED",
        "Dom(R_CMB) requires support, normalization, firewall, and replay evidence not yet certified jointly",
        False,
        "requires accepted domain rule over seed, null, and source objects",
    ))
    rows.append(audit_row(
        "concrete_readout_map",
        "BLOCKED_R_CMB_NOT_MATERIALIZED",
        "predicate audit does not materialize a concrete CMB readout map",
        False,
        "requires concrete R_CMB materialization after carrier/domain certification",
    ))
    rows.append(audit_row(
        "source_object_and_null_admissibility",
        "BLOCKED_SOURCE_AND_NULL_OBJECTS_NOT_ACCEPTED",
        "source objects and null control remain candidate/admissibility rules rather than accepted domain elements",
        False,
        "requires endpoint-blind source object packet plus null-domain replay",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_predicate_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(CANDIDATE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "predicate_candidate_audited": clean,
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDITED_BLOCKED_NOT_SCORE_READY"
            if clean
            else "CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_certificate_requirements_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Predicate Candidate Audit v01

**Doc class:** carrier/domain predicate candidate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the candidate carrier/domain predicate for the CMB readout
route. It verifies predicate-row shape, upstream certificate-audit lineage,
field completeness, accounting, promotion-firewall closure, and claim-boundary
discipline. It does not certify the carrier, certify `Dom(R_CMB)`, materialize
`R_CMB`, open score entry, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The predicate candidate is audit-visible and internally clean, but still
blocked. It narrows the next proof obligation to a carrier/domain certificate
requirements artifact.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain predicate candidate.")
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
