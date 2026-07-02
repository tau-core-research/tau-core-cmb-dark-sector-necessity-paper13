#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COORDINATE_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_v01.csv"
COORDINATE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_summary_v01.json"
BASIS_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_space_basis_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_acoustic_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_acoustic_audit_v01_audit_only_"
    "coordinate_not_accepted_no_acoustic_score_no_likelihood_no_concrete_R_CMB_no_carrier_certification_no_verdict"
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
    required = [COORDINATE_TABLE, COORDINATE_SUMMARY, BASIS_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    coord_rows = read_csv(COORDINATE_TABLE)
    summary = load_json(COORDINATE_SUMMARY)
    basis_audit = load_json(BASIS_AUDIT)
    components = [row.get("coordinate_component") for row in coord_rows]
    expected = [
        "potential_source_presence",
        "phase_support",
        "relative_peak_height",
        "baryon_loading_coupling",
        "scale_horizon_guard",
        "failure_branch",
    ]
    rows.append(audit_row(
        "coordinate_row_shape",
        "PASS_ACOUSTIC_COORDINATE_ROWS_PRESENT" if components == expected else "FAIL_ACOUSTIC_COORDINATE_ROW_SHAPE",
        f"coordinate_components={components}",
        components == expected,
        "acoustic coordinate audit requires the six declared components",
    ))

    input_ok = (
        summary.get("status") == "ACOUSTIC_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED"
        and summary.get("input_basis_audit_clean") is True
        and basis_audit.get("status") == "CMB_READOUT_ROLE_SPACE_BASIS_AUDITED_BLOCKED_NOT_CERTIFIED"
        and basis_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_basis_chain",
        "PASS_BASIS_AUDIT_CHAIN" if input_ok else "FAIL_BASIS_AUDIT_CHAIN",
        "acoustic coordinate follows a clean role-space basis audit",
        input_ok,
        "acoustic coordinate audit must be downstream of the audited role-space basis",
    ))

    formal_slots_ok = all(row.get("formal_slot") for row in coord_rows)
    rows.append(audit_row(
        "formal_slots_declared",
        "PASS_FORMAL_SLOTS_DECLARED" if formal_slots_ok else "FAIL_FORMAL_SLOTS",
        "each acoustic coordinate component has a formal slot",
        formal_slots_ok,
        "coordinate components need formal slots before materialization",
    ))

    dimension_roles_ok = all(row.get("dimension_role") for row in coord_rows)
    rows.append(audit_row(
        "dimension_roles_declared",
        "PASS_DIMENSION_ROLES_DECLARED" if dimension_roles_ok else "FAIL_DIMENSION_ROLES",
        "each acoustic coordinate component has a dimension/convention role",
        dimension_roles_ok,
        "coordinate typing requires dimension or convention roles",
    ))

    source_dependencies_ok = all(row.get("source_dependency") for row in coord_rows)
    rows.append(audit_row(
        "source_dependencies_declared",
        "PASS_SOURCE_DEPENDENCIES_DECLARED" if source_dependencies_ok else "FAIL_SOURCE_DEPENDENCIES",
        "each acoustic coordinate component is tied to an existing blocker/evidence artifact",
        source_dependencies_ok,
        "coordinate candidate must remain traceable to existing protocol artifacts",
    ))

    blocked_count = sum(row.get("coordinate_status", "").startswith("BLOCKED") for row in coord_rows)
    guard_count = sum("GUARD" in row.get("coordinate_status", "") or "FAILURE_BRANCH" in row.get("coordinate_status", "") for row in coord_rows)
    block_guard_ok = blocked_count == 4 and guard_count == 2 and summary.get("blocked_rows") == 4 and summary.get("guard_rows") == 2
    rows.append(audit_row(
        "block_guard_accounting",
        "PASS_BLOCK_GUARD_ACCOUNTING" if block_guard_ok else "FAIL_BLOCK_GUARD_ACCOUNTING",
        f"blocked_count={blocked_count}, guard_count={guard_count}",
        block_guard_ok,
        "acoustic coordinate should have four physics blocks and two guard rows",
    ))

    permissions_closed = (
        all(row.get("allows_coordinate_acceptance") == "false" for row in coord_rows)
        and all(row.get("allows_acoustic_score") == "false" for row in coord_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in coord_rows)
        and all(row.get("allows_carrier_certification") == "false" for row in coord_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in coord_rows)
        and summary.get("coordinate_acceptance_allowed") is False
        and summary.get("acoustic_score_allowed") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("carrier_certification_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_ACOUSTIC_COORDINATE_FIREWALL_CLOSED" if permissions_closed else "FAIL_ACOUSTIC_COORDINATE_FIREWALL",
        "coordinate acceptance, acoustic score, concrete R_CMB, carrier certification, and verdict permissions remain closed",
        permissions_closed,
        "acoustic coordinate candidate must not enter scoring or carrier certification",
    ))

    rows.append(audit_row(
        "source_materialization",
        "BLOCKED_SOURCE_NOT_DERIVED",
        "pre-recombination Tau potential/source handoff is not derived",
        False,
        "requires endpoint-blind Phi_tau_eff handoff and source timing/sign",
    ))
    rows.append(audit_row(
        "oscillator_response",
        "BLOCKED_OSCILLATOR_RESPONSE_NOT_EVALUATED",
        "photon-baryon oscillator response is not evaluated for the Tau source",
        False,
        "requires reduced oscillator convention and source-time dependence",
    ))
    rows.append(audit_row(
        "amplitude_and_coupling",
        "BLOCKED_AMPLITUDE_AND_COUPLING_NOT_SUPPLIED",
        "endpoint-blind amplitude and baryon-loading coupling sign are missing",
        False,
        "requires A_tau normalization and coupling-sign convention",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_acoustic_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_coordinate_table": rel(COORDINATE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "acoustic_coordinate_audited": True,
        "coordinate_acceptance_allowed": False,
        "acoustic_score_allowed": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "ACOUSTIC_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED",
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_density_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Readout Role Coordinate Acoustic Audit v01

**Doc class:** acoustic role-coordinate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the acoustic role-coordinate candidate has the
expected components, formal slots, dimension roles, dependency trace, and
promotion firewall. It does not accept the coordinate, compute an acoustic
score, materialize concrete `R_CMB`, certify the carrier, or decide the
dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The acoustic coordinate is audit-visible but not materialized. It remains
blocked on the Tau pre-recombination source handoff, oscillator response,
endpoint-blind amplitude, and baryon-loading coupling sign.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB acoustic readout role-coordinate candidate.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
