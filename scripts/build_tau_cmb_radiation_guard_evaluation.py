#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_radiation_guard_evaluation_v01_partial_evaluation_no_bound_score_no_likelihood_no_verdict"

FIELDS = [
    "evaluation_row_id",
    "guard_component",
    "evaluation_result",
    "evidence_source",
    "evaluation_statement",
    "remaining_blocker",
    "scorecard_update",
    "can_compute_radiation_score",
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
    "can_compute_radiation_score",
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
            "guard_component": "tau_radiation_like_contribution",
            "evaluation_result": "BLOCKED_TAU_DELTA_NEFF_NOT_DERIVED",
            "evidence_source": "tau_cmb_radiation_guard_bound_check_v01",
            "evaluation_statement": "Delta_N_eff_tau is declared as a dimensionless slot but is not derived from Tau response.",
            "remaining_blocker": "derive Delta_N_eff_tau under the same convention as the external bound",
            "scorecard_update": "radiation score cannot be computed",
        },
        {
            "guard_component": "external_bound_convention",
            "evaluation_result": "CLOSED_REQUIRED_BOUND_CONVENTION_GUARD",
            "evidence_source": "tau_cmb_radiation_guard_bound_check_v01",
            "evaluation_statement": "any guard evaluation must declare the external Neff/damping-tail convention and dataset family before comparison",
            "remaining_blocker": "select concrete numeric bound and provenance before future evaluation",
            "scorecard_update": "formal bound-convention guard is closed, but it does not make the radiation row score-ready",
        },
        {
            "guard_component": "damping_tail_guard",
            "evaluation_result": "BLOCKED_BOUND_INEQUALITY_NOT_EVALUATED",
            "evidence_source": "tau_cmb_radiation_guard_bound_check_v01",
            "evaluation_statement": "the inequality Delta_N_eff_tau <= Delta_N_eff_bound is declared but no numerical left-hand side or bound is evaluated",
            "remaining_blocker": "supply Tau contribution and selected external bound, then evaluate the inequality",
            "scorecard_update": "no pass/fail damping-tail decision is allowed",
        },
        {
            "guard_component": "cross_role_consistency",
            "evaluation_result": "BLOCKED_DEPENDENT_ROLES_STILL_OPEN",
            "evidence_source": "tau_cmb_density_amplitude_closure_v01; tau_cmb_acoustic_reduced_evaluation_v01; tau_cmb_lensing_transfer_reduced_evaluation_v01; tau_cmb_growth_transfer_kernel_closure_v01",
            "evaluation_statement": "density, acoustic, lensing, and growth roles are not score-ready, so the radiation guard cannot be aggregated consistently",
            "remaining_blocker": "close dependent role inputs before cross-role radiation consistency",
            "scorecard_update": "prevents radiation pass from being used as global support",
        },
        {
            "guard_component": "explicit_failure_branch",
            "evaluation_result": "PARTIAL_EVALUATION_FAILURE_BRANCH_READY",
            "evidence_source": "tau_cmb_known_limit_failure_map_v01",
            "evaluation_statement": "the radiation row has an explicit FAIL path if the Tau contribution cannot be defined or exceeds the adopted bound",
            "remaining_blocker": "run the guard or explicitly assign FAIL",
            "scorecard_update": "failure discipline is ready, but no radiation decision is assigned",
        },
    ]
    return [
        {
            "evaluation_row_id": f"TCMBRGE01_{index:03d}",
            "can_compute_radiation_score": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "false",
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
            "summary_id": "TAU_CMB_RADIATION_GUARD_EVALUATION_V01",
            "evaluation_rows_declared": len(rows),
            "closed_rows": sum(row["evaluation_result"].startswith("CLOSED") for row in rows),
            "partial_evaluation_rows": sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows),
            "blocked_rows": sum(row["evaluation_result"].startswith("BLOCKED") for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "can_compute_radiation_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "RADIATION_GUARD_EVALUATION_PARTIAL_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_known_limit_decision_update_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_radiation_guard_evaluation_v01.md").write_text(
        """# Tau CMB Radiation Guard Evaluation v01

**Doc class:** radiation-guard reduced evaluation
**Status:** partial evaluation; radiation score still blocked, no bound score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_radiation_guard_evaluation.py
```

Derived outputs:

```text
data/derived/tau_cmb_radiation_guard_evaluation_v01.csv
data/derived/tau_cmb_radiation_guard_evaluation_summary_v01.csv
```

This artifact evaluates the radiation guard only at reduced protocol level. The
external-bound convention guard is closed as a required precondition.

The physics-bearing guard remains open because no Tau-side contribution is
derived and no numerical inequality is evaluated:

```text
Delta_N_eff_tau <= Delta_N_eff_bound
```

The radiation score therefore remains blocked.

## Claim Boundary

This artifact is a partial reduced evaluation only. It evaluates no numerical
bound, computes no radiation score, supplies no CMB likelihood, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = evaluation_rows()
    write_csv(DERIVED / "tau_cmb_radiation_guard_evaluation_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_radiation_guard_evaluation_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_RADIATION_GUARD_EVALUATION_V01_BUILT")


if __name__ == "__main__":
    main()
