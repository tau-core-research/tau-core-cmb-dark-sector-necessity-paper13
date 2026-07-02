#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COORDINATE_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_null_v01.csv"
COORDINATE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_null_summary_v01.json"
RADIATION_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_audit_v01.json"
ZERO_CONTROL_AUDIT = ROOT / "data/derived/tau_cmb_seed_zero_control_audit_v01.json"
QUOTIENT_AUDIT = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_null_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_null_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_null_audit_v01_audit_only_"
    "null_not_accepted_no_physical_response_no_quotient_proof_no_concrete_R_CMB_"
    "no_carrier_certification_no_score_no_verdict"
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
    required = [COORDINATE_TABLE, COORDINATE_SUMMARY, RADIATION_AUDIT, ZERO_CONTROL_AUDIT, QUOTIENT_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    coord_rows = read_csv(COORDINATE_TABLE)
    summary = load_json(COORDINATE_SUMMARY)
    radiation_audit = load_json(RADIATION_AUDIT)
    zero_audit = load_json(ZERO_CONTROL_AUDIT)
    quotient_audit = load_json(QUOTIENT_AUDIT)
    components = [row.get("coordinate_component") for row in coord_rows]
    expected = [
        "null_seed_anchor",
        "null_readout_anchor",
        "quotient_relation_hook",
        "zero_source_consistency",
        "forbidden_promotion",
    ]
    rows.append(audit_row(
        "coordinate_row_shape",
        "PASS_NULL_COORDINATE_ROWS_PRESENT" if components == expected else "FAIL_NULL_COORDINATE_ROW_SHAPE",
        f"coordinate_components={components}",
        components == expected,
        "null coordinate audit requires the five declared components",
    ))

    input_ok = (
        summary.get("status") == "NULL_ROLE_COORDINATE_CONTROL_CANDIDATE_DECLARED_BLOCKED_NOT_ACCEPTED"
        and summary.get("input_control_chain_clean") is True
        and radiation_audit.get("status") == "RADIATION_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED"
        and radiation_audit.get("failed_rows") == 0
        and zero_audit.get("status") == "SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED"
        and zero_audit.get("failed_rows") == 0
        and quotient_audit.get("status") == "SEED_READOUT_QUOTIENT_RELATION_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED"
        and quotient_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_control_chain",
        "PASS_CONTROL_AUDIT_CHAIN" if input_ok else "FAIL_CONTROL_AUDIT_CHAIN",
        "null coordinate follows clean radiation, zero-control, and quotient-relation candidate audits",
        input_ok,
        "null coordinate audit must be downstream of clean control-chain audits",
    ))

    formal_slots_ok = all(row.get("formal_slot") for row in coord_rows)
    rows.append(audit_row(
        "formal_slots_declared",
        "PASS_FORMAL_SLOTS_DECLARED" if formal_slots_ok else "FAIL_FORMAL_SLOTS",
        "each null coordinate component has a formal slot",
        formal_slots_ok,
        "coordinate components need formal slots before materialization",
    ))

    dimension_roles_ok = all(row.get("dimension_role") for row in coord_rows)
    rows.append(audit_row(
        "dimension_roles_declared",
        "PASS_DIMENSION_ROLES_DECLARED" if dimension_roles_ok else "FAIL_DIMENSION_ROLES",
        "each null coordinate component has a control/dimension role",
        dimension_roles_ok,
        "null coordinate typing requires explicit control roles",
    ))

    source_dependencies_ok = all(row.get("source_dependency") for row in coord_rows)
    rows.append(audit_row(
        "source_dependencies_declared",
        "PASS_SOURCE_DEPENDENCIES_DECLARED" if source_dependencies_ok else "FAIL_SOURCE_DEPENDENCIES",
        "each null coordinate component is tied to existing zero-control or quotient artifacts",
        source_dependencies_ok,
        "null coordinate candidate must remain traceable to control artifacts",
    ))

    blocked_count = sum(row.get("coordinate_status", "").startswith("BLOCKED") for row in coord_rows)
    guard_count = sum("GUARD" in row.get("coordinate_status", "") or "FORBIDDEN" in row.get("coordinate_status", "") for row in coord_rows)
    block_guard_ok = blocked_count == 3 and guard_count == 2 and summary.get("blocked_rows") == 3 and summary.get("guard_rows") == 2
    rows.append(audit_row(
        "block_guard_accounting",
        "PASS_BLOCK_GUARD_ACCOUNTING" if block_guard_ok else "FAIL_BLOCK_GUARD_ACCOUNTING",
        f"blocked_count={blocked_count}, guard_count={guard_count}",
        block_guard_ok,
        "null coordinate should have three acceptance blocks and two control guards",
    ))

    permissions_closed = (
        all(row.get("allows_coordinate_acceptance") == "false" for row in coord_rows)
        and all(row.get("allows_physical_response") == "false" for row in coord_rows)
        and all(row.get("allows_quotient_proof") == "false" for row in coord_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in coord_rows)
        and all(row.get("allows_carrier_certification") == "false" for row in coord_rows)
        and all(row.get("allows_score_entry") == "false" for row in coord_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in coord_rows)
        and summary.get("coordinate_acceptance_allowed") is False
        and summary.get("physical_response_allowed") is False
        and summary.get("quotient_proof_allowed") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("carrier_certification_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_NULL_COORDINATE_FIREWALL_CLOSED" if permissions_closed else "FAIL_NULL_COORDINATE_FIREWALL",
        "coordinate acceptance, physical response, quotient proof, concrete R_CMB, carrier certification, score, and verdict permissions remain closed",
        permissions_closed,
        "null coordinate candidate must not enter physical response, score, or verdict channels",
    ))

    rows.append(audit_row(
        "null_seed_acceptance",
        "BLOCKED_NULL_SEED_NOT_ACCEPTED",
        "null seed is audited as control but not accepted as a readout-domain member",
        False,
        "requires readout-domain certificate for the null control side",
    ))
    rows.append(audit_row(
        "null_readout_materialization",
        "BLOCKED_NULL_READOUT_NOT_MATERIALIZED",
        "R_CMB(null_seed) := null_readout is declared but concrete R_CMB is not materialized",
        False,
        "requires concrete readout map or explicit materialization rule",
    ))
    rows.append(audit_row(
        "quotient_relation_proof",
        "BLOCKED_QUOTIENT_RELATION_NOT_PROVED",
        "quotient relation hook is declared but equivalence relation, quotient map, and survival condition are not proved",
        False,
        "requires equivalence proof and non-null survival test",
    ))
    rows.append(audit_row(
        "zero_control_not_physical_proof",
        "GUARD_ZERO_SOURCE_CONTROL_NOT_PHYSICAL_PROOF",
        "zero-control is kept separate from physical zero-source projection proof",
        True,
        "zero-control may not substitute for physical projection zero-source proof",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_null_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_coordinate_table": rel(COORDINATE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "null_coordinate_audited": True,
        "coordinate_acceptance_allowed": False,
        "physical_response_allowed": False,
        "quotient_proof_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "NULL_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_ACCEPTED",
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_bundle_closure_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Readout Role Coordinate Null Audit v01

**Doc class:** null/control role-coordinate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the null/control role-coordinate candidate has the
expected components, formal slots, control roles, dependency trace,
block/guard accounting, and promotion firewall. It does not accept the null
coordinate, claim physical Tau response, prove the quotient relation,
materialize concrete `R_CMB`, certify the carrier, open score entry, or decide
the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The null coordinate is audit-visible but not accepted. It remains blocked on
null-seed domain acceptance, concrete null-readout materialization, and
quotient-relation proof. The audit also preserves the guard that zero-control
is not a physical zero-source proof.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB null readout role-coordinate candidate.")
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
