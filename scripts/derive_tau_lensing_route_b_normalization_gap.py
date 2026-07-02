#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GRID = ROOT / "payloads/tau_lensing_response_delta_pp_v01.csv"
DEFAULT_BANDPOWERS = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/clkk_bandpowers_act.txt"
DEFAULT_COV = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/covmat_act.txt"
DEFAULT_BINNING = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/binning_matrix_act.txt"
DEFAULT_FIDUCIAL = (
    ROOT
    / "data/external/act_dr6_lensing/extracted/v1.2/like_corrs/cosmo2017_10K_acc3_lenspotentialCls.dat"
)
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_normalization_gap_derivation_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_route_b_normalization_gap_derivation_v01.md"
EXPECTED_L = np.arange(10, 3010, dtype=float)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_grid(path: Path) -> np.ndarray:
    values = np.loadtxt(path, delimiter=",")
    values = np.asarray(values, dtype=float)
    if values.ndim == 2 and values.shape[1] == 2:
        if values.shape[0] != 3000:
            raise ValueError(f"expected 3000 L,value rows, got {values.shape[0]}")
        if not np.allclose(values[:, 0], EXPECTED_L, rtol=0.0, atol=0.0):
            raise ValueError("two-column grid must use L values exactly 10..3009")
        values = values[:, 1]
    if values.shape != (3000,):
        raise ValueError(f"grid must have shape (3000,), got {values.shape}")
    if not np.all(np.isfinite(values)):
        raise ValueError("grid contains non-finite values")
    return values


def load_fiducial_pp(path: Path) -> np.ndarray:
    table = np.loadtxt(path)
    if table.ndim != 2 or table.shape[1] < 6:
        raise ValueError("fiducial lenspotential table must contain columns L TT EE BB TE PP ...")
    by_l = {int(row[0]): float(row[5]) for row in table}
    try:
        pp = np.array([by_l[int(L)] for L in EXPECTED_L], dtype=float)
    except KeyError as exc:
        raise ValueError(f"fiducial table missing L={exc.args[0]}") from exc
    if pp.shape != (3000,) or not np.all(np.isfinite(pp)):
        raise ValueError("fiducial PP extraction failed")
    return pp


def chi2(y: np.ndarray, model: np.ndarray, cov: np.ndarray) -> float:
    residual = y - model
    return float(residual.T @ np.linalg.solve(cov, residual))


def best_cov_scale(y: np.ndarray, model: np.ndarray, cov: np.ndarray) -> tuple[float, float, float]:
    cov_inv_model = np.linalg.solve(cov, model)
    numerator = float(model.T @ np.linalg.solve(cov, y))
    denominator = float(model.T @ cov_inv_model)
    if denominator == 0.0:
        raise ValueError("scale denominator is zero")
    alpha = numerator / denominator
    return alpha, numerator, denominator


def stats(values: np.ndarray) -> dict[str, float]:
    return {
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "median": float(np.median(values)),
        "mean": float(np.mean(values)),
    }


def build_report(
    grid_path: Path,
    bandpowers_path: Path,
    cov_path: Path,
    binning_path: Path,
    fiducial_path: Path,
) -> dict[str, Any]:
    grid = load_grid(grid_path)
    bandpowers = np.loadtxt(bandpowers_path)
    cov = np.loadtxt(cov_path)
    binning = np.loadtxt(binning_path)
    fid_pp = load_fiducial_pp(fiducial_path)
    if bandpowers.shape != (18,):
        raise ValueError(f"bandpowers must have shape (18,), got {bandpowers.shape}")
    if cov.shape != (18, 18):
        raise ValueError(f"covariance must have shape (18,18), got {cov.shape}")
    if binning.shape != (18, 3000):
        raise ValueError(f"binning matrix must have shape (18,3000), got {binning.shape}")

    tau_projected = binning @ grid
    fid_projected = binning @ fid_pp
    alpha_tau, numerator, denominator = best_cov_scale(bandpowers, tau_projected, cov)
    alpha_fid, fid_num, fid_den = best_cov_scale(bandpowers, fid_projected, cov)
    scaled_tau = alpha_tau * tau_projected
    scaled_fid = alpha_fid * fid_projected

    fid_to_unit_shape_scale = float(np.median(fid_pp / np.maximum(grid, np.finfo(float).tiny)))
    projected_fid_to_tau_ratio = float(np.median(fid_projected / np.maximum(tau_projected, np.finfo(float).tiny)))

    return {
        "report_id": "cmb_tau_lensing_route_b_normalization_gap_derivation_v01",
        "claim_boundary": "normalization_gap_derivation_diagnostic_only_not_endpoint_blind_no_dark_sector_verdict",
        "derivation_status": "ALGEBRAIC_SCALE_DERIVED_PHYSICAL_TAU_NORMALIZATION_NOT_DERIVED",
        "inputs": {
            "tau_grid": rel(grid_path),
            "act_bandpowers": rel(bandpowers_path),
            "act_covariance": rel(cov_path),
            "act_binning_matrix": rel(binning_path),
            "fiducial_lenspotential_pp": rel(fiducial_path),
        },
        "locked_algebra": {
            "adapter": "m = B_ACT @ s",
            "weighted_least_squares_scale": "alpha_star = (m^T C^-1 y) / (m^T C^-1 m)",
            "chi2_at_scale": "chi2(alpha_star) = (y - alpha_star m)^T C^-1 (y - alpha_star m)",
        },
        "tau_unit_shape_diagnostic": {
            "grid_stats": stats(grid),
            "projected_stats": stats(tau_projected),
            "best_scale_alpha_star": alpha_tau,
            "scale_numerator": numerator,
            "scale_denominator": denominator,
            "unscaled_chi2": chi2(bandpowers, tau_projected, cov),
            "scaled_chi2": chi2(bandpowers, scaled_tau, cov),
            "scaled_chi2_per_18_bandpowers": chi2(bandpowers, scaled_tau, cov) / 18.0,
            "scaled_projected_stats": stats(scaled_tau),
        },
        "fiducial_pp_context": {
            "fiducial_pp_stats_L10_to_L3009": stats(fid_pp),
            "fiducial_projected_stats": stats(fid_projected),
            "fiducial_best_scale_alpha_star": alpha_fid,
            "fiducial_unscaled_chi2": chi2(bandpowers, fid_projected, cov),
            "fiducial_scaled_chi2": chi2(bandpowers, scaled_fid, cov),
            "median_fiducial_pp_divided_by_tau_unit_shape": fid_to_unit_shape_scale,
            "median_projected_fiducial_divided_by_projected_tau_unit_shape": projected_fid_to_tau_ratio,
        },
        "act_bandpower_stats": stats(bandpowers),
        "interpretation": (
            "The approximately 1e-8 factor is the covariance-weighted algebraic scale required to "
            "map the current unit-normalized Route B shape into the ACT clkk bandpower amplitude. "
            "The same order also appears by comparing the unit Route B shape with the ACT fiducial "
            "PP column. This does not derive a physical Tau amplitude; it derives the missing "
            "normalization gap that a parent-side Tau projection rule must explain before a new "
            "endpoint-blind score can be claimed."
        ),
        "blocked_physical_promotion_until": [
            "Tau-side amplitude or dimensionless normalization is derived before endpoint residual inspection",
            "PP/clkk convention and binning normalization are locked as a source-side adapter rule",
            "the normalization rule is written into the formula spec before a new score attempt",
            "a new payload is materialized from that predeclared rule and re-scored without post-score fitting",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    tau = report["tau_unit_shape_diagnostic"]
    fid = report["fiducial_pp_context"]
    text = f"""# CMB Tau Lensing Route B Normalization Gap Derivation v01

**Doc class:** data-frontier diagnostic derivation
**Reader role:** Paper 13 Tau-grid implementer
**Status:** algebraic normalization-gap derivation, not physical Tau normalization
**Canonical parent:** `docs/cmb_lensing_reduced_score_adapter_contract_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

This note derives the algebraic scale implied by the current reduced ACT
lensing adapter. It does not derive a Tau Core physical amplitude and it does
not support a dark-sector verdict.

## Locked Algebra

Let

```text
y = ACT DR6 clkk bandpower vector
C = ACT covariance
s = current Route B unit-normalized Tau-side grid
B = ACT binning matrix
m = B s
```

For a single global diagnostic scale, the covariance-weighted least-squares
solution is

```text
alpha_* = (m^T C^-1 y) / (m^T C^-1 m)
chi2(alpha_*) = (y - alpha_* m)^T C^-1 (y - alpha_* m)
```

This is an adapter diagnostic. Because `alpha_*` is computed after inspecting
the endpoint bandpowers, it is not endpoint-blind.

## Numerical Result

For the current Route B payload:

```text
alpha_* = {tau["best_scale_alpha_star"]:.17e}
unscaled chi2 = {tau["unscaled_chi2"]:.17e}
scaled chi2 = {tau["scaled_chi2"]:.17e}
scaled chi2 / 18 = {tau["scaled_chi2_per_18_bandpowers"]:.17e}
```

The active Tau grid has unit-shape scale:

```text
grid min..max = {tau["grid_stats"]["min"]:.6e} .. {tau["grid_stats"]["max"]:.6e}
B @ grid min..max = {tau["projected_stats"]["min"]:.6e} .. {tau["projected_stats"]["max"]:.6e}
```

The ACT bandpowers live at lensing amplitude scale:

```text
ACT clkk min..max = {report["act_bandpower_stats"]["min"]:.6e} .. {report["act_bandpower_stats"]["max"]:.6e}
```

So the `~1e-8` factor is not mysterious: it is the amplitude conversion needed
to turn the present unit-normalized Route B shape into the ACT lensing
bandpower scale.

## Fiducial PP Context

The ACT source package also contains a fiducial lensing-potential table with a
`PP` column. In the same L=10..3009 range:

```text
fiducial PP min..max = {fid["fiducial_pp_stats_L10_to_L3009"]["min"]:.6e} .. {fid["fiducial_pp_stats_L10_to_L3009"]["max"]:.6e}
B @ fiducial PP min..max = {fid["fiducial_projected_stats"]["min"]:.6e} .. {fid["fiducial_projected_stats"]["max"]:.6e}
median(fiducial PP / Tau unit shape) = {fid["median_fiducial_pp_divided_by_tau_unit_shape"]:.17e}
median(B @ fiducial PP / B @ Tau unit shape) = {fid["median_projected_fiducial_divided_by_projected_tau_unit_shape"]:.17e}
```

This shows the same order-of-magnitude gap from an independent source-side
reference in the ACT package. It still does not prove the Tau amplitude.

## What Remains To Derive

To turn this into an admissible endpoint-blind Tau score, the next payload must
derive and predeclare a normalization rule before scoring:

```text
N_tau = N_parent_source * N_projection * N_PP_or_clkk_convention
tau_grid(L) = N_tau * shape_tau(L)
```

Allowed promotion requires:

```text
Tau-side normalization derived before endpoint residual inspection
PP/clkk convention locked as an adapter rule
formula spec updated before materialization
new payload generated from the predeclared rule
new score run without post-score scale fitting
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive the diagnostic Route B normalization gap.")
    parser.add_argument("--grid", default=str(DEFAULT_GRID))
    parser.add_argument("--bandpowers", default=str(DEFAULT_BANDPOWERS))
    parser.add_argument("--cov", default=str(DEFAULT_COV))
    parser.add_argument("--binning", default=str(DEFAULT_BINNING))
    parser.add_argument("--fiducial", default=str(DEFAULT_FIDUCIAL))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()

    report = build_report(
        Path(args.grid).resolve(),
        Path(args.bandpowers).resolve(),
        Path(args.cov).resolve(),
        Path(args.binning).resolve(),
        Path(args.fiducial).resolve(),
    )
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
