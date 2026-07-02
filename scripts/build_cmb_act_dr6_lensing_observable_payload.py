#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACT_DIR = ROOT / "data/external/act_dr6_lensing/extracted/v1.2"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "cmb_act_dr6_lensing_observable_payload_v01"
CLAIM_BOUNDARY = (
    "cmb_act_dr6_lensing_observable_payload_v01_observed_lensing_payload_only_"
    "no_tau_prediction_no_likelihood_run_no_score_no_dark_sector_verdict"
)

SOURCE_FILES = {
    "act_dr6_lensing_bandpowers": ACT_DIR / "clkk_bandpowers_act.txt",
    "act_dr6_lensing_covariance": ACT_DIR / "covmat_act.txt",
    "act_dr6_lensing_binning_matrix": ACT_DIR / "binning_matrix_act.txt",
}

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
    "absolute_snr",
    "observable_role",
    "accepted_as_observable_payload",
    "accepted_for_scoring_now",
    "claim_boundary",
]

SOURCE_AUDIT_FIELDS = [
    "source_row_id",
    "source_component",
    "local_path",
    "file_exists",
    "file_size_bytes",
    "sha256",
    "numeric_rows",
    "numeric_columns",
    "accepted_as_observable_payload_source",
    "accepted_for_scoring_now",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "source_files_expected",
    "source_files_present",
    "source_files_hash_bound",
    "bandpower_rows",
    "covariance_rows",
    "covariance_columns",
    "binning_matrix_rows",
    "binning_matrix_columns",
    "shape_consistent",
    "observable_payload_rows",
    "accepted_observable_payload_rows",
    "accepted_for_scoring_rows",
    "tau_prediction_rows",
    "likelihood_adapter_rows",
    "score_rows",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def numeric_rows(path: Path) -> list[list[float]]:
    rows: list[list[float]] = []
    if not path.exists():
        return rows
    with path.open() as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            rows.append([float(part) for part in stripped.split()])
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_audit_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, (component, path) in enumerate(SOURCE_FILES.items(), start=1):
        parsed = numeric_rows(path)
        column_counts = sorted({len(row) for row in parsed})
        rows.append(
            {
                "source_row_id": f"ACTOBS01_SOURCE_{index:03d}",
                "source_component": component,
                "local_path": str(path.relative_to(ROOT)),
                "file_exists": str(path.exists()).lower(),
                "file_size_bytes": path.stat().st_size if path.exists() else 0,
                "sha256": sha256(path) if path.exists() else "",
                "numeric_rows": len(parsed),
                "numeric_columns": column_counts[0] if len(column_counts) == 1 else "|".join(map(str, column_counts)),
                "accepted_as_observable_payload_source": str(path.exists() and bool(parsed)).lower(),
                "accepted_for_scoring_now": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def payload_rows(
    bandpowers: list[list[float]],
    covariance: list[list[float]],
    binning: list[list[float]],
    shape_consistent: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not shape_consistent:
        return rows
    for index, band_row in enumerate(bandpowers, start=1):
        weights = binning[index - 1]
        nonzero = [(ell_index + 1, weight) for ell_index, weight in enumerate(weights) if weight != 0.0]
        abs_weight_sum = sum(abs(weight) for _, weight in nonzero)
        ell_eff = (
            sum(ell * abs(weight) for ell, weight in nonzero) / abs_weight_sum
            if abs_weight_sum
            else math.nan
        )
        variance = covariance[index - 1][index - 1]
        sigma = math.sqrt(variance) if variance >= 0 else math.nan
        observed = band_row[0]
        rows.append(
            {
                "payload_row_id": f"ACTOBS01_BAND_{index:03d}",
                "band_index": index,
                "ell_support_min": nonzero[0][0] if nonzero else "",
                "ell_support_max": nonzero[-1][0] if nonzero else "",
                "ell_effective_abs_weighted": f"{ell_eff:.12g}" if math.isfinite(ell_eff) else "",
                "binning_nonzero_weight_count": len(nonzero),
                "binning_weight_sum": f"{sum(weights):.12e}",
                "observed_clkk": f"{observed:.18e}",
                "covariance_variance": f"{variance:.18e}",
                "sigma_clkk": f"{sigma:.18e}" if math.isfinite(sigma) else "",
                "absolute_snr": f"{abs(observed) / sigma:.12g}" if sigma and math.isfinite(sigma) else "",
                "observable_role": "ACT_DR6_LENSING_CONVERGENCE_POWER_BANDPOWER",
                "accepted_as_observable_payload": "true",
                "accepted_for_scoring_now": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# ACT DR6 Lensing Observable Payload v01

**Doc class:** observed CMB lensing payload
**Status:** local ACT DR6 lensing baseline bandpower payload extracted
**Canonical parent:** Paper 13 CMB source-data acquisition and scoring path

This artifact extracts a compact observable payload from the locally acquired
ACT DR6 lensing likelihood data package. It binds three local source files:
`clkk_bandpowers_act.txt`, `covmat_act.txt`, and `binning_matrix_act.txt`.

Summary:

```text
source_files_expected={summary["source_files_expected"]}
source_files_present={summary["source_files_present"]}
source_files_hash_bound={summary["source_files_hash_bound"]}
bandpower_rows={summary["bandpower_rows"]}
covariance_shape={summary["covariance_rows"]}x{summary["covariance_columns"]}
binning_matrix_shape={summary["binning_matrix_rows"]}x{summary["binning_matrix_columns"]}
shape_consistent={summary["shape_consistent"]}
observable_payload_rows={summary["observable_payload_rows"]}
accepted_observable_payload_rows={summary["accepted_observable_payload_rows"]}
accepted_for_scoring_rows=0
```

## Claim Boundary

This is an observed-lensing payload only. It does not construct a Tau-side
prediction, does not run the ACT likelihood, does not compute a score, and does
not decide whether a dark-sector or no-dark-sector Tau Core route is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    bandpowers = numeric_rows(SOURCE_FILES["act_dr6_lensing_bandpowers"])
    covariance = numeric_rows(SOURCE_FILES["act_dr6_lensing_covariance"])
    binning = numeric_rows(SOURCE_FILES["act_dr6_lensing_binning_matrix"])

    cov_cols = sorted({len(row) for row in covariance})
    bin_cols = sorted({len(row) for row in binning})
    shape_consistent = (
        len(bandpowers) > 0
        and len(covariance) == len(bandpowers)
        and cov_cols == [len(bandpowers)]
        and len(binning) == len(bandpowers)
        and len(bin_cols) == 1
    )

    audit = source_audit_rows()
    payload = payload_rows(bandpowers, covariance, binning, shape_consistent)
    summary = {
        "summary_id": "CMB_ACT_DR6_LENSING_OBSERVABLE_PAYLOAD_V01",
        "source_files_expected": len(SOURCE_FILES),
        "source_files_present": sum(path.exists() for path in SOURCE_FILES.values()),
        "source_files_hash_bound": sum(bool(row["sha256"]) for row in audit),
        "bandpower_rows": len(bandpowers),
        "covariance_rows": len(covariance),
        "covariance_columns": cov_cols[0] if len(cov_cols) == 1 else 0,
        "binning_matrix_rows": len(binning),
        "binning_matrix_columns": bin_cols[0] if len(bin_cols) == 1 else 0,
        "shape_consistent": str(shape_consistent).lower(),
        "observable_payload_rows": len(payload),
        "accepted_observable_payload_rows": sum(row["accepted_as_observable_payload"] == "true" for row in payload),
        "accepted_for_scoring_rows": 0,
        "tau_prediction_rows": 0,
        "likelihood_adapter_rows": 0,
        "score_rows": 0,
        "overall_status": (
            "OBSERVED_ACT_DR6_LENSING_PAYLOAD_EXTRACTED_SCORING_STILL_BLOCKED"
            if payload
            else "ACT_DR6_LENSING_PAYLOAD_NOT_EXTRACTED_SCORING_BLOCKED"
        ),
        "next_required_artifact": "build_tau_side_lensing_response_and_likelihood_adapter",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(DERIVED / f"{PREFIX}.csv", payload, PAYLOAD_FIELDS)
    write_csv(DERIVED / f"{PREFIX}_source_audit.csv", audit, SOURCE_AUDIT_FIELDS)
    write_csv(DERIVED / f"{PREFIX}_summary.csv", [summary], SUMMARY_FIELDS)
    write_doc(summary)
    print(
        ",".join(
            str(summary[field])
            for field in [
                "summary_id",
                "source_files_present",
                "source_files_hash_bound",
                "bandpower_rows",
                "covariance_rows",
                "covariance_columns",
                "binning_matrix_rows",
                "binning_matrix_columns",
                "observable_payload_rows",
                "accepted_for_scoring_rows",
                "overall_status",
            ]
        )
    )


if __name__ == "__main__":
    main()
