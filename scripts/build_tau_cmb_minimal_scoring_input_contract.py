#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_minimal_scoring_input_contract_v01_contract_only_no_score_no_likelihood_no_verdict"

FIELDS = [
    "contract_row_id",
    "cmb_role",
    "required_scoring_input",
    "required_source_artifact",
    "contract_requirement",
    "current_contract_status",
    "missing_condition",
    "score_entry_allowed",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "contract_rows_declared",
    "satisfied_rows",
    "unsatisfied_rows",
    "score_entry_allowed_rows",
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

CONTRACTS = {
    "acoustic_peak_phase_and_height": (
        "acoustic-ready Phi_tau_eff, A_tau, source timing/sign, and baryon-loading coupling",
        "tau_cmb_acoustic_reduced_evaluation_v01",
        "provide endpoint-blind source and reduced oscillator inputs sufficient for acoustic phase/height scoring",
        "Phi_tau_eff, A_tau, timing/sign, and coupling remain missing",
    ),
    "omega_c_h2_density_inference": (
        "endpoint-blind rho_tau_eff and A_tau with Omega_c h^2 comparison convention",
        "tau_cmb_density_amplitude_closure_v01",
        "provide a derived density amplitude and a declared density-role comparison rule",
        "rho_tau_eff, endpoint-blind A_tau, and numerical density comparison remain missing",
    ),
    "cmb_lensing_potential": (
        "lensing-ready Phi_tau_eff, T_tau_CMB, projection convention, and amplitude/shape response",
        "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "provide a transfer-ready potential source and reduced lensing response",
        "potential source, transfer kernel, and amplitude/shape response remain missing",
    ),
    "damping_tail_and_radiation_guard": (
        "Delta_N_eff_tau and selected Delta_N_eff_bound convention",
        "tau_cmb_radiation_guard_evaluation_v01",
        "provide Tau radiation-like contribution and evaluate the damping-tail bound inequality",
        "Delta_N_eff_tau and numerical bound evaluation remain missing",
    ),
    "growth_seed_and_transfer_consistency": (
        "Transfer_tau[X_tau_CMB](k,a) with domain, codomain, time/scale convention, and cross-role check",
        "tau_cmb_growth_transfer_kernel_closure_v01",
        "provide a lawful transfer operator or explicitly fail the growth-transfer role",
        "transfer operator and cross-role consistency remain missing",
    ),
    "known_limit_or_explicit_failure": (
        "role-level REPRODUCE, APPROXIMATE, or FAIL decisions for all score rows",
        "tau_cmb_known_limit_decision_update_v01",
        "provide explicit decision evidence for every CMB role before any aggregate score",
        "all known-limit decisions remain unresolved",
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


def contract_rows() -> list[dict[str, str]]:
    blocker_rows = read_csv(DERIVED / "tau_cmb_scorecard_prescore_blocker_summary_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(blocker_rows, start=1):
        required_input, artifact, requirement, missing = CONTRACTS[row["cmb_role"]]
        rows.append(
            {
                "contract_row_id": f"TCMBMSIC01_{index:03d}",
                "cmb_role": row["cmb_role"],
                "required_scoring_input": required_input,
                "required_source_artifact": artifact,
                "contract_requirement": requirement,
                "current_contract_status": "UNSATISFIED_INPUT_MISSING",
                "missing_condition": missing,
                "score_entry_allowed": "false",
                "hard_failure_triggered": row["hard_failure_triggered"],
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
            "summary_id": "TAU_CMB_MINIMAL_SCORING_INPUT_CONTRACT_V01",
            "contract_rows_declared": len(rows),
            "satisfied_rows": sum(row["current_contract_status"].startswith("SATISFIED") for row in rows),
            "unsatisfied_rows": sum(row["current_contract_status"].startswith("UNSATISFIED") for row in rows),
            "score_entry_allowed_rows": sum(row["score_entry_allowed"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "MINIMAL_SCORING_INPUT_CONTRACT_DECLARED_ALL_INPUTS_UNSATISFIED",
            "next_required_artifact": "tau_cmb_scoring_execution_gate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_minimal_scoring_input_contract_v01.md").write_text(
        """# Tau CMB Minimal Scoring Input Contract v01

**Doc class:** minimal scoring input contract
**Status:** contract declared; all scoring inputs unsatisfied, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_minimal_scoring_input_contract.py
```

Derived outputs:

```text
data/derived/tau_cmb_minimal_scoring_input_contract_v01.csv
data/derived/tau_cmb_minimal_scoring_input_contract_summary_v01.csv
```

This artifact declares the minimum inputs required before the CMB scorecard is
allowed to run. It does not provide those inputs and does not compute scores.

Every contract row remains:

```text
UNSATISFIED_INPUT_MISSING
```

Therefore:

```text
score_entry_allowed_rows = 0
```

The contract is useful because it turns the current blockers into explicit
entry conditions for future scoring.

## Claim Boundary

This artifact is a scoring-input contract only. It computes no score, supplies
no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = contract_rows()
    write_csv(DERIVED / "tau_cmb_minimal_scoring_input_contract_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_minimal_scoring_input_contract_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_MINIMAL_SCORING_INPUT_CONTRACT_V01_BUILT")


if __name__ == "__main__":
    main()
