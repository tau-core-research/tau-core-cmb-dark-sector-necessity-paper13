#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_projection_operator_rule_requirement_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_operator_rule_requirement_v01.md"


def build_report() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_projection_operator_rule_requirement_v01",
        "claim_boundary": "projection_operator_rule_requirement_only_no_operator_no_score_no_dark_sector_verdict",
        "operator_rule_status": "BLOCKED_OPERATOR_RULE_NOT_SUPPLIED_FAILURE_BRANCH_READY",
        "target_operator": "Projection_PP[Phi_lens_tau](L)",
        "accepted_forms": [
            "closed operator equation with declared measure/kernel and dimensions",
            "hash-bound kernel table mapping accepted Phi_lens_tau support to L=10..3009",
            "transfer/projection integral with declared distance, window, and Fourier conventions",
            "explicit failure statement explaining why no lawful projection operator is currently supplied",
        ],
        "required_metadata": [
            "domain source: accepted Phi_lens_tau(a,k) contract or values",
            "codomain: tau_PP(L) or delta_PP_tau(L), L=10..3009",
            "line-of-sight or projection geometry convention",
            "k convention and L convention",
            "normalization and sign convention",
            "known-limit behavior for zero source",
            "endpoint firewall certificate",
        ],
        "explicit_failure_branch": {
            "status": "READY_AS_ALLOWED_NON_SCORE_BRANCH",
            "failure_statement_must_name": [
                "missing operator equation/kernel/integral",
                "missing physical normalization",
                "missing source-to-grid replay",
                "next theoretical blocker",
            ],
            "effect": "keeps physical N_projection blocked but converts the row from vague missingness to explicit fail discipline",
        },
        "source_evidence": [
            "docs/cmb_tau_lensing_grid_equation_packet_v01.md",
            "docs/cmb_tau_lensing_projection_normalization_split_v01.md",
            "docs/tau_cmb_lensing_transfer_benchmark_v01.md",
            "docs/tau_cmb_growth_transfer_kernel_closure_v01.md",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    forms = "\n".join(f"- {item}" for item in report["accepted_forms"])
    metadata = "\n".join(f"- {item}" for item in report["required_metadata"])
    failure = "\n".join(f"- {item}" for item in report["explicit_failure_branch"]["failure_statement_must_name"])
    sources = "\n".join(f"- `{item}`" for item in report["source_evidence"])
    text = f"""# CMB Tau Lensing Projection Operator Rule Requirement v01

**Doc class:** projection-operator rule requirement
**Reader role:** Paper 13 Tau-grid implementer
**Status:** operator rule blocked; explicit failure branch ready
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Target

```text
{report["target_operator"]}
```

## Accepted Forms

{forms}

## Required Metadata

{metadata}

## Explicit Failure Branch

If no lawful projection operator is supplied, the row may be closed only as an
explicit non-score failure. The failure statement must name:

{failure}

This does not accept `N_projection_physical`; it only prevents the blocker from
remaining vague.

## Source Evidence

{sources}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the physical projection operator-rule requirement packet.")
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
