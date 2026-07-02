#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_physical_projection_domain_lock_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_physical_projection_domain_lock_v01.md"


def build_report() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_physical_projection_domain_lock_v01",
        "claim_boundary": "projection_domain_lock_only_no_numeric_phi_lens_no_operator_no_score_no_dark_sector_verdict",
        "domain_lock_status": "DOMAIN_CONTRACT_LOCKED_FOR_TRANSFER_DEFINITION_ONLY",
        "projection_input_object": "Phi_lens_tau(a,k)",
        "construction_contract": "Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]",
        "accepted_domain_contract": {
            "variables": ["a", "k"],
            "a_role": "scale-factor/time support over the lensing-relevant transfer interval",
            "k_role": "Fourier scale variable under a declared k convention",
            "codomain_role": "potential-like scalar readout compatible with PP projection after transfer",
            "status": "contract only; no numeric field supplied",
        },
        "source_evidence": [
            "docs/cmb_tau_lensing_phi_source_acceptance_audit_v02.md",
            "docs/cmb_tau_lensing_transfer_payload_v01.md",
            "docs/cmb_tau_lensing_response_derivation_route_v01.md",
            "docs/cmb_tau_lensing_grid_equation_packet_v01.md",
        ],
        "locked_for_projection_packet": {
            "component_id": "projection_domain",
            "accepted_value": (
                "Phi_lens_tau(a,k) over declared a,k transfer-domain contract; "
                "input object is transfer-defined, not numerically supplied"
            ),
            "current_status": "DOMAIN_CONTRACT_LOCKED_TRANSFER_DEFINITION_ONLY",
        },
        "still_missing": [
            "numeric or replayable T_tau_CMB operator",
            "accepted Phi_lens_tau values/kernel",
            "gauge/sign normalization pass",
            "physical projection operator rule",
            "projection normalization",
            "source-to-grid replay",
            "projection endpoint firewall certificate",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    missing = "\n".join(f"- {item}" for item in report["still_missing"])
    sources = "\n".join(f"- `{item}`" for item in report["source_evidence"])
    text = f"""# CMB Tau Lensing Physical Projection Domain Lock v01

**Doc class:** projection-domain contract lock
**Reader role:** Paper 13 Tau-grid implementer
**Status:** domain contract locked for transfer definition only
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Domain Contract

The physical projection input object is:

```text
{report["projection_input_object"]}
{report["construction_contract"]}
```

Accepted domain variables:

```text
a: scale-factor/time support over the lensing-relevant transfer interval
k: Fourier scale variable under a declared k convention
```

This locks the domain contract only. It does not supply a numeric
`Phi_lens_tau(a,k)` field and does not derive the projection operator.

## Source Evidence

{sources}

## Still Missing

{missing}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build physical Tau lensing projection domain lock.")
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
