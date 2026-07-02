#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GAP_MATRIX = ROOT / "data/derived/tau_cmb_scoring_input_gap_matrix_summary_v01.json"
ROLE_BASIS_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_space_basis_audit_v01.json"
NULL_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_null_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_concrete_R_CMB_carrier_certificate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_concrete_R_CMB_carrier_certificate_v01_certificate_requirements_only_"
    "carrier_not_certified_R_CMB_not_materialized_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "certificate_row_id",
    "certificate_component",
    "formal_object",
    "requirement",
    "evidence_source",
    "current_evidence",
    "certificate_status",
    "blocking_reason",
    "allows_carrier_certificate",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "certificate_component": "carrier_predicate",
        "formal_object": "C_CMB^seed",
        "requirement": "define the well-formed CMB role-space carrier on which R_CMB and quotient relations act",
        "evidence_source": "tau_cmb_readout_role_space_basis_audit_v01",
        "current_evidence": "role-space basis is audited but not carrier-certified",
        "certificate_status": "BLOCKED_CARRIER_PREDICATE_NOT_CERTIFIED",
        "blocking_reason": "carrier predicate remains candidate-level and lacks domain certification",
    },
    {
        "certificate_component": "domain_rule",
        "formal_object": "Dom(R_CMB)",
        "requirement": "state which Tau-side seed/source/control objects are admissible inputs to the CMB readout",
        "evidence_source": "tau_cmb_seed_readout_domain_certificate_v01",
        "current_evidence": "domain-certificate requirements exist but domain is not certified",
        "certificate_status": "BLOCKED_DOMAIN_RULE_NOT_CERTIFIED",
        "blocking_reason": "no accepted domain rule for seed, null seed, or source objects",
    },
    {
        "certificate_component": "codomain_role_space",
        "formal_object": "C_CMB^role = span/product(e_acoustic,e_density,e_lensing,e_growth,e_radiation,e_null)",
        "requirement": "lock the codomain role-space family and role-coordinate typing before concrete readout use",
        "evidence_source": "tau_cmb_readout_role_coordinate_bundle_closure_audit_v01",
        "current_evidence": "six role coordinates are audited but blocked/not score-ready",
        "certificate_status": "PARTIAL_CODOMAIN_AUDITED_NOT_CERTIFIED",
        "blocking_reason": "role coordinates are audit-visible but not materialized as concrete readout coordinates",
    },
    {
        "certificate_component": "concrete_readout_map",
        "formal_object": "R_CMB : Dom(R_CMB) -> C_CMB^role",
        "requirement": "provide the concrete readout map or executable materialization rule from domain objects to role-space coordinates",
        "evidence_source": "tau_cmb_seed_readout_interface_candidate_v01; tau_cmb_scoring_input_gap_matrix_v01",
        "current_evidence": "R_CMB is a schema/interface symbol only",
        "certificate_status": "BLOCKED_CONCRETE_R_CMB_NOT_MATERIALIZED",
        "blocking_reason": "no concrete map, executable rule, replay, or output object is supplied",
    },
    {
        "certificate_component": "null_anchor_compatibility",
        "formal_object": "R_CMB(null_seed_tau_CMB) := null_readout",
        "requirement": "ensure the null/control side is in-domain, materialized, and separated from physical response evidence",
        "evidence_source": "tau_cmb_readout_role_coordinate_null_audit_v01",
        "current_evidence": "null coordinate is audited but blocked/not accepted",
        "certificate_status": "BLOCKED_NULL_ANCHOR_NOT_ACCEPTED",
        "blocking_reason": "null seed is not domain-certified and null readout is not materialized",
    },
    {
        "certificate_component": "dimension_gauge_replay",
        "formal_object": "dimension/gauge/normalization replay for R_CMB",
        "requirement": "lock dimensions, gauge/sign, normalization, and replay metadata for every role coordinate",
        "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01; role-coordinate audits",
        "current_evidence": "dimension roles are declared but replay certificates are not accepted",
        "certificate_status": "BLOCKED_DIMENSION_GAUGE_REPLAY_NOT_CERTIFIED",
        "blocking_reason": "no accepted replay certificate covers the concrete readout map and role outputs",
    },
    {
        "certificate_component": "endpoint_firewall",
        "formal_object": "endpoint_blind(R_CMB materialization)",
        "requirement": "prove that R_CMB carrier/map/codomain choices are not fitted from CMB residuals, scores, or likelihood deltas",
        "evidence_source": "tau_cmb_scoring_input_gap_matrix_v01; endpoint-firewall artifacts",
        "current_evidence": "firewall discipline is declared but cannot certify absent concrete R_CMB values",
        "certificate_status": "BLOCKED_ENDPOINT_FIREWALL_REPLAY_NOT_RUN",
        "blocking_reason": "firewall must be rerun after concrete R_CMB materialization inputs exist",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "certificate_row_id": f"TCMBCRCCC01_{index:03d}",
            "allows_carrier_certificate": "false",
            "allows_concrete_R_CMB": "false",
            "allows_score_entry": "false",
            "allows_likelihood": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(ROWS, start=1)
    ]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    gap = load_json(GAP_MATRIX) if GAP_MATRIX.exists() else {}
    basis = load_json(ROLE_BASIS_AUDIT) if ROLE_BASIS_AUDIT.exists() else {}
    null = load_json(NULL_AUDIT) if NULL_AUDIT.exists() else {}
    input_ok = (
        gap.get("status") == "SCORING_INPUT_GAP_MATRIX_DECLARED_ALL_ROWS_BLOCKED_NO_SCORE"
        and gap.get("input_bundle_closure_audit_clean") is True
        and basis.get("status") == "CMB_READOUT_ROLE_SPACE_BASIS_AUDITED_BLOCKED_NOT_CERTIFIED"
        and basis.get("failed_rows") == 0
        and null.get("status") == "NULL_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_ACCEPTED"
        and null.get("failed_rows") == 0
    )
    return {
        "report_id": "tau_cmb_concrete_R_CMB_carrier_certificate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_scoring_gap_matrix": rel(GAP_MATRIX),
        "input_role_basis_audit": rel(ROLE_BASIS_AUDIT),
        "input_null_coordinate_audit": rel(NULL_AUDIT),
        "input_chain_clean": input_ok,
        "certificate_rows": len(rows),
        "blocked_rows": sum(row["certificate_status"].startswith("BLOCKED") for row in rows),
        "partial_rows": sum(row["certificate_status"].startswith("PARTIAL") for row in rows),
        "carrier_certificate_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED"
            if input_ok
            else "CONCRETE_R_CMB_CARRIER_CERTIFICATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['certificate_component']}`: {row['certificate_status']} | `{row['formal_object']}`"
        for row in rows
    )
    text = f"""# Tau CMB Concrete R_CMB Carrier Certificate v01

**Doc class:** concrete readout carrier certificate requirements
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the requirements for certifying the CMB readout carrier
and concrete `R_CMB` map. It does not certify the carrier, materialize `R_CMB`,
open score entry, compute a likelihood, or decide the dark-sector question.

## Certificate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The first scoring-input gap is now specified as a finite certificate
requirement set. All score permissions remain closed in v01.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB concrete R_CMB carrier certificate requirements.")
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
