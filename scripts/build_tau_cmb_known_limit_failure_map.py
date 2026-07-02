#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_known_limit_failure_map_v01_map_only_no_scores_no_likelihood_no_verdict"

FIELDS = [
    "known_limit_row_id",
    "cmb_role",
    "standard_role_to_compare",
    "tau_object_to_evaluate",
    "allowed_decision_states",
    "current_decision_state",
    "minimum_evidence_for_reproduce",
    "minimum_evidence_for_approximate",
    "minimum_evidence_for_fail",
    "current_blocker",
    "next_unblock_artifact",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "known_limit_rows_declared",
    "allowed_decision_states_per_row",
    "resolved_rows",
    "unresolved_rows",
    "failures_declared",
    "reproductions_declared",
    "approximations_declared",
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

ROLE_MAP = {
    "acoustic_peak_phase_and_height": (
        "pre-recombination gravitational-potential support for acoustic phase and peak-height ratios",
        "Phi_tau_eff(a,k) with baryon-photon acoustic response",
        "quantitative acoustic phase and relative-height compatibility under declared benchmark",
        "reduced acoustic benchmark shows correct phase/height tendency but incomplete quantitative match",
        "wrong phase, missing potential source, or incompatible peak-height behavior",
        "potential handoff and acoustic benchmark not supplied",
        "tau_cmb_acoustic_role_reduced_benchmark_v01",
    ),
    "omega_c_h2_density_inference": (
        "density-like source role inferred as Omega_c h^2",
        "rho_tau_eff(a,k) and A_tau(a,k)",
        "endpoint-blind A_tau derivation quantitatively replaces the density role",
        "dimensionally valid density slot with partial Omega_c h^2 role support",
        "no endpoint-blind density amplitude or wrong density dimension",
        "A_tau derivation and density normalization not supplied",
        "tau_cmb_density_amplitude_derivation_v01",
    ),
    "cmb_lensing_potential": (
        "CMB lensing-potential amplitude and shape role",
        "Phi_tau_eff(a,k) and T_tau_CMB(k,a)",
        "quantitative CMB lensing-potential compatibility under declared benchmark",
        "potential and transfer slots support lensing qualitatively but remain incomplete",
        "missing or incompatible lensing potential transfer",
        "lensing-transfer benchmark not supplied",
        "tau_cmb_lensing_transfer_benchmark_v01",
    ),
    "damping_tail_and_radiation_guard": (
        "radiation-content and damping-tail guard role",
        "Delta_N_eff_tau",
        "bound check satisfies adopted damping-tail/Neff benchmark",
        "dimensionless guard declared but bound comparison incomplete",
        "Tau response overproduces radiation-like damping contribution",
        "Delta_N_eff_tau bound comparison not supplied",
        "tau_cmb_radiation_guard_bound_check_v01",
    ),
    "growth_seed_and_transfer_consistency": (
        "early growth-seed and transfer role",
        "T_tau_CMB(k,a)",
        "quantitative transfer compatibility across CMB lensing/growth benchmark",
        "transfer skeleton supports the role but lacks quantitative comparison",
        "no transfer kernel or incompatible scale/epoch propagation",
        "transfer kernel and growth benchmark not supplied",
        "tau_cmb_growth_transfer_kernel_v01",
    ),
    "known_limit_or_explicit_failure": (
        "global LCDM source-role comparison discipline",
        "LCDM_role_limit_or_failure",
        "all CMB roles have explicit reproduce/approximate/fail assignments",
        "some roles assigned while others remain unresolved",
        "no lawful map from Tau variables to standard comparison variables",
        "global role decision map declared here but individual evidence rows remain missing",
        "tau_cmb_density_amplitude_derivation_v01",
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


def known_limit_rows() -> list[dict[str, str]]:
    scorecard_rows = read_csv(DERIVED / "tau_cmb_role_scorecard_template_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(scorecard_rows, start=1):
        (
            standard_role,
            tau_object,
            reproduce_evidence,
            approximate_evidence,
            fail_evidence,
            blocker,
            next_artifact,
        ) = ROLE_MAP[row["cmb_role"]]
        rows.append(
            {
                "known_limit_row_id": f"TCMBKLF01_{index:03d}",
                "cmb_role": row["cmb_role"],
                "standard_role_to_compare": standard_role,
                "tau_object_to_evaluate": tau_object,
                "allowed_decision_states": "REPRODUCE;APPROXIMATE;FAIL;UNRESOLVED",
                "current_decision_state": "UNRESOLVED_INPUT_MISSING",
                "minimum_evidence_for_reproduce": reproduce_evidence,
                "minimum_evidence_for_approximate": approximate_evidence,
                "minimum_evidence_for_fail": fail_evidence,
                "current_blocker": blocker,
                "next_unblock_artifact": next_artifact,
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
            "summary_id": "TAU_CMB_KNOWN_LIMIT_FAILURE_MAP_V01",
            "known_limit_rows_declared": len(rows),
            "allowed_decision_states_per_row": 4,
            "resolved_rows": sum(row["current_decision_state"] != "UNRESOLVED_INPUT_MISSING" for row in rows),
            "unresolved_rows": sum(row["current_decision_state"] == "UNRESOLVED_INPUT_MISSING" for row in rows),
            "failures_declared": 0,
            "reproductions_declared": 0,
            "approximations_declared": 0,
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "KNOWN_LIMIT_FAILURE_MAP_DECLARED_ALL_ROLES_UNRESOLVED",
            "next_required_artifact": "tau_cmb_density_amplitude_derivation_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_known_limit_failure_map_v01.md").write_text(
        """# Tau CMB Known-Limit Failure Map v01

**Doc class:** known-limit / explicit-failure map
**Status:** map declared; all role decisions unresolved, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_known_limit_failure_map.py
```

Derived outputs:

```text
data/derived/tau_cmb_known_limit_failure_map_v01.csv
data/derived/tau_cmb_known_limit_failure_map_summary_v01.csv
```

This artifact defines the decision states that every CMB role must eventually
enter:

```text
REPRODUCE
APPROXIMATE
FAIL
UNRESOLVED
```

In v01 every row remains:

```text
UNRESOLVED_INPUT_MISSING
```

The value of this map is not that it proves a role. Its value is that it
prevents a hidden promotion from "we have a Tau-like source slot" to "Tau Core
has replaced the CMB dark-sector role." A later artifact must provide enough
evidence to move each row from unresolved into reproduce, approximate, or fail.

The next useful artifact is:

```text
tau_cmb_density_amplitude_derivation_v01
```

## Claim Boundary

This artifact declares comparison states only. It computes no scores, supplies
no CMB likelihood, declares no reproduction, declares no failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = known_limit_rows()
    write_csv(DERIVED / "tau_cmb_known_limit_failure_map_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_known_limit_failure_map_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_KNOWN_LIMIT_FAILURE_MAP_V01_BUILT")


if __name__ == "__main__":
    main()
