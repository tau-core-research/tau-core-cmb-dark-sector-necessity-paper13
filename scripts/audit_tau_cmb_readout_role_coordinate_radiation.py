#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COORDINATE_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_v01.csv"
COORDINATE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_summary_v01.json"
GROWTH_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_growth_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_radiation_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_radiation_audit_v01_audit_only_"
    "coordinate_not_accepted_no_radiation_score_no_neff_bound_eval_no_concrete_R_CMB_"
    "no_carrier_certification_no_verdict"
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
    required = [COORDINATE_TABLE, COORDINATE_SUMMARY, GROWTH_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    coord_rows = read_csv(COORDINATE_TABLE)
    summary = load_json(COORDINATE_SUMMARY)
    growth_audit = load_json(GROWTH_AUDIT)
    components = [row.get("coordinate_component") for row in coord_rows]
    expected = [
        "tau_radiation_like_contribution",
        "external_bound_convention",
        "damping_tail_inequality",
        "cross_role_consistency",
        "radiation_stop_rule",
    ]
    rows.append(audit_row(
        "coordinate_row_shape",
        "PASS_RADIATION_COORDINATE_ROWS_PRESENT" if components == expected else "FAIL_RADIATION_COORDINATE_ROW_SHAPE",
        f"coordinate_components={components}",
        components == expected,
        "radiation coordinate audit requires the five declared components",
    ))

    input_ok = (
        summary.get("status") == "RADIATION_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED"
        and summary.get("input_growth_coordinate_audit_clean") is True
        and growth_audit.get("status") == "GROWTH_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED"
        and growth_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_growth_chain",
        "PASS_GROWTH_AUDIT_CHAIN" if input_ok else "FAIL_GROWTH_AUDIT_CHAIN",
        "radiation coordinate follows a clean growth coordinate audit and radiation candidate summary",
        input_ok,
        "radiation coordinate audit must be downstream of the audited growth coordinate and clean candidate summary",
    ))

    formal_slots_ok = all(row.get("formal_slot") for row in coord_rows)
    rows.append(audit_row(
        "formal_slots_declared",
        "PASS_FORMAL_SLOTS_DECLARED" if formal_slots_ok else "FAIL_FORMAL_SLOTS",
        "each radiation coordinate component has a formal slot",
        formal_slots_ok,
        "coordinate components need formal slots before materialization",
    ))

    dimension_roles_ok = all(row.get("dimension_role") for row in coord_rows)
    rows.append(audit_row(
        "dimension_roles_declared",
        "PASS_DIMENSION_ROLES_DECLARED" if dimension_roles_ok else "FAIL_DIMENSION_ROLES",
        "each radiation coordinate component has a dimension/convention role",
        dimension_roles_ok,
        "coordinate typing requires dimension or convention roles",
    ))

    source_dependencies_ok = all(row.get("source_dependency") for row in coord_rows)
    rows.append(audit_row(
        "source_dependencies_declared",
        "PASS_SOURCE_DEPENDENCIES_DECLARED" if source_dependencies_ok else "FAIL_SOURCE_DEPENDENCIES",
        "each radiation coordinate component is tied to an existing blocker/evidence artifact",
        source_dependencies_ok,
        "coordinate candidate must remain traceable to existing protocol artifacts",
    ))

    blocked_count = sum(row.get("coordinate_status", "").startswith("BLOCKED") for row in coord_rows)
    guard_count = sum("GUARD" in row.get("coordinate_status", "") or "STOP_RULE" in row.get("coordinate_status", "") for row in coord_rows)
    block_guard_ok = blocked_count == 3 and guard_count == 2 and summary.get("blocked_rows") == 3 and summary.get("guard_rows") == 2
    rows.append(audit_row(
        "block_guard_accounting",
        "PASS_BLOCK_GUARD_ACCOUNTING" if block_guard_ok else "FAIL_BLOCK_GUARD_ACCOUNTING",
        f"blocked_count={blocked_count}, guard_count={guard_count}",
        block_guard_ok,
        "radiation coordinate should have three physics blocks and two guard rows",
    ))

    permissions_closed = (
        all(row.get("allows_coordinate_acceptance") == "false" for row in coord_rows)
        and all(row.get("allows_radiation_score") == "false" for row in coord_rows)
        and all(row.get("allows_neff_bound_eval") == "false" for row in coord_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in coord_rows)
        and all(row.get("allows_carrier_certification") == "false" for row in coord_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in coord_rows)
        and summary.get("coordinate_acceptance_allowed") is False
        and summary.get("radiation_score_allowed") is False
        and summary.get("neff_bound_eval_allowed") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("carrier_certification_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_RADIATION_COORDINATE_FIREWALL_CLOSED" if permissions_closed else "FAIL_RADIATION_COORDINATE_FIREWALL",
        "coordinate acceptance, radiation score, Neff bound evaluation, concrete R_CMB, carrier certification, and verdict permissions remain closed",
        permissions_closed,
        "radiation coordinate candidate must not enter scoring or carrier certification",
    ))

    rows.append(audit_row(
        "tau_radiation_like_contribution",
        "BLOCKED_TAU_DELTA_NEFF_NOT_DERIVED",
        "Delta_N_eff_tau is declared only as a dimensionless contribution slot",
        False,
        "requires endpoint-blind derivation of Delta_N_eff_tau under the adopted convention",
    ))
    rows.append(audit_row(
        "damping_tail_inequality",
        "BLOCKED_BOUND_INEQUALITY_NOT_EVALUATED",
        "Delta_N_eff_tau <= Delta_N_eff_bound is declared but not numerically evaluated",
        False,
        "requires Tau contribution and selected external bound under shared convention",
    ))
    rows.append(audit_row(
        "cross_role_consistency",
        "BLOCKED_DEPENDENT_ROLES_STILL_OPEN",
        "density, acoustic, lensing, and growth role coordinates remain blocked and unmaterialized",
        False,
        "requires compatible density, acoustic, lensing, growth, and radiation role-coordinate materialization",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_radiation_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_coordinate_table": rel(COORDINATE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "radiation_coordinate_audited": True,
        "coordinate_acceptance_allowed": False,
        "radiation_score_allowed": False,
        "neff_bound_eval_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "RADIATION_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED",
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_null_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Readout Role Coordinate Radiation Audit v01

**Doc class:** radiation role-coordinate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the radiation role-coordinate candidate has the
expected components, formal slots, dimension roles, dependency trace,
block/guard accounting, and promotion firewall. It does not accept the
coordinate, compute a radiation score, evaluate a numerical `Delta_N_eff`
bound, materialize concrete `R_CMB`, certify the carrier, or decide the
dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The radiation coordinate is audit-visible but not materialized. It remains
blocked on deriving `Delta_N_eff_tau`, evaluating the damping-tail inequality
under a selected external bound, and checking cross-role consistency with the
density, acoustic, lensing, and growth coordinates.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB radiation readout role-coordinate candidate.")
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
