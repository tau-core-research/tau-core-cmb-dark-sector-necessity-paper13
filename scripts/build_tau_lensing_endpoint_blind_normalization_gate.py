#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.md"
GAP_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_normalization_gap_derivation_v01.json"
SPEC = ROOT / "payload_staging/tau_lensing_route_b_parent_source_formula_spec_v01.json"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def build_report() -> dict[str, Any]:
    gap = load_json(GAP_REPORT)
    spec = load_json(SPEC)
    spec_norm = spec.get("normalization")
    spec_norm_statement = str(spec.get("normalization_statement", ""))
    has_only_dimensionless_convention = spec_norm == 1.0 and "dimensionless" in spec_norm_statement.lower()
    score_informed_alpha = (
        gap.get("tau_unit_shape_diagnostic", {}).get("best_scale_alpha_star")
        if isinstance(gap.get("tau_unit_shape_diagnostic"), dict)
        else None
    )
    checks = [
        {
            "name": "diagnostic_gap_report_exists",
            "passes": GAP_REPORT.exists(),
            "detail": rel(GAP_REPORT),
        },
        {
            "name": "formula_spec_exists",
            "passes": SPEC.exists(),
            "detail": rel(SPEC),
        },
        {
            "name": "current_formula_spec_has_only_conventional_unit_normalization",
            "passes": bool(has_only_dimensionless_convention),
            "detail": {
                "normalization": spec_norm,
                "normalization_statement": spec_norm_statement,
            },
        },
        {
            "name": "score_informed_alpha_not_promotable",
            "passes": score_informed_alpha is not None,
            "detail": {
                "diagnostic_alpha_star": score_informed_alpha,
                "promotion_rule": "may be used as target magnitude to explain, not as endpoint-blind input",
            },
        },
    ]
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_normalization_gate_v01",
        "claim_boundary": "normalization_gate_only_no_payload_promotion_no_score_no_dark_sector_verdict",
        "gate_status": "BLOCKED_FOR_PHYSICAL_SCORE_RETRY",
        "checks": checks,
        "current_blocker": (
            "The active Route B formula spec uses a unit dimensionless normalization. "
            "The post-score alpha gap is derived algebraically, but it is not an "
            "endpoint-blind Tau-side normalization."
        ),
        "required_endpoint_blind_normalization_object": {
            "object_id": "N_tau_CMB_lensing_v01",
            "formula": "N_tau = N_parent_source * N_projection * N_PP_or_clkk_convention",
            "required_fields": [
                "source-side derivation of N_parent_source",
                "projection operator normalization N_projection",
                "PP/clkk and binning convention normalization N_PP_or_clkk_convention",
                "dimension statement",
                "known-limit statement N_tau -> 0 or delta_PP_tau -> 0 when parent response -> 0",
                "endpoint-firewall statement excluding ACT/Planck residuals and score outputs",
                "frozen value/range before materialization",
            ],
        },
        "admissible_next_routes": [
            {
                "route": "strict_physical_retry",
                "action": "derive N_tau from Tau-side and adapter-convention sources, update formula spec, rematerialize payload, rerun score",
                "claim_level_if_successful": "endpoint_blind_physical_candidate_score",
            },
            {
                "route": "diagnostic_parameterized_retry",
                "action": "declare a prior/range for normalization before scoring and treat score as parameterized diagnostic",
                "claim_level_if_successful": "diagnostic_fit_not_dark_sector_verdict",
            },
            {
                "route": "shape_kernel_revision",
                "action": "replace the current power-law cutoff unit shape from Tau-side theory before any new endpoint comparison",
                "claim_level_if_successful": "new_endpoint_blind_shape_candidate_pending_score",
            },
        ],
        "non_admissible_action": (
            "Do not set normalization to the post-score alpha_star and call it a Tau "
            "derivation. That would be endpoint leakage."
        ),
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    req = report["required_endpoint_blind_normalization_object"]
    alpha = next(
        (
            row["detail"]["diagnostic_alpha_star"]
            for row in report["checks"]
            if row["name"] == "score_informed_alpha_not_promotable"
            and isinstance(row.get("detail"), dict)
            and row["detail"].get("diagnostic_alpha_star") is not None
        ),
        None,
    )
    fields = "\n".join(f"- {item}" for item in req["required_fields"])
    routes = "\n".join(f"- `{row['route']}`: {row['action']}" for row in report["admissible_next_routes"])
    text = f"""# CMB Tau Lensing Endpoint-Blind Normalization Gate v01

**Doc class:** scoring precondition gate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocks physical score retry until normalization is predeclared
**Canonical parent:** `docs/cmb_tau_lensing_route_b_normalization_gap_derivation_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Gate Status

```text
{report["gate_status"]}
```

The current Route B formula spec uses unit dimensionless normalization. The
diagnostic algebra gives:

```text
alpha_* = {alpha}
```

but `alpha_*` is not endpoint-blind because it was computed from the ACT
bandpowers. It may define the amplitude gap to explain; it may not be inserted
as the physical Tau normalization.

## Required Object

```text
{req["object_id"]}
{req["formula"]}
```

It must contain:

{fields}

## Allowed Next Routes

{routes}

## Forbidden Shortcut

```text
{report["non_admissible_action"]}
```

## Downstream Tau-Side Obligation

The remaining Tau-side proof obligation is tracked at:

```text
docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md
data/derived/cmb_tau_lensing_tau_side_normalization_obligation_v01.json
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the endpoint-blind normalization gate for Tau CMB lensing.")
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
