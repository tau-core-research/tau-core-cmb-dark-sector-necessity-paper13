#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_lensing_transfer_reduced_evaluation_v01_partial_evaluation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "evaluation_row_id",
    "benchmark_component",
    "evaluation_result",
    "evidence_source",
    "reduced_evaluation_statement",
    "remaining_blocker",
    "scorecard_update",
    "can_compute_lensing_score",
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
    "can_compute_lensing_score",
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
            "benchmark_component": "lensing_potential_source_presence",
            "evaluation_result": "BLOCKED_POTENTIAL_SOURCE_NOT_DERIVED",
            "evidence_source": "tau_cmb_effective_source_equation_v01",
            "reduced_evaluation_statement": "Phi_tau_eff(a,k) remains a target slot rather than a derived lensing-era source.",
            "remaining_blocker": "derive metric handoff convention and effective potential normalization over the lensing range",
            "scorecard_update": "lensing score cannot be computed",
        },
        {
            "benchmark_component": "transfer_kernel_presence",
            "evaluation_result": "BLOCKED_TRANSFER_KERNEL_NOT_SPECIFIED",
            "evidence_source": "tau_cmb_growth_transfer_kernel_v01",
            "reduced_evaluation_statement": "T_tau_CMB(k,a) is not yet a specified transfer operator with domain, codomain, and normalization.",
            "remaining_blocker": "supply lawful Transfer_tau definition and time/scale convention",
            "scorecard_update": "no lensing transfer decision is allowed",
        },
        {
            "benchmark_component": "projection_geometry_convention",
            "evaluation_result": "CLOSED_REQUIRED_PROJECTION_GUARD",
            "evidence_source": "tau_cmb_lensing_transfer_benchmark_v01",
            "reduced_evaluation_statement": "line-of-sight, distance, and projection-kernel conventions are mandatory before amplitude or shape comparison",
            "remaining_blocker": "concrete numeric projection convention still required for future evaluation",
            "scorecard_update": "formal projection guard is closed, but it does not make the lensing row score-ready",
        },
        {
            "benchmark_component": "amplitude_shape_support",
            "evaluation_result": "BLOCKED_AMPLITUDE_SHAPE_NOT_EVALUATED",
            "evidence_source": "tau_cmb_lensing_transfer_benchmark_v01",
            "reduced_evaluation_statement": "no reduced lensing amplitude/shape tendency has been computed from a Tau source and transfer kernel",
            "remaining_blocker": "derive transfer response and compare reduced amplitude/shape direction",
            "scorecard_update": "lensing amplitude/shape support remains unscored",
        },
        {
            "benchmark_component": "cross_readout_consistency",
            "evaluation_result": "BLOCKED_CROSS_READOUT_NOT_AVAILABLE",
            "evidence_source": "tau_cmb_density_amplitude_closure_v01; tau_cmb_acoustic_reduced_evaluation_v01",
            "reduced_evaluation_statement": "density and acoustic roles are still blocked, so lensing consistency cannot be checked",
            "remaining_blocker": "close source, density, acoustic, and transfer conventions before cross-role aggregation",
            "scorecard_update": "prevents lensing score promotion from an isolated projection slot",
        },
        {
            "benchmark_component": "explicit_failure_branch",
            "evaluation_result": "PARTIAL_EVALUATION_FAILURE_BRANCH_READY",
            "evidence_source": "tau_cmb_known_limit_failure_map_v01",
            "reduced_evaluation_statement": "the lensing row has an explicit fail branch if source, transfer, projection, or shape checks cannot be supplied",
            "remaining_blocker": "run the reduced checks or explicitly assign FAIL",
            "scorecard_update": "failure discipline is ready, but no lensing decision is assigned",
        },
    ]
    return [
        {
            "evaluation_row_id": f"TCMBLTRE01_{index:03d}",
            "can_compute_lensing_score": "false",
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
            "summary_id": "TAU_CMB_LENSING_TRANSFER_REDUCED_EVALUATION_V01",
            "evaluation_rows_declared": len(rows),
            "closed_rows": sum(row["evaluation_result"].startswith("CLOSED") for row in rows),
            "partial_evaluation_rows": sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows),
            "blocked_rows": sum(row["evaluation_result"].startswith("BLOCKED") for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "can_compute_lensing_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "LENSING_TRANSFER_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_growth_transfer_kernel_closure_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_lensing_transfer_reduced_evaluation_v01.md").write_text(
        """# Tau CMB Lensing Transfer Reduced Evaluation v01

**Doc class:** reduced lensing-transfer evaluation
**Status:** partial evaluation; lensing score still blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_lensing_transfer_reduced_evaluation.py
```

Derived outputs:

```text
data/derived/tau_cmb_lensing_transfer_reduced_evaluation_v01.csv
data/derived/tau_cmb_lensing_transfer_reduced_evaluation_summary_v01.csv
```

This artifact evaluates the declared lensing-transfer benchmark only at reduced
protocol level. It does not evaluate Planck or ACT lensing data and does not
compute a CMB lensing spectrum.

The formal projection-geometry guard is closed as a required precondition. The
failure branch is partially ready. The physics-bearing checks remain blocked
because the Tau effective potential, transfer kernel, amplitude/shape response,
and cross-readout consistency are not yet supplied.

The lensing score therefore remains blocked.

## Claim Boundary

This artifact is a partial reduced evaluation only. It computes no lensing
score, supplies no CMB likelihood, declares no lensing reproduction or failure,
validates no Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = evaluation_rows()
    write_csv(DERIVED / "tau_cmb_lensing_transfer_reduced_evaluation_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_lensing_transfer_reduced_evaluation_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_LENSING_TRANSFER_REDUCED_EVALUATION_V01_BUILT")


if __name__ == "__main__":
    main()
