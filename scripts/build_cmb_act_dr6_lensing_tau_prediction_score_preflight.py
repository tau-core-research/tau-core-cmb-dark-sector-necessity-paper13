#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
TEMPLATES = ROOT / "data/score_ready_input_templates"
SCORE_READY = ROOT / "data/score_ready_input"

ADAPTER_VECTOR = DERIVED / "cmb_act_dr6_lensing_observed_score_adapter_v01_vector.csv"
INV_COV = DERIVED / "cmb_act_dr6_lensing_observed_score_adapter_v01_inverse_covariance.csv"
EXPECTED_PREDICTION = SCORE_READY / "act_dr6_lensing_tau_prediction_vector_v01.csv"
TEMPLATE = TEMPLATES / "act_dr6_lensing_tau_prediction_vector_template.csv"

PREFIX = "cmb_act_dr6_lensing_tau_prediction_score_preflight_v01"
CLAIM_BOUNDARY = (
    "cmb_act_dr6_lensing_tau_prediction_score_preflight_v01_exact_tau_vector_requirement_"
    "no_endpoint_observed_fit_allowed_score_only_if_prediction_supplied_no_dark_sector_verdict"
)

TEMPLATE_FIELDS = [
    "band_index",
    "ell_support_min",
    "ell_support_max",
    "ell_effective_abs_weighted",
    "tau_predicted_clkk",
    "tau_prediction_source_id",
    "tau_derivation_artifact",
    "endpoint_blind_policy",
    "normalization_convention",
    "readout_basis",
    "claim_boundary",
]

PREFLIGHT_FIELDS = [
    "preflight_row_id",
    "band_index",
    "tau_prediction_slot",
    "expected_field_present",
    "tau_value_present",
    "tau_value_finite",
    "endpoint_blind_policy_declared",
    "readout_basis_matches",
    "accepted_for_score",
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


def build_template(adapter_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in adapter_rows:
        rows.append(
            {
                "band_index": row["band_index"],
                "ell_support_min": row["ell_support_min"],
                "ell_support_max": row["ell_support_max"],
                "ell_effective_abs_weighted": row["ell_effective_abs_weighted"],
                "tau_predicted_clkk": "",
                "tau_prediction_source_id": "",
                "tau_derivation_artifact": "",
                "endpoint_blind_policy": "must_be_declared_endpoint_blind_before_observed_score",
                "normalization_convention": "ACT_DR6_clkk_no_extra_factors",
                "readout_basis": "ACT_DR6_LENSING_BASELINE_18_BIN_CLKK",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def finite_float(value: str) -> bool:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(parsed)


def preflight_rows(prediction_rows: list[dict[str, str]], adapter_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by_band = {row.get("band_index", ""): row for row in prediction_rows}
    rows: list[dict[str, object]] = []
    required = set(TEMPLATE_FIELDS)
    for adapter in adapter_rows:
        band = adapter["band_index"]
        prediction = by_band.get(band, {})
        fields_present = required.issubset(prediction.keys())
        value_present = bool(prediction.get("tau_predicted_clkk", ""))
        value_finite = finite_float(prediction.get("tau_predicted_clkk", ""))
        endpoint_blind = prediction.get("endpoint_blind_policy") == "endpoint_blind_declared_no_observed_endpoint_fit"
        basis_matches = prediction.get("readout_basis") == "ACT_DR6_LENSING_BASELINE_18_BIN_CLKK"
        accepted = fields_present and value_present and value_finite and endpoint_blind and basis_matches
        rows.append(
            {
                "preflight_row_id": f"ACTTAUPREFLIGHT01_{int(band):03d}",
                "band_index": band,
                "tau_prediction_slot": adapter["tau_prediction_slot"],
                "expected_field_present": str(fields_present).lower(),
                "tau_value_present": str(value_present).lower(),
                "tau_value_finite": str(value_finite).lower(),
                "endpoint_blind_policy_declared": str(endpoint_blind).lower(),
                "readout_basis_matches": str(basis_matches).lower(),
                "accepted_for_score": str(accepted).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def compute_score(adapter_rows: list[dict[str, str]], prediction_rows: list[dict[str, str]]) -> dict[str, object]:
    by_band = {int(row["band_index"]): row for row in prediction_rows}
    y_obs = np.array([float(row["observed_clkk"]) for row in adapter_rows], dtype=float)
    y_tau = np.array([float(by_band[int(row["band_index"])]["tau_predicted_clkk"]) for row in adapter_rows], dtype=float)
    inv_cov = np.loadtxt(INV_COV, delimiter=",")
    residual = y_obs - y_tau
    chi2 = float(residual.T @ inv_cov @ residual)
    return {
        "score_computed": True,
        "chi2_tau": chi2,
        "naive_dof": int(y_obs.shape[0]),
        "chi2_per_naive_dof": chi2 / float(y_obs.shape[0]),
        "residual_max_abs": float(np.max(np.abs(residual))),
    }


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# ACT DR6 Lensing Tau Prediction Score Preflight v01

**Doc class:** Tau-side prediction score preflight
**Status:** exact 18-bin Tau prediction input shape locked
**Canonical parent:** Paper 13 ACT DR6 lensing scoring route

This artifact converts the observed-side ACT DR6 lensing adapter into an exact
Tau-side input requirement. The required file is:

```text
data/score_ready_input/act_dr6_lensing_tau_prediction_vector_v01.csv
```

The file must contain 18 rows, one per ACT DR6 lensing bin, in the readout basis
`ACT_DR6_LENSING_BASELINE_18_BIN_CLKK`. The score can execute only if all rows
provide finite `tau_predicted_clkk` values and declare the endpoint-blind policy
`endpoint_blind_declared_no_observed_endpoint_fit`.

If the supplied source id is `tau_core_null_response_control_v01`, the resulting
score is a null-response control score only. It is not a physical Tau response
claim and cannot decide dark-sector necessity.

Summary:

```text
template_rows={summary["template_rows"]}
prediction_file_present={summary["prediction_file_present"]}
prediction_rows={summary["prediction_rows"]}
accepted_prediction_rows={summary["accepted_prediction_rows"]}
score_executable_now={summary["score_executable_now"]}
score_computed={summary["score_computed"]}
chi2_tau={summary["chi2_tau"]}
chi2_per_naive_dof={summary["chi2_per_naive_dof"]}
next_required_artifact={summary["next_required_artifact"]}
```

## Claim Boundary

This preflight does not derive the Tau prediction vector. It only defines and
checks the exact score input shape. A later supplied vector must be justified by
a Tau-side derivation and must not be fitted to the observed endpoint.
""",
        encoding="utf-8",
    )


def main() -> None:
    adapter = read_csv(ADAPTER_VECTOR)
    template_rows = build_template(adapter)
    write_csv(TEMPLATE, template_rows, TEMPLATE_FIELDS)

    prediction_present = EXPECTED_PREDICTION.exists()
    prediction_rows = read_csv(EXPECTED_PREDICTION) if prediction_present else []
    preflight = preflight_rows(prediction_rows, adapter)
    accepted_rows = sum(row["accepted_for_score"] == "true" for row in preflight)
    score_executable = prediction_present and accepted_rows == len(adapter)
    score = compute_score(adapter, prediction_rows) if score_executable else {
        "score_computed": False,
        "chi2_tau": None,
        "naive_dof": 18,
        "chi2_per_naive_dof": None,
        "residual_max_abs": None,
    }

    write_csv(DERIVED / f"{PREFIX}.csv", preflight, PREFLIGHT_FIELDS)
    summary = {
        "summary_id": "CMB_ACT_DR6_LENSING_TAU_PREDICTION_SCORE_PREFLIGHT_V01",
        "adapter_vector_path": str(ADAPTER_VECTOR.relative_to(ROOT)),
        "adapter_vector_sha256": sha256(ADAPTER_VECTOR),
        "inverse_covariance_path": str(INV_COV.relative_to(ROOT)),
        "inverse_covariance_sha256": sha256(INV_COV),
        "template_path": str(TEMPLATE.relative_to(ROOT)),
        "template_sha256": sha256(TEMPLATE),
        "expected_prediction_path": str(EXPECTED_PREDICTION.relative_to(ROOT)),
        "prediction_file_present": prediction_present,
        "prediction_sha256": sha256(EXPECTED_PREDICTION) if prediction_present else "",
        "template_rows": len(template_rows),
        "prediction_rows": len(prediction_rows),
        "preflight_rows": len(preflight),
        "accepted_prediction_rows": accepted_rows,
        "score_executable_now": score_executable,
        "score_computed": score["score_computed"],
        "chi2_tau": score["chi2_tau"],
        "naive_dof": score["naive_dof"],
        "chi2_per_naive_dof": score["chi2_per_naive_dof"],
        "residual_max_abs": score["residual_max_abs"],
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": (
            "none_score_computed_review_claim_boundary"
            if score_executable
            else "supply_endpoint_blind_tau_prediction_vector_in_act_dr6_18_bin_basis"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    (DERIVED / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                str(summary["template_rows"]),
                str(summary["prediction_file_present"]).lower(),
                str(summary["prediction_rows"]),
                str(summary["accepted_prediction_rows"]),
                str(summary["score_executable_now"]).lower(),
                str(summary["score_computed"]).lower(),
                summary["next_required_artifact"],
            ]
        )
    )


if __name__ == "__main__":
    main()
