#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_morphological_seed_descriptor_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_morphological_seed_descriptor_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_morphological_seed_descriptor_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_morphological_seed_descriptor_candidate_v01_candidate_only_"
    "no_seed_acceptance_no_source_acceptance_no_A_tau_derivation_no_phi_derivation_no_score_no_verdict"
)

TAU_CORE_MORPHOLOGY_PRINCIPLE = (
    "/Users/jolcsak/Projects/tau-core-theory/source_material/"
    "tau_core_foundations/morphology_conditioned_projection_principle_v01.md"
)
UNBLOCK_PLAN = "docs/tau_cmb_parent_source_component_unblock_plan_v01.md"

FIELDS = [
    "seed_row_id",
    "descriptor_component",
    "candidate_value",
    "candidate_role",
    "tau_core_anchor",
    "endpoint_blind_basis",
    "dimension_or_unit_status",
    "support_domain",
    "activation_path",
    "required_next_audit",
    "current_status",
    "artifact_hash",
    "allows_seed_acceptance",
    "allows_source_acceptance",
    "allows_A_tau_derivation",
    "allows_phi_tau_derivation",
    "allows_score_entry",
    "claim_boundary",
]


ROWS = [
    {
        "descriptor_component": "seed_identity",
        "candidate_value": "seed_tau_CMB_morphology_readout_activation_candidate_v01",
        "candidate_role": "stable name for an endpoint-blind CMB morphological seed descriptor candidate",
        "tau_core_anchor": TAU_CORE_MORPHOLOGY_PRINCIPLE,
        "endpoint_blind_basis": "declared from Tau Core morphology/readout principle and Paper 13 source-grounding route, not from CMB endpoint residuals",
        "dimension_or_unit_status": "not_physical_identifier",
        "support_domain": "CMB parent-source freeze packet / morphological_seed row",
        "activation_path": "seed_tau_CMB -> possible A_tau(a,k) activation object",
        "required_next_audit": "identity stability and endpoint-exclusion audit",
        "current_status": "CANDIDATE_DECLARED_NOT_ACCEPTED",
    },
    {
        "descriptor_component": "intrinsic_morphology_basis",
        "candidate_value": "M_tau^CMB as parent-side projection-conditioning morphology class",
        "candidate_role": "connect CMB source route to intrinsic Tau morphology rather than projected endpoint residuals",
        "tau_core_anchor": TAU_CORE_MORPHOLOGY_PRINCIPLE,
        "endpoint_blind_basis": "uses parent-side morphology definition only; no endpoint residual shape is read",
        "dimension_or_unit_status": "dimensionless_structure_class_pending_normalization",
        "support_domain": "parent Tau morphology / CMB readout sector",
        "activation_path": "M_tau^CMB conditions P_CMB[M_tau] and may constrain A_tau(a,k)",
        "required_next_audit": "admissible morphology and quotient/null survival audit",
        "current_status": "CANDIDATE_DECLARED_NOT_ACCEPTED",
    },
    {
        "descriptor_component": "readout_context",
        "candidate_value": "CMB readout family with acoustic/lensing/growth/radiation roles declared but unscored",
        "candidate_role": "bind seed to a CMB readout context without importing endpoint score information",
        "tau_core_anchor": "docs/tau_cmb_cosmology_derivation_spine_v01.md",
        "endpoint_blind_basis": "role families are declared by the derivation spine and constraints, not selected from fit improvement",
        "dimension_or_unit_status": "readout_context_not_physical_quantity",
        "support_domain": "rho_tau_eff, Phi_tau_eff, T_tau_CMB, K_tau_PP obligations",
        "activation_path": "readout context constrains where seed may act; it does not set amplitude",
        "required_next_audit": "readout-survival and role-boundary audit",
        "current_status": "CANDIDATE_DECLARED_NOT_ACCEPTED",
    },
    {
        "descriptor_component": "activation_claim_boundary",
        "candidate_value": "seed may only support a future A_tau(a,k) activation after quotient, closure, and readout audits pass",
        "candidate_role": "prevent seed descriptor from being treated as an amplitude or source equation",
        "tau_core_anchor": UNBLOCK_PLAN,
        "endpoint_blind_basis": "boundary is declared before endpoint scoring and forbids residual-derived amplitude",
        "dimension_or_unit_status": "not_physical_guard",
        "support_domain": "A_tau(a,k) role boundary",
        "activation_path": "seed descriptor -> audit gates -> possible A_tau candidate, not direct source acceptance",
        "required_next_audit": "activation sufficiency audit",
        "current_status": "BOUNDARY_DECLARED_NOT_ACCEPTED",
    },
    {
        "descriptor_component": "forbidden_endpoint_inputs",
        "candidate_value": "ACT residuals; Planck residuals; CMB role scores; likelihood deltas; peak residual shapes; lensing residual directions",
        "candidate_role": "declare fields that cannot enter the seed descriptor",
        "tau_core_anchor": "docs/tau_cmb_parent_source_freeze_packet_v01.md",
        "endpoint_blind_basis": "explicit firewall list",
        "dimension_or_unit_status": "not_physical_firewall_metadata",
        "support_domain": "seed_tau_CMB firewall",
        "activation_path": "firewall metadata protects later activation audit",
        "required_next_audit": "endpoint-token and provenance firewall audit",
        "current_status": "FIREWALL_METADATA_DECLARED_NOT_EXECUTED",
    },
]


def stable_row_hash(row: dict[str, str]) -> str:
    payload = json.dumps({k: v for k, v in row.items() if k != "artifact_hash"}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(ROWS, start=1):
        full = {
            "seed_row_id": f"TCMBMSD01_{index:03d}",
            "artifact_hash": "",
            "allows_seed_acceptance": "false",
            "allows_source_acceptance": "false",
            "allows_A_tau_derivation": "false",
            "allows_phi_tau_derivation": "false",
            "allows_score_entry": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        full["artifact_hash"] = stable_row_hash(full)
        rows.append(full)
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_morphological_seed_descriptor_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "rows": len(rows),
        "artifact_hash_rows": sum(bool(row["artifact_hash"]) for row in rows),
        "seed_candidate_declared": True,
        "seed_accepted": False,
        "source_acceptance_allowed": False,
        "A_tau_derivation_allowed": False,
        "phi_tau_derivation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "MORPHOLOGICAL_SEED_DESCRIPTOR_CANDIDATE_DECLARED_NOT_ACCEPTED",
        "next_minimal_unblock": "audit_endpoint_blind_morphological_seed_descriptor_candidate",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['seed_row_id']}` `{row['descriptor_component']}`: {row['current_status']} | `{row['candidate_value']}`"
        for row in rows
    )
    text = f"""# Tau CMB Morphological Seed Descriptor Candidate v01

**Doc class:** endpoint-blind CMB morphological-seed descriptor candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact materializes the first component from the parent-source unblock
plan: an endpoint-blind morphological-seed descriptor candidate. It is motivated
by the Tau Core morphology-conditioned projection principle, but it is not an
accepted seed and not a source equation.

## Candidate Rows

{row_text}

## Interpretation

The candidate says only this:

```text
There may be a parent-side CMB morphology/readout activation descriptor worth
auditing before any A_tau(a,k), rho_tau_eff, Phi_tau_eff, or score route is
opened.
```

It does not supply an amplitude, transfer operator, projection kernel, or CMB
fit. It cannot be used for source acceptance.

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
    parser = argparse.ArgumentParser(description="Build Tau CMB morphological seed descriptor candidate.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    rows = table_rows()
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
