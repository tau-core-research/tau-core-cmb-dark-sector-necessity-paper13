#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_scoring_input_fulfillment_plan_v01_plan_only_no_score_no_likelihood_no_verdict"

FIELDS = [
    "fulfillment_row_id",
    "priority_rank",
    "cmb_role",
    "blocked_gate_decision",
    "fulfillment_action",
    "acceptance_criterion",
    "required_artifact_to_build",
    "stop_rule",
    "completed_in_v01",
    "score_entry_allowed_after_completion",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "fulfillment_rows_declared",
    "ranked_rows",
    "completed_rows",
    "pending_rows",
    "hard_failures_triggered",
    "score_entry_allowed_rows",
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

PLAN = {
    "acoustic_peak_phase_and_height": (
        "1",
        "define a common endpoint-blind Phi_tau_eff source handoff before acoustic phase/height scoring",
        "Phi_tau_eff convention, normalization, timing/sign, and coupling role are declared without fitting CMB residuals",
        "tau_cmb_effective_potential_source_handoff_v01",
        "if no lawful pre-recombination potential-like source can be supplied, mark the acoustic role FAIL",
    ),
    "omega_c_h2_density_inference": (
        "2",
        "derive endpoint-blind rho_tau_eff and A_tau under the selected source handoff",
        "A_tau is derived, dimensionally checked, provenance-clean, and comparable to the density role",
        "tau_cmb_density_amplitude_fulfillment_v01",
        "if no endpoint-blind density amplitude can be derived, mark the density role FAIL",
    ),
    "growth_seed_and_transfer_consistency": (
        "3",
        "derive or explicitly fail the Transfer_tau operator connecting CMB-era response to later readout",
        "domain, codomain, time/scale convention, normalization, and operator rule are supplied",
        "tau_cmb_transfer_operator_fulfillment_v01",
        "if no lawful transfer operator can be supplied, mark the growth-transfer role FAIL",
    ),
    "cmb_lensing_potential": (
        "4",
        "evaluate the lensing reduced response using the source handoff and transfer operator",
        "projection convention and amplitude/shape response are supplied without contradicting density or acoustic roles",
        "tau_cmb_lensing_response_fulfillment_v01",
        "if source/transfer predicts incompatible lensing tendency, mark the lensing role FAIL",
    ),
    "damping_tail_and_radiation_guard": (
        "5",
        "derive Delta_N_eff_tau and evaluate the selected damping-tail bound",
        "Delta_N_eff_tau and Delta_N_eff_bound share a convention and the inequality is evaluated",
        "tau_cmb_radiation_bound_fulfillment_v01",
        "if the Tau contribution necessarily exceeds the selected bound, mark the radiation guard FAIL",
    ),
    "known_limit_or_explicit_failure": (
        "6",
        "update all known-limit decisions after the role fulfillment artifacts exist",
        "every CMB role has REPRODUCE, APPROXIMATE, or FAIL evidence before any aggregate score",
        "tau_cmb_known_limit_resolution_v01",
        "if any role remains unresolved, keep aggregate scoring blocked",
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


def fulfillment_rows() -> list[dict[str, str]]:
    gate_rows = read_csv(DERIVED / "tau_cmb_scoring_execution_gate_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(gate_rows, start=1):
        rank, action, criterion, artifact, stop_rule = PLAN[row["cmb_role"]]
        rows.append(
            {
                "fulfillment_row_id": f"TCMBSIFP01_{index:03d}",
                "priority_rank": rank,
                "cmb_role": row["cmb_role"],
                "blocked_gate_decision": row["execution_gate_decision"],
                "fulfillment_action": action,
                "acceptance_criterion": criterion,
                "required_artifact_to_build": artifact,
                "stop_rule": stop_rule,
                "completed_in_v01": "false",
                "score_entry_allowed_after_completion": "true",
                "hard_failure_triggered": row["hard_failure_triggered"],
                "blocks_no_dark_claim": row["blocks_no_dark_claim"],
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: int(row["priority_rank"]))


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_SCORING_INPUT_FULFILLMENT_PLAN_V01",
            "fulfillment_rows_declared": len(rows),
            "ranked_rows": len({row["priority_rank"] for row in rows}),
            "completed_rows": sum(row["completed_in_v01"] == "true" for row in rows),
            "pending_rows": sum(row["completed_in_v01"] == "false" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "score_entry_allowed_rows": 0,
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_INPUT_FULFILLMENT_PLAN_DECLARED_NO_INPUTS_COMPLETED",
            "next_required_artifact": "tau_cmb_effective_potential_source_handoff_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_scoring_input_fulfillment_plan_v01.md").write_text(
        """# Tau CMB Scoring Input Fulfillment Plan v01

**Doc class:** scoring-input fulfillment plan
**Status:** plan declared; no input completed, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scoring_input_fulfillment_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_scoring_input_fulfillment_plan_v01.csv
data/derived/tau_cmb_scoring_input_fulfillment_plan_summary_v01.csv
```

This artifact converts the blocked scoring execution gate into a ranked
fulfillment plan. It does not complete any scoring input and does not compute a
score.

The first required artifact is:

```text
tau_cmb_effective_potential_source_handoff_v01
```

because acoustic and lensing scoring both depend on a common endpoint-blind
Tau effective-potential handoff. In v01:

```text
completed_rows = 0
pending_rows = 6
```

## Claim Boundary

This artifact is a fulfillment plan only. It computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = fulfillment_rows()
    write_csv(DERIVED / "tau_cmb_scoring_input_fulfillment_plan_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_scoring_input_fulfillment_plan_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_SCORING_INPUT_FULFILLMENT_PLAN_V01_BUILT")


if __name__ == "__main__":
    main()
