#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_score_input_unblock_plan_v01_plan_only_no_scores_no_likelihood_no_verdict"

FIELDS = [
    "unblock_plan_row_id",
    "priority_rank",
    "cmb_role",
    "minimum_unblock_artifact",
    "unblock_goal",
    "why_this_priority",
    "upstream_dependency",
    "expected_scorecard_effect",
    "can_unlock_score_without_likelihood",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "unblock_rows_declared",
    "ranked_rows",
    "immediate_next_artifact",
    "likelihood_required_for_verdict",
    "scores_computed",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

PLAN = {
    "known_limit_or_explicit_failure": (
        1,
        "define reproduce/approximate/fail branches for every standard CMB source role",
        "highest leverage: prevents hidden CDM-role replacement and gives every later score a claim boundary",
        "role scorecard template and LCDM role rubric",
        "unblocks score interpretation and failure-mode assignment across all rows",
        "false",
    ),
    "omega_c_h2_density_inference": (
        2,
        "derive or fail the endpoint-blind A_tau density-amplitude map",
        "smallest formula-bearing source slot and directly tests the density role normally inferred as Omega_c h^2",
        "dimensionless A_tau convention and rho_cdm_ref normalization",
        "can make the density row scoreable at reduced-benchmark level",
        "true",
    ),
    "acoustic_peak_phase_and_height": (
        3,
        "build a reduced acoustic role benchmark for Phi_tau_eff before full Boltzmann insertion",
        "core CMB pressure point: if acoustic phase/height fails, no-dark cosmology is blocked early",
        "effective potential convention and density-amplitude row",
        "can make the acoustic row scoreable at reduced-benchmark level",
        "true",
    ),
    "cmb_lensing_potential": (
        4,
        "define a lensing-transfer benchmark for Phi_tau_eff and T_tau_CMB",
        "independent CMB lensing constrains the same source role through a different readout",
        "effective potential row and transfer-kernel row",
        "can make the lensing row partially scoreable before full likelihood",
        "true",
    ),
    "growth_seed_and_transfer_consistency": (
        5,
        "supply the Tau CMB transfer kernel or explicit transfer failure",
        "needed to connect early source behavior to lensing and later growth roles",
        "Response_tau_CMB codomain and propagation convention",
        "unblocks transfer/growth score and strengthens lensing interpretation",
        "true",
    ),
    "damping_tail_and_radiation_guard": (
        6,
        "compute the Delta_N_eff_tau bound check under an adopted convention",
        "important guardrail, but it is not the main no-dark blocker in the current scorecard",
        "Tau radiation-like contribution and external bound convention",
        "can make the radiation-guard row scoreable",
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


def unblock_rows() -> list[dict[str, str]]:
    scorecard_rows = read_csv(DERIVED / "tau_cmb_role_scorecard_template_v01.csv")
    rows: list[dict[str, str]] = []
    for row in scorecard_rows:
        rank, goal, why, dependency, effect, unlock_without_likelihood = PLAN[row["cmb_role"]]
        rows.append(
            {
                "unblock_plan_row_id": f"TCMBSIUP01_{rank:03d}",
                "priority_rank": str(rank),
                "cmb_role": row["cmb_role"],
                "minimum_unblock_artifact": row["minimum_unblock_artifact"],
                "unblock_goal": goal,
                "why_this_priority": why,
                "upstream_dependency": dependency,
                "expected_scorecard_effect": effect,
                "can_unlock_score_without_likelihood": unlock_without_likelihood,
                "blocks_no_dark_claim": row["blocks_no_dark_claim"],
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda item: int(item["priority_rank"]))


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    immediate_next = rows[0]["minimum_unblock_artifact"]
    return [
        {
            "summary_id": "TAU_CMB_SCORE_INPUT_UNBLOCK_PLAN_V01",
            "unblock_rows_declared": len(rows),
            "ranked_rows": sum(row["priority_rank"] != "" for row in rows),
            "immediate_next_artifact": immediate_next,
            "likelihood_required_for_verdict": "true",
            "scores_computed": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORE_INPUT_UNBLOCK_PLAN_DECLARED_NO_SCORES_COMPUTED",
            "next_required_artifact": immediate_next,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc(rows: list[dict[str, str]]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    ranked = "\n".join(
        f"{row['priority_rank']}. {row['minimum_unblock_artifact']} - {row['cmb_role']}" for row in rows
    )
    (DOCS / "tau_cmb_score_input_unblock_plan_v01.md").write_text(
        f"""# Tau CMB Score Input Unblock Plan v01

**Doc class:** scoring input unblock plan
**Status:** ranked plan declared; no scores computed, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_score_input_unblock_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_score_input_unblock_plan_v01.csv
data/derived/tau_cmb_score_input_unblock_plan_summary_v01.csv
```

This artifact ranks the blocked scorecard inputs. It does not compute CMB
scores. Its purpose is to prevent the project from branching into every
possible missing proof at once.

The ranked unblock order is:

```text
{ranked}
```

The immediate next artifact is therefore:

```text
tau_cmb_known_limit_failure_map_v01
```

This is chosen first because it gives the whole scorecard a disciplined
reproduce/approximate/fail map before the paper attempts detailed numerical
or reduced-benchmark scoring.

## Claim Boundary

This artifact is a plan only. It computes no scores, supplies no CMB likelihood,
validates no Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = unblock_rows()
    write_csv(DERIVED / "tau_cmb_score_input_unblock_plan_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_score_input_unblock_plan_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc(rows)
    print("PAPER13_TAU_CMB_SCORE_INPUT_UNBLOCK_PLAN_V01_BUILT")


if __name__ == "__main__":
    main()
