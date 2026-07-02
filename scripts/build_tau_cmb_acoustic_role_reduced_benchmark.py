#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_acoustic_role_reduced_benchmark_v01_benchmark_only_no_fit_no_likelihood_no_verdict"

FIELDS = [
    "benchmark_row_id",
    "benchmark_component",
    "observable_role",
    "tau_quantity_to_test",
    "reduced_benchmark_condition",
    "current_status",
    "required_input",
    "hard_failure_if",
    "scorecard_effect",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "benchmark_rows_declared",
    "evaluated_rows",
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


def benchmark_rows() -> list[dict[str, str]]:
    rows = [
        {
            "benchmark_component": "potential_source_presence",
            "observable_role": "pre-recombination gravitational driving source",
            "tau_quantity_to_test": "Phi_tau_eff(a,k)",
            "reduced_benchmark_condition": "Phi_tau_eff must be a defined pre-recombination potential-like source under a stated convention",
            "required_input": "metric handoff convention and effective potential definition",
            "hard_failure_if": "no potential-like Tau source can be supplied before recombination",
            "scorecard_effect": "keeps acoustic score blocked until potential handoff is supplied",
        },
        {
            "benchmark_component": "acoustic_phase_support",
            "observable_role": "acoustic peak phase support",
            "tau_quantity_to_test": "Phi_tau_eff(a,k) with baryon-photon acoustic response",
            "reduced_benchmark_condition": "source timing and sign must not shift the acoustic extrema into a wrong phase family",
            "required_input": "reduced acoustic oscillator convention and source-time dependence",
            "hard_failure_if": "Tau source drives the acoustic oscillator with incompatible phase behavior",
            "scorecard_effect": "can later support score 1 or 2 for acoustic phase only after evaluation",
        },
        {
            "benchmark_component": "relative_peak_height_support",
            "observable_role": "relative acoustic peak-height support",
            "tau_quantity_to_test": "A_tau(a,k) and Phi_tau_eff(a,k)",
            "reduced_benchmark_condition": "density amplitude and potential response must support peak-height modulation in the standard role direction",
            "required_input": "A_tau derivation, potential normalization, and reduced peak-height benchmark",
            "hard_failure_if": "Tau response cannot produce the required gravitational modulation of peak heights",
            "scorecard_effect": "links density-amplitude row to acoustic scoring",
        },
        {
            "benchmark_component": "baryon_loading_compatibility",
            "observable_role": "baryon-photon loading compatibility",
            "tau_quantity_to_test": "Phi_tau_eff(a,k) coupled to baryon-photon response",
            "reduced_benchmark_condition": "Tau effective source must not erase the baryon-loading odd/even peak role",
            "required_input": "baryon-loading convention and source-coupling sign",
            "hard_failure_if": "Tau source destroys the known baryon-loading role instead of complementing it",
            "scorecard_effect": "prevents acoustic score promotion from a density slot alone",
        },
        {
            "benchmark_component": "scale_horizon_convention",
            "observable_role": "sound-horizon and scale convention",
            "tau_quantity_to_test": "k, a, sound-horizon convention, and Phi_tau_eff(a,k)",
            "reduced_benchmark_condition": "all phase and peak-height checks must use a declared k/a/sound-horizon convention",
            "required_input": "scale convention and recombination-era reference epoch",
            "hard_failure_if": "acoustic comparison is convention-free or mixes incompatible scale definitions",
            "scorecard_effect": "guards against false acoustic matches from inconsistent units/conventions",
        },
        {
            "benchmark_component": "explicit_failure_branch",
            "observable_role": "known-limit failure discipline",
            "tau_quantity_to_test": "acoustic_peak_phase_and_height decision state",
            "reduced_benchmark_condition": "if any required acoustic role cannot be supplied, the row must move to FAIL rather than remain ambiguous",
            "required_input": "known-limit/failure map update after benchmark evaluation",
            "hard_failure_if": "failure is hidden as an unevaluated residual or unconstrained fit parameter",
            "scorecard_effect": "prepares acoustic row for reproduce/approximate/fail assignment",
        },
    ]
    return [
        {
            "benchmark_row_id": f"TCMBARB01_{index:03d}",
            "current_status": "DECLARED_NOT_EVALUATED",
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
            "summary_id": "TAU_CMB_ACOUSTIC_ROLE_REDUCED_BENCHMARK_V01",
            "benchmark_rows_declared": len(rows),
            "evaluated_rows": sum(row["current_status"] != "DECLARED_NOT_EVALUATED" for row in rows),
            "hard_failures_triggered": 0,
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_REDUCED_BENCHMARK_DECLARED_NOT_EVALUATED",
            "next_required_artifact": "tau_cmb_lensing_transfer_benchmark_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_acoustic_role_reduced_benchmark_v01.md").write_text(
        """# Tau CMB Acoustic Role Reduced Benchmark v01

**Doc class:** reduced acoustic benchmark
**Status:** benchmark declared; no evaluation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_acoustic_role_reduced_benchmark.py
```

Derived outputs:

```text
data/derived/tau_cmb_acoustic_role_reduced_benchmark_v01.csv
data/derived/tau_cmb_acoustic_role_reduced_benchmark_summary_v01.csv
```

This artifact declares the reduced acoustic checks that must be evaluated
before a full CMB likelihood is worth attempting:

```text
potential source presence
acoustic phase support
relative peak-height support
baryon-loading compatibility
scale / sound-horizon convention
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_EVALUATED
```

The benchmark does not solve the photon-baryon Boltzmann system. It only states
what a Tau effective potential would have to preserve or reproduce at reduced
role level before the acoustic scorecard row can be promoted.

## Claim Boundary

This artifact declares reduced acoustic benchmark conditions only. It evaluates
no spectrum, computes no score, supplies no CMB likelihood, declares no acoustic
success or failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = benchmark_rows()
    write_csv(DERIVED / "tau_cmb_acoustic_role_reduced_benchmark_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_role_reduced_benchmark_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_ACOUSTIC_ROLE_REDUCED_BENCHMARK_V01_BUILT")


if __name__ == "__main__":
    main()
