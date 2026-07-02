#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
SCORE_READY = ROOT / "data/score_ready_input"

CONTROLS = DERIVED / "cmb_act_dr6_lensing_tau_shape_response_controls_v01.csv"
SCOREBOARD = DERIVED / "cmb_act_dr6_lensing_tau_shape_response_controls_v01_scoreboard.csv"
CONTROL_SUMMARY = DERIVED / "cmb_act_dr6_lensing_tau_shape_response_controls_v01_summary.json"
ADAPTER_VECTOR = DERIVED / "cmb_act_dr6_lensing_observed_score_adapter_v01_vector.csv"

PREFIX = "cmb_act_dr6_lensing_tau_nonzero_response_candidate_packet_v01"
VECTOR_OUT = SCORE_READY / "act_dr6_lensing_tau_nonzero_shape_candidate_vector_v01.csv"
CLAIM_BOUNDARY = (
    "cmb_act_dr6_lensing_tau_nonzero_response_candidate_packet_v01_best_screened_control_as_candidate_"
    "requires_tau_side_derivation_not_physical_prediction_no_dark_sector_verdict"
)

VECTOR_FIELDS = [
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

OBLIGATION_FIELDS = [
    "obligation_id",
    "requirement",
    "current_status",
    "acceptance_test",
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


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# ACT DR6 Lensing Tau Nonzero Response Candidate Packet v01

**Doc class:** nonzero response candidate packet
**Status:** best screened shape-control materialized as a candidate, not promoted to physical prediction
**Canonical parent:** Paper 13 ACT DR6 lensing scoring route

This artifact materializes the best currently screened nonzero Tau Core-style
lensing response control as a separate candidate vector:

```text
{summary["candidate_vector_path"]}
```

The candidate is selected from the locked shape-screening artifact, not derived
from a completed Tau-side field equation. It is therefore a diagnostic candidate
packet only. It can guide the next derivation target, but it cannot by itself
validate Tau Core or decide dark-sector necessity.

Summary:

```text
candidate_id={summary["candidate_id"]}
candidate_rows={summary["candidate_rows"]}
chi2_tau={summary["chi2_tau"]}
chi2_per_naive_dof={summary["chi2_per_naive_dof"]}
delta_chi2_vs_null={summary["delta_chi2_vs_null"]}
fractional_chi2_improvement_vs_null={summary["fractional_chi2_improvement_vs_null"]}
obligations_total={summary["obligations_total"]}
obligations_open={summary["obligations_open"]}
```

## Claim Boundary

This is not a fitted physical Tau response and not an ACT likelihood result.
The candidate must be derived or rejected from the Tau side before any stronger
physical claim is allowed.
""",
        encoding="utf-8",
    )


def main() -> None:
    summary_in = json.loads(CONTROL_SUMMARY.read_text())
    best_candidate = summary_in["best_candidate_id"]
    controls = [row for row in read_csv(CONTROLS) if row["candidate_id"] == best_candidate]
    scoreboard = read_csv(SCOREBOARD)
    best_score = next(row for row in scoreboard if row["candidate_id"] == best_candidate)
    adapter_by_band = {row["band_index"]: row for row in read_csv(ADAPTER_VECTOR)}

    vector_rows: list[dict[str, object]] = []
    for row in controls:
        vector_rows.append(
            {
                "band_index": row["band_index"],
                "ell_support_min": adapter_by_band[row["band_index"]]["ell_support_min"],
                "ell_support_max": adapter_by_band[row["band_index"]]["ell_support_max"],
                "ell_effective_abs_weighted": row["ell_effective_abs_weighted"],
                "tau_predicted_clkk": row["tau_predicted_clkk"],
                "tau_prediction_source_id": "tau_core_nonzero_shape_candidate_from_screening_v01",
                "tau_derivation_artifact": "pending_tau_side_derivation_or_rejection",
                "endpoint_blind_policy": "endpoint_blind_screening_candidate_not_endpoint_fit",
                "normalization_convention": row["normalization_convention"],
                "readout_basis": row["readout_basis"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VECTOR_OUT, vector_rows, VECTOR_FIELDS)

    obligations = [
        {
            "obligation_id": "NZRESP_OBL_001",
            "requirement": "derive analytic shape parameters ell_c_rise_fall_from_tau_side_morphology",
            "current_status": "open",
            "acceptance_test": "parameters_obtained_without_act_endpoint_fit_and_reproduce_candidate_shape_family",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "obligation_id": "NZRESP_OBL_002",
            "requirement": "derive_or_bound_amplitude_from_tau_side_normalization",
            "current_status": "open",
            "acceptance_test": "amplitude_not_selected_by_act_endpoint_minimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "obligation_id": "NZRESP_OBL_003",
            "requirement": "prove_known_limit_zero_response_recovery_when_tau_source_is_absent",
            "current_status": "open",
            "acceptance_test": "candidate_operator_has_documented_null_limit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "obligation_id": "NZRESP_OBL_004",
            "requirement": "test_same_tau_side_candidate_on_independent_readout_or_holdout",
            "current_status": "open",
            "acceptance_test": "no_single_endpoint_only_promotion",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    obligation_path = DERIVED / f"{PREFIX}_obligations.csv"
    write_csv(obligation_path, obligations, OBLIGATION_FIELDS)

    summary = {
        "summary_id": "CMB_ACT_DR6_LENSING_TAU_NONZERO_RESPONSE_CANDIDATE_PACKET_V01",
        "source_controls_path": str(CONTROLS.relative_to(ROOT)),
        "source_controls_sha256": sha256(CONTROLS),
        "source_scoreboard_path": str(SCOREBOARD.relative_to(ROOT)),
        "source_scoreboard_sha256": sha256(SCOREBOARD),
        "adapter_vector_path": str(ADAPTER_VECTOR.relative_to(ROOT)),
        "adapter_vector_sha256": sha256(ADAPTER_VECTOR),
        "candidate_vector_path": str(VECTOR_OUT.relative_to(ROOT)),
        "candidate_vector_sha256": sha256(VECTOR_OUT),
        "obligations_path": str(obligation_path.relative_to(ROOT)),
        "obligations_sha256": sha256(obligation_path),
        "candidate_id": best_candidate,
        "candidate_rows": len(vector_rows),
        "chi2_tau": float(best_score["chi2_tau"]),
        "chi2_per_naive_dof": float(best_score["chi2_per_naive_dof"]),
        "delta_chi2_vs_null": float(best_score["delta_chi2_vs_null"]),
        "fractional_chi2_improvement_vs_null": float(best_score["fractional_chi2_improvement_vs_null"]),
        "obligations_total": len(obligations),
        "obligations_open": sum(row["current_status"] == "open" for row in obligations),
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "tau_side_derivation_or_rejection_of_nonzero_lensing_response_candidate",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                str(summary["candidate_rows"]),
                f"{summary['chi2_tau']:.12g}",
                f"{summary['delta_chi2_vs_null']:.12g}",
                str(summary["obligations_open"]),
            ]
        )
    )


if __name__ == "__main__":
    main()
