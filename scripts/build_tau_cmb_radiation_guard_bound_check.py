#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_radiation_guard_bound_check_v01_guard_only_no_bound_eval_no_likelihood_no_verdict"

FIELDS = [
    "guard_row_id",
    "guard_component",
    "role",
    "symbol_or_object",
    "required_check",
    "current_status",
    "dimension_status",
    "hard_failure_if",
    "scorecard_effect",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "guard_rows_declared",
    "evaluated_rows",
    "dimensionless_rows_declared",
    "hard_failures_triggered",
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


def guard_rows() -> list[dict[str, str]]:
    rows = [
        {
            "guard_component": "tau_radiation_like_contribution",
            "role": "Tau radiation-like contribution slot",
            "symbol_or_object": "Delta_N_eff_tau",
            "required_check": "define the Tau contribution using the same effective relativistic-degree convention as the external bound",
            "dimension_status": "DIMENSIONLESS_SLOT_DECLARED_NOT_EVALUATED",
            "hard_failure_if": "Delta_N_eff_tau cannot be defined as a dimensionless quantity under the adopted convention",
            "scorecard_effect": "keeps radiation-guard row blocked until Tau contribution is defined",
        },
        {
            "guard_component": "external_bound_convention",
            "role": "external CMB damping-tail / Neff bound convention",
            "symbol_or_object": "Delta_N_eff_bound",
            "required_check": "declare the external bound convention and dataset family before comparison",
            "dimension_status": "DIMENSIONLESS_BOUND_DECLARED_NOT_SELECTED",
            "hard_failure_if": "bound comparison uses an unstated or incompatible Neff convention",
            "scorecard_effect": "prevents false pass/fail from mismatched bound definitions",
        },
        {
            "guard_component": "damping_tail_guard",
            "role": "damping-tail compatibility guard",
            "symbol_or_object": "Delta_N_eff_tau <= Delta_N_eff_bound",
            "required_check": "evaluate whether the Tau radiation-like contribution stays within the adopted bound",
            "dimension_status": "DIMENSIONLESS_INEQUALITY_DECLARED_NOT_EVALUATED",
            "hard_failure_if": "Tau response necessarily exceeds the damping-tail / Neff bound",
            "scorecard_effect": "can later make the radiation-guard row scoreable",
        },
        {
            "guard_component": "cross_role_consistency",
            "role": "compatibility with density, acoustic, lensing, and growth roles",
            "symbol_or_object": "Delta_N_eff_tau with A_tau, Phi_tau_eff, T_tau_CMB",
            "required_check": "radiation guard must not require assumptions that contradict other CMB role scaffolds",
            "dimension_status": "CONSISTENCY_GATE_DECLARED_NOT_EVALUATED",
            "hard_failure_if": "radiation guard passes only by contradicting density, acoustic, lensing, or growth assumptions",
            "scorecard_effect": "prepares score aggregation without damping-tail inconsistency",
        },
        {
            "guard_component": "explicit_failure_branch",
            "role": "known-limit failure discipline",
            "symbol_or_object": "damping_tail_and_radiation_guard decision state",
            "required_check": "if the guard cannot be defined or violates the bound, move the row to FAIL rather than leave it ambiguous",
            "dimension_status": "FAILURE_BRANCH_DECLARED_NOT_TRIGGERED",
            "hard_failure_if": "radiation-like excess is hidden as an unconstrained residual or omitted guard",
            "scorecard_effect": "prepares radiation row for reproduce/approximate/fail assignment",
        },
    ]
    return [
        {
            "guard_row_id": f"TCMBRGB01_{index:03d}",
            "current_status": "DECLARED_NOT_EVALUATED",
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
            "summary_id": "TAU_CMB_RADIATION_GUARD_BOUND_CHECK_V01",
            "guard_rows_declared": len(rows),
            "evaluated_rows": sum(row["current_status"] != "DECLARED_NOT_EVALUATED" for row in rows),
            "dimensionless_rows_declared": sum("DIMENSIONLESS" in row["dimension_status"] for row in rows),
            "hard_failures_triggered": 0,
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "RADIATION_GUARD_BOUND_CHECK_DECLARED_NOT_EVALUATED",
            "next_required_artifact": "tau_cmb_scorecard_readiness_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_radiation_guard_bound_check_v01.md").write_text(
        """# Tau CMB Radiation Guard Bound Check v01

**Doc class:** radiation-guard bound-check scaffold
**Status:** guard requirements declared; no bound evaluation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_radiation_guard_bound_check.py
```

Derived outputs:

```text
data/derived/tau_cmb_radiation_guard_bound_check_v01.csv
data/derived/tau_cmb_radiation_guard_bound_check_summary_v01.csv
```

This artifact declares what the radiation guard must check:

```text
Delta_N_eff_tau definition
external Delta_N_eff_bound convention
damping-tail inequality
cross-role consistency
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_EVALUATED
```

The artifact does not evaluate a numerical Neff bound and does not compare to
Planck, ACT, or other damping-tail data. It only records the guard that must be
run before the radiation row can be scored.

## Claim Boundary

This artifact declares radiation-guard requirements only. It evaluates no bound,
computes no score, supplies no CMB likelihood, validates no Tau-response source,
and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = guard_rows()
    write_csv(DERIVED / "tau_cmb_radiation_guard_bound_check_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_radiation_guard_bound_check_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_RADIATION_GUARD_BOUND_CHECK_V01_BUILT")


if __name__ == "__main__":
    main()
