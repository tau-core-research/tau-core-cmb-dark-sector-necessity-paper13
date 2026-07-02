#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/tau_cmb_lensing_N_parent_projection_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_lensing_N_parent_projection_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_lensing_N_parent_projection_packet_v01.md"


ROWS = [
    {
        "component_id": "N_parent_source",
        "role": "Tau-side CMB source amplitude/units before lensing projection",
        "symbol": "N_parent_source",
        "required_derivation": "endpoint-blind Phi_tau_eff(a,k) source normalization and A_tau(a,k) amplitude convention",
        "current_value": "",
        "dimension_status": "BLOCKED_DIMENSION_OR_UNIT_PROOF_NOT_SUPPLIED",
        "firewall_status": "BLOCKED_ENDPOINT_FIREWALL_CERTIFICATE_NOT_SUPPLIED",
        "source_evidence": "docs/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.md; docs/tau_cmb_effective_potential_source_handoff_v01.md",
        "acceptance_rule": "must be fixed before ACT/Planck residual or score inspection",
        "claim_boundary": "packet_skeleton_only_no_numeric_normalization_no_score_no_verdict",
    },
    {
        "component_id": "N_projection",
        "role": "Tau effective-potential/readout source to L-space PP or delta_PP_tau projection normalization",
        "symbol": "N_projection",
        "required_derivation": "projection operator domain/codomain, lensing kernel support, L-space transfer convention, replay rule",
        "current_value": "",
        "dimension_status": "EXPLICIT_NON_SCORE_FAILURE_PHYSICAL_PROJECTION_OPERATOR_NOT_SUPPLIED",
        "firewall_status": "FIREWALL_PASS_FOR_CURRENT_SKELETON_ONLY_RERUN_AFTER_VALUES",
        "source_evidence": "docs/cmb_tau_lensing_projection_operator_explicit_failure_v01.md; docs/cmb_tau_lensing_projection_operator_decision_gate_v01.md; docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md; docs/cmb_tau_lensing_projection_normalization_split_v01.md",
        "acceptance_rule": "may resume only by replacing explicit failure with endpoint-blind Projection_PP operator, normalization, replay, and firewall",
        "claim_boundary": "packet_skeleton_only_no_numeric_normalization_no_score_no_verdict",
    },
    {
        "component_id": "N_tau_remaining",
        "role": "product of Tau-side source and projection normalizations after ACT adapter convention lock",
        "symbol": "N_parent_source * N_projection",
        "required_derivation": "accepted N_parent_source row and accepted N_projection row",
        "current_value": "",
        "dimension_status": "BLOCKED_PRODUCT_COMPONENTS_NOT_ACCEPTED",
        "firewall_status": "BLOCKED_PRODUCT_COMPONENTS_NOT_ACCEPTED",
        "source_evidence": "docs/cmb_tau_lensing_adapter_convention_normalization_lock_v01.md",
        "acceptance_rule": "may be written into formula spec only after both product factors pass",
        "claim_boundary": "packet_skeleton_only_no_numeric_normalization_no_score_no_verdict",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0].keys()))
        writer.writeheader()
        writer.writerows(ROWS)


def build_summary(packet_path: Path) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_lensing_N_parent_projection_packet_summary_v01",
        "claim_boundary": "parent_projection_packet_skeleton_only_no_numeric_normalization_no_score_no_dark_sector_verdict",
        "packet": rel(packet_path),
        "packet_status": "N_PROJECTION_EXPLICIT_NON_SCORE_FAILURE_N_PARENT_SOURCE_STILL_BLOCKED",
        "rows": len(ROWS),
        "blocked_components": [
            row["component_id"]
            for row in ROWS
            if "BLOCKED" in row["dimension_status"] or "BLOCKED" in row["firewall_status"]
        ],
        "failed_components": [
            row["component_id"]
            for row in ROWS
            if "FAILURE" in row["dimension_status"] or "FAILURE" in row["firewall_status"]
        ],
        "unblocks_when": [
            "N_parent_source has a source-side derivation and dimension/gauge/firewall certificate",
            "N_projection has a projection operator derivation and replay certificate",
            "N_tau_remaining is computed from accepted factors before formula materialization",
            "formula spec is updated before any new score attempt",
        ],
        "non_admissible_action": "do not populate current_value from post-score alpha_star or endpoint residuals",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    row_lines = "\n".join(
        f"- `{row['component_id']}`: {row['dimension_status']}; {row['firewall_status']}" for row in ROWS
    )
    unblock = "\n".join(f"- {item}" for item in summary["unblocks_when"])
    text = f"""# Tau CMB Lensing N Parent Projection Packet v01

**Doc class:** normalization packet skeleton
**Reader role:** Paper 13 Tau-grid implementer
**Status:** skeleton only; no numeric normalization
**Canonical parent:** `docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

This packet is the concrete container for the remaining Tau-side normalization:

```text
N_tau_remaining = N_parent_source * N_projection
```

It intentionally contains no numeric normalization. The empty value slots may
only be populated from endpoint-blind Tau-side derivation evidence.

## Packet

```text
{summary["packet"]}
```

## Current Rows

{row_lines}

## Unblocks When

{unblock}

## Forbidden Shortcut

```text
{summary["non_admissible_action"]}
```

## Projection Split

The `N_projection` row separates two notions:

```text
Route B adapter replay: B_ACT @ grid, convention-locked for diagnostics
Physical Tau projection: Projection_PP[Phi_lens_tau](L), explicit non-score failure in current packet
```

Tracked at:

```text
docs/cmb_tau_lensing_projection_normalization_split_v01.md
data/derived/cmb_tau_lensing_projection_normalization_split_v01.json
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB lensing parent/projection normalization packet skeleton.")
    parser.add_argument("--write-packet", nargs="?", const=str(DEFAULT_PACKET))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()

    packet_path = Path(args.write_packet or DEFAULT_PACKET)
    write_csv(packet_path)
    summary = build_summary(packet_path)
    if args.write_summary:
        path = Path(args.write_summary)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(summary, Path(args.write_doc))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
