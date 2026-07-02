#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

FACTORIZED_SUMMARY = DERIVED / "cmb_tau_lensing_factorized_response_derivation_attempt_v01_summary.json"
FACTORIZED_FACTORS = DERIVED / "cmb_tau_lensing_factorized_response_derivation_attempt_v01.csv"
FACTORIZED_NEXT = DERIVED / "cmb_tau_lensing_factorized_response_derivation_attempt_v01_next_steps.csv"

PREFIX = "cmb_tau_lensing_seed_screening_minimal_closure_attempt_v01"
CLAIM_BOUNDARY = (
    "cmb_tau_lensing_seed_screening_minimal_closure_attempt_v01_conditional_formula_closure_only_"
    "seed_activation_and_base_field_screening_not_unconditional_tau_derivation_no_physical_tau_claim_no_verdict"
)

ASSUMPTION_FIELDS = [
    "assumption_id",
    "target_factor",
    "minimal_tau_side_assumption",
    "mathematical_consequence",
    "status",
    "claim_boundary",
]

CLOSURE_FIELDS = [
    "closure_id",
    "factor",
    "formula_piece",
    "closure_result",
    "unconditional_tau_derivation",
    "endpoint_blind_status",
    "claim_boundary",
]

NEXT_FIELDS = [
    "next_step_id",
    "target",
    "required_closure",
    "acceptance_condition",
    "claim_boundary",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# Tau Lensing Seed-Screening Minimal Closure Attempt v01

**Doc class:** conditional formula-closure attempt
**Status:** seed activation and base-field screening are conditionally closed at formula level
**Canonical parent:** Paper 13 ACT/Planck lensing route

This artifact takes the factorized response kernel and asks whether the two
central shape factors can be expressed as a minimal interaction between an
initial morphological seed condition and the Tau base-field response medium.

It does not prove the physical Tau response. It records a conditional closure:
if the initial seed condition is read through an admissible response coordinate,
and if the Tau base field supplies a saturating screening transfer, then the
two factors of the current diagnostic kernel follow. The seed is not the whole
source; it is the initial morphology/constraint state that co-determines the
later response together with the base-field properties.

Conditional route:

```text
x = L/L_c
M_seed = initial morphological/constraint state
B_tau  = Tau base-field response medium
M_tau  = F_tau(M_seed, B_tau, constraints)
seed-conditioned activation:       alpha(M_tau,B_tau;x) = x^{summary["candidate_rise_power"]}
base-field screening transfer:     S_B(M_tau,B_tau;x) = 1/(1+x^{summary["candidate_p_plus_q"]})
conditional response shape:        alpha(M_tau,B_tau;x) * S_B(M_tau,B_tau;x)
```

Inverse-constraint reading:

```text
source-frozen morphology/readout evidence
+ 4D residual/readout behavior
+ null, gauge, and wrong-family controls
-> compatible B_tau response-family candidates.
```

This is not an identification of the Tau base field. It says only that
morphology and 4D readout data can constrain which base-field response families
remain viable.

Formula-level status:

```text
assumptions_total={summary["assumptions_total"]}
conditional_factor_closures={summary["conditional_factor_closures"]}
unconditional_tau_derivations={summary["unconditional_tau_derivations"]}
reconstructs_factorized_kernel={summary["reconstructs_factorized_kernel"]}
score_readiness_unlocked={summary["score_readiness_unlocked"]}
```

## Claim Boundary

This artifact is useful but deliberately limited. It turns two open factors
into explicit conditional assumptions about seed--base-field co-determination.
It does not derive \(p=0.5\), \(p+q=1.5\), \(L_c=120\), or \(A=10^{-7}\)
from Tau Core, and it does not decide whether a dark-sector-like Tau
base-field response is physically required.
""",
        encoding="utf-8",
    )


def main() -> None:
    factorized = json.loads(FACTORIZED_SUMMARY.read_text())
    p = factorized["candidate_rise_power"]
    pq = factorized["candidate_p_plus_q"]
    ell_c = factorized["candidate_ell_c"]
    amp = factorized["candidate_amplitude"]

    assumption_rows = [
        {
            "assumption_id": "ASSUME_001",
            "target_factor": "seed_activation_factor",
            "minimal_tau_side_assumption": "morphological_seed_is_initial_constraint_state_and_base_field_response_admits_square_root_like_activation_coordinate",
            "mathematical_consequence": f"alpha(M_tau,B_tau;x)=x^{p}",
            "status": "conditional_formula_assumption_declared",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "assumption_id": "ASSUME_002",
            "target_factor": "base_field_screening_factor",
            "minimal_tau_side_assumption": "tau_base_field_properties_shape_stabilized_morphology_and_supply_saturating_high_scale_screening_transfer",
            "mathematical_consequence": f"S_B(M_tau,B_tau;x)=1/(1+x^{pq})",
            "status": "conditional_formula_assumption_declared",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "assumption_id": "ASSUME_003",
            "target_factor": "transition_scale",
            "minimal_tau_side_assumption": "lensing_transition_scale_is_supplied_by_tau_morphological_or_readout_scale",
            "mathematical_consequence": f"x=L/{ell_c}",
            "status": "still_open_no_tau_side_scale_derivation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "assumption_id": "ASSUME_004",
            "target_factor": "amplitude_slot",
            "minimal_tau_side_assumption": "response_strength_is_supplied_by_tau_seed_capacity_or_base_field_coupling_normalization",
            "mathematical_consequence": f"A={amp}",
            "status": "still_open_no_tau_side_amplitude_derivation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    closure_rows = [
        {
            "closure_id": "CLOSURE_001",
            "factor": "seed_activation_factor",
            "formula_piece": f"x^{p}",
            "closure_result": "conditionally_closed_by_seed_conditioned_base_field_activation_assumption",
            "unconditional_tau_derivation": "false",
            "endpoint_blind_status": "formula_assumption_only_not_endpoint_derived",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "closure_id": "CLOSURE_002",
            "factor": "base_field_screening_factor",
            "formula_piece": f"1/(1+x^{pq})",
            "closure_result": "conditionally_closed_by_saturating_base_field_transfer_assumption",
            "unconditional_tau_derivation": "false",
            "endpoint_blind_status": "formula_assumption_only_not_endpoint_derived",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "closure_id": "CLOSURE_003",
            "factor": "combined_shape_kernel",
            "formula_piece": f"x^{p}/(1+x^{pq})",
            "closure_result": "reconstructs_unnormalized_factorized_shape_under_seed_base_field_codetermination_assumptions",
            "unconditional_tau_derivation": "false",
            "endpoint_blind_status": "formula_reconstruction_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "closure_id": "CLOSURE_004",
            "factor": "transition_scale_and_amplitude",
            "formula_piece": f"L_c={ell_c}; A={amp}",
            "closure_result": "not_closed_values_remain_external_to_conditional_factor_model",
            "unconditional_tau_derivation": "false",
            "endpoint_blind_status": "open_origin",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    next_rows = [
        {
            "next_step_id": "NEXT_001",
            "target": "seed_activation_exponent",
            "required_closure": f"derive_or_reject_p={p}_from_tau_seed_admissibility_or_morphological_capacity_scaling",
            "acceptance_condition": "p_obtained_without_ACT_or_Planck_lensing_endpoint_selection",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_step_id": "NEXT_002",
            "target": "base_field_screening_exponent",
            "required_closure": f"derive_or_reject_p_plus_q={pq}_from_tau_base_field_transfer_or_response_spectrum",
            "acceptance_condition": "p_plus_q_obtained_without_endpoint_selection_and_preserves_zero_limit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_step_id": "NEXT_003",
            "target": "conditional_scoring_boundary",
            "required_closure": "decide_whether_a_conditional_formula_score_is_allowed_before_unconditional_tau_derivation",
            "acceptance_condition": "score_label_must_state_conditional_assumption_based_not_physical_tau_validation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_step_id": "NEXT_004",
            "target": "transition_scale_and_amplitude",
            "required_closure": f"derive_or_bound_L_c={ell_c}_and_A={amp}_from_endpoint_blind_tau_side_inputs",
            "acceptance_condition": "no_minimization_against_ACT_or_Planck_lensing_values",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    assumptions_path = DERIVED / f"{PREFIX}_assumptions.csv"
    closures_path = DERIVED / f"{PREFIX}_closures.csv"
    next_path = DERIVED / f"{PREFIX}_next_steps.csv"
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    write_csv(assumptions_path, assumption_rows, ASSUMPTION_FIELDS)
    write_csv(closures_path, closure_rows, CLOSURE_FIELDS)
    write_csv(next_path, next_rows, NEXT_FIELDS)

    summary = {
        "summary_id": "CMB_TAU_LENSING_SEED_SCREENING_MINIMAL_CLOSURE_ATTEMPT_V01",
        "factorized_summary_path": str(FACTORIZED_SUMMARY.relative_to(ROOT)),
        "factorized_summary_sha256": sha256(FACTORIZED_SUMMARY),
        "factorized_factors_path": str(FACTORIZED_FACTORS.relative_to(ROOT)),
        "factorized_factors_sha256": sha256(FACTORIZED_FACTORS),
        "factorized_next_steps_path": str(FACTORIZED_NEXT.relative_to(ROOT)),
        "factorized_next_steps_sha256": sha256(FACTORIZED_NEXT),
        "assumptions_path": str(assumptions_path.relative_to(ROOT)),
        "assumptions_sha256": sha256(assumptions_path),
        "closures_path": str(closures_path.relative_to(ROOT)),
        "closures_sha256": sha256(closures_path),
        "next_steps_path": str(next_path.relative_to(ROOT)),
        "next_steps_sha256": sha256(next_path),
        "candidate_id": factorized["candidate_id"],
        "candidate_rise_power": p,
        "candidate_p_plus_q": pq,
        "candidate_ell_c": ell_c,
        "candidate_amplitude": amp,
        "assumptions_total": len(assumption_rows),
        "conditional_factor_closures": 2,
        "unconditional_tau_derivations": 0,
        "reconstructs_factorized_kernel": True,
        "seed_activation_conditionally_closed": True,
        "base_field_screening_conditionally_closed": True,
        "seed_is_initial_morphological_state_not_standalone_source": True,
        "base_field_codetermines_stabilized_morphology": True,
        "transition_scale_derived": False,
        "amplitude_derived": False,
        "score_readiness_unlocked": False,
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "derive_transition_scale_and_amplitude_or_define_conditional_score_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                str(summary["conditional_factor_closures"]),
                str(summary["unconditional_tau_derivations"]),
                str(summary["reconstructs_factorized_kernel"]).lower(),
                str(summary["score_readiness_unlocked"]).lower(),
            ]
        )
    )


if __name__ == "__main__":
    main()
