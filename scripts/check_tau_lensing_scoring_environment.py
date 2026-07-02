#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_scoring_environment_report_v01.json"
ACT_DIR = ROOT / "data/external/act_dr6_lensing/extracted/v1.2"
BINNING = ACT_DIR / "binning_matrix_act.txt"
BANDPOWERS = ACT_DIR / "clkk_bandpowers_act.txt"
COV = ACT_DIR / "covmat_act.txt"


def array_report(path: Path, expected_shape: tuple[int, ...]) -> dict[str, Any]:
    if not path.exists():
        return {
            "file": str(path.relative_to(ROOT)),
            "exists": False,
            "expected_shape": list(expected_shape),
            "shape": None,
            "finite": False,
            "passes": False,
        }
    values = np.loadtxt(path)
    shape = tuple(values.shape)
    finite = bool(np.all(np.isfinite(values)))
    return {
        "file": str(path.relative_to(ROOT)),
        "exists": True,
        "expected_shape": list(expected_shape),
        "shape": list(shape),
        "finite": finite,
        "passes": shape == expected_shape and finite,
    }


def covariance_report(path: Path) -> dict[str, Any]:
    base = array_report(path, (18, 18))
    if not base["passes"]:
        base.update({"symmetric": False, "positive_eigenvalues": False, "min_eigenvalue": None})
        return base
    values = np.loadtxt(path)
    symmetric = bool(np.allclose(values, values.T, rtol=1e-10, atol=1e-14))
    eigenvalues = np.linalg.eigvalsh(values)
    min_eigenvalue = float(np.min(eigenvalues))
    positive = bool(min_eigenvalue > 0.0)
    base.update(
        {
            "symmetric": symmetric,
            "positive_eigenvalues": positive,
            "min_eigenvalue": min_eigenvalue,
            "passes": bool(base["passes"] and symmetric and positive),
        }
    )
    return base


def build_report() -> dict[str, Any]:
    checks = {
        "act_binning_matrix": array_report(BINNING, (18, 3000)),
        "act_bandpowers": array_report(BANDPOWERS, (18,)),
        "act_covariance": covariance_report(COV),
    }
    environment_ready = all(check["passes"] for check in checks.values())
    return {
        "report_id": "tau_lensing_scoring_environment_v01",
        "claim_boundary": "scoring_environment_check_only_no_tau_grid_no_score_no_dark_sector_verdict",
        "environment_ready_for_reduced_score_once_tau_replay_exists": environment_ready,
        "checks": checks,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "fill_exactly_one_staging_route_evidence_set_then_run_guarded_staging_promotion"
            if environment_ready
            else "repair_act_scoring_environment"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check ACT-side files required by the reduced Tau lensing score.")
    parser.add_argument(
        "--write-report",
        default=None,
        nargs="?",
        const=str(DEFAULT_REPORT),
        help=f"Optional JSON report path. Defaults to {DEFAULT_REPORT} when passed without a path.",
    )
    args = parser.parse_args()

    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
