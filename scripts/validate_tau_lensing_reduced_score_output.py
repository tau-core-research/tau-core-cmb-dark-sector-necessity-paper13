#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "report_id",
    "claim_boundary",
    "route_id",
    "grid_sha256",
    "projected_shape",
    "chi2_tau",
    "naive_dof",
    "chi2_per_naive_dof",
    "likelihood_run",
    "dark_sector_verdict",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_score(payload: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS - set(payload)
    extra = set(payload) - REQUIRED_FIELDS
    require(not missing, f"missing required score fields: {sorted(missing)}")
    require(not extra, f"unexpected score fields: {sorted(extra)}")
    require(payload["report_id"] == "tau_lensing_reduced_score_v01", "bad report_id")
    require(
        payload["claim_boundary"] == "reduced_tau_lensing_score_only_no_likelihood_no_dark_sector_verdict",
        "bad claim_boundary",
    )
    require(payload["route_id"] in {"direct_tau_PP_grid", "delta_PP_tau"}, "bad route_id")
    require(isinstance(payload["grid_sha256"], str) and len(payload["grid_sha256"]) == 64, "bad grid_sha256")
    require(payload["projected_shape"] == [18], "projected_shape must be [18]")
    require(isinstance(payload["chi2_tau"], (int, float)), "chi2_tau must be numeric")
    require(payload["chi2_tau"] >= 0.0, "chi2_tau must be nonnegative")
    require(payload["naive_dof"] == 18, "naive_dof must be 18")
    require(isinstance(payload["chi2_per_naive_dof"], (int, float)), "chi2_per_naive_dof must be numeric")
    require(payload["chi2_per_naive_dof"] >= 0.0, "chi2_per_naive_dof must be nonnegative")
    require(payload["likelihood_run"] is False, "likelihood_run must be false")
    require(payload["dark_sector_verdict"] is False, "dark_sector_verdict must be false")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate reduced Tau lensing score JSON schema and claim boundary.")
    parser.add_argument("score_json", help="Reduced score JSON output from run_tau_lensing_reduced_score.py.")
    args = parser.parse_args()

    path = Path(args.score_json)
    payload = json.loads(path.read_text())
    validate_score(payload)
    print(json.dumps({"validated": True, "score_json": str(path), "claim_boundary_ok": True}, sort_keys=True))


if __name__ == "__main__":
    main()
