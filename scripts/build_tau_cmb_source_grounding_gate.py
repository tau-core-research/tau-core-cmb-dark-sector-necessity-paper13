#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_source_grounding_gate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_source_grounding_gate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_source_grounding_gate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_source_grounding_gate_v01_gate_only_"
    "no_cmb_source_acceptance_no_transfer_kernel_no_projection_kernel_"
    "no_score_no_dark_sector_verdict"
)

PAPER10_SOURCE_FREEZE = (
    "/Users/jolcsak/Projects/tau-core-cosmology-friedmann-readout-paper10/"
    "data/source_manifest/cosmology_source_grounding_gate_v1.csv"
)
TAU_CORE_MORPHOLOGY_PRINCIPLE = (
    "/Users/jolcsak/Projects/tau-core-theory/source_material/"
    "tau_core_foundations/morphology_conditioned_projection_principle_v01.md"
)
TAU_CORE_READOUT_FORMALIZATION = (
    "/Users/jolcsak/Projects/tau-core-theory/docs/"
    "tau_core_morphological_readout_formalization_sketches_001.md"
)
DERIVATION_SPINE = "docs/tau_cmb_cosmology_derivation_spine_v01.md"
PARENT_SOURCE_FREEZE_PACKET = "docs/tau_cmb_parent_source_freeze_packet_v01.md"


ROWS = [
    {
        "gate_component": "paper10_source_freeze_import",
        "role": "Import the Paper 10 rule that source labels must be frozen before endpoint residuals, role scores, or fit-improvement information are used.",
        "source_anchor": PAPER10_SOURCE_FREEZE,
        "cmb_spine_binding": "precondition for TCMBCDS01_002 rho_tau_eff(a,k)",
        "required_test": "CMB parent/source inputs must exclude ACT/Planck residuals, CMB role scores, likelihood residuals, and post-hoc source choices.",
        "current_status": "METHOD_IMPORTED_NOT_CMB_SOURCE_ACCEPTANCE",
        "blocks": "rho_tau_eff cannot be promoted from a residual-selected CMB source",
    },
    {
        "gate_component": "morphology_activation",
        "role": "Require a Tau-side morphology or seed descriptor that conditions the CMB readout route before a source amplitude is accepted.",
        "source_anchor": TAU_CORE_MORPHOLOGY_PRINCIPLE,
        "cmb_spine_binding": "precondition for A_tau(a,k) in TCMBCDS01_002",
        "required_test": "Declare the parent-side morphology/readout object and show why it activates a CMB source channel without seeing the endpoint.",
        "current_status": "DECLARED_NOT_DERIVED_FOR_CMB",
        "blocks": "A_tau remains a role amplitude rather than a Tau-derived activation",
    },
    {
        "gate_component": "quotient_survival",
        "role": "Remove null, gauge, survey, convention, and coordinate artifacts without erasing the candidate source.",
        "source_anchor": TAU_CORE_READOUT_FORMALIZATION,
        "cmb_spine_binding": "precondition for TCMBCDS01_002 and TCMBCDS01_003",
        "required_test": "Show that the candidate survives the relevant quotient/null controls as a source object, not a coordinate or readout artifact.",
        "current_status": "REQUIRED_NOT_PROVED",
        "blocks": "rho_tau_eff and Phi_tau_eff cannot be distinguished from null/gauge leakage",
    },
    {
        "gate_component": "closure_stability",
        "role": "Require a stable source/readout closure relation before using the candidate in the CMB perturbation chain.",
        "source_anchor": DERIVATION_SPINE,
        "cmb_spine_binding": "precondition for TCMBCDS01_003 Phi_tau_eff(a,k)",
        "required_test": "Demonstrate a stable closure path from the source to the effective potential slot under the declared conventions.",
        "current_status": "REQUIRED_NOT_PROVED",
        "blocks": "Phi_tau_eff remains a comparison slot, not a stable Tau-side potential source",
    },
    {
        "gate_component": "readout_survival",
        "role": "Require the source to survive the CMB readout map into acoustic, lensing, growth, and radiation-guard roles.",
        "source_anchor": TAU_CORE_READOUT_FORMALIZATION,
        "cmb_spine_binding": "precondition for TCMBCDS01_004 T_tau_CMB(k,a)",
        "required_test": "Show nonzero, convention-stable readout response under the CMB transfer/readout family before score use.",
        "current_status": "REQUIRED_NOT_PROVED",
        "blocks": "T_tau_CMB cannot be treated as an available physical transfer operator",
    },
    {
        "gate_component": "derivation_spine_binding",
        "role": "Bind the accepted source path to the declared CMB formula chain instead of allowing an untracked residual handoff.",
        "source_anchor": DERIVATION_SPINE,
        "cmb_spine_binding": "TCMBCDS01_002 -> TCMBCDS01_006",
        "required_test": "Every accepted source row must map to rho_tau_eff, Phi_tau_eff, T_tau_CMB, K_tau_PP, and N_projection_physical obligations.",
        "current_status": "BINDING_DECLARED_PARTIAL",
        "blocks": "source grounding does not yet discharge kernel, measure, normalization, or zero-source obligations",
    },
    {
        "gate_component": "endpoint_firewall",
        "role": "Prevent source acceptance or scoring from using endpoint data before the source route is frozen and replayable.",
        "source_anchor": PAPER10_SOURCE_FREEZE,
        "cmb_spine_binding": "precondition for TCMBCDS01_008 endpoint-blind CMB score grid",
        "required_test": "Reject any source or operator packet populated from CMB endpoint residuals, score deltas, or target-shape leakage.",
        "current_status": "REQUIRED_NOT_PASSED_FOR_POPULATED_SOURCE",
        "blocks": "no score, no physical Tau-route score, and no dark-sector verdict may be run from this gate",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(ROWS, start=1):
        rows.append(
            {
                "gate_row_id": f"TCMBSGG01_{index:03d}",
                "source_acceptance_allowed": "false",
                "score_entry_allowed": "false",
                "physical_tau_score_allowed": "false",
                "dark_sector_verdict_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                **row,
            }
        )
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_source_grounding_gate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "status": "SOURCE_GROUNDING_GATE_DECLARED_BLOCKED",
        "gate_rows": len(rows),
        "method_imported_rows": [row["gate_row_id"] for row in rows if row["current_status"].startswith("METHOD_IMPORTED")],
        "declared_partial_rows": [row["gate_row_id"] for row in rows if "DECLARED" in row["current_status"]],
        "required_not_proved_rows": [row["gate_row_id"] for row in rows if "NOT_PROVED" in row["current_status"]],
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "physical_tau_score_allowed": False,
        "dark_sector_verdict_allowed": False,
        "paper10_source_freeze_reference": PAPER10_SOURCE_FREEZE,
        "tau_core_morphology_reference": TAU_CORE_MORPHOLOGY_PRINCIPLE,
        "tau_core_readout_reference": TAU_CORE_READOUT_FORMALIZATION,
        "derivation_spine": DERIVATION_SPINE,
        "parent_source_freeze_packet": PARENT_SOURCE_FREEZE_PACKET,
        "next_minimal_unblock": (
            "populate_endpoint_blind_CMB_parent_source_freeze_packet_with_hashable_replay"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['gate_row_id']}` `{row['gate_component']}`: "
            f"{row['current_status']} | binding: `{row['cmb_spine_binding']}` | "
            f"blocks: {row['blocks']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Source Grounding Gate v01

**Doc class:** CMB source-grounding gate
**Reader role:** Paper 13 / Tau CMB implementer
**Status:** declared but blocked; no source acceptance, no score, no verdict
**Canonical parent:** `paper13_submission_source/main.tex`
**Direct spine:** `{DERIVATION_SPINE}`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact directly binds three already-separated pieces of the program:

```text
Paper 10 source-freeze discipline
+ Tau Core morphology/readout principle
-> Paper 13 CMB derivation spine
```

It is not a new CMB source derivation. It is a gate that says what must be true
before a Tau-side CMB source may enter the formula chain

```text
rho_tau_eff(a,k)
-> Phi_tau_eff(a,k)
-> T_tau_CMB(k,a)
-> K_tau_PP(L; a,k) dmu(a,k)
-> tau_PP(L)
```

The gate preserves the Paper 10 source-freeze idea: source-side labels,
operators, and amplitudes must be fixed before endpoint residuals, scores, or
fit-improvement information are inspected.

## External Program Anchors

- Paper 10 source-freeze/source-grounding gate:
  `{PAPER10_SOURCE_FREEZE}`
- Tau Core morphology-conditioned projection principle:
  `{TAU_CORE_MORPHOLOGY_PRINCIPLE}`
- Tau Core morphological readout formalization:
  `{TAU_CORE_READOUT_FORMALIZATION}`
- Paper 13 derivation spine:
  `{DERIVATION_SPINE}`
- CMB parent-source freeze packet:
  `{PARENT_SOURCE_FREEZE_PACKET}`

## Gate Rows

{row_text}

## Logical Map

```text
source-freeze
-> morphology activation
-> quotient/null survival
-> closure stability
-> CMB readout survival
-> derivation spine binding
-> endpoint firewall
-> only then: scoring-entry consideration
```

## Status

```text
{summary["status"]}
```

This gate accepts no CMB source in v01. It supplies no `T_tau_CMB`, no
`K_tau_PP`, no projection measure, no physical normalization, and no score.
It therefore permits no no-dark claim, no Tau-response success claim, and no
dark-sector verdict.

The first concrete downstream deliverable is the parent-source freeze packet:

```text
{PARENT_SOURCE_FREEZE_PACKET}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB source-grounding gate.")
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
