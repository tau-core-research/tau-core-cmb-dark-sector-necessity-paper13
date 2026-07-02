#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_known_limit_decision_update_v01_no_role_resolved_no_score_no_likelihood_no_verdict"

FIELDS = [
    "decision_row_id",
    "cmb_role",
    "prior_decision_state",
    "updated_decision_state",
    "evidence_artifact",
    "decision_reason",
    "hard_failure_triggered",
    "score_ready",
    "next_required_input",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "decision_rows_declared",
    "resolved_rows",
    "unresolved_rows",
    "failures_declared",
    "reproductions_declared",
    "approximations_declared",
    "hard_failures_triggered",
    "score_ready_rows",
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

ROLE_UPDATES = {
    "acoustic_peak_phase_and_height": (
        "tau_cmb_acoustic_reduced_evaluation_v01",
        "reduced acoustic evaluation has no hard failure but lacks Phi_tau_eff, endpoint-blind A_tau, timing/sign, and baryon-loading coupling",
        "derive acoustic-ready Phi_tau_eff, A_tau, source timing/sign, and baryon-loading coupling",
    ),
    "omega_c_h2_density_inference": (
        "tau_cmb_density_amplitude_closure_v01",
        "density closure has a formal dimensionless ratio but lacks rho_tau_eff, endpoint-blind A_tau, and Omega_c h^2 comparison",
        "derive endpoint-blind rho_tau_eff and A_tau, then compare the density role",
    ),
    "cmb_lensing_potential": (
        "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "reduced lensing evaluation has no hard failure but lacks Phi_tau_eff, T_tau_CMB, amplitude/shape response, and cross-readout consistency",
        "derive lensing-ready potential source, transfer kernel, and amplitude/shape response",
    ),
    "damping_tail_and_radiation_guard": (
        "tau_cmb_radiation_guard_evaluation_v01",
        "radiation guard evaluation closes only the bound-convention guard and lacks Delta_N_eff_tau and numerical inequality evaluation",
        "derive Delta_N_eff_tau and evaluate the selected damping-tail/Neff bound",
    ),
    "growth_seed_and_transfer_consistency": (
        "tau_cmb_growth_transfer_kernel_closure_v01",
        "growth kernel closure narrows formal domain/codomain but lacks a Transfer_tau operator and cross-role consistency",
        "derive Transfer_tau[X_tau_CMB](k,a) or explicitly fail the growth-transfer role",
    ),
    "known_limit_or_explicit_failure": (
        "all v01 closure/evaluation artifacts",
        "all role rows remain unresolved because no reproduce, approximate, or fail evidence threshold is met",
        "promote only after each role has explicit reproduce, approximate, or fail evidence",
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


def decision_rows() -> list[dict[str, str]]:
    known_limit_rows = read_csv(DERIVED / "tau_cmb_known_limit_failure_map_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(known_limit_rows, start=1):
        evidence_artifact, reason, next_input = ROLE_UPDATES[row["cmb_role"]]
        rows.append(
            {
                "decision_row_id": f"TCMBKLDU01_{index:03d}",
                "cmb_role": row["cmb_role"],
                "prior_decision_state": row["current_decision_state"],
                "updated_decision_state": "UNRESOLVED_EVIDENCE_INSUFFICIENT",
                "evidence_artifact": evidence_artifact,
                "decision_reason": reason,
                "hard_failure_triggered": "false",
                "score_ready": "false",
                "next_required_input": next_input,
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
            "summary_id": "TAU_CMB_KNOWN_LIMIT_DECISION_UPDATE_V01",
            "decision_rows_declared": len(rows),
            "resolved_rows": sum(
                row["updated_decision_state"] in {"REPRODUCE", "APPROXIMATE", "FAIL"} for row in rows
            ),
            "unresolved_rows": sum(row["updated_decision_state"].startswith("UNRESOLVED") for row in rows),
            "failures_declared": sum(row["updated_decision_state"] == "FAIL" for row in rows),
            "reproductions_declared": sum(row["updated_decision_state"] == "REPRODUCE" for row in rows),
            "approximations_declared": sum(row["updated_decision_state"] == "APPROXIMATE" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "score_ready_rows": sum(row["score_ready"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "KNOWN_LIMIT_DECISION_UPDATE_ALL_ROLES_UNRESOLVED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_scorecard_prescore_blocker_summary_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_known_limit_decision_update_v01.md").write_text(
        """# Tau CMB Known-Limit Decision Update v01

**Doc class:** known-limit decision update
**Status:** no role resolved; no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_known_limit_decision_update.py
```

Derived outputs:

```text
data/derived/tau_cmb_known_limit_decision_update_v01.csv
data/derived/tau_cmb_known_limit_decision_update_summary_v01.csv
```

This artifact updates the known-limit decision map after the focused v01
closure/evaluation gates:

```text
density amplitude closure
acoustic reduced evaluation
lensing-transfer reduced evaluation
growth-transfer kernel closure
radiation guard evaluation
```

No role is promoted to `REPRODUCE`, `APPROXIMATE`, or `FAIL`. This is deliberate:
the focused gates triggered no hard failures, but they also did not provide the
source, operator, amplitude, bound, or cross-role evidence needed to score a CMB
role.

Every row remains:

```text
UNRESOLVED_EVIDENCE_INSUFFICIENT
```

The known-limit decision update therefore keeps the scorecard blocked.

## Claim Boundary

This artifact updates decision states only. It computes no score, supplies no
CMB likelihood, declares no reproduction, declares no failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = decision_rows()
    write_csv(DERIVED / "tau_cmb_known_limit_decision_update_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_known_limit_decision_update_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_KNOWN_LIMIT_DECISION_UPDATE_V01_BUILT")


if __name__ == "__main__":
    main()
