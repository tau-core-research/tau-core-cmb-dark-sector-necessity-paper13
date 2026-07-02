#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

ADAPTER_VECTOR = DERIVED / "cmb_act_dr6_lensing_observed_score_adapter_v01_vector.csv"
INV_COV = DERIVED / "cmb_act_dr6_lensing_observed_score_adapter_v01_inverse_covariance.csv"
NULL_SUMMARY = DERIVED / "cmb_act_dr6_lensing_tau_prediction_score_preflight_v01_summary.json"

PREFIX = "cmb_act_dr6_lensing_tau_shape_response_controls_v01"
CLAIM_BOUNDARY = (
    "cmb_act_dr6_lensing_tau_shape_response_controls_v01_endpoint_blind_shape_screening_only_"
    "not_physical_tau_response_no_likelihood_no_dark_sector_verdict"
)

CONTROL_FIELDS = [
    "control_row_id",
    "candidate_id",
    "band_index",
    "ell_effective_abs_weighted",
    "amplitude",
    "ell_c",
    "rise_power",
    "fall_power",
    "shape_unit",
    "tau_predicted_clkk",
    "tau_prediction_source_id",
    "endpoint_blind_policy",
    "normalization_convention",
    "readout_basis",
    "claim_boundary",
]

SCORE_FIELDS = [
    "candidate_id",
    "tau_prediction_source_id",
    "amplitude",
    "ell_c",
    "rise_power",
    "fall_power",
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


def score_vector(y_obs: np.ndarray, y_tau: np.ndarray, inv_cov: np.ndarray) -> dict[str, float]:
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
        f"""# ACT DR6 Lensing Tau Shape Response Controls v01

**Doc class:** nonzero Tau response control screening
**Status:** endpoint-blind analytic shape controls scored against ACT DR6 lensing adapter
**Canonical parent:** Paper 13 ACT DR6 lensing scoring route

This artifact screens a small predeclared family of nonzero Tau Core-style
lensing response controls in the locked ACT DR6 18-bin readout basis. The
control shape is analytic:

```text
s(L) = (L/L_c)^p / (1 + (L/L_c)^(p+q)), normalized to max(s)=1
y_tau(L) = A s(L)
```

The candidates use fixed amplitudes and shape parameters declared by the
script. They are diagnostic controls, not fitted physical Tau predictions.

Summary:

```text
candidate_count={summary["candidate_count"]}
null_chi2={summary["null_chi2"]}
best_candidate_id={summary["best_candidate_id"]}
best_chi2={summary["best_chi2"]}
best_delta_chi2_vs_null={summary["best_delta_chi2_vs_null"]}
best_fractional_chi2_improvement_vs_null={summary["best_fractional_chi2_improvement_vs_null"]}
best_chi2_per_naive_dof={summary["best_chi2_per_naive_dof"]}
```

## Claim Boundary

This is a shape-screening control artifact only. It does not run the ACT
likelihood, does not fit a final Tau response, does not validate Tau Core, and
does not decide dark-sector necessity.
""",
        encoding="utf-8",
    )


def main() -> None:
    adapter = read_csv(ADAPTER_VECTOR)
    inv_cov = np.loadtxt(INV_COV, delimiter=",")
    null_summary = json.loads(NULL_SUMMARY.read_text())
    null_chi2 = float(null_summary["chi2_tau"])

    ells = np.array([float(row["ell_effective_abs_weighted"]) for row in adapter], dtype=float)
    y_obs = np.array([float(row["observed_clkk"]) for row in adapter], dtype=float)

    # Predeclared endpoint-blind control family: broad lensing-like humps with
    # fixed amplitude ladder in ACT C_L^kk units. These are controls, not fits.
    amplitudes = [1.0e-8, 3.0e-8, 1.0e-7, 3.0e-7]
    shape_specs = [
        ("morph_lensing_broad_lowL", 120.0, 0.5, 1.0),
        ("morph_lensing_mid_band", 350.0, 0.8, 1.2),
        ("morph_lensing_high_tail", 800.0, 0.8, 1.0),
    ]

    control_rows: list[dict[str, object]] = []
    score_rows: list[dict[str, object]] = []
    for shape_name, ell_c, rise_power, fall_power in shape_specs:
        unit = tau_shape(ells, ell_c, rise_power, fall_power)
        for amplitude in amplitudes:
            candidate_id = f"tau_shape_control_{shape_name}_A{amplitude:.0e}".replace("+", "")
            y_tau = amplitude * unit
            score = score_vector(y_obs, y_tau, inv_cov)
            delta = null_chi2 - score["chi2_tau"]
            fractional = delta / null_chi2 if null_chi2 else 0.0
            score_rows.append(
                {
                    "candidate_id": candidate_id,
                    "tau_prediction_source_id": "tau_core_morphological_lensing_shape_control_v01",
                    "amplitude": f"{amplitude:.18e}",
                    "ell_c": f"{ell_c:.6g}",
                    "rise_power": f"{rise_power:.6g}",
                    "fall_power": f"{fall_power:.6g}",
                    "chi2_tau": f"{score['chi2_tau']:.18e}",
                    "chi2_per_naive_dof": f"{score['chi2_per_naive_dof']:.18e}",
                    "delta_chi2_vs_null": f"{delta:.18e}",
                    "fractional_chi2_improvement_vs_null": f"{fractional:.18e}",
                    "residual_max_abs": f"{score['residual_max_abs']:.18e}",
                    "score_role": "endpoint_blind_shape_screening_control_not_final_prediction",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            for row, shape_value, prediction in zip(adapter, unit, y_tau, strict=True):
                control_rows.append(
                    {
                        "control_row_id": f"{candidate_id}_B{int(row['band_index']):03d}",
                        "candidate_id": candidate_id,
                        "band_index": row["band_index"],
                        "ell_effective_abs_weighted": row["ell_effective_abs_weighted"],
                        "amplitude": f"{amplitude:.18e}",
                        "ell_c": f"{ell_c:.6g}",
                        "rise_power": f"{rise_power:.6g}",
                        "fall_power": f"{fall_power:.6g}",
                        "shape_unit": f"{shape_value:.18e}",
                        "tau_predicted_clkk": f"{prediction:.18e}",
                        "tau_prediction_source_id": "tau_core_morphological_lensing_shape_control_v01",
                        "endpoint_blind_policy": "endpoint_blind_declared_predeclared_shape_family_no_observed_fit",
                        "normalization_convention": "ACT_DR6_clkk_no_extra_factors",
                        "readout_basis": "ACT_DR6_LENSING_BASELINE_18_BIN_CLKK",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )

    score_rows_sorted = sorted(score_rows, key=lambda row: float(row["chi2_tau"]))
    best = score_rows_sorted[0]
    summary = {
        "summary_id": "CMB_ACT_DR6_LENSING_TAU_SHAPE_RESPONSE_CONTROLS_V01",
        "adapter_vector_path": str(ADAPTER_VECTOR.relative_to(ROOT)),
        "adapter_vector_sha256": sha256(ADAPTER_VECTOR),
        "inverse_covariance_path": str(INV_COV.relative_to(ROOT)),
        "inverse_covariance_sha256": sha256(INV_COV),
        "null_summary_path": str(NULL_SUMMARY.relative_to(ROOT)),
        "null_summary_sha256": sha256(NULL_SUMMARY),
        "candidate_count": len(score_rows),
        "control_rows": len(control_rows),
        "null_chi2": null_chi2,
        "null_chi2_per_naive_dof": float(null_summary["chi2_per_naive_dof"]),
        "best_candidate_id": best["candidate_id"],
        "best_chi2": float(best["chi2_tau"]),
        "best_chi2_per_naive_dof": float(best["chi2_per_naive_dof"]),
        "best_delta_chi2_vs_null": float(best["delta_chi2_vs_null"]),
        "best_fractional_chi2_improvement_vs_null": float(best["fractional_chi2_improvement_vs_null"]),
        "score_role": "endpoint_blind_shape_screening_control_not_final_prediction",
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "derive_or_reject_nonzero_tau_lensing_response_from_tau_side_not_endpoint_fit",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(DERIVED / f"{PREFIX}.csv", control_rows, CONTROL_FIELDS)
    write_csv(DERIVED / f"{PREFIX}_scoreboard.csv", score_rows_sorted, SCORE_FIELDS)
    (DERIVED / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                str(summary["candidate_count"]),
                f"{summary['null_chi2']:.12g}",
                summary["best_candidate_id"],
                f"{summary['best_chi2']:.12g}",
                f"{summary['best_delta_chi2_vs_null']:.12g}",
                f"{summary['best_fractional_chi2_improvement_vs_null']:.12g}",
            ]
        )
    )


if __name__ == "__main__":
    main()
