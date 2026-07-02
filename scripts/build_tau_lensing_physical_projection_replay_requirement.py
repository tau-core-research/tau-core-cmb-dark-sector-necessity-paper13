#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_physical_projection_replay_requirement_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_physical_projection_replay_requirement_v01.md"


def build_report() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_physical_projection_replay_requirement_v01",
        "claim_boundary": "physical_projection_replay_requirement_only_no_replay_no_score_no_dark_sector_verdict",
        "replay_status": "OUTPUT_REPLAY_SPEC_DECLARED_NOT_FILLED_OPERATOR_AND_NORMALIZATION_NOT_SUPPLIED",
        "replay_target": "source-to-3000-grid replay certificate",
        "distinction": {
            "adapter_replay": "B_ACT @ already materialized grid -> 18-vector; implemented by materialize-replay",
            "physical_projection_replay": (
                "Phi_lens_tau plus Projection_PP operator plus N_projection_physical "
                "-> 3000-row tau_PP or delta_PP grid"
            ),
        },
        "required_inputs": [
            "accepted projection_domain row",
            "accepted projection_codomain row",
            "accepted projection_operator_rule row",
            "accepted projection_normalization row",
            "endpoint firewall certificate for populated values",
        ],
        "required_replay_contents": [
            "input source artifact paths and hashes",
            "operator rule artifact path and hash",
            "normalization artifact path/value/range and hash",
            "output grid path and sha256",
            "L alignment L=10..3009",
            "zero-source known-limit check",
            "claim boundary no score/no verdict",
        ],
        "spec_scaffold_links": [
            "docs/cmb_tau_lensing_projection_output_replay_spec_scaffold_v01.md",
            "data/derived/cmb_tau_lensing_projection_output_replay_spec_scaffold_v01.csv",
        ],
        "current_decision": "PHYSICAL_REPLAY_NOT_MATERIALIZABLE_YET",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    inputs = "\n".join(f"- {item}" for item in report["required_inputs"])
    contents = "\n".join(f"- {item}" for item in report["required_replay_contents"])
    links = "\n".join(f"- `{item}`" for item in report["spec_scaffold_links"])
    text = f"""# CMB Tau Lensing Physical Projection Replay Requirement v01

**Doc class:** physical projection replay requirement
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocked; operator and normalization not supplied
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Distinction

```text
adapter replay:
{report["distinction"]["adapter_replay"]}

physical projection replay:
{report["distinction"]["physical_projection_replay"]}
```

The current `materialize-replay` target covers adapter replay only. A physical
projection replay requires the physics-side operator and normalization first.

## Required Inputs

{inputs}

## Required Replay Contents

{contents}

## Spec Scaffold Links

{links}

## Current Decision

```text
{report["current_decision"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build physical Tau lensing projection replay requirement.")
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
