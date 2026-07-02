#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ACT_DIR = ROOT / "data/external/act_dr6_lensing/extracted/v1.2"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

OBSERVED_PAYLOAD = DERIVED / "cmb_act_dr6_lensing_observable_payload_v01.csv"
COVARIANCE = ACT_DIR / "covmat_act.txt"

PREFIX = "cmb_act_dr6_lensing_observed_score_adapter_v01"
CLAIM_BOUNDARY = (
    "cmb_act_dr6_lensing_observed_score_adapter_v01_observed_side_chi2_adapter_only_"
    "requires_tau_prediction_no_likelihood_run_no_score_no_dark_sector_verdict"
)

VECTOR_FIELDS = [
    "adapter_row_id",
    "band_index",
    "ell_support_min",
    "ell_support_max",
    "ell_effective_abs_weighted",
    "observed_clkk",
    "sigma_clkk",
    "tau_prediction_required",
    "tau_prediction_slot",
    "accepted_observed_adapter_row",
    "score_executable_now",
    "claim_boundary",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_payload(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_matrix(path: Path, matrix: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(path, matrix, delimiter=",", fmt="%.18e")


def adapter_rows(payload: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in payload:
        band = int(row["band_index"])
        rows.append(
            {
                "adapter_row_id": f"ACTOBSADAPT01_{band:03d}",
                "band_index": band,
                "ell_support_min": row["ell_support_min"],
                "ell_support_max": row["ell_support_max"],
                "ell_effective_abs_weighted": row["ell_effective_abs_weighted"],
                "observed_clkk": row["observed_clkk"],
                "sigma_clkk": row["sigma_clkk"],
                "tau_prediction_required": "true",
                "tau_prediction_slot": f"tau_clkk_prediction_band_{band:03d}",
                "accepted_observed_adapter_row": row["accepted_as_observable_payload"],
                "score_executable_now": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# ACT DR6 Lensing Observed Score Adapter v01

**Doc class:** observed-side score adapter
**Status:** observed vector and covariance adapter locked; Tau prediction absent
**Canonical parent:** Paper 13 ACT DR6 lensing payload route

This artifact freezes the observed-side reduced score adapter for the ACT DR6
lensing baseline payload. It defines the score expression

```text
chi2_tau = (y_obs - y_tau)^T C_obs^{-1} (y_obs - y_tau)
```

where `y_obs` is the 18-bin ACT DR6 lensing convergence bandpower vector and
`y_tau` must be a Tau-side prediction vector in the same 18-bin readout basis.

Summary:

```text
observed_payload_rows={summary["observed_payload_rows"]}
covariance_shape={summary["covariance_shape"]}
inverse_covariance_shape={summary["inverse_covariance_shape"]}
covariance_symmetric={summary["covariance_symmetric"]}
covariance_positive_definite={summary["covariance_positive_definite"]}
covariance_condition_number={summary["covariance_condition_number"]}
tau_prediction_required_shape={summary["tau_prediction_required_shape"]}
tau_prediction_rows_present=0
score_executable_now=false
```

## Claim Boundary

This is an observed-side adapter only. It does not provide `y_tau`, does not run
the ACT likelihood, does not compute a Tau score, and does not decide dark-sector
necessity.
""",
        encoding="utf-8",
    )


def main() -> None:
    payload = read_payload(OBSERVED_PAYLOAD)
    y_obs = np.array([float(row["observed_clkk"]) for row in payload], dtype=float)
    cov = np.loadtxt(COVARIANCE)
    if y_obs.shape != (18,):
        raise ValueError(f"observed vector must have shape (18,), got {y_obs.shape}")
    if cov.shape != (18, 18):
        raise ValueError(f"covariance must have shape (18, 18), got {cov.shape}")

    inv_cov = np.linalg.inv(cov)
    eigenvalues = np.linalg.eigvalsh(cov)
    identity_check = np.einsum("ik,kj->ij", cov, inv_cov)
    identity_residual = np.max(np.abs(identity_check - np.eye(18)))
    symmetric_residual = np.max(np.abs(cov - cov.T))
    positive_definite = bool(np.all(eigenvalues > 0.0))
    condition_number = float(np.linalg.cond(cov))

    rows = adapter_rows(payload)
    write_csv(DERIVED / f"{PREFIX}_vector.csv", rows, VECTOR_FIELDS)
    write_matrix(DERIVED / f"{PREFIX}_inverse_covariance.csv", inv_cov)

    summary = {
        "summary_id": "CMB_ACT_DR6_LENSING_OBSERVED_SCORE_ADAPTER_V01",
        "observed_payload_path": str(OBSERVED_PAYLOAD.relative_to(ROOT)),
        "observed_payload_sha256": sha256(OBSERVED_PAYLOAD),
        "covariance_path": str(COVARIANCE.relative_to(ROOT)),
        "covariance_sha256": sha256(COVARIANCE),
        "inverse_covariance_path": f"data/derived/{PREFIX}_inverse_covariance.csv",
        "inverse_covariance_sha256": sha256(DERIVED / f"{PREFIX}_inverse_covariance.csv"),
        "observed_payload_rows": int(y_obs.shape[0]),
        "covariance_shape": list(cov.shape),
        "inverse_covariance_shape": list(inv_cov.shape),
        "covariance_symmetric": bool(symmetric_residual < 1.0e-28),
        "covariance_symmetric_residual_max_abs": f"{symmetric_residual:.18e}",
        "covariance_positive_definite": positive_definite,
        "covariance_eigenvalue_min": f"{float(np.min(eigenvalues)):.18e}",
        "covariance_eigenvalue_max": f"{float(np.max(eigenvalues)):.18e}",
        "covariance_condition_number": f"{condition_number:.12g}",
        "inverse_identity_residual_max_abs": f"{float(identity_residual):.18e}",
        "score_formula": "chi2_tau=(y_obs-y_tau)^T C_obs^{-1} (y_obs-y_tau)",
        "tau_prediction_required_shape": [18],
        "tau_prediction_rows_present": 0,
        "likelihood_run": False,
        "score_executable_now": False,
        "score_rows": 0,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "supply_tau_lensing_prediction_vector_in_act_dr6_18_bin_basis",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    (DERIVED / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                str(summary["observed_payload_rows"]),
                "18x18",
                str(summary["covariance_positive_definite"]).lower(),
                str(summary["covariance_condition_number"]),
                str(summary["score_executable_now"]).lower(),
                summary["next_required_artifact"],
            ]
        )
    )


if __name__ == "__main__":
    main()
