#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_bundle_closure_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_bundle_closure_v01.md"

ROLE_AUDITS = {
    "acoustic": ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_audit_v01.json",
    "density": ROOT / "data/derived/tau_cmb_readout_role_coordinate_density_audit_v01.json",
    "lensing": ROOT / "data/derived/tau_cmb_readout_role_coordinate_lensing_audit_v01.json",
    "growth": ROOT / "data/derived/tau_cmb_readout_role_coordinate_growth_audit_v01.json",
    "radiation": ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_audit_v01.json",
    "null": ROOT / "data/derived/tau_cmb_readout_role_coordinate_null_audit_v01.json",
}

EXPECTED_STATUS = {
    "acoustic": "ACOUSTIC_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED",
    "density": "DENSITY_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED",
    "lensing": "LENSING_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED",
    "growth": "GROWTH_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED",
    "radiation": "RADIATION_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED",
    "null": "NULL_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_ACCEPTED",
}

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_bundle_closure_v01_closure_only_"
    "bundle_audited_not_score_ready_no_concrete_R_CMB_no_carrier_certification_"
    "no_likelihood_no_dark_sector_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report() -> dict[str, Any]:
    missing = [role for role, path in ROLE_AUDITS.items() if not path.exists()]
    role_rows: list[dict[str, Any]] = []
    if missing:
        for role in missing:
            role_rows.append({
                "role": role,
                "audit_path": rel(ROLE_AUDITS[role]),
                "audit_status": "MISSING",
                "expected_status": EXPECTED_STATUS[role],
                "passed_rows": 0,
                "blocked_rows": 0,
                "failed_rows": 1,
                "role_audit_clean": False,
            })
        return finalize(role_rows)

    for role, path in ROLE_AUDITS.items():
        audit = load_json(path)
        clean = audit.get("status") == EXPECTED_STATUS[role] and audit.get("failed_rows") == 0
        role_rows.append({
            "role": role,
            "audit_path": rel(path),
            "audit_status": audit.get("status"),
            "expected_status": EXPECTED_STATUS[role],
            "passed_rows": audit.get("passed_rows", 0),
            "blocked_rows": audit.get("blocked_rows", 0),
            "failed_rows": audit.get("failed_rows", 0),
            "role_audit_clean": clean,
            "coordinate_acceptance_allowed": audit.get("coordinate_acceptance_allowed", False),
            "carrier_certification_allowed": audit.get("carrier_certification_allowed", False),
            "dark_sector_verdict_allowed": audit.get("dark_sector_verdict_allowed", False),
        })
    return finalize(role_rows)


def finalize(role_rows: list[dict[str, Any]]) -> dict[str, Any]:
    all_present = len(role_rows) == len(ROLE_AUDITS) and all(row["audit_status"] != "MISSING" for row in role_rows)
    all_clean = all(row.get("role_audit_clean") is True for row in role_rows)
    failed_total = sum(int(row.get("failed_rows", 0)) for row in role_rows)
    blocked_total = sum(int(row.get("blocked_rows", 0)) for row in role_rows)
    passed_total = sum(int(row.get("passed_rows", 0)) for row in role_rows)
    permissions_closed = all(
        row.get("coordinate_acceptance_allowed") is False
        and row.get("carrier_certification_allowed") is False
        and row.get("dark_sector_verdict_allowed") is False
        for row in role_rows
    )
    return {
        "report_id": "tau_cmb_readout_role_coordinate_bundle_closure_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "role_rows": role_rows,
        "role_count": len(role_rows),
        "expected_role_count": len(ROLE_AUDITS),
        "all_role_audits_present": all_present,
        "all_role_audits_clean": all_clean,
        "passed_rows_total": passed_total,
        "blocked_rows_total": blocked_total,
        "failed_rows_total": failed_total,
        "promotion_firewall_closed": permissions_closed,
        "coordinate_bundle_audited": all_present and all_clean and permissions_closed,
        "bundle_score_ready": False,
        "concrete_R_CMB_allowed": False,
        "carrier_certification_allowed": False,
        "cmb_likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "READOUT_ROLE_COORDINATE_BUNDLE_AUDITED_BLOCKED_NOT_SCORE_READY"
            if all_present and all_clean and permissions_closed
            else "READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_BLOCKED_BY_INPUTS"
        ),
        "remaining_core_blockers": [
            "concrete R_CMB materialization",
            "carrier/domain certification",
            "quotient/equivalence and non-null survival proof",
            "endpoint-blind rho_tau_eff, A_tau, Phi_tau_eff, and T_tau_CMB",
            "cross-role consistency across acoustic, density, lensing, growth, radiation, and null controls",
        ],
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_bundle_closure_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['role']}`: {row['audit_status']} | pass={row['passed_rows']} block={row['blocked_rows']} fail={row['failed_rows']}"
        for row in report["role_rows"]
    )
    blockers = "\n".join(f"- {item}" for item in report["remaining_core_blockers"])
    text = f"""# Tau CMB Readout Role Coordinate Bundle Closure v01

**Doc class:** readout-role coordinate bundle closure
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact closes the six audited CMB readout-role coordinates into one
bundle-level status object:

```text
e_acoustic, e_density, e_lensing, e_growth, e_radiation, e_null
```

It does not certify the carrier, materialize concrete `R_CMB`, compute a CMB
likelihood, open scoring, or decide the dark-sector question.

## Role Audit Inputs

{rows}

## Remaining Core Blockers

{blockers}

## Status

```text
{report["status"]}
```

The coordinate bundle is audit-visible and internally enumerated, but it is not
score-ready. Each role has a clean audit package, yet the physics-bearing and
quotient/readout blockers remain open.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB readout role-coordinate bundle closure.")
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
