#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_tau_side_normalization_obligation_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md"

INPUTS = {
    "normalization_gap": ROOT / "docs/cmb_tau_lensing_route_b_normalization_gap_derivation_v01.md",
    "normalization_gate": ROOT / "docs/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.md",
    "adapter_lock": ROOT / "docs/cmb_tau_lensing_adapter_convention_normalization_lock_v01.md",
    "phi_contract": ROOT / "docs/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.md",
    "potential_handoff": ROOT / "docs/tau_cmb_effective_potential_source_handoff_v01.md",
    "minimal_source_candidate": ROOT / "docs/tau_cmb_minimal_source_term_candidate_v01.md",
}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def path_rows() -> list[dict[str, Any]]:
    rows = []
    for key, path in INPUTS.items():
        rows.append({"component": key, "path": rel(path), "exists": path.exists()})
    return rows


def build_report() -> dict[str, Any]:
    rows = path_rows()
    all_inputs_exist = all(row["exists"] for row in rows)
    obligation_rows = [
        {
            "factor": "N_parent_source",
            "meaning": "amplitude/units carried by the endpoint-blind Tau CMB source before lensing projection",
            "current_status": "BLOCKED_PHI_TAU_EFF_NOT_DERIVED",
            "depends_on": [
                "endpoint-blind Phi_tau_eff(a,k) derivation",
                "dimensionless or dimensionful A_tau(a,k) normalization",
                "source sign and gauge convention",
                "known-limit rule: parent response -> 0 implies delta_PP_tau -> 0",
            ],
            "not_allowed": "cannot be set from ACT/Planck bandpower residuals or post-score alpha",
        },
        {
            "factor": "N_projection",
            "meaning": "normalization of the map from Tau effective potential/readout source to L-space PP or delta_PP_tau grid",
            "current_status": "EXPLICIT_NON_SCORE_FAILURE_PHYSICAL_PROJECTION_OPERATOR_NOT_SUPPLIED",
            "depends_on": [
                "resume from failure by supplying endpoint-blind Projection_PP operator",
                "operator-implied N_projection_physical normalization",
                "source-to-3000-grid physical replay certificate",
                "post-population endpoint firewall certificate",
            ],
            "not_allowed": "cannot be inferred from the observed ACT amplitude after scoring",
        },
    ]
    return {
        "report_id": "cmb_tau_lensing_tau_side_normalization_obligation_v01",
        "claim_boundary": "tau_side_normalization_obligation_only_no_numeric_tau_normalization_no_score_no_dark_sector_verdict",
        "obligation_status": "BLOCKED_PENDING_TAU_SIDE_SOURCE_AND_PROJECTION_DERIVATION",
        "input_chain": rows,
        "input_chain_complete": all_inputs_exist,
        "remaining_formula_after_adapter_lock": "N_tau_remaining = N_parent_source * N_projection",
        "obligation_rows": obligation_rows,
        "minimum_pre_score_payload_to_unblock": {
            "object_id": "tau_cmb_lensing_N_parent_projection_packet_v01",
            "required_files_or_fields": [
                "parent_source_normalization row/table for N_parent_source",
                "projection_operator_normalization row/table for N_projection",
                "dimension and unit audit",
                "gauge/sign convention audit",
                "endpoint firewall certificate",
                "materialization replay from source packet to tau_lensing_response_delta_pp_v01.csv",
                "formula-spec update that freezes N_tau before scoring",
            ],
        },
        "decision": (
            "The current evidence is sufficient to define the missing Tau-side objects. "
            "N_projection is explicitly failed for the current physical projection packet; "
            "N_parent_source remains blocked by missing endpoint-blind Phi_tau_eff derivation."
        ),
        "admissible_next_action": (
            "build a concrete N_parent_projection packet or revise the Route B shape kernel before another physical score"
        ),
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    input_lines = "\n".join(
        f"- `{row['component']}`: `{row['path']}` ({'exists' if row['exists'] else 'missing'})"
        for row in report["input_chain"]
    )
    obligation_lines = []
    for row in report["obligation_rows"]:
        deps = "\n".join(f"  - {item}" for item in row["depends_on"])
        obligation_lines.append(
            f"### {row['factor']}\n\n"
            f"{row['meaning']}\n\n"
            f"```text\n{row['current_status']}\n```\n\n"
            f"Depends on:\n\n{deps}\n\n"
            f"Forbidden shortcut:\n\n```text\n{row['not_allowed']}\n```\n"
        )
    required = "\n".join(
        f"- {item}" for item in report["minimum_pre_score_payload_to_unblock"]["required_files_or_fields"]
    )
    text = f"""# CMB Tau Lensing Tau-Side Normalization Obligation v01

**Doc class:** Tau-side normalization proof obligation
**Reader role:** Paper 13 Tau-grid implementer
**Status:** remaining normalization decomposition, no numeric Tau amplitude
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Remaining Formula

After the ACT adapter convention lock, the unresolved Tau-side factor is:

```text
{report["remaining_formula_after_adapter_lock"]}
```

This artifact does not assign a value to either factor. It defines what must be
proved before a new endpoint-blind physical score retry is allowed.

## Input Chain

{input_lines}

## Obligations

{chr(10).join(obligation_lines)}

## Minimum Packet To Unblock A Physical Retry

```text
{report["minimum_pre_score_payload_to_unblock"]["object_id"]}
```

It must contain:

{required}

The packet skeleton is tracked at:

```text
docs/tau_cmb_lensing_N_parent_projection_packet_v01.md
data/derived/tau_cmb_lensing_N_parent_projection_packet_v01.csv
data/derived/tau_cmb_lensing_N_parent_projection_packet_summary_v01.json
```

## Decision

```text
{report["decision"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau-side normalization obligation packet.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    if args.write_doc:
        write_doc(report, Path(args.write_doc))
    print(text)


if __name__ == "__main__":
    main()
