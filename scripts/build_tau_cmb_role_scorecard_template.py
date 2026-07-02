#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_role_scorecard_template_v01_template_only_no_scores_no_likelihood_no_verdict"

FIELDS = [
    "scorecard_row_id",
    "rubric_row_id",
    "cmb_role",
    "tau_object_to_score",
    "score_status",
    "assigned_score",
    "score_evidence_pointer",
    "blocking_reason",
    "minimum_unblock_artifact",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "scorecard_rows_declared",
    "scores_computed",
    "not_computed_rows",
    "hard_failures_triggered",
    "blocked_rows",
    "no_dark_blockers",
    "cmb_likelihood_available",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

BLOCKERS = {
    "acoustic_peak_phase_and_height": (
        "potential handoff and acoustic benchmark not supplied",
        "tau_cmb_acoustic_role_reduced_benchmark_v01",
    ),
    "omega_c_h2_density_inference": (
        "A_tau derivation and endpoint-blind density mapping not supplied",
        "tau_cmb_density_amplitude_derivation_v01",
    ),
    "cmb_lensing_potential": (
        "lensing transfer prediction not supplied",
        "tau_cmb_lensing_transfer_benchmark_v01",
    ),
    "damping_tail_and_radiation_guard": (
        "Delta_N_eff_tau bound comparison not computed",
        "tau_cmb_radiation_guard_bound_check_v01",
    ),
    "growth_seed_and_transfer_consistency": (
        "transfer kernel and growth benchmark not supplied",
        "tau_cmb_growth_transfer_kernel_v01",
    ),
    "known_limit_or_explicit_failure": (
        "LCDM role limit/failure map not supplied",
        "tau_cmb_known_limit_failure_map_v01",
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


def scorecard_rows() -> list[dict[str, str]]:
    rubric_rows = read_csv(DERIVED / "tau_cmb_lcdm_role_scoring_rubric_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(rubric_rows, start=1):
        blocking_reason, unblock_artifact = BLOCKERS[row["cmb_role"]]
        rows.append(
            {
                "scorecard_row_id": f"TCMBRST01_{index:03d}",
                "rubric_row_id": row["rubric_row_id"],
                "cmb_role": row["cmb_role"],
                "tau_object_to_score": row["tau_object_to_score"],
                "score_status": "NOT_COMPUTED_INPUT_BLOCKED",
                "assigned_score": "NA",
                "score_evidence_pointer": "NA",
                "blocking_reason": blocking_reason,
                "minimum_unblock_artifact": unblock_artifact,
                "hard_failure_triggered": "false",
                "blocks_no_dark_claim": row["blocks_no_dark_claim"],
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_ROLE_SCORECARD_TEMPLATE_V01",
            "scorecard_rows_declared": len(rows),
            "scores_computed": 0,
            "not_computed_rows": sum(row["score_status"] == "NOT_COMPUTED_INPUT_BLOCKED" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "blocked_rows": sum(row["score_status"].endswith("_BLOCKED") for row in rows),
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ROLE_SCORECARD_TEMPLATE_DECLARED_ALL_SCORES_BLOCKED",
            "next_required_artifact": "tau_cmb_score_input_unblock_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_role_scorecard_template_v01.md").write_text(
        """# Tau CMB Role Scorecard Template v01

**Doc class:** scorecard template
**Status:** template declared; all scores blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_role_scorecard_template.py
```

Derived outputs:

```text
data/derived/tau_cmb_role_scorecard_template_v01.csv
data/derived/tau_cmb_role_scorecard_template_summary_v01.csv
```

This artifact converts the LCDM-role scoring rubric into the empty scorecard
that a future CMB scoring run must fill. It deliberately computes no scores.
Every row is marked:

```text
NOT_COMPUTED_INPUT_BLOCKED
```

The template also names the minimum artifact needed to unblock each role:

```text
acoustic benchmark
density-amplitude derivation
lensing-transfer benchmark
radiation-guard bound check
growth-transfer kernel
known-limit/failure map
```

This is the first place where Paper 13 has the shape of an actual scorecard,
but it remains a blocked template rather than a result.

## Claim Boundary

This artifact is a scorecard template only. It computes no scores, triggers no
hard failure, provides no CMB likelihood, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = scorecard_rows()
    write_csv(DERIVED / "tau_cmb_role_scorecard_template_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_role_scorecard_template_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_ROLE_SCORECARD_TEMPLATE_V01_BUILT")


if __name__ == "__main__":
    main()
