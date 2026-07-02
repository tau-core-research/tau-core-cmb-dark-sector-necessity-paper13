#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACT_BANDPOWERS = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/clkk_bandpowers_act.txt"
DEFAULT_ACT_COV = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/covmat_act.txt"


def load_replay(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"projection replay JSON missing: {path}")
    replay = json.loads(path.read_text())
    if replay.get("score_computed") is not False:
        raise ValueError("replay JSON must come from validator and must have score_computed=false")
    if replay.get("dark_sector_verdict") is not False:
        raise ValueError("replay JSON must have dark_sector_verdict=false")
    projection = replay.get("projection_replay")
    if not isinstance(projection, dict):
        raise ValueError("replay JSON is missing projection_replay")
    if projection.get("projected_shape") != [18]:
        raise ValueError(f"projected_shape must be [18], got {projection.get('projected_shape')}")
    return replay


def load_grid_from_replay(replay: dict[str, Any]) -> np.ndarray:
    grid_file = Path(replay["grid_file"])
    if not grid_file.exists():
        raise FileNotFoundError(f"grid file from replay missing: {grid_file}")
    try:
        values = np.loadtxt(grid_file, delimiter=",")
    except ValueError:
        values = np.loadtxt(grid_file)
    values = np.asarray(values, dtype=float)
    if values.ndim == 2 and 1 in values.shape:
        values = values.reshape(-1)
    if values.ndim == 2 and values.shape[1] == 2:
        values = values[:, 1]
    if values.shape != (3000,):
        raise ValueError(f"grid must have shape (3000,), got {values.shape}")
    if not np.all(np.isfinite(values)):
        raise ValueError("grid contains non-finite values")
    return values


def run_score(replay: dict[str, Any], bandpowers_path: Path, cov_path: Path) -> dict[str, Any]:
    grid = load_grid_from_replay(replay)
    projection_info = replay["projection_replay"]
    binning = np.loadtxt(projection_info["act_binning_file"])
    y = np.loadtxt(bandpowers_path)
    cov = np.loadtxt(cov_path)
    if binning.shape != (18, 3000):
        raise ValueError(f"ACT binning matrix must have shape (18, 3000), got {binning.shape}")
    if y.shape != (18,):
        raise ValueError(f"ACT bandpowers must have shape (18,), got {y.shape}")
    if cov.shape != (18, 18):
        raise ValueError(f"ACT covariance must have shape (18, 18), got {cov.shape}")
    projected = binning @ grid
    residual = y - projected
    chi2 = float(residual.T @ np.linalg.solve(cov, residual))
    return {
        "report_id": "tau_lensing_reduced_score_v01",
        "claim_boundary": "reduced_tau_lensing_score_only_no_likelihood_no_dark_sector_verdict",
        "route_id": replay["route_id"],
        "grid_sha256": replay["grid_sha256"],
        "projected_shape": list(projected.shape),
        "chi2_tau": chi2,
        "naive_dof": int(y.shape[0]),
        "chi2_per_naive_dof": chi2 / float(y.shape[0]),
        "likelihood_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the reduced ACT lensing Tau score only from a validator projection replay."
    )
    parser.add_argument("projection_replay_json", help="Validator replay JSON produced with --project.")
    parser.add_argument("--act-bandpowers", default=str(DEFAULT_ACT_BANDPOWERS))
    parser.add_argument("--act-cov", default=str(DEFAULT_ACT_COV))
    parser.add_argument("--write-score", help="Optional output JSON path for the reduced score report.")
    args = parser.parse_args()

    replay = load_replay(Path(args.projection_replay_json))
    result = run_score(replay, Path(args.act_bandpowers), Path(args.act_cov))
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.write_score:
        Path(args.write_score).write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
