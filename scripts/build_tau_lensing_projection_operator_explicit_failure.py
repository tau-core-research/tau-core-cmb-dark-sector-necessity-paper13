#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_projection_operator_explicit_failure_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_operator_explicit_failure_v01.md"


def build_report() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_projection_operator_explicit_failure_v01",
        "claim_boundary": "projection_operator_explicit_failure_no_operator_no_score_no_dark_sector_verdict",
        "failure_status": "EXPLICIT_NON_SCORE_FAILURE_DECLARED_FOR_CURRENT_PACKET",
        "failed_target": "Projection_PP[Phi_lens_tau](L)",
        "failure_statement": (
            "No lawful endpoint-blind physical projection operator is supplied in the current packet. "
            "Therefore the physical Phi_lens_tau -> PP/delta_PP route must not be scored."
        ),
        "missing_items_named": [
            "operator equation/kernel/integral",
            "physical projection normalization N_projection_physical",
            "source-to-3000-grid physical replay",
            "post-population endpoint firewall certificate",
        ],
        "next_theoretical_blocker": (
            "fill the projection-operator formula-spec scaffold with an endpoint-blind kernel, measure, "
            "normalization, zero-source limit, dimension/sign audit, and replay; or keep the physical "
            "projection route failed and use only clearly labeled Route B diagnostics"
        ),
        "allowed_after_failure": [
            "do not run physical score retry for this route",
            "keep adapter replay diagnostics separate from physical projection claims",
            "resume only by replacing this failure with a supplied endpoint-blind operator packet",
        ],
        "not_a_claim_about": [
            "Tau Core global validity",
            "CMB data fit quality",
            "dark-sector necessity",
            "no-dark success or failure",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    missing = "\n".join(f"- {item}" for item in report["missing_items_named"])
    allowed = "\n".join(f"- {item}" for item in report["allowed_after_failure"])
    nonclaims = "\n".join(f"- {item}" for item in report["not_a_claim_about"])
    text = f"""# CMB Tau Lensing Projection Operator Explicit Failure v01

**Doc class:** explicit non-score failure statement
**Reader role:** Paper 13 Tau-grid implementer
**Status:** current physical projection route failed, no score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_decision_gate_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Failure Target

```text
{report["failed_target"]}
```

## Failure Statement

{report["failure_statement"]}

## Missing Items

{missing}

## Next Theoretical Blocker

{report["next_theoretical_blocker"]}

## Allowed After Failure

{allowed}

## Non-Claims

{nonclaims}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build explicit non-score failure for missing physical Projection_PP operator.")
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
