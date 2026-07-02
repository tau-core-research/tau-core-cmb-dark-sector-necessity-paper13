#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_acoustic_reduced_evaluation_v01_partial_evaluation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "evaluation_row_id",
    "benchmark_component",
    "evaluation_result",
    "evidence_source",
    "reduced_evaluation_statement",
    "remaining_blocker",
    "scorecard_update",
    "can_compute_acoustic_score",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "evaluation_rows_declared",
    "closed_rows",
    "partial_evaluation_rows",
    "blocked_rows",
    "hard_failures_triggered",
    "can_compute_acoustic_score",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def evaluation_rows() -> list[dict[str, str]]:
    rows = [
        {
            "benchmark_component": "potential_source_presence",
            "evaluation_result": "BLOCKED_POTENTIAL_SOURCE_NOT_DERIVED",
            "evidence_source": "tau_cmb_effective_source_equation_v01",
            "reduced_evaluation_statement": "Phi_tau_eff(a,k) remains a target slot rather than a derived pre-recombination source.",
            "remaining_blocker": "derive metric handoff convention and effective potential definition",
            "scorecard_update": "acoustic score cannot be computed",
        },
        {
            "benchmark_component": "acoustic_phase_support",
            "evaluation_result": "BLOCKED_OSCILLATOR_RESPONSE_NOT_EVALUATED",
            "evidence_source": "tau_cmb_acoustic_role_reduced_benchmark_v01",
            "reduced_evaluation_statement": "no reduced photon-baryon oscillator response has been evaluated for Tau source timing and sign",
            "remaining_blocker": "supply reduced oscillator convention and source-time dependence",
            "scorecard_update": "no reproduce/approximate/fail phase decision is allowed",
        },
        {
            "benchmark_component": "relative_peak_height_support",
            "evaluation_result": "BLOCKED_DENSITY_AMPLITUDE_NOT_AVAILABLE",
            "evidence_source": "tau_cmb_density_amplitude_closure_v01",
            "reduced_evaluation_statement": "A_tau(a,k) is only a formal ratio; endpoint-blind amplitude is not available.",
            "remaining_blocker": "derive endpoint-blind A_tau and potential normalization",
            "scorecard_update": "peak-height support remains unscored",
        },
        {
            "benchmark_component": "baryon_loading_compatibility",
            "evaluation_result": "BLOCKED_COUPLING_SIGN_MISSING",
            "evidence_source": "tau_cmb_acoustic_role_reduced_benchmark_v01",
            "reduced_evaluation_statement": "Tau source coupling sign relative to baryon loading is not specified.",
            "remaining_blocker": "supply source-coupling sign and baryon-loading convention",
            "scorecard_update": "prevents acoustic score promotion from density information alone",
        },
        {
            "benchmark_component": "scale_horizon_convention",
            "evaluation_result": "CLOSED_REQUIRED_CONVENTION_GUARD",
            "evidence_source": "tau_cmb_acoustic_role_reduced_benchmark_v01",
            "reduced_evaluation_statement": "evaluation must use declared k, a, recombination epoch, and sound-horizon conventions before any comparison",
            "remaining_blocker": "concrete numeric convention still required for future evaluation",
            "scorecard_update": "formal guard is closed, but it does not make the acoustic row score-ready",
        },
        {
            "benchmark_component": "explicit_failure_branch",
            "evaluation_result": "PARTIAL_EVALUATION_FAILURE_BRANCH_READY",
            "evidence_source": "tau_cmb_known_limit_failure_map_v01",
            "reduced_evaluation_statement": "the acoustic row has an explicit fail branch if required source, phase, or height checks cannot be supplied",
            "remaining_blocker": "run the reduced checks or explicitly assign FAIL",
            "scorecard_update": "failure discipline is ready, but no acoustic decision is assigned",
        },
    ]
    return [
        {
            "evaluation_row_id": f"TCMBARE01_{index:03d}",
            "can_compute_acoustic_score": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_REDUCED_EVALUATION_V01",
            "evaluation_rows_declared": len(rows),
            "closed_rows": sum(row["evaluation_result"].startswith("CLOSED") for row in rows),
            "partial_evaluation_rows": sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows),
            "blocked_rows": sum(row["evaluation_result"].startswith("BLOCKED") for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "can_compute_acoustic_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_lensing_transfer_reduced_evaluation_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_acoustic_reduced_evaluation_v01.md").write_text(
        """# Tau CMB Acoustic Reduced Evaluation v01

**Doc class:** reduced acoustic evaluation
**Status:** partial evaluation; acoustic score still blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_acoustic_reduced_evaluation.py
```

Derived outputs:

```text
data/derived/tau_cmb_acoustic_reduced_evaluation_v01.csv
data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv
```

This artifact evaluates the declared acoustic benchmark only at reduced protocol
level. It does not solve the photon-baryon Boltzmann system and does not compute
a CMB spectrum.

The formal scale/sound-horizon convention guard is closed as a required
precondition. The failure branch is partially ready. The physics-bearing
acoustic checks remain blocked because the Tau effective potential,
endpoint-blind amplitude, source timing/sign, and baryon-loading coupling are
not yet supplied.

The acoustic score therefore remains blocked.

## Claim Boundary

This artifact is a partial reduced evaluation only. It computes no acoustic
score, supplies no CMB likelihood, declares no acoustic reproduction or failure,
validates no Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = evaluation_rows()
    write_csv(DERIVED / "tau_cmb_acoustic_reduced_evaluation_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_reduced_evaluation_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_ACOUSTIC_REDUCED_EVALUATION_V01_BUILT")


if __name__ == "__main__":
    main()
