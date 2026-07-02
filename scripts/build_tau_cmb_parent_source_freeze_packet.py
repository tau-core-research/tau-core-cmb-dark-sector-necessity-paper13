#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_parent_source_freeze_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_parent_source_freeze_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_parent_source_freeze_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_parent_source_freeze_packet_v01_freeze_packet_only_"
    "no_source_acceptance_no_phi_derivation_no_transfer_kernel_no_score_no_verdict"
)

SOURCE_GROUNDING_GATE = "docs/tau_cmb_source_grounding_gate_v01.md"
PARENT_INPUT_MANIFEST = "docs/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.md"
DERIVATION_SPINE = "docs/tau_cmb_cosmology_derivation_spine_v01.md"
SUBMISSION_TEMPLATE = "payload_templates/tau_cmb_parent_source_freeze_packet_submission_TEMPLATE_v01.csv"
SUBMISSION_CANDIDATE = "payloads/tau_cmb_parent_source_freeze_packet_submission_candidate_v01.csv"


ROWS = [
    {
        "freeze_component": "freeze_packet_identity",
        "object_to_freeze": "CMB_parent_source_freeze_packet_v01",
        "freeze_requirement": "Declare a named packet before any CMB endpoint residual, role score, or likelihood output is read.",
        "allowed_input_family": "pre-endpoint Tau-side source metadata and replay metadata",
        "forbidden_input_family": "ACT residuals; Planck residuals; CMB role score outputs; fit-improvement flags; post-hoc source choices",
        "binding_target": "TCMBSGG01_001 paper10_source_freeze_import",
        "current_status": "FREEZE_PACKET_DECLARED_NOT_ACCEPTED",
        "remaining_blocker": "packet is not populated with accepted parent-side source records",
    },
    {
        "freeze_component": "base_field_state",
        "object_to_freeze": "B_tau_base^CMB",
        "freeze_requirement": "Freeze the Tau base-field state descriptor used by the CMB source route.",
        "allowed_input_family": "Tau Core base-field/theory-side assumptions, non-endpoint parent evidence, declared prior conventions",
        "forbidden_input_family": "density-role residuals; acoustic mismatch shape; lensing mismatch amplitude",
        "binding_target": "rho_tau_eff(a,k) source carrier",
        "current_status": "REQUIRED_NOT_SUPPLIED",
        "remaining_blocker": "no concrete base-field descriptor is supplied",
    },
    {
        "freeze_component": "morphological_seed",
        "object_to_freeze": "seed_tau^CMB",
        "freeze_requirement": "Freeze the morphology/seed descriptor that may activate the CMB source route.",
        "allowed_input_family": "parent-side morphology, seed, boundary, capacity, or readout-context descriptors",
        "forbidden_input_family": "peak-residual pattern; lensing residual direction; endpoint-selected morphology",
        "binding_target": "A_tau(a,k) morphology activation",
        "current_status": "REQUIRED_NOT_SUPPLIED",
        "remaining_blocker": "no accepted morphology/seed descriptor is supplied",
    },
    {
        "freeze_component": "response_operator_input",
        "object_to_freeze": "R_tau^CMB input set",
        "freeze_requirement": "Freeze the response-operator input set before deriving Phi_tau_eff.",
        "allowed_input_family": "declared Tau response rule inputs, source-side scale/time labels, predeclared operator domain",
        "forbidden_input_family": "operator tuning from CMB likelihood, score deltas, or endpoint target shape",
        "binding_target": "Phi_tau_eff(a,k) derivation path",
        "current_status": "REQUIRED_NOT_SUPPLIED",
        "remaining_blocker": "no replayable response-operator input set is supplied",
    },
    {
        "freeze_component": "gauge_normalization_metadata",
        "object_to_freeze": "gauge_norm_tau^CMB",
        "freeze_requirement": "Freeze units, sign, gauge, scale, and normalization conventions before acoustic/lensing comparison.",
        "allowed_input_family": "convention declarations, dimensional metadata, fixed normalization policy",
        "forbidden_input_family": "normalization selected after endpoint comparison",
        "binding_target": "shared Phi_tau_eff convention and K_tau_PP/N_projection obligations",
        "current_status": "REQUIRED_NOT_LOCKED",
        "remaining_blocker": "metadata are not locked and audited",
    },
    {
        "freeze_component": "endpoint_firewall_certificate",
        "object_to_freeze": "source_freeze_firewall_certificate",
        "freeze_requirement": "Certify that the packet contains no endpoint-derived fields.",
        "allowed_input_family": "static audit metadata and pre-score provenance checks",
        "forbidden_input_family": "score outputs; endpoint residual tables; target-shape labels; fit-selected source choices",
        "binding_target": "TCMBSGG01_007 endpoint_firewall",
        "current_status": "REQUIRED_NOT_EXECUTED",
        "remaining_blocker": "no packet-level endpoint firewall certificate is supplied",
    },
    {
        "freeze_component": "provenance_replay_rule",
        "object_to_freeze": "freeze_packet_replay_rule",
        "freeze_requirement": "Provide a replay rule that can regenerate the frozen packet before score execution.",
        "allowed_input_family": "scripted source-side packet build inputs and hash/provenance metadata",
        "forbidden_input_family": "manual post-score edits; runtime reads from score directories; residual-derived patch data",
        "binding_target": "score entry precondition",
        "current_status": "REQUIRED_NOT_SUPPLIED",
        "remaining_blocker": "no executable replay rule or hash certificate is supplied",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(ROWS, start=1):
        rows.append(
            {
                "freeze_row_id": f"TCMBPSF01_{index:03d}",
                "frozen_value_supplied": "false",
                "packet_acceptance_allowed": "false",
                "source_acceptance_allowed": "false",
                "score_entry_allowed": "false",
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
        "report_id": "tau_cmb_parent_source_freeze_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "source_grounding_gate": SOURCE_GROUNDING_GATE,
        "parent_input_manifest": PARENT_INPUT_MANIFEST,
        "derivation_spine": DERIVATION_SPINE,
        "submission_template": SUBMISSION_TEMPLATE,
        "submission_candidate": SUBMISSION_CANDIDATE,
        "status": "PARENT_SOURCE_FREEZE_PACKET_DECLARED_UNPOPULATED",
        "freeze_rows": len(rows),
        "frozen_value_supplied_rows": 0,
        "required_not_supplied_rows": [
            row["freeze_row_id"]
            for row in rows
            if "REQUIRED_NOT" in row["current_status"]
        ],
        "packet_acceptance_allowed": False,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_minimal_unblock": "populate_endpoint_blind_CMB_parent_source_freeze_packet_with_hashable_replay",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['freeze_row_id']}` `{row['freeze_component']}`: "
            f"{row['current_status']} | freeze: `{row['object_to_freeze']}` | "
            f"blocks: {row['remaining_blocker']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Parent-Source Freeze Packet v01

**Doc class:** endpoint-blind CMB parent-source freeze packet
**Reader role:** Paper 13 / Tau CMB implementer
**Status:** declared but unpopulated; no source acceptance, no score, no verdict
**Source-grounding gate:** `{SOURCE_GROUNDING_GATE}`
**Parent-input manifest:** `{PARENT_INPUT_MANIFEST}`
**Derivation spine:** `{DERIVATION_SPINE}`
**Submission template:** `{SUBMISSION_TEMPLATE}`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet is the first concrete source-freeze object under the CMB
source-grounding gate. It specifies what must be frozen before a Tau-side CMB
source can be considered for

```text
rho_tau_eff(a,k) -> Phi_tau_eff(a,k).
```

It does not populate those values. It does not accept a source. It does not
derive `Phi_tau_eff`, `T_tau_CMB`, or `K_tau_PP`, and it does not permit a score.

## Frozen Fields

{row_text}

## Forbidden Endpoint Inputs

The packet must not read or encode:

```text
ACT residuals
Planck residuals
CMB role score outputs
fit-improvement flags
post-hoc source choices
operator tuning from endpoint target shape
```

## Status

```text
{summary["status"]}
```

The packet is intentionally unpopulated in v01. Its value is that it turns the
next step into a finite deliverable: supply the frozen base-field state,
morphological seed, response-operator inputs, gauge/normalization metadata,
firewall certificate, and replay rule before any scoring route is opened.

The concrete submission shape is:

```text
{SUBMISSION_TEMPLATE}
```

The current replayable negative candidate is:

```text
{SUBMISSION_CANDIDATE}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB parent-source freeze packet.")
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
