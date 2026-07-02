#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md"


ROWS = [
    {
        "component_id": "projection_domain",
        "required_object": "Phi_lens_tau(a,k)",
        "required_content": "domain variables, support range, gauge/sign convention, dimensional convention",
        "current_status": "DOMAIN_CONTRACT_LOCKED_TRANSFER_DEFINITION_ONLY",
        "accepted_value": "Phi_lens_tau(a,k) over declared a,k transfer-domain contract; no numeric field supplied",
        "source_evidence": "docs/cmb_tau_lensing_physical_projection_domain_lock_v01.md; docs/cmb_tau_lensing_phi_source_acceptance_audit_v02.md; docs/cmb_tau_lensing_response_derivation_route_v01.md",
    },
    {
        "component_id": "projection_codomain",
        "required_object": "tau_PP(L) or delta_PP_tau(L), L=10..3009",
        "required_content": "codomain units/convention and explicit L-grid alignment",
        "current_status": "CODOMAIN_CONVENTION_LOCKED_NO_PHYSICAL_NORMALIZATION",
        "accepted_value": "3000-row L-space PP-style codomain: tau_PP(L) or delta_PP_tau(L), L=10..3009",
        "source_evidence": "docs/cmb_lensing_theory_convention_lock_v01.md; docs/cmb_tau_lensing_pp_grid_projection_payload_v01.md; docs/cmb_tau_lensing_projection_normalization_split_v01.md",
    },
    {
        "component_id": "projection_operator_rule",
        "required_object": "Projection_PP[Phi_lens_tau](L)",
        "required_content": "operator equation, kernel table, transfer integral, or explicit failure statement",
        "current_status": "EXPLICIT_FAILURE_DECLARED_NO_PHYSICAL_OPERATOR_NO_SCORE",
        "accepted_value": "no lawful endpoint-blind physical Projection_PP operator is supplied in the current packet",
        "source_evidence": "docs/cmb_tau_lensing_projection_operator_explicit_failure_v01.md; docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md; docs/cmb_tau_lensing_projection_operator_rule_requirement_v01.md; docs/cmb_tau_lensing_grid_equation_packet_v01.md",
    },
    {
        "component_id": "projection_normalization",
        "required_object": "N_projection_physical",
        "required_content": "normalization value/range derived before endpoint comparison",
        "current_status": "BLOCKED_NORMALIZATION_DEPENDS_ON_OPERATOR_RULE_REQUIREMENT_DECLARED",
        "accepted_value": "",
        "source_evidence": "docs/cmb_tau_lensing_projection_normalization_requirement_v01.md; docs/cmb_tau_lensing_projection_normalization_split_v01.md",
    },
    {
        "component_id": "projection_replay",
        "required_object": "source-to-3000-grid replay certificate",
        "required_content": "hash-bound replay from physical projection inputs to 3000-row PP/delta_PP grid",
        "current_status": "BLOCKED_PHYSICAL_REPLAY_NOT_MATERIALIZABLE_REQUIREMENT_DECLARED",
        "accepted_value": "",
        "source_evidence": "docs/cmb_tau_lensing_physical_projection_replay_requirement_v01.md; docs/cmb_tau_lensing_projection_replay_materializer_contract_v01.md",
    },
    {
        "component_id": "endpoint_firewall",
        "required_object": "projection endpoint firewall certificate",
        "required_content": "proof that ACT/Planck residuals, reduced chi2, and score outputs were not used",
        "current_status": "FIREWALL_PASS_FOR_CURRENT_SKELETON_ONLY_RERUN_AFTER_VALUES",
        "accepted_value": "current physical projection packet contains no endpoint-derived operator, normalization, replay, or score value",
        "source_evidence": "docs/cmb_tau_lensing_physical_projection_firewall_certificate_v01.md; docs/cmb_tau_lensing_route_evidence_firewall_contract_v01.md",
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
        "report_id": "cmb_tau_lensing_physical_projection_operator_packet_summary_v01",
        "claim_boundary": "physical_projection_operator_packet_skeleton_only_no_operator_no_score_no_dark_sector_verdict",
        "packet": rel(packet_path),
        "packet_status": "PHYSICAL_PROJECTION_ROUTE_EXPLICIT_FAILURE_NO_SCORE",
        "operator_target": "Projection_PP[Phi_lens_tau](L)",
        "normalization_target": "N_projection_physical",
        "rows": len(ROWS),
        "locked_components": [
            row["component_id"]
            for row in ROWS
            if (
                "LOCKED" in row["current_status"]
                or "ACCEPTED" in row["current_status"]
                or "PASS" in row["current_status"]
            )
            and str(row["accepted_value"]).strip()
        ],
        "blocked_components": [row["component_id"] for row in ROWS if "BLOCKED" in row["current_status"]],
        "failed_components": [row["component_id"] for row in ROWS if "FAILURE" in row["current_status"]],
        "unblocks_N_projection_when": [
            "domain and codomain conventions are accepted",
            "an endpoint-blind operator rule is supplied; explicit failure documents non-score closure but does not unblock",
            "N_projection_physical is derived before endpoint comparison",
            "source-to-grid replay certificate exists",
            "endpoint firewall certificate passes",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(f"- `{row['component_id']}`: {row['current_status']}" for row in ROWS)
    unblock = "\n".join(f"- {item}" for item in summary["unblocks_N_projection_when"])
    text = f"""# CMB Tau Lensing Physical Projection Operator Packet v01

**Doc class:** physical projection operator packet skeleton
**Reader role:** Paper 13 Tau-grid implementer
**Status:** codomain convention locked; no physical projection operator
**Canonical parent:** `docs/cmb_tau_lensing_projection_normalization_split_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

This is the concrete packet for the blocked physical projection:

```text
{summary["operator_target"]}
{summary["normalization_target"]}
```

It is not the Route B adapter replay. It is the missing physics-side map from
Tau lensing-era potential/readout source into a 3000-row `PP` or `delta_PP_tau`
grid.

## Packet

```text
{summary["packet"]}
```

## Current Rows

{rows}

The domain and codomain rows are locked only as contracts. The firewall row
passes only for the current skeleton and must be rerun after values are added.
The operator-rule row is closed only as an explicit non-score failure for the
current packet. The replay row distinguishes physical source-to-grid replay from
adapter replay. The normalization row remains blocked because no operator rule
supplies its measure/sign/unit convention. The domain lock does not supply a
numeric `Phi_lens_tau(a,k)` field. The codomain lock does not supply
`N_projection_physical` and does not derive `Projection_PP[Phi_lens_tau](L)`.

## Unblocks `N_projection` When

{unblock}

## Decision Gate

The current operator-core decision is tracked at:

```text
docs/cmb_tau_lensing_projection_operator_decision_gate_v01.md
data/derived/cmb_tau_lensing_projection_operator_decision_gate_v01.json
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build physical Tau lensing projection operator packet skeleton.")
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
