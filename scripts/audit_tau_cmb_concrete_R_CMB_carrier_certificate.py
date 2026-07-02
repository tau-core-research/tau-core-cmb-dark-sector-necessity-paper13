#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CERT_TABLE = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_v01.csv"
CERT_SUMMARY = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_summary_v01.json"
GAP_MATRIX = ROOT / "data/derived/tau_cmb_scoring_input_gap_matrix_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01_audit_only_"
    "requirements_clean_but_carrier_not_certified_R_CMB_not_materialized_"
    "no_score_no_likelihood_no_verdict"
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
    required = [CERT_TABLE, CERT_SUMMARY, GAP_MATRIX]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    cert_rows = read_csv(CERT_TABLE)
    summary = load_json(CERT_SUMMARY)
    gap = load_json(GAP_MATRIX)
    components = [row.get("certificate_component") for row in cert_rows]
    expected = [
        "carrier_predicate",
        "domain_rule",
        "codomain_role_space",
        "concrete_readout_map",
        "null_anchor_compatibility",
        "dimension_gauge_replay",
        "endpoint_firewall",
    ]
    rows.append(audit_row(
        "certificate_row_shape",
        "PASS_CERTIFICATE_REQUIREMENT_ROWS_PRESENT" if components == expected else "FAIL_CERTIFICATE_REQUIREMENT_ROW_SHAPE",
        f"certificate_components={components}",
        components == expected,
        "carrier certificate audit requires the seven declared requirement components",
    ))

    input_ok = (
        summary.get("status") == "CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED"
        and summary.get("input_chain_clean") is True
        and gap.get("status") == "SCORING_INPUT_GAP_MATRIX_DECLARED_ALL_ROWS_BLOCKED_NO_SCORE"
    )
    rows.append(audit_row(
        "input_gap_chain",
        "PASS_GAP_MATRIX_CHAIN" if input_ok else "FAIL_GAP_MATRIX_CHAIN",
        "certificate requirements follow a clean scoring-input gap matrix",
        input_ok,
        "carrier certificate audit must be downstream of the scoring-input gap matrix",
    ))

    fields_ok = all(row.get("formal_object") and row.get("requirement") and row.get("evidence_source") for row in cert_rows)
    rows.append(audit_row(
        "requirement_fields_declared",
        "PASS_REQUIREMENT_FIELDS_DECLARED" if fields_ok else "FAIL_REQUIREMENT_FIELDS",
        "each certificate row declares formal object, requirement, and evidence source",
        fields_ok,
        "certificate requirements need formal object, requirement, and evidence source",
    ))

    accounting_ok = (
        len(cert_rows) == 7
        and summary.get("certificate_rows") == 7
        and summary.get("blocked_rows") == 6
        and summary.get("partial_rows") == 1
    )
    rows.append(audit_row(
        "block_partial_accounting",
        "PASS_BLOCK_PARTIAL_ACCOUNTING" if accounting_ok else "FAIL_BLOCK_PARTIAL_ACCOUNTING",
        f"certificate_rows={summary.get('certificate_rows')}, blocked_rows={summary.get('blocked_rows')}, partial_rows={summary.get('partial_rows')}",
        accounting_ok,
        "carrier certificate requirements should have six blocked rows and one partial codomain row",
    ))

    permissions_closed = (
        all(row.get("allows_carrier_certificate") == "false" for row in cert_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in cert_rows)
        and all(row.get("allows_score_entry") == "false" for row in cert_rows)
        and all(row.get("allows_likelihood") == "false" for row in cert_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in cert_rows)
        and summary.get("carrier_certificate_allowed") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_CERTIFICATE_FIREWALL_CLOSED" if permissions_closed else "FAIL_CERTIFICATE_FIREWALL",
        "carrier certificate, concrete R_CMB, score, likelihood, and verdict permissions remain closed",
        permissions_closed,
        "requirements artifact must not certify the carrier or open scoring",
    ))

    rows.append(audit_row(
        "carrier_and_domain",
        "BLOCKED_CARRIER_AND_DOMAIN_NOT_CERTIFIED",
        "carrier predicate and domain rule are requirements only",
        False,
        "requires accepted carrier predicate and Dom(R_CMB) rule",
    ))
    rows.append(audit_row(
        "concrete_readout_map",
        "BLOCKED_CONCRETE_R_CMB_NOT_MATERIALIZED",
        "R_CMB remains a schema/interface symbol rather than a concrete map",
        False,
        "requires concrete readout map or executable materialization rule",
    ))
    rows.append(audit_row(
        "replay_and_firewall",
        "BLOCKED_REPLAY_AND_FIREWALL_NOT_RUN",
        "dimension/gauge replay and endpoint firewall cannot pass before concrete R_CMB inputs exist",
        False,
        "requires replay certificate and endpoint firewall rerun after materialization",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(CERT_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "certificate_requirements_audited": clean,
        "carrier_certificate_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED"
            if clean
            else "CONCRETE_R_CMB_CARRIER_CERTIFICATE_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_predicate_candidate_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Concrete R_CMB Carrier Certificate Audit v01

**Doc class:** concrete readout carrier certificate requirements audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the finite requirement set for the CMB readout carrier and
concrete `R_CMB` map. It does not certify the carrier, materialize `R_CMB`, open
score entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The certificate requirements are audit-visible but blocked. The shortest next
step is to define a carrier/domain predicate candidate before attempting a
concrete readout map.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB concrete R_CMB carrier certificate requirements.")
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
