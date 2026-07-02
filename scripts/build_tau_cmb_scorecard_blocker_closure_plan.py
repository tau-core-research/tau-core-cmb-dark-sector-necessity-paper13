#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_scorecard_blocker_closure_plan_v01_plan_only_no_scores_no_likelihood_no_verdict"

FIELDS = [
    "closure_row_id",
    "priority_rank",
    "cmb_role",
    "current_blocker",
    "closure_action",
    "closure_criterion",
    "stop_rule",
    "promotion_rule_after_closure",
    "next_artifact_to_build",
    "can_compute_score_after_closure",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "closure_rows_declared",
    "ranked_rows",
    "immediate_next_artifact",
    "closures_completed",
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

CLOSURE_PLAN = {
    "omega_c_h2_density_inference": (
        1,
        "endpoint-blind A_tau(a,k) derivation missing",
        "derive or explicitly fail A_tau(a,k) from Tau-side source data under the declared density normalization",
        "A_tau is either endpoint-blind and dimensionally valid, or the density row moves to FAIL",
        "do not continue density scoring by fitting CMB residuals",
        "update density scorecard row to scoreable or failed",
        "tau_cmb_density_amplitude_closure_v01",
        "true",
    ),
    "acoustic_peak_phase_and_height": (
        2,
        "reduced acoustic benchmark not evaluated",
        "evaluate potential-source presence, phase support, peak-height support, baryon-loading compatibility, and scale convention",
        "all reduced acoustic rows are evaluated or an explicit acoustic FAIL is recorded",
        "do not open full Boltzmann likelihood until reduced acoustic rows are evaluated",
        "update acoustic scorecard row to scoreable, approximate, or failed",
        "tau_cmb_acoustic_reduced_evaluation_v01",
        "true",
    ),
    "cmb_lensing_potential": (
        3,
        "reduced lensing-transfer benchmark not evaluated",
        "evaluate potential source, transfer kernel presence, projection convention, amplitude/shape support, and cross-readout consistency",
        "all reduced lensing rows are evaluated or an explicit lensing FAIL is recorded",
        "do not claim CMB lensing support from potential-slot existence alone",
        "update lensing scorecard row to scoreable, approximate, or failed",
        "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "true",
    ),
    "growth_seed_and_transfer_consistency": (
        4,
        "growth transfer kernel not specified",
        "supply or explicitly fail domain, codomain, time/scale convention, and operator rule",
        "kernel is specified enough for reduced comparison or the growth row moves to FAIL",
        "do not infer growth transfer from acoustic or lensing scaffolds without an operator rule",
        "update growth scorecard row to scoreable or failed",
        "tau_cmb_growth_transfer_kernel_closure_v01",
        "true",
    ),
    "damping_tail_and_radiation_guard": (
        5,
        "radiation guard bound not evaluated",
        "evaluate Delta_N_eff_tau definition, external bound convention, and damping-tail inequality",
        "guard is passed under a declared convention or the radiation row moves to FAIL",
        "do not ignore radiation guard even though it is not the primary no-dark blocker",
        "update radiation scorecard row to scoreable or failed",
        "tau_cmb_radiation_guard_evaluation_v01",
        "true",
    ),
    "known_limit_or_explicit_failure": (
        6,
        "known-limit decision states unresolved",
        "assign reproduce, approximate, or fail after the evidence rows above are closed",
        "every CMB role has a non-ambiguous decision state or remains blocked with a named missing input",
        "do not assign known-limit outcomes before evidence rows are closed",
        "update known-limit scorecard row and prepare aggregate scorecard",
        "tau_cmb_known_limit_decision_update_v01",
        "true",
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def closure_rows() -> list[dict[str, str]]:
    readiness_rows = read_csv(DERIVED / "tau_cmb_scorecard_readiness_audit_v01.csv")
    rows: list[dict[str, str]] = []
    for row in readiness_rows:
        (
            rank,
            blocker,
            action,
            criterion,
            stop_rule,
            promotion,
            next_artifact,
            can_compute,
        ) = CLOSURE_PLAN[row["cmb_role"]]
        rows.append(
            {
                "closure_row_id": f"TCMBSBCP01_{rank:03d}",
                "priority_rank": str(rank),
                "cmb_role": row["cmb_role"],
                "current_blocker": blocker,
                "closure_action": action,
                "closure_criterion": criterion,
                "stop_rule": stop_rule,
                "promotion_rule_after_closure": promotion,
                "next_artifact_to_build": next_artifact,
                "can_compute_score_after_closure": can_compute,
                "blocks_no_dark_claim": row["blocks_no_dark_claim"],
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda item: int(item["priority_rank"]))


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    immediate_next = rows[0]["next_artifact_to_build"]
    return [
        {
            "summary_id": "TAU_CMB_SCORECARD_BLOCKER_CLOSURE_PLAN_V01",
            "closure_rows_declared": len(rows),
            "ranked_rows": sum(row["priority_rank"] != "" for row in rows),
            "immediate_next_artifact": immediate_next,
            "closures_completed": 0,
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "BLOCKER_CLOSURE_PLAN_DECLARED_NO_CLOSURES_COMPLETED",
            "next_required_artifact": immediate_next,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc(rows: list[dict[str, str]]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    ranked = "\n".join(
        f"{row['priority_rank']}. {row['next_artifact_to_build']} - {row['cmb_role']}" for row in rows
    )
    (DOCS / "tau_cmb_scorecard_blocker_closure_plan_v01.md").write_text(
        f"""# Tau CMB Scorecard Blocker Closure Plan v01

**Doc class:** scorecard blocker closure plan
**Status:** closure plan declared; no closures completed, no scores, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scorecard_blocker_closure_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_scorecard_blocker_closure_plan_v01.csv
data/derived/tau_cmb_scorecard_blocker_closure_plan_summary_v01.csv
```

This artifact turns the readiness audit into a closure plan. The ranked closure
order is:

```text
{ranked}
```

Each row has a closure criterion and a stop rule. The purpose is to prevent the
scorecard from expanding into unrelated proof work before the named blockers
are closed or explicitly failed.

The immediate next artifact is:

```text
{rows[0]['next_artifact_to_build']}
```

## Claim Boundary

This artifact is a closure plan only. It completes no closure, computes no
score, supplies no CMB likelihood, validates no Tau-response source, and permits
no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = closure_rows()
    write_csv(DERIVED / "tau_cmb_scorecard_blocker_closure_plan_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_scorecard_blocker_closure_plan_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc(rows)
    print("PAPER13_TAU_CMB_SCORECARD_BLOCKER_CLOSURE_PLAN_V01_BUILT")


if __name__ == "__main__":
    main()
