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
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_scale_fit_diagnostic_v01.json"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_grid(path: Path) -> np.ndarray:
    values = np.loadtxt(path, delimiter=",")
    if values.ndim == 2 and values.shape[1] == 2:
        values = values[:, 1]
    if values.shape != (3000,):
        raise ValueError(f"grid must have shape (3000,), got {values.shape}")
    if not np.all(np.isfinite(values)):
        raise ValueError("grid contains non-finite values")
    return values


def chi2(y: np.ndarray, model: np.ndarray, cov: np.ndarray) -> float:
    residual = y - model
    return float(residual.T @ np.linalg.solve(cov, residual))


def build_report(grid_path: Path, bandpowers_path: Path, cov_path: Path, binning_path: Path) -> dict[str, Any]:
    grid = load_grid(grid_path)
    bandpowers = np.loadtxt(bandpowers_path)
    cov = np.loadtxt(cov_path)
    binning = np.loadtxt(binning_path)
    projected = binning @ grid
    cov_inv = np.linalg.inv(cov)
    denominator = float(projected.T @ cov_inv @ projected)
    numerator = float(projected.T @ cov_inv @ bandpowers)
    scale = numerator / denominator
    chi2_unscaled = chi2(bandpowers, projected, cov)
    scaled_projected = scale * projected
    chi2_scaled = chi2(bandpowers, scaled_projected, cov)
    return {
        "report_id": "cmb_tau_lensing_route_b_scale_fit_diagnostic_v01",
        "claim_boundary": "post_score_scale_fit_diagnostic_only_not_endpoint_blind_no_dark_sector_verdict",
        "diagnostic_status": "POST_SCORE_TUNING_DIAGNOSTIC_NOT_PHYSICAL_CLAIM",
        "grid": rel(grid_path),
        "bandpowers": rel(bandpowers_path),
        "covariance": rel(cov_path),
        "binning_matrix": rel(binning_path),
        "unscaled": {
            "chi2": chi2_unscaled,
            "chi2_per_naive_dof": chi2_unscaled / float(bandpowers.shape[0]),
            "projected_min": float(np.min(projected)),
            "projected_max": float(np.max(projected)),
        },
        "best_scale": scale,
        "scaled": {
            "chi2": chi2_scaled,
            "chi2_per_naive_dof": chi2_scaled / float(bandpowers.shape[0]),
            "projected_min": float(np.min(scaled_projected)),
            "projected_max": float(np.max(scaled_projected)),
        },
        "bandpower_range": {
            "min": float(np.min(bandpowers)),
            "max": float(np.max(bandpowers)),
        },
        "interpretation": (
            "The current Route B candidate has a large amplitude mismatch. A score-informed "
            "global scale can remove the order-of-magnitude failure, but this is not endpoint-blind "
            "and cannot be promoted as physical evidence without an independent Tau-side "
            "normalization rule."
        ),
        "next_required_action": "derive_endpoint_blind_tau_side_normalization_near_best_scale_or_change_shape_family",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fit only a diagnostic global scale for the Route B candidate.")
    parser.add_argument("--grid", default=str(DEFAULT_GRID))
    parser.add_argument("--bandpowers", default=str(DEFAULT_BANDPOWERS))
    parser.add_argument("--cov", default=str(DEFAULT_COV))
    parser.add_argument("--binning", default=str(DEFAULT_BINNING))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    report = build_report(Path(args.grid).resolve(), Path(args.bandpowers).resolve(), Path(args.cov).resolve(), Path(args.binning).resolve())
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
