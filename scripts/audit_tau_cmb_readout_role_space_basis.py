#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASIS_TABLE = ROOT / "data/derived/tau_cmb_readout_role_space_basis_v01.csv"
BASIS_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_space_basis_summary_v01.json"
AXIOM_OBLIGATION = ROOT / "data/derived/tau_cmb_seed_readout_equivalence_axiom_proof_obligation_summary_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_readout_role_space_basis_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_space_basis_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_space_basis_audit_v01_audit_only_"
    "carrier_basis_not_certified_no_concrete_R_CMB_no_equivalence_proof_no_readout_evaluation_no_score_no_verdict"
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
    required = [BASIS_TABLE, BASIS_SUMMARY, AXIOM_OBLIGATION]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    basis_rows = read_csv(BASIS_TABLE)
    summary = load_json(BASIS_SUMMARY)
    obligation = load_json(AXIOM_OBLIGATION)
    role_slots = [row.get("role_slot") for row in basis_rows]
    expected_slots = [
        "acoustic_phase_height",
        "density_amplitude",
        "lensing_potential",
        "growth_transfer",
        "radiation_damping_guard",
        "null_readout",
    ]
    rows.append(audit_row(
        "basis_row_shape",
        "PASS_ROLE_SLOTS_PRESENT" if role_slots == expected_slots else "FAIL_ROLE_SLOT_SHAPE",
        f"role_slots={role_slots}",
        role_slots == expected_slots,
        "basis audit requires the six declared CMB readout role slots",
    ))

    input_ok = (
        summary.get("status") == "CMB_READOUT_ROLE_SPACE_BASIS_CANDIDATE_DECLARED_NOT_CERTIFIED"
        and summary.get("input_axiom_obligation_clean") is True
        and obligation.get("status") == "SEED_READOUT_EQUIVALENCE_AXIOM_PROOF_OBLIGATION_DECLARED_BLOCKED"
    )
    rows.append(audit_row(
        "input_obligation_chain",
        "PASS_AXIOM_OBLIGATION_CHAIN" if input_ok else "FAIL_AXIOM_OBLIGATION_CHAIN",
        "basis candidate follows a clean equivalence axiom proof-obligation input",
        input_ok,
        "basis audit must be downstream of the equivalence axiom proof obligation",
    ))

    symbols = [row.get("basis_symbol") for row in basis_rows]
    expected_symbols = ["e_acoustic", "e_density", "e_lensing", "e_growth", "e_radiation", "e_null"]
    rows.append(audit_row(
        "basis_symbols",
        "PASS_BASIS_SYMBOLS_DECLARED" if symbols == expected_symbols else "FAIL_BASIS_SYMBOLS",
        f"basis_symbols={symbols}",
        symbols == expected_symbols,
        "basis symbols must match the carrier predicate candidate",
    ))

    endpoint_firewall_ok = all(
        any(
            token in row.get("forbidden_dependency", "").lower()
            for token in ["endpoint", "residual", "mismatch", "likelihood", "score", "tune", "fitting"]
        )
        for row in basis_rows
    )
    rows.append(audit_row(
        "endpoint_firewall_labels",
        "PASS_FORBIDDEN_ENDPOINT_DEPENDENCIES_DECLARED" if endpoint_firewall_ok else "FAIL_ENDPOINT_FIREWALL_LABELS",
        "each role slot declares a forbidden endpoint-tuning dependency",
        endpoint_firewall_ok,
        "basis candidate must identify endpoint-derived dependencies as forbidden",
    ))

    dimension_roles_ok = all(row.get("dimension_role") for row in basis_rows)
    rows.append(audit_row(
        "dimension_role_labels",
        "PASS_DIMENSION_ROLES_DECLARED" if dimension_roles_ok else "FAIL_DIMENSION_ROLES",
        "each role slot has a dimension/unit role label",
        dimension_roles_ok,
        "carrier typing requires declared dimension or convention labels",
    ))

    null_anchor_ok = any(
        row.get("role_slot") == "null_readout"
        and row.get("basis_symbol") == "e_null"
        and "zero" in row.get("dimension_role", "").lower()
        and "audited zero-control" in row.get("source_dependency", "")
        for row in basis_rows
    )
    rows.append(audit_row(
        "null_basis_anchor",
        "PASS_NULL_BASIS_ANCHOR_DECLARED" if null_anchor_ok else "FAIL_NULL_BASIS_ANCHOR",
        "null readout basis anchor is declared from audited zero-control",
        null_anchor_ok,
        "role-space basis needs a null anchor for later null-class tests",
    ))

    permissions_closed = (
        all(row.get("allows_carrier_certification") == "false" for row in basis_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in basis_rows)
        and all(row.get("allows_equivalence_proof") == "false" for row in basis_rows)
        and all(row.get("allows_readout_evaluation") == "false" for row in basis_rows)
        and all(row.get("allows_score_entry") == "false" for row in basis_rows)
        and summary.get("carrier_certification_allowed") is False
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("equivalence_proof_allowed") is False
        and summary.get("readout_evaluation_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_BASIS_PROMOTION_FIREWALL_CLOSED" if permissions_closed else "FAIL_BASIS_PROMOTION_FIREWALL",
        "carrier certification, concrete R_CMB, equivalence proof, readout, score, and verdict permissions remain closed",
        permissions_closed,
        "basis candidate must not certify the carrier or enter scoring",
    ))

    materialization_missing = all("NOT_MATERIALIZED" in row.get("basis_status", "") or "NOT_ACCEPTED" in row.get("basis_status", "") for row in basis_rows)
    rows.append(audit_row(
        "role_coordinate_materialization",
        "BLOCKED_ROLE_COORDINATES_NOT_MATERIALIZED" if materialization_missing else "FAIL_ROLE_COORDINATE_STATE",
        "role coordinates are declared but not materialized",
        False,
        "each role coordinate needs endpoint-blind definition, unit/dimension replay, and provenance",
    ))

    carrier_block = summary.get("carrier_certification_allowed") is False
    rows.append(audit_row(
        "carrier_certification",
        "BLOCKED_CARRIER_NOT_CERTIFIED" if carrier_block else "FAIL_CARRIER_CERTIFICATION_OPEN",
        "carrier predicate remains a candidate and is not certified",
        False,
        "carrier certification requires audited role coordinates and null-domain acceptance",
    ))

    concrete_readout_block = summary.get("concrete_R_CMB_allowed") is False
    rows.append(audit_row(
        "concrete_readout",
        "BLOCKED_CONCRETE_R_CMB_NOT_MATERIALIZED" if concrete_readout_block else "FAIL_CONCRETE_READOUT_OPEN",
        "basis candidate does not materialize a concrete R_CMB map",
        False,
        "concrete R_CMB requires a certified carrier plus coordinate maps",
    ))

    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_readout_role_space_basis_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_basis_table": rel(BASIS_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "role_space_basis_audited": True,
        "carrier_certification_allowed": False,
        "concrete_R_CMB_allowed": False,
        "equivalence_proof_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "CMB_READOUT_ROLE_SPACE_BASIS_AUDITED_BLOCKED_NOT_CERTIFIED",
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_acoustic_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Readout Role Space Basis Audit v01

**Doc class:** CMB readout role-space basis audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the CMB readout role-space basis candidate has the
expected role slots, basis symbols, endpoint-firewall labels, dimension labels,
and null anchor. It does not certify the carrier, materialize concrete `R_CMB`,
prove equivalence, evaluate readout, enter scoring, or decide the dark-sector
question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The role-space basis is now audit-visible as a carrier candidate. It remains
blocked because the role coordinates are not materialized, the carrier is not
certified, and no concrete `R_CMB` map is supplied.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB readout role-space basis candidate.")
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
