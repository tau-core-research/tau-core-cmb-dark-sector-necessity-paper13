#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_bundle_closure_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_scoring_input_gap_matrix_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_scoring_input_gap_matrix_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_scoring_input_gap_matrix_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_scoring_input_gap_matrix_v01_gap_matrix_only_"
    "no_input_fulfilled_no_score_no_likelihood_no_dark_sector_verdict"
)

FIELDS = [
    "gap_row_id",
    "priority_rank",
    "gap_name",
    "blocking_scope",
    "required_scoring_input",
    "minimum_artifact_to_build",
    "acceptance_criterion",
    "blocked_roles",
    "unblocks_if_satisfied",
    "stop_rule",
    "gap_status",
    "completed_in_v01",
    "score_allowed_after_row",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

GAPS = [
    {
        "priority_rank": 1,
        "gap_name": "carrier_and_R_CMB_materialization",
        "blocking_scope": "global readout carrier",
        "required_scoring_input": "concrete R_CMB map plus carrier/domain certificate",
        "minimum_artifact_to_build": "tau_cmb_concrete_R_CMB_carrier_certificate_v01",
        "acceptance_criterion": "carrier predicate, domain rule, null anchor, and concrete readout map are certified without endpoint residual tuning",
        "blocked_roles": "all",
        "unblocks_if_satisfied": "allows role-coordinate materialization audit to move from abstract slots to concrete readout inputs",
        "stop_rule": "if concrete R_CMB cannot be supplied, keep all aggregate scoring blocked",
        "gap_status": "BLOCKED_GLOBAL_READOUT_CARRIER_MISSING",
    },
    {
        "priority_rank": 2,
        "gap_name": "quotient_survival_and_non_null_test",
        "blocking_scope": "readout quotient/null survival",
        "required_scoring_input": "equivalence relation, quotient map, null class, and non-null survival test",
        "minimum_artifact_to_build": "tau_cmb_quotient_survival_proof_packet_v01",
        "acceptance_criterion": "reflexivity, symmetry, transitivity, quotient well-definedness, null anchor compatibility, and non-null survival are proved or explicitly fail",
        "blocked_roles": "all; especially null and source acceptance",
        "unblocks_if_satisfied": "separates physical readout contribution from null/gauge/control leakage",
        "stop_rule": "if quotient survival fails, reject score entry for Tau-side CMB source route",
        "gap_status": "BLOCKED_QUOTIENT_SURVIVAL_NOT_PROVED",
    },
    {
        "priority_rank": 3,
        "gap_name": "endpoint_blind_source_objects",
        "blocking_scope": "Tau-side source handoff",
        "required_scoring_input": "rho_tau_eff, A_tau, Phi_tau_eff, and T_tau_CMB",
        "minimum_artifact_to_build": "tau_cmb_endpoint_blind_source_object_packet_v01",
        "acceptance_criterion": "source objects are derived from accepted parent-side inputs with dimension/gauge replay and endpoint firewall pass",
        "blocked_roles": "density; acoustic; lensing; growth",
        "unblocks_if_satisfied": "opens reduced density, acoustic, lensing, and transfer scoring inputs",
        "stop_rule": "if source objects cannot be derived endpoint-blind, mark affected roles FAIL rather than tune residuals",
        "gap_status": "BLOCKED_ENDPOINT_BLIND_SOURCE_OBJECTS_MISSING",
    },
    {
        "priority_rank": 4,
        "gap_name": "cross_role_consistency",
        "blocking_scope": "role bundle compatibility",
        "required_scoring_input": "single convention-compatible assignment across acoustic, density, lensing, growth, radiation, and null controls",
        "minimum_artifact_to_build": "tau_cmb_cross_role_consistency_matrix_v01",
        "acceptance_criterion": "all role inputs use compatible carrier, gauge, normalization, time/scale, null-control, and source conventions",
        "blocked_roles": "all",
        "unblocks_if_satisfied": "prevents isolated role passes from becoming inconsistent aggregate evidence",
        "stop_rule": "if roles require incompatible conventions, keep aggregate verdict blocked and record role conflict",
        "gap_status": "BLOCKED_CROSS_ROLE_CONSISTENCY_NOT_PROVED",
    },
    {
        "priority_rank": 5,
        "gap_name": "role_specific_numeric_guards",
        "blocking_scope": "reduced role scoring",
        "required_scoring_input": "Omega_c h^2 comparison, lensing amplitude/shape response, growth transfer comparison, Delta_N_eff bound evaluation",
        "minimum_artifact_to_build": "tau_cmb_role_specific_numeric_guard_packet_v01",
        "acceptance_criterion": "each role-specific comparison is evaluated under the accepted source/readout bundle or explicitly fails",
        "blocked_roles": "density; lensing; growth; radiation",
        "unblocks_if_satisfied": "opens reduced score rows after global source/readout gates pass",
        "stop_rule": "if a numeric guard fails, assign role-level FAIL before any aggregate score",
        "gap_status": "BLOCKED_ROLE_SPECIFIC_NUMERIC_GUARDS_NOT_EVALUATED",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "gap_row_id": f"TCMBSIGM01_{index:03d}",
            "priority_rank": str(row["priority_rank"]),
            "completed_in_v01": "false",
            "score_allowed_after_row": "false",
            "allows_likelihood": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **{k: str(v) for k, v in row.items() if k != "priority_rank"},
        }
        for index, row in enumerate(GAPS, start=1)
    ]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    bundle_audit = load_json(BUNDLE_AUDIT) if BUNDLE_AUDIT.exists() else {}
    input_ok = (
        bundle_audit.get("status") == "READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_AUDITED_BLOCKED_NOT_SCORE_READY"
        and bundle_audit.get("failed_rows") == 0
        and bundle_audit.get("bundle_score_ready") is False
    )
    return {
        "report_id": "tau_cmb_scoring_input_gap_matrix_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_bundle_closure_audit": rel(BUNDLE_AUDIT),
        "input_bundle_closure_audit_clean": input_ok,
        "gap_rows": len(rows),
        "completed_rows": sum(row["completed_in_v01"] == "true" for row in rows),
        "blocked_rows": sum(row["gap_status"].startswith("BLOCKED") for row in rows),
        "score_allowed_rows": sum(row["score_allowed_after_row"] == "true" for row in rows),
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "SCORING_INPUT_GAP_MATRIX_DECLARED_ALL_ROWS_BLOCKED_NO_SCORE"
            if input_ok
            else "SCORING_INPUT_GAP_MATRIX_BLOCKED_BY_INPUTS"
        ),
        "immediate_next_artifact": rows[0]["minimum_artifact_to_build"],
        "next_minimal_unblock": "tau_cmb_concrete_R_CMB_carrier_certificate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"{row['priority_rank']}. `{row['gap_name']}` -> `{row['minimum_artifact_to_build']}`"
        for row in rows
    )
    text = f"""# Tau CMB Scoring Input Gap Matrix v01

**Doc class:** scoring-input gap matrix
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact converts the audited readout-role bundle into a ranked scoring
input gap matrix. It does not fulfill any input, compute a score, open a CMB
likelihood, or decide the dark-sector question.

## Ranked Gaps

{row_text}

## Status

```text
{summary["status"]}
```

All rows remain blocked in v01. The immediate next artifact is:

```text
{summary["immediate_next_artifact"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB scoring input gap matrix.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
