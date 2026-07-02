#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_projection_normalization_split_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_normalization_split_v01.md"
REPLAY = ROOT / "payloads/tau_lensing_pp_grid_projection_replay_v01.json"
EQUATION_PACKET = ROOT / "docs/cmb_tau_lensing_grid_equation_packet_v01.md"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def build_report() -> dict[str, Any]:
    replay = load_json(REPLAY)
    projection = replay.get("projection_replay", {}) if isinstance(replay.get("projection_replay"), dict) else {}
    route_id = replay.get("route_id")
    projected_shape = projection.get("projected_shape")
    operation = projection.get("operation")
    adapter_replay_locked = projected_shape == [18] and operation == "B_ACT @ grid"
    return {
        "report_id": "cmb_tau_lensing_projection_normalization_split_v01",
        "claim_boundary": "projection_normalization_split_only_no_physical_projection_derivation_no_score_no_dark_sector_verdict",
        "split_status": "ROUTE_B_ADAPTER_REPLAY_LOCKED_PHYSICAL_PROJECTION_EXPLICIT_NON_SCORE_FAILURE",
        "inputs": {
            "projection_replay": rel(REPLAY),
            "equation_packet": rel(EQUATION_PACKET),
        },
        "route_b_adapter_projection": {
            "meaning": "validation/replay map from an already materialized L-space Tau grid to ACT bandpower comparison space",
            "operator": "B_ACT @ grid",
            "N_projection_adapter_replay": 1.0,
            "route_id": route_id,
            "projected_shape": projected_shape,
            "locked": adapter_replay_locked,
            "claim": "adapter replay normalization only; not a physical Phi-to-PP projection",
        },
        "physical_projection_obligation": {
            "meaning": "Tau physics map from Phi_lens_tau(a,k) to tau_PP(L) or delta_PP_tau(L)",
            "operator": "Projection_PP[Phi_lens_tau](L)",
            "N_projection_physical": None,
            "status": "EXPLICIT_NON_SCORE_FAILURE_NO_PHYSICAL_PROJECTION_OPERATOR_SUPPLIED",
            "locked": [
                "domain contract: Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff], transfer-defined over a,k, no numeric field supplied",
                "codomain convention: 3000-row L-space PP-style target, tau_PP(L) or delta_PP_tau(L), L=10..3009",
                "endpoint firewall: pass for current skeleton only; rerun after operator/normalization/replay values"
            ],
            "partially_structured": [
                "operator-rule accepted forms are declared and the current packet records an explicit non-score operator failure",
                "physical source-to-grid replay requirements are declared but not materializable on the failure branch",
                "N_projection_physical policy is declared; no numeric normalization before an accepted operator rule replaces the failure"
            ],
            "missing": [
                "lensing kernel or transfer support",
                "Fourier and L-space convention",
                "linearity/nonlinearity rule",
                "dimension and sign convention",
                "endpoint-blind replay from parent source to 3000-point PP grid",
            ],
        },
        "effect_on_parent_projection_packet": {
            "N_projection_row_status": (
                "adapter replay can be marked convention-locked for Route B diagnostics; "
                "physical projection normalization is an explicit non-score failure until the operator route is resumed"
            ),
            "may_populate_numeric_N_projection_for_physical_score": False,
            "may_reference_adapter_replay_N_for_protocol_audit": True,
        },
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    adapter = report["route_b_adapter_projection"]
    physical = report["physical_projection_obligation"]
    missing = "\n".join(f"- {item}" for item in physical["missing"])
    text = f"""# CMB Tau Lensing Projection Normalization Split v01

**Doc class:** projection-normalization split
**Reader role:** Paper 13 Tau-grid implementer
**Status:** Route B adapter replay locked; physical projection explicit non-score failure
**Canonical parent:** `docs/tau_cmb_lensing_N_parent_projection_packet_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Split

There are two different projection notions in the current pipeline.

### Route B Adapter Replay

```text
operator = {adapter["operator"]}
N_projection_adapter_replay = {adapter["N_projection_adapter_replay"]}
locked = {adapter["locked"]}
```

This is only the validation/replay map from a pre-materialized L-space Tau grid
to the ACT 18-band comparison vector. It does not derive a physical Tau
`Phi -> PP` projection.

### Physical Tau Projection

```text
operator = {physical["operator"]}
N_projection_physical = BLOCKED
```

Already locked:

```text
domain contract: Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff], transfer-defined over a,k, no numeric field supplied
codomain convention: 3000-row L-space PP-style target, tau_PP(L) or delta_PP_tau(L), L=10..3009
endpoint firewall: pass for current skeleton only; rerun after operator/normalization/replay values
```

Structured failure branch:

```text
operator-rule accepted forms are declared and the current packet records an explicit non-score operator failure
physical source-to-grid replay requirements are declared but not materializable on the failure branch
N_projection_physical policy is declared; no numeric normalization before an accepted operator rule replaces the failure
```

The missing pieces are:

{missing}

## Consequence

For Route B diagnostics, the adapter replay normalization is convention-locked.
For a physical endpoint-blind score retry, the `N_projection` row in the parent
projection packet is not merely open. It is explicitly failed for the current
packet and may only resume if an endpoint-blind physical projection operator,
normalization, replay, and refreshed firewall certificate replace the failure
before scoring.

The physical projection packet and audit are tracked at:

```text
docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md
data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv
data/derived/cmb_tau_lensing_physical_projection_operator_packet_audit_v01.json
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Split adapter replay normalization from physical Tau projection normalization.")
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
