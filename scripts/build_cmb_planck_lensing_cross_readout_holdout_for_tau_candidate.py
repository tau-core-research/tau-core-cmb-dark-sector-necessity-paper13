#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ACT_DIR = ROOT / "data/external/act_dr6_lensing/extracted/v1.2"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PLANCK_BANDPOWERS = ACT_DIR / "clkk_bandpowers_planck.txt"
PLANCK_BINNING = ACT_DIR / "binning_matrix_planck.txt"
ACTPLANCK_COV = ACT_DIR / "covmat_actplanck.txt"
ACT_SHAPE_SUMMARY = DERIVED / "cmb_act_dr6_lensing_tau_shape_response_controls_v01_summary.json"
ACT_SHAPE_SCOREBOARD = DERIVED / "cmb_act_dr6_lensing_tau_shape_response_controls_v01_scoreboard.csv"

PREFIX = "cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01"
CLAIM_BOUNDARY = (
    "cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01_act_selected_shape_transferred_"
    "unchanged_to_planck_block_diagnostic_not_likelihood_no_physical_tau_claim_no_dark_sector_verdict"
)

PAYLOAD_FIELDS = [
    "payload_row_id",
    "band_index",
    "ell_support_min",
    "ell_support_max",
    "ell_effective_abs_weighted",
    "binning_nonzero_weight_count",
    "binning_weight_sum",
    "observed_clkk",
    "covariance_variance",
    "sigma_clkk",
    "tau_predicted_clkk",
    "residual_clkk",
    "readout_role",
    "candidate_id",
    "claim_boundary",
]

SCORE_FIELDS = [
    "score_id",
    "candidate_id",
    "readout_basis",
    "rows",
    "chi2_tau",
    "chi2_per_naive_dof",
    "delta_chi2_vs_null",
    "fractional_chi2_improvement_vs_null",
    "residual_max_abs",
    "score_role",
    "claim_boundary",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def tau_shape(ells: np.ndarray, ell_c: float, rise_power: float, fall_power: float) -> np.ndarray:
    x = np.maximum(ells, 1.0) / ell_c
    raw = np.power(x, rise_power) / (1.0 + np.power(x, rise_power + fall_power))
    peak = float(np.max(raw))
    if peak <= 0.0:
        raise ValueError("shape peak must be positive")
    return raw / peak


def effective_ell_rows(binning: np.ndarray) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index, weights in enumerate(binning, start=1):
        nonzero_indices = np.nonzero(weights)[0]
        if nonzero_indices.size == 0:
            raise ValueError(f"empty binning row at Planck band {index}")
        ell_values = nonzero_indices + 1
        nonzero_weights = weights[nonzero_indices]
        abs_weight_sum = float(np.sum(np.abs(nonzero_weights)))
        ell_eff = float(np.sum(ell_values * np.abs(nonzero_weights)) / abs_weight_sum)
        rows.append(
            {
                "band_index": index,
                "ell_support_min": int(ell_values[0]),
                "ell_support_max": int(ell_values[-1]),
                "ell_effective_abs_weighted": ell_eff,
                "binning_nonzero_weight_count": int(nonzero_indices.size),
                "binning_weight_sum": float(np.sum(weights)),
            }
        )
    return rows


def score(y_obs: np.ndarray, y_tau: np.ndarray, inv_cov: np.ndarray) -> dict[str, float]:
    residual = y_obs - y_tau
    chi2 = float(residual.T @ inv_cov @ residual)
    return {
        "chi2_tau": chi2,
        "chi2_per_naive_dof": chi2 / float(y_obs.shape[0]),
        "residual_max_abs": float(np.max(np.abs(residual))),
    }


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# Planck Lensing Cross-Readout Holdout for Tau Candidate v01

**Doc class:** cross-readout holdout diagnostic
**Status:** ACT-selected nonzero Tau-shape candidate transferred unchanged to the Planck lensing block
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact tests whether the best ACT-screened nonzero Tau Core-style
lensing response control remains useful when transferred unchanged to the
Planck lensing bandpower block distributed in the same ACT DR6 lensing package.
The candidate parameters are not refitted to Planck.

The Planck-only diagnostic covariance is taken as the bottom-right \(9\\times9\)
block of `covmat_actplanck.txt`, corresponding to the 18 ACT rows followed by
the 9 Planck rows. This is a reduced cross-readout diagnostic, not a full
Planck likelihood evaluation.

Summary:

```text
planck_rows={summary["planck_rows"]}
planck_covariance_shape={summary["planck_covariance_shape"]}
planck_covariance_positive_definite={summary["planck_covariance_positive_definite"]}
candidate_id={summary["candidate_id"]}
transferred_amplitude={summary["transferred_amplitude"]}
transferred_ell_c={summary["transferred_ell_c"]}
transferred_rise_power={summary["transferred_rise_power"]}
transferred_fall_power={summary["transferred_fall_power"]}
null_chi2={summary["null_chi2"]}
candidate_chi2={summary["candidate_chi2"]}
candidate_delta_chi2_vs_null={summary["candidate_delta_chi2_vs_null"]}
candidate_fractional_chi2_improvement_vs_null={summary["candidate_fractional_chi2_improvement_vs_null"]}
obligation_NZRESP_OBL_004_status={summary["obligation_NZRESP_OBL_004_status"]}
```

## Claim Boundary

This artifact supports only a holdout diagnostic statement: the same
ACT-selected nonzero shape candidate can be evaluated on a Planck lensing
readout block without refitting. It is not a physical Tau prediction, not a
Planck likelihood run, and not a dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    planck_bandpowers = np.atleast_1d(np.loadtxt(PLANCK_BANDPOWERS)).astype(float)
    planck_binning = np.atleast_2d(np.loadtxt(PLANCK_BINNING)).astype(float)
    actplanck_cov = np.atleast_2d(np.loadtxt(ACTPLANCK_COV)).astype(float)

    if planck_bandpowers.shape[0] != 9:
        raise ValueError("expected 9 Planck bandpowers")
    if planck_binning.shape != (9, 3000):
        raise ValueError(f"unexpected Planck binning shape {planck_binning.shape}")
    if actplanck_cov.shape != (27, 27):
        raise ValueError(f"unexpected ACT+Planck covariance shape {actplanck_cov.shape}")

    planck_cov = actplanck_cov[18:, 18:]
    eigvals = np.linalg.eigvalsh(planck_cov)
    positive_definite = bool(np.all(eigvals > 0.0))
    if not positive_definite:
        raise ValueError("Planck covariance block is not positive definite")
    inv_cov = np.linalg.inv(planck_cov)

    shape_summary = json.loads(ACT_SHAPE_SUMMARY.read_text())
    best_candidate_id = str(shape_summary["best_candidate_id"])
    best_score = next(row for row in read_csv(ACT_SHAPE_SCOREBOARD) if row["candidate_id"] == best_candidate_id)

    amplitude = float(best_score["amplitude"])
    ell_c = float(best_score["ell_c"])
    rise_power = float(best_score["rise_power"])
    fall_power = float(best_score["fall_power"])

    ell_rows = effective_ell_rows(planck_binning)
    ells = np.array([row["ell_effective_abs_weighted"] for row in ell_rows], dtype=float)
    y_null = np.zeros_like(planck_bandpowers)
    y_candidate = amplitude * tau_shape(ells, ell_c, rise_power, fall_power)

    null_score = score(planck_bandpowers, y_null, inv_cov)
    candidate_score = score(planck_bandpowers, y_candidate, inv_cov)
    delta = null_score["chi2_tau"] - candidate_score["chi2_tau"]
    fractional = delta / null_score["chi2_tau"] if null_score["chi2_tau"] else 0.0

    payload_rows: list[dict[str, object]] = []
    for row, observed, prediction, variance in zip(
        ell_rows, planck_bandpowers, y_candidate, np.diag(planck_cov), strict=True
    ):
        payload_rows.append(
            {
                "payload_row_id": f"PLANCK_HOLDOUT_BAND_{int(row['band_index']):03d}",
                "band_index": int(row["band_index"]),
                "ell_support_min": int(row["ell_support_min"]),
                "ell_support_max": int(row["ell_support_max"]),
                "ell_effective_abs_weighted": f"{row['ell_effective_abs_weighted']:.12g}",
                "binning_nonzero_weight_count": int(row["binning_nonzero_weight_count"]),
                "binning_weight_sum": f"{row['binning_weight_sum']:.12e}",
                "observed_clkk": f"{observed:.18e}",
                "covariance_variance": f"{variance:.18e}",
                "sigma_clkk": f"{math.sqrt(float(variance)):.18e}",
                "tau_predicted_clkk": f"{prediction:.18e}",
                "residual_clkk": f"{(observed - prediction):.18e}",
                "readout_role": "PLANCK_LENSING_BLOCK_FROM_ACT_DR6_PACKAGE_CROSS_READOUT_DIAGNOSTIC",
                "candidate_id": best_candidate_id,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    score_rows = [
        {
            "score_id": "PLANCK_HOLDOUT_NULL_RESPONSE",
            "candidate_id": "tau_core_null_response_control_v01",
            "readout_basis": "PLANCK_LENSING_9_BIN_BLOCK_FROM_ACT_DR6_PACKAGE",
            "rows": planck_bandpowers.shape[0],
            "chi2_tau": f"{null_score['chi2_tau']:.18e}",
            "chi2_per_naive_dof": f"{null_score['chi2_per_naive_dof']:.18e}",
            "delta_chi2_vs_null": f"{0.0:.18e}",
            "fractional_chi2_improvement_vs_null": f"{0.0:.18e}",
            "residual_max_abs": f"{null_score['residual_max_abs']:.18e}",
            "score_role": "cross_readout_null_control",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "score_id": "PLANCK_HOLDOUT_ACT_SELECTED_NONZERO_CANDIDATE",
            "candidate_id": best_candidate_id,
            "readout_basis": "PLANCK_LENSING_9_BIN_BLOCK_FROM_ACT_DR6_PACKAGE",
            "rows": planck_bandpowers.shape[0],
            "chi2_tau": f"{candidate_score['chi2_tau']:.18e}",
            "chi2_per_naive_dof": f"{candidate_score['chi2_per_naive_dof']:.18e}",
            "delta_chi2_vs_null": f"{delta:.18e}",
            "fractional_chi2_improvement_vs_null": f"{fractional:.18e}",
            "residual_max_abs": f"{candidate_score['residual_max_abs']:.18e}",
            "score_role": "act_selected_candidate_transferred_unchanged_to_planck_holdout",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    payload_path = DERIVED / f"{PREFIX}.csv"
    score_path = DERIVED / f"{PREFIX}_scoreboard.csv"
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    write_csv(payload_path, payload_rows, PAYLOAD_FIELDS)
    write_csv(score_path, score_rows, SCORE_FIELDS)

    summary = {
        "summary_id": "CMB_PLANCK_LENSING_CROSS_READOUT_HOLDOUT_FOR_TAU_CANDIDATE_V01",
        "planck_bandpowers_path": str(PLANCK_BANDPOWERS.relative_to(ROOT)),
        "planck_bandpowers_sha256": sha256(PLANCK_BANDPOWERS),
        "planck_binning_path": str(PLANCK_BINNING.relative_to(ROOT)),
        "planck_binning_sha256": sha256(PLANCK_BINNING),
        "actplanck_covariance_path": str(ACTPLANCK_COV.relative_to(ROOT)),
        "actplanck_covariance_sha256": sha256(ACTPLANCK_COV),
        "act_shape_summary_path": str(ACT_SHAPE_SUMMARY.relative_to(ROOT)),
        "act_shape_summary_sha256": sha256(ACT_SHAPE_SUMMARY),
        "payload_path": str(payload_path.relative_to(ROOT)),
        "payload_sha256": sha256(payload_path),
        "scoreboard_path": str(score_path.relative_to(ROOT)),
        "scoreboard_sha256": sha256(score_path),
        "planck_rows": int(planck_bandpowers.shape[0]),
        "planck_covariance_shape": "9x9_from_bottom_right_block_of_27x27_actplanck_covariance",
        "planck_covariance_positive_definite": positive_definite,
        "planck_covariance_condition_number": float(np.linalg.cond(planck_cov)),
        "planck_covariance_min_eigenvalue": float(np.min(eigvals)),
        "candidate_id": best_candidate_id,
        "transferred_amplitude": amplitude,
        "transferred_ell_c": ell_c,
        "transferred_rise_power": rise_power,
        "transferred_fall_power": fall_power,
        "null_chi2": null_score["chi2_tau"],
        "null_chi2_per_naive_dof": null_score["chi2_per_naive_dof"],
        "candidate_chi2": candidate_score["chi2_tau"],
        "candidate_chi2_per_naive_dof": candidate_score["chi2_per_naive_dof"],
        "candidate_delta_chi2_vs_null": delta,
        "candidate_fractional_chi2_improvement_vs_null": fractional,
        "candidate_transferred_without_planck_refit": True,
        "obligation_NZRESP_OBL_004_status": "partially_addressed_by_planck_cross_readout_diagnostic_not_closed",
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "tau_side_shape_and_amplitude_derivation_or_rejection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                str(summary["planck_rows"]),
                f"{summary['null_chi2']:.12g}",
                f"{summary['candidate_chi2']:.12g}",
                f"{summary['candidate_delta_chi2_vs_null']:.12g}",
            ]
        )
    )


if __name__ == "__main__":
    main()
