#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GRID_VALIDATOR = ROOT / "scripts/validate_tau_lensing_grid_payload.py"
SCORE_RUNNER = ROOT / "scripts/run_tau_lensing_reduced_score.py"
SCORE_VALIDATOR = ROOT / "scripts/validate_tau_lensing_reduced_score_output.py"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="tau_lensing_positive_smoke_") as tmp:
        tmpdir = Path(tmp)
        grid = tmpdir / "synthetic_zero_grid.csv"
        replay = tmpdir / "synthetic_zero_replay.json"
        score = tmpdir / "synthetic_zero_score.json"
        with grid.open("w") as handle:
            for ell in range(10, 3010):
                handle.write(f"{ell},0.0\n")

        replay_report = run_json(
            [
                sys.executable,
                str(GRID_VALIDATOR),
                str(grid),
                "--route",
                "direct_tau_PP_grid",
                "--project",
                "--write-replay",
                str(replay),
            ]
        )
        score_report = run_json(
            [
                sys.executable,
                str(SCORE_RUNNER),
                str(replay),
                "--write-score",
                str(score),
            ]
        )
        score_validation = run_json([sys.executable, str(SCORE_VALIDATOR), str(score)])

    report = {
        "report_id": "tau_lensing_positive_score_path_smoke_v01",
        "claim_boundary": "positive_score_path_smoke_synthetic_grid_only_no_tau_evidence_no_dark_sector_verdict",
        "synthetic_input": "zero_grid_L_10_to_3009",
        "tau_evidence_used": False,
        "projection_replay_valid_shape": replay_report.get("projection_replay", {}).get("projected_shape") == [18],
        "score_schema_validated": score_validation.get("validated") is True,
        "score_report_id": score_report.get("report_id"),
        "score_claim_boundary": score_report.get("claim_boundary"),
        "likelihood_run": score_report.get("likelihood_run"),
        "score_run": True,
        "score_is_physical_tau_score": False,
        "dark_sector_verdict": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
