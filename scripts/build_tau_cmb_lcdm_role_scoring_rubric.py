#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_lcdm_role_scoring_rubric_v01_rubric_only_no_scores_no_likelihood_no_verdict"

FIELDS = [
    "rubric_row_id",
    "cmb_role",
    "tau_object_to_score",
    "external_constraint_family",
    "minimum_required_evidence",
    "score_0_condition",
    "score_1_condition",
    "score_2_condition",
    "hard_failure_condition",
    "depends_on_source_component",
    "currently_scoreable",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "rubric_rows_declared",
    "score_levels_declared_per_row",
    "currently_scoreable_rows",
    "hard_failure_rules_declared",
    "no_dark_blockers",
    "scores_computed",
    "cmb_likelihood_available",
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


def rubric_rows() -> list[dict[str, str]]:
    rows = [
        {
            "cmb_role": "acoustic_peak_phase_and_height",
            "tau_object_to_score": "Phi_tau_eff(a,k) with baryon-photon acoustic response",
            "external_constraint_family": "Planck acoustic spectrum and ACT extended-model consistency",
            "minimum_required_evidence": "Boltzmann-compatible source insertion or reduced analytic acoustic role check",
            "score_0_condition": "no potential handoff or wrong acoustic phase/height role",
            "score_1_condition": "qualitative role match with incomplete peak-ratio or phase validation",
            "score_2_condition": "quantitative acoustic phase and relative-height compatibility under stated likelihood or benchmark",
            "hard_failure_condition": "cannot supply a pre-recombination gravitational-potential source role",
            "depends_on_source_component": "effective_potential_poisson_slot",
            "currently_scoreable": "false",
            "blocks_no_dark_claim": "true",
        },
        {
            "cmb_role": "omega_c_h2_density_inference",
            "tau_object_to_score": "rho_tau_eff(a,k)",
            "external_constraint_family": "Planck base-parameter matter-density inference",
            "minimum_required_evidence": "dimensionally valid density-like mapping with endpoint-blind amplitude derivation",
            "score_0_condition": "A_tau unavailable, fitted only from residuals, or wrong density dimension",
            "score_1_condition": "dimensionally valid density slot but no quantitative Omega_c h^2 comparison",
            "score_2_condition": "quantitative Omega_c h^2 role replacement or explicit successful approximation",
            "hard_failure_condition": "cannot define a density-like source independent of endpoint residual fitting",
            "depends_on_source_component": "effective_density_source",
            "currently_scoreable": "false",
            "blocks_no_dark_claim": "true",
        },
        {
            "cmb_role": "cmb_lensing_potential",
            "tau_object_to_score": "Phi_tau_eff(a,k) and T_tau_CMB(k,a)",
            "external_constraint_family": "Planck lensing and ACT DR6 lensing",
            "minimum_required_evidence": "lensing-potential transfer prediction or reduced benchmark against CMB lensing amplitude/shape",
            "score_0_condition": "no lensing transfer or incompatible potential response",
            "score_1_condition": "potential slot exists but transfer/lensing amplitude remains unconstrained",
            "score_2_condition": "quantitative lensing-potential compatibility under stated benchmark",
            "hard_failure_condition": "cannot connect early source response to CMB lensing potential",
            "depends_on_source_component": "effective_potential_poisson_slot;transfer_kernel_slot",
            "currently_scoreable": "false",
            "blocks_no_dark_claim": "true",
        },
        {
            "cmb_role": "damping_tail_and_radiation_guard",
            "tau_object_to_score": "Delta_N_eff_tau",
            "external_constraint_family": "Planck and ACT damping-tail/extended-parameter constraints",
            "minimum_required_evidence": "dimensionless radiation-like contribution bound under stated Neff convention",
            "score_0_condition": "radiation-like contribution unbounded or incompatible with damping-tail constraints",
            "score_1_condition": "dimensionless guard declared but no external-bound comparison computed",
            "score_2_condition": "quantitative bound check satisfies the adopted damping-tail/Neff benchmark",
            "hard_failure_condition": "Tau response necessarily overproduces radiation-like damping effects",
            "depends_on_source_component": "radiation_guard_slot",
            "currently_scoreable": "false",
            "blocks_no_dark_claim": "false",
        },
        {
            "cmb_role": "growth_seed_and_transfer_consistency",
            "tau_object_to_score": "T_tau_CMB(k,a)",
            "external_constraint_family": "CMB growth seeds, lensing transfer, and late structure consistency",
            "minimum_required_evidence": "transfer kernel from early response to later perturbation/growth observables",
            "score_0_condition": "no transfer kernel or incompatible scale dependence",
            "score_1_condition": "transfer skeleton exists but no growth/lensing comparison is computed",
            "score_2_condition": "quantitative transfer compatibility across CMB lensing and growth benchmark",
            "hard_failure_condition": "cannot propagate Tau response from CMB epoch to observable growth/lensing roles",
            "depends_on_source_component": "transfer_kernel_slot",
            "currently_scoreable": "false",
            "blocks_no_dark_claim": "true",
        },
        {
            "cmb_role": "known_limit_or_explicit_failure",
            "tau_object_to_score": "LCDM_role_limit_or_failure",
            "external_constraint_family": "standard LambdaCDM role comparison",
            "minimum_required_evidence": "explicit map saying reproduce, approximate, or fail each standard source role",
            "score_0_condition": "no known-limit map or hidden replacement of CDM role by residual fitting",
            "score_1_condition": "partial known-limit map with unresolved roles",
            "score_2_condition": "complete known-limit/failure map with every CMB role assigned",
            "hard_failure_condition": "cannot state how Tau variables relate to standard comparison variables",
            "depends_on_source_component": "known_limit_branch",
            "currently_scoreable": "false",
            "blocks_no_dark_claim": "true",
        },
    ]
    return [
        {
            "rubric_row_id": f"TCMBLRSR01_{index:03d}",
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
            "summary_id": "TAU_CMB_LCDM_ROLE_SCORING_RUBRIC_V01",
            "rubric_rows_declared": len(rows),
            "score_levels_declared_per_row": 3,
            "currently_scoreable_rows": sum(row["currently_scoreable"] == "true" for row in rows),
            "hard_failure_rules_declared": sum(row["hard_failure_condition"] != "" for row in rows),
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "LCDM_ROLE_SCORING_RUBRIC_DECLARED_NO_SCORES_COMPUTED",
            "next_required_artifact": "tau_cmb_role_scorecard_template_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_lcdm_role_scoring_rubric_v01.md").write_text(
        """# Tau CMB LCDM Role Scoring Rubric v01

**Doc class:** scoring rubric
**Status:** rubric declared; no scores computed, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_lcdm_role_scoring_rubric.py
```

Derived outputs:

```text
data/derived/tau_cmb_lcdm_role_scoring_rubric_v01.csv
data/derived/tau_cmb_lcdm_role_scoring_rubric_summary_v01.csv
```

This artifact defines how a future Tau CMB source candidate should be scored
against the roles normally carried by the standard non-baryonic sector. It is
not a scorecard and it computes no numerical result.

Each row has three possible score levels:

```text
0 = role absent, wrong, or hard-failed
1 = qualitative/partial role support, not enough for verdict
2 = quantitative compatibility under a stated benchmark or likelihood
```

The rubric covers six CMB role families:

```text
acoustic peak phase and height
Omega_c h^2 density inference
CMB lensing potential
damping-tail / radiation guard
growth-seed and transfer consistency
known-limit or explicit failure branch
```

All rows are currently marked not scoreable because the preceding artifacts
have not yet supplied the response operator, transfer kernel, known-limit map,
or likelihood benchmark.

## Claim Boundary

This artifact declares scoring rules only. It computes no scores, provides no
CMB likelihood, matches no LCDM role, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = rubric_rows()
    write_csv(DERIVED / "tau_cmb_lcdm_role_scoring_rubric_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_lcdm_role_scoring_rubric_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_LCDM_ROLE_SCORING_RUBRIC_V01_BUILT")


if __name__ == "__main__":
    main()
