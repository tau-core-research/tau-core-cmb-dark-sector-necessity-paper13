#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD = ROOT / "data/derived/tau_cmb_parent_source_unavailability_record_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_parent_source_component_unblock_plan_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_parent_source_component_unblock_plan_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_parent_source_component_unblock_plan_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_parent_source_component_unblock_plan_v01_plan_only_"
    "no_component_supplied_no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)

FIELDS = [
    "plan_row_id",
    "component",
    "priority_rank",
    "why_first_or_later",
    "minimum_deliverable",
    "endpoint_blind_acceptance_test",
    "dimension_or_unit_requirement",
    "replay_requirement",
    "firewall_requirement",
    "current_status",
    "allows_source_acceptance",
    "allows_phi_tau_derivation",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "component": "morphological_seed",
        "priority_rank": "1",
        "why_first_or_later": "Most directly connects Tau Core morphology/readout principle to the CMB source route; without it A_tau remains a free role amplitude.",
        "minimum_deliverable": "endpoint-blind seed_tau_CMB_descriptor with support domain, scale/readout context, and reason it may activate the CMB route",
        "endpoint_blind_acceptance_test": "descriptor must be fixed without CMB peak residuals, lensing residual directions, role scores, or likelihood deltas",
        "dimension_or_unit_requirement": "declare whether seed is dimensionless, scale-indexed, or carries units; if dimensionless, state normalization convention",
        "replay_requirement": "script or static manifest must reproduce the descriptor and hash before scoring",
        "firewall_requirement": "prove no endpoint-derived fields enter the seed descriptor",
        "current_status": "PLANNED_NOT_SUPPLIED",
    },
    {
        "component": "base_field_state",
        "priority_rank": "2",
        "why_first_or_later": "Needed to give the seed a carrier, but by itself it may remain too generic without morphology activation.",
        "minimum_deliverable": "B_tau_base_CMB_descriptor with state class, allowed prior/theory source, and density-slot relation boundary",
        "endpoint_blind_acceptance_test": "must not be selected from density-role, acoustic, or lensing residuals",
        "dimension_or_unit_requirement": "declare field/state dimension or explicitly dimensionless convention",
        "replay_requirement": "manifest or script must reproduce state descriptor and hash",
        "firewall_requirement": "prove no endpoint residual or score field enters B_tau descriptor",
        "current_status": "PLANNED_NOT_SUPPLIED",
    },
    {
        "component": "gauge_normalization_metadata",
        "priority_rank": "3",
        "why_first_or_later": "Can be locked early to prevent convention drift, but it does not create a source by itself.",
        "minimum_deliverable": "locked units, sign, gauge, scale, and normalization policy for shared acoustic/lensing source use",
        "endpoint_blind_acceptance_test": "must be declared before any endpoint comparison and unchanged after scoring",
        "dimension_or_unit_requirement": "complete unit/sign/normalization table",
        "replay_requirement": "hashable convention manifest",
        "firewall_requirement": "prove convention choices are not endpoint-tuned",
        "current_status": "PLANNED_NOT_LOCKED",
    },
    {
        "component": "response_operator_input",
        "priority_rank": "4",
        "why_first_or_later": "Should follow seed/base-field descriptors; otherwise R_tau risks being an unconstrained operator placeholder.",
        "minimum_deliverable": "R_tau_CMB input set with declared domain, codomain, and source-side dependencies",
        "endpoint_blind_acceptance_test": "must not be tuned from CMB likelihood, score deltas, or target shape",
        "dimension_or_unit_requirement": "declare dimensional map from inputs to Phi_tau_eff ingredients",
        "replay_requirement": "script or manifest must reproduce operator input set and hash",
        "firewall_requirement": "prove no role-score or residual-tuning fields enter R_tau",
        "current_status": "PLANNED_NOT_SUPPLIED",
    },
    {
        "component": "endpoint_firewall_certificate",
        "priority_rank": "5",
        "why_first_or_later": "Certificate is required for acceptance, but it must certify a populated component rather than an empty shell.",
        "minimum_deliverable": "packet-level endpoint firewall certificate for at least one populated source component",
        "endpoint_blind_acceptance_test": "must reject score outputs, residual tables, target-shape labels, and fit-selected choices",
        "dimension_or_unit_requirement": "not physical; must bind to component dimensional metadata",
        "replay_requirement": "certificate generation command and hash",
        "firewall_requirement": "the certificate is the firewall artifact",
        "current_status": "PLANNED_NOT_EXECUTED",
    },
    {
        "component": "provenance_replay_rule",
        "priority_rank": "6",
        "why_first_or_later": "Replay must accompany supplied values; alone it only reproduces absence.",
        "minimum_deliverable": "replay rule regenerating the populated component and artifact hashes without endpoint reads",
        "endpoint_blind_acceptance_test": "must not read score directories, residual tables, or post-score patch files",
        "dimension_or_unit_requirement": "not physical; must preserve component dimensional metadata",
        "replay_requirement": "the replay rule is the required object",
        "firewall_requirement": "replay logs must show no endpoint-derived inputs",
        "current_status": "PLANNED_NOT_SUPPLIED",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "plan_row_id": f"TCMBPSUP01_{index:03d}",
            "allows_source_acceptance": "false",
            "allows_phi_tau_derivation": "false",
            "allows_score_entry": "false",
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


def build_summary(record_path: Path, table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    record = read_json(record_path)
    return {
        "report_id": "tau_cmb_parent_source_component_unblock_plan_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_unavailability_record": rel(record_path),
        "source_unavailability_status": record.get("status", "UNKNOWN"),
        "table": rel(table_path),
        "plan_rows": len(rows),
        "first_component_to_attempt": "morphological_seed",
        "first_component_reason": "It is the shortest bridge from Tau Core morphology/readout theory to A_tau(a,k) activation without endpoint data.",
        "component_supplied": False,
        "source_acceptance_allowed": False,
        "phi_tau_derivation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "PARENT_SOURCE_COMPONENT_UNBLOCK_PLAN_DECLARED_NO_COMPONENT_SUPPLIED",
        "next_minimal_unblock": "materialize_endpoint_blind_morphological_seed_descriptor_candidate",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['plan_row_id']}` rank {row['priority_rank']} `{row['component']}`: {row['minimum_deliverable']}"
        for row in rows
    )
    text = f"""# Tau CMB Parent-Source Component Unblock Plan v01

**Doc class:** parent-source component unblock plan
**Status:** {summary["status"]}
**Source unavailability record:** `{summary["source_unavailability_record"]}`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact turns the clean source-unavailability stop-state into a ranked
component plan. It does not supply any component and does not accept a CMB
source. It only answers which single component should be attempted first.

## Ranked Components

{row_text}

## First Component

```text
{summary["first_component_to_attempt"]}
```

Reason:

```text
{summary["first_component_reason"]}
```

Starting with the morphological seed is the narrowest Tau Core-specific move:
it tests whether the CMB source route has a morphology/readout activation
object before trying to define a response operator or score-facing potential.

## Status

```text
{summary["status"]}
```

No source acceptance, `Phi_tau_eff` derivation, score entry, no-dark claim,
Tau-response success claim, or dark-sector verdict is allowed.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB parent-source component unblock plan.")
    parser.add_argument("--record", default=str(DEFAULT_RECORD))
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    rows = table_rows()
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(Path(args.record), table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
