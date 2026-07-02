#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_adapter_convention_normalization_lock_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_adapter_convention_normalization_lock_v01.md"
DEFAULT_BINNING = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/binning_matrix_act.txt"
DEFAULT_FIDUCIAL = (
    ROOT
    / "data/external/act_dr6_lensing/extracted/v1.2/like_corrs/cosmo2017_10K_acc3_lenspotentialCls.dat"
)
DEFAULT_README = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/README"
EXPECTED_L = np.arange(10, 3010, dtype=float)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def stats(values: np.ndarray) -> dict[str, float]:
    return {
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "median": float(np.median(values)),
        "mean": float(np.mean(values)),
    }


def load_fiducial_pp(path: Path) -> np.ndarray:
    table = np.loadtxt(path)
    by_l = {int(row[0]): float(row[5]) for row in table}
    return np.array([by_l[int(L)] for L in EXPECTED_L], dtype=float)


def build_report() -> dict[str, Any]:
    binning = np.loadtxt(DEFAULT_BINNING)
    fid_pp = load_fiducial_pp(DEFAULT_FIDUCIAL)
    fid_projected = binning @ fid_pp
    readme = DEFAULT_README.read_text(errors="ignore") if DEFAULT_README.exists() else ""
    return {
        "report_id": "cmb_tau_lensing_adapter_convention_normalization_lock_v01",
        "claim_boundary": "adapter_convention_lock_only_no_tau_normalization_no_score_no_dark_sector_verdict",
        "lock_status": "SOURCE_SIDE_ADAPTER_CONVENTION_LOCK_CANDIDATE",
        "inputs": {
            "act_readme": rel(DEFAULT_README),
            "act_binning_matrix": rel(DEFAULT_BINNING),
            "fiducial_lenspotential_pp": rel(DEFAULT_FIDUCIAL),
        },
        "source_side_observations": [
            "ACT package README identifies the directory as DR6 Lensing Likelihood Data v1.2.",
            "The fiducial lenspotential file header includes a PP column.",
            "The reduced local adapter contract uses m_ACT = B_ACT @ theory_lenspotential_PP_grid.",
            "This lock concerns package units only; it is not a Tau-side amplitude derivation.",
        ],
        "readme_version_line_present": "Version: v1.2" in readme,
        "binning_shape": list(binning.shape),
        "fiducial_pp_stats_L10_to_L3009": stats(fid_pp),
        "projected_fiducial_pp_stats": stats(fid_projected),
        "adapter_convention_candidate": {
            "N_PP_or_clkk_convention": 1.0,
            "meaning": (
                "Within the reduced local adapter, the accepted theory object is the package "
                "lenspotential PP grid and the package binning matrix maps it directly to the "
                "18-vector comparison space. No additional Tau-side factor is introduced here."
            ),
            "formula": "m_ACT = B_ACT @ PP_grid",
        },
        "remaining_tau_normalization_after_this_lock": "N_tau_remaining = N_parent_source * N_projection",
        "non_claims": [
            "does not prove that CAMB/ACT PP is identical to a fundamental Tau readout variable",
            "does not derive N_parent_source",
            "does not derive N_projection",
            "does not run a score",
            "does not support a dark-sector verdict",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    text = f"""# CMB Tau Lensing Adapter Convention Normalization Lock v01

**Doc class:** source-side adapter convention lock
**Reader role:** Paper 13 Tau-grid implementer
**Status:** package-unit convention candidate, not Tau-side normalization
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Lock

For the reduced local ACT lensing adapter, the source-side convention is:

```text
m_ACT = B_ACT @ PP_grid
N_PP_or_clkk_convention = 1
```

This means that no extra Tau-side amplitude is hidden in the adapter. The
adapter accepts a package-style `PP_grid` and uses the package binning matrix to
produce the 18-vector comparison object.

## Source-Side Scale Check

Using the ACT package fiduciary `PP` column over L=10..3009:

```text
PP min..max = {report["fiducial_pp_stats_L10_to_L3009"]["min"]:.6e} .. {report["fiducial_pp_stats_L10_to_L3009"]["max"]:.6e}
B_ACT @ PP min..max = {report["projected_fiducial_pp_stats"]["min"]:.6e} .. {report["projected_fiducial_pp_stats"]["max"]:.6e}
```

This is a package-unit sanity check. It is not a Tau amplitude derivation and
does not use a Tau model score.

## Consequence

After this convention lock, the remaining Tau-side normalization obligation is:

```text
N_tau_remaining = N_parent_source * N_projection
```

The next physical retry must derive those two factors before materialization.

The Tau-side obligation is decomposed at:

```text
docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md
data/derived/cmb_tau_lensing_tau_side_normalization_obligation_v01.json
```

## Non-Claims

```text
does not prove that CAMB/ACT PP is identical to a fundamental Tau readout variable
does not derive N_parent_source
does not derive N_projection
does not run a score
does not support a dark-sector verdict
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the ACT adapter convention normalization lock.")
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
