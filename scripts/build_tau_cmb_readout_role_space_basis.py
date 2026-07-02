#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OBLIGATION_SUMMARY = ROOT / "data/derived/tau_cmb_seed_readout_equivalence_axiom_proof_obligation_summary_v01.json"
DERIVATION_SPINE = ROOT / "data/derived/tau_cmb_cosmology_derivation_spine_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_space_basis_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_space_basis_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_space_basis_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_space_basis_v01_basis_candidate_only_"
    "carrier_not_certified_no_concrete_R_CMB_no_equivalence_proof_no_readout_evaluation_no_score_no_verdict"
)

FIELDS = [
    "basis_row_id",
    "role_slot",
    "basis_symbol",
    "role_space_component",
    "dimension_role",
    "source_dependency",
    "forbidden_dependency",
    "basis_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_carrier_certification",
    "allows_concrete_R_CMB",
    "allows_equivalence_proof",
    "allows_readout_evaluation",
    "allows_score_entry",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "role_slot": "acoustic_phase_height",
        "basis_symbol": "e_acoustic",
        "role_space_component": "acoustic peak phase and relative-height role coordinate",
        "dimension_role": "dimensionless comparison role; no endpoint amplitude fitted",
        "source_dependency": "Tau CMB derivation spine role map and acoustic reduced-evaluation blocker",
        "forbidden_dependency": "ACT/Planck peak residual optimization or likelihood tuning",
        "basis_status": "BASIS_ROLE_DECLARED_NOT_MATERIALIZED",
        "blocking_reason": "no concrete readout coordinate, uncertainty model, or transfer normalization is supplied",
        "next_required_artifact": "tau_cmb_readout_role_coordinate_acoustic_v01",
    },
    {
        "role_slot": "density_amplitude",
        "basis_symbol": "e_density",
        "role_space_component": "omega_c_h2 / rho_tau_eff role coordinate",
        "dimension_role": "density-slot role; physical density units only after rho_ref and A_tau are accepted",
        "source_dependency": "rho_tau_eff(a,k) conditional role formula",
        "forbidden_dependency": "choosing A_tau from CMB density residuals",
        "basis_status": "BASIS_ROLE_DECLARED_NOT_MATERIALIZED",
        "blocking_reason": "rho_ref, A_tau derivation, and density normalization are not accepted",
        "next_required_artifact": "tau_cmb_readout_role_coordinate_density_v01",
    },
    {
        "role_slot": "lensing_potential",
        "basis_symbol": "e_lensing",
        "role_space_component": "Phi_lens_tau / C_L^phiphi / PP role coordinate",
        "dimension_role": "potential or PP convention must be declared before comparison",
        "source_dependency": "T_tau_CMB, K_tau_PP, and N_projection_physical obligations",
        "forbidden_dependency": "post-hoc PP residual shape or score-grid fitting",
        "basis_status": "BASIS_ROLE_DECLARED_NOT_MATERIALIZED",
        "blocking_reason": "transfer operator, projection kernel, and normalization are not accepted",
        "next_required_artifact": "tau_cmb_readout_role_coordinate_lensing_v01",
    },
    {
        "role_slot": "growth_transfer",
        "basis_symbol": "e_growth",
        "role_space_component": "growth/transfer consistency role coordinate",
        "dimension_role": "dimensionless transfer or growth ratio convention required",
        "source_dependency": "growth transfer kernel closure scaffold",
        "forbidden_dependency": "using endpoint growth mismatch to define the coordinate",
        "basis_status": "BASIS_ROLE_DECLARED_NOT_MATERIALIZED",
        "blocking_reason": "no accepted growth-transfer kernel or normalization is supplied",
        "next_required_artifact": "tau_cmb_readout_role_coordinate_growth_v01",
    },
    {
        "role_slot": "radiation_damping_guard",
        "basis_symbol": "e_radiation",
        "role_space_component": "damping-tail / radiation guard role coordinate",
        "dimension_role": "guard role; no source amplitude without radiation-limit proof",
        "source_dependency": "radiation guard evaluation and known-limit audit",
        "forbidden_dependency": "using damping-tail residuals to tune a Tau source",
        "basis_status": "BASIS_ROLE_DECLARED_NOT_MATERIALIZED",
        "blocking_reason": "radiation-limit proof and guard-bound acceptance are not supplied",
        "next_required_artifact": "tau_cmb_readout_role_coordinate_radiation_v01",
    },
    {
        "role_slot": "null_readout",
        "basis_symbol": "e_null",
        "role_space_component": "null_readout baseline coordinate",
        "dimension_role": "zero/null control role; not physical source evidence",
        "source_dependency": "audited zero-control candidate",
        "forbidden_dependency": "nonzero baseline inserted to improve score readiness",
        "basis_status": "NULL_BASIS_ANCHOR_DECLARED_NOT_ACCEPTED",
        "blocking_reason": "zero-control is audited but not accepted as a readout-domain member",
        "next_required_artifact": "tau_cmb_seed_readout_domain_certificate_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "basis_row_id": f"TCMBRRSB01_{index:03d}",
            "allows_carrier_certification": "false",
            "allows_concrete_R_CMB": "false",
            "allows_equivalence_proof": "false",
            "allows_readout_evaluation": "false",
            "allows_score_entry": "false",
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
    obligation = load_json(OBLIGATION_SUMMARY) if OBLIGATION_SUMMARY.exists() else {}
    input_ok = (
        obligation.get("status") == "SEED_READOUT_EQUIVALENCE_AXIOM_PROOF_OBLIGATION_DECLARED_BLOCKED"
        and obligation.get("input_equivalence_audit_clean") is True
    )
    spine_exists = DERIVATION_SPINE.exists()
    return {
        "report_id": "tau_cmb_readout_role_space_basis_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_axiom_obligation": rel(OBLIGATION_SUMMARY),
        "input_axiom_obligation_clean": input_ok,
        "derivation_spine_present": spine_exists,
        "basis_rows": len(rows),
        "role_slots_declared": [row["role_slot"] for row in rows],
        "carrier_predicate_candidate": "C_CMB^seed := span_or_product_role_basis(e_acoustic,e_density,e_lensing,e_growth,e_radiation,e_null)",
        "carrier_certification_allowed": False,
        "concrete_R_CMB_allowed": False,
        "equivalence_proof_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_SPACE_BASIS_CANDIDATE_DECLARED_NOT_CERTIFIED"
            if input_ok and spine_exists
            else "CMB_READOUT_ROLE_SPACE_BASIS_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_space_basis_audit_v01"
            if input_ok and spine_exists
            else "repair_role_space_basis_inputs"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['basis_row_id']}` `{row['role_slot']}`: {row['basis_status']} | `{row['basis_symbol']}`"
        for row in rows
    )
    text = f"""# Tau CMB Readout Role Space Basis v01

**Doc class:** CMB readout role-space basis candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the candidate role-space basis needed to type the future
carrier predicate `C_CMB^seed`. It does not certify the carrier, materialize a
concrete `R_CMB`, prove the equivalence relation, evaluate CMB readout, enter
scoring, or decide the dark-sector question.

## Candidate Carrier Shape

```text
{summary["carrier_predicate_candidate"]}
```

This is a role-space basis candidate, not a vector-space theorem and not a
numerical CMB likelihood basis. Each role coordinate still needs its own
coordinate definition, unit/dimension replay, and endpoint-blind provenance.

## Basis Rows

{row_text}

## Status

```text
{summary["status"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB readout role-space basis candidate.")
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
