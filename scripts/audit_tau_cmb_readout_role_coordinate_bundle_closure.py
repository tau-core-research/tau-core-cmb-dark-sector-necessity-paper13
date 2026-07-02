#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_CLOSURE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_bundle_closure_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_bundle_closure_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_bundle_closure_audit_v01.md"

EXPECTED_ROLES = ["acoustic", "density", "lensing", "growth", "radiation", "null"]
REQUIRED_BLOCKERS = [
    "concrete R_CMB materialization",
    "carrier/domain certification",
    "quotient/equivalence and non-null survival proof",
    "endpoint-blind rho_tau_eff, A_tau, Phi_tau_eff, and T_tau_CMB",
    "cross-role consistency across acoustic, density, lensing, growth, radiation, and null controls",
]

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_bundle_closure_audit_v01_audit_only_"
    "bundle_closure_clean_but_not_score_ready_no_concrete_R_CMB_no_carrier_"
    "no_likelihood_no_dark_sector_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


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
    rows: list[dict[str, Any]] = []
    if not BUNDLE_CLOSURE.exists():
        rows.append(audit_row(
            "bundle_closure_input",
            "FAIL_MISSING_BUNDLE_CLOSURE",
            f"missing {rel(BUNDLE_CLOSURE)}",
            False,
            "bundle closure must exist before audit",
        ))
        return finalize(rows, {})

    bundle = load_json(BUNDLE_CLOSURE)
    role_rows = bundle.get("role_rows", [])
    roles = [row.get("role") for row in role_rows]
    role_set_ok = roles == EXPECTED_ROLES
    rows.append(audit_row(
        "role_set",
        "PASS_EXPECTED_ROLE_SET" if role_set_ok else "FAIL_ROLE_SET",
        f"roles={roles}",
        role_set_ok,
        "bundle must contain acoustic, density, lensing, growth, radiation, and null roles in order",
    ))

    present_ok = bundle.get("role_count") == 6 and bundle.get("expected_role_count") == 6 and bundle.get("all_role_audits_present") is True
    rows.append(audit_row(
        "role_audit_presence",
        "PASS_ALL_ROLE_AUDITS_PRESENT" if present_ok else "FAIL_ROLE_AUDIT_PRESENCE",
        "all six role-coordinate audits are present",
        present_ok,
        "every role coordinate must have an audit input before bundle closure",
    ))

    clean_ok = bundle.get("all_role_audits_clean") is True and bundle.get("failed_rows_total") == 0
    rows.append(audit_row(
        "role_audit_cleanliness",
        "PASS_ROLE_AUDITS_CLEAN" if clean_ok else "FAIL_ROLE_AUDITS_NOT_CLEAN",
        f"failed_rows_total={bundle.get('failed_rows_total')}",
        clean_ok,
        "bundle closure requires zero failed role-audit rows",
    ))

    accounting_ok = bundle.get("passed_rows_total") == 43 and bundle.get("blocked_rows_total") == 20
    rows.append(audit_row(
        "aggregate_accounting",
        "PASS_AGGREGATE_ACCOUNTING" if accounting_ok else "FAIL_AGGREGATE_ACCOUNTING",
        f"passed_rows_total={bundle.get('passed_rows_total')}, blocked_rows_total={bundle.get('blocked_rows_total')}",
        accounting_ok,
        "bundle audit expects the current six-role accounting totals",
    ))

    firewall_ok = (
        bundle.get("promotion_firewall_closed") is True
        and bundle.get("concrete_R_CMB_allowed") is False
        and bundle.get("carrier_certification_allowed") is False
        and bundle.get("cmb_likelihood_allowed") is False
        and bundle.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "bundle_promotion_firewall",
        "PASS_BUNDLE_FIREWALL_CLOSED" if firewall_ok else "FAIL_BUNDLE_FIREWALL",
        "concrete R_CMB, carrier certification, CMB likelihood, and dark-sector verdict permissions remain closed",
        firewall_ok,
        "bundle closure must not promote role audits into scoring or verdict claims",
    ))

    status_ok = (
        bundle.get("status") == "READOUT_ROLE_COORDINATE_BUNDLE_AUDITED_BLOCKED_NOT_SCORE_READY"
        and bundle.get("coordinate_bundle_audited") is True
        and bundle.get("bundle_score_ready") is False
    )
    rows.append(audit_row(
        "closure_status",
        "PASS_BUNDLE_AUDITED_NOT_SCORE_READY" if status_ok else "FAIL_BUNDLE_STATUS",
        f"status={bundle.get('status')}, bundle_score_ready={bundle.get('bundle_score_ready')}",
        status_ok,
        "bundle closure must be audited but not score-ready",
    ))

    blockers = bundle.get("remaining_core_blockers", [])
    blockers_ok = blockers == REQUIRED_BLOCKERS
    rows.append(audit_row(
        "remaining_core_blockers",
        "PASS_REMAINING_BLOCKERS_DECLARED" if blockers_ok else "FAIL_REMAINING_BLOCKERS",
        f"remaining_core_blockers={blockers}",
        blockers_ok,
        "bundle closure must preserve the five core blockers before scoring",
    ))

    rows.append(audit_row(
        "score_readiness",
        "BLOCKED_CONCRETE_R_CMB_AND_CARRIER_NOT_CERTIFIED",
        "bundle is enumerated, but concrete R_CMB and carrier/domain certification are missing",
        False,
        "requires concrete R_CMB materialization and carrier/domain certification",
    ))
    rows.append(audit_row(
        "source_objects",
        "BLOCKED_ENDPOINT_BLIND_SOURCE_OBJECTS_MISSING",
        "rho_tau_eff, A_tau, Phi_tau_eff, and T_tau_CMB remain source/readout slots rather than accepted endpoint-blind objects",
        False,
        "requires endpoint-blind source object derivations before scoring",
    ))
    rows.append(audit_row(
        "quotient_and_cross_role",
        "BLOCKED_QUOTIENT_SURVIVAL_AND_CROSS_ROLE_CONSISTENCY",
        "quotient/equivalence survival and cross-role consistency are not proved",
        False,
        "requires quotient survival proof and compatible role materialization",
    ))
    return finalize(rows, bundle)


def finalize(rows: list[dict[str, Any]], bundle: dict[str, Any]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0 and bundle.get("status") == "READOUT_ROLE_COORDINATE_BUNDLE_AUDITED_BLOCKED_NOT_SCORE_READY"
    return {
        "report_id": "tau_cmb_readout_role_coordinate_bundle_closure_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_bundle": rel(BUNDLE_CLOSURE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "bundle_closure_audited": clean,
        "bundle_score_ready": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "cmb_likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_AUDITED_BLOCKED_NOT_SCORE_READY"
            if clean
            else "READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_scoring_input_gap_matrix_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Readout Role Coordinate Bundle Closure Audit v01

**Doc class:** readout-role coordinate bundle closure audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the bundle-level status of the six CMB readout-role
coordinates. It verifies role presence, clean role audits, aggregate accounting,
promotion-firewall closure, not-score-ready status, and preservation of the core
blockers. It does not materialize `R_CMB`, certify the carrier, compute a CMB
likelihood, open scoring, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The bundle closure is cleanly audited but remains blocked before scoring.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB readout role-coordinate bundle closure.")
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
