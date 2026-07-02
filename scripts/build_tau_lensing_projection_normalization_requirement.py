#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_projection_normalization_requirement_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_normalization_requirement_v01.md"


def build_report() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_projection_normalization_requirement_v01",
        "claim_boundary": "projection_normalization_requirement_only_no_numeric_normalization_no_score_no_dark_sector_verdict",
        "normalization_status": "NORMALIZATION_SPEC_DECLARED_NOT_FILLED_NO_NUMERIC_VALUE",
        "target": "N_projection_physical",
        "definition_policy": (
            "N_projection_physical is not a free post-score scale. It is the normalization "
            "implied by an accepted Projection_PP operator equation/kernel/integral, including "
            "its measure, distance/window convention, sign, units, and zero-source limit."
        ),
        "required_before_acceptance": [
            "accepted projection_operator_rule row",
            "declared measure/kernel/integral normalization",
            "declared sign convention",
            "declared units or dimensionless convention",
            "zero-source known-limit check",
            "endpoint firewall certificate after value is populated",
        ],
        "forbidden_sources": [
            "post-score alpha_star",
            "ACT residual minimization",
            "Planck residual minimization",
            "reduced chi2 tuning",
            "dark-sector verdict preference",
        ],
        "allowed_value_forms": [
            "exact value derived by operator convention",
            "finite prior/range declared before scoring for diagnostic parameterized retry",
            "explicit failure if no lawful normalization can be supplied",
        ],
        "evidence_links": [
            "docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md",
            "docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md",
            "data/derived/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.csv",
            "docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md",
            "data/derived/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.csv",
        ],
        "current_decision": "DO_NOT_POPULATE_N_PROJECTION_PHYSICAL_YET",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    required = "\n".join(f"- {item}" for item in report["required_before_acceptance"])
    forbidden = "\n".join(f"- {item}" for item in report["forbidden_sources"])
    allowed = "\n".join(f"- {item}" for item in report["allowed_value_forms"])
    evidence = "\n".join(f"- `{item}`" for item in report["evidence_links"])
    text = f"""# CMB Tau Lensing Projection Normalization Requirement v01

**Doc class:** projection-normalization requirement
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocked; depends on physical projection operator
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Target

```text
{report["target"]}
```

## Policy

{report["definition_policy"]}

## Required Before Acceptance

{required}

## Forbidden Sources

{forbidden}

## Allowed Value Forms

{allowed}

## Evidence Links

{evidence}

## Current Decision

```text
{report["current_decision"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build physical projection normalization requirement.")
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
