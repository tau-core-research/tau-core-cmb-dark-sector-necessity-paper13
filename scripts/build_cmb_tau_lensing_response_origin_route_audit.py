#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

STATUS_SUMMARY = DERIVED / "cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01_summary.json"
STATUS_AUDIT = DERIVED / "cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01.csv"
FORMULA_SPEC = DERIVED / "cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01_formula_spec.csv"
HOLDOUT_SUMMARY = DERIVED / "cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01_summary.json"

PREFIX = "cmb_tau_lensing_response_origin_route_audit_v01"
CLAIM_BOUNDARY = (
    "cmb_tau_lensing_response_origin_route_audit_v01_origin_route_audit_only_"
    "seed_only_base_field_hybrid_routes_declared_no_route_selected_no_physical_tau_claim_no_dark_sector_verdict"
)

ROUTE_FIELDS = [
    "route_id",
    "route_name",
    "tau_side_map",
    "four_d_lensing_readout",
    "what_must_be_derived",
    "current_status",
    "allowed_claim",
    "primary_failure_mode",
    "claim_boundary",
]

REQUIREMENT_FIELDS = [
    "requirement_id",
    "required_object",
    "candidate_value_or_formula",
    "required_tau_side_explanation",
    "status",
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
        f"""# Tau Lensing Response Origin Route Audit v01

**Doc class:** response-origin route audit
**Status:** seed-only, base-field, and hybrid Tau-origin routes declared; no route selected
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact turns the nonzero lensing candidate into an origin problem. The
ACT and Planck reduced diagnostics show that a nonzero broad low-\(L\) response
is much better than the null response, but they do not say where that response
comes from. This audit therefore separates the viable Tau-origin routes.

Candidate target:

```text
candidate_id={summary["candidate_id"]}
R_tau^kk(L) = A*S(L; L_c,p,q)
A={summary["candidate_amplitude"]}
L_c={summary["candidate_ell_c"]}
p={summary["candidate_rise_power"]}
q={summary["candidate_fall_power"]}
ACT_delta_chi2_vs_null={summary["act_delta_chi2_vs_null"]}
Planck_delta_chi2_vs_null={summary["planck_delta_chi2_vs_null"]}
```

Route status:

```text
routes_declared={summary["routes_declared"]}
route_selected_now={summary["route_selected_now"]}
seed_only_route_status={summary["seed_only_route_status"]}
base_field_route_status={summary["base_field_route_status"]}
hybrid_route_status={summary["hybrid_route_status"]}
physical_tau_response_claim_allowed={summary["physical_tau_response_claim_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Interpretation

The seed-only route would make the morphology seed itself carry the scale and
amplitude of the lensing response. The base-field route would make the seed act
as an excitation/source for a Tau base-substrate response, with the response
operator producing the broad lensing shape. The hybrid route allows direct seed
projection plus base-field response, but it has the highest proof burden.

No route is selected by this artifact. The next successful step must derive or
reject at least one route by producing the candidate \(L_c,p,q,A\) without
endpoint selection.
""",
        encoding="utf-8",
    )


def main() -> None:
    status = json.loads(STATUS_SUMMARY.read_text())
    holdout = json.loads(HOLDOUT_SUMMARY.read_text())

    candidate_id = status["candidate_id"]
    amplitude = status["transferred_amplitude"]
    ell_c = status["transferred_ell_c"]
    rise_power = status["transferred_rise_power"]
    fall_power = status["transferred_fall_power"]

    route_rows = [
        {
            "route_id": "ROUTE_00_NULL",
            "route_name": "zero_response_control",
            "tau_side_map": "M_seed_absent_or_A=0 -> R_tau^kk(L)=0",
            "four_d_lensing_readout": "y_tau=0_in_all_ACT_or_Planck_lensing_bins",
            "what_must_be_derived": "already_closed_for_diagnostic_formula_family_only",
            "current_status": "rejected_as_best_diagnostic_by_ACT_and_Planck_reduced_scores_not_rejected_as_known_limit",
            "allowed_claim": "known_limit_control_only",
            "primary_failure_mode": "large_chi2_relative_to_nonzero_candidate",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "route_id": "ROUTE_01_SEED_ONLY",
            "route_name": "seed_only_projection",
            "tau_side_map": "M_seed -> Pi_lens[M_seed] -> R_tau^kk(L)",
            "four_d_lensing_readout": "direct_seed_projection_supplies_A_and_S(L;L_c,p,q)",
            "what_must_be_derived": "show_seed_morphology_carries_L_c_p_q_and_A_without_base_field_response_or_endpoint_fit",
            "current_status": "open_viable_but_unproved",
            "allowed_claim": "candidate_origin_route_only",
            "primary_failure_mode": "seed_may_not_naturally_carry_broad_nonlocal_scale_and_normalization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "route_id": "ROUTE_02_BASE_FIELD",
            "route_name": "seed_induced_tau_base_field_response",
            "tau_side_map": "M_seed + B_tau -> Phi_tau_eff=D_tau[M_seed] -> Pi_lens[Phi_tau_eff] -> R_tau^kk(L)",
            "four_d_lensing_readout": "base_field_response_operator_supplies_broad_low_L_shape_and_amplitude",
            "what_must_be_derived": "derive_response_operator_D_tau_and_lensing_projection_Pi_lens_that_yield_L_c_p_q_A",
            "current_status": "open_viable_but_unproved",
            "allowed_claim": "candidate_origin_route_only",
            "primary_failure_mode": "requires_tau_base_field_response_equation_and_normalization_rule",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "route_id": "ROUTE_03_HYBRID",
            "route_name": "seed_projection_plus_base_field_response",
            "tau_side_map": "M_seed -> direct_projection + D_tau[M_seed] -> combined_R_tau^kk(L)",
            "four_d_lensing_readout": "direct_and_induced_terms_together_supply_candidate_shape",
            "what_must_be_derived": "separate_direct_and_induced_terms_without_double_counting_or_endpoint_fit",
            "current_status": "open_high_burden_route",
            "allowed_claim": "candidate_origin_route_only",
            "primary_failure_mode": "risk_of_degeneracy_and_double_counting_between_projection_and_response_terms",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    requirement_rows = [
        {
            "requirement_id": "REQ_SHAPE_ELL_C",
            "required_object": "candidate_lensing_scale_L_c",
            "candidate_value_or_formula": f"{ell_c}",
            "required_tau_side_explanation": "why_the_seed_or_response_operator_selects_this_lensing_transition_scale",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "REQ_SHAPE_RISE",
            "required_object": "low_L_rise_power_p",
            "candidate_value_or_formula": f"{rise_power}",
            "required_tau_side_explanation": "why_low_L_response_scales_as_(L/L_c)^p_before_turnover",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "REQ_SHAPE_FALL",
            "required_object": "high_L_suppression_power_q",
            "candidate_value_or_formula": f"{fall_power}",
            "required_tau_side_explanation": "why_high_L_response_is_suppressed_by_the_denominator_power_p_plus_q",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "REQ_AMPLITUDE",
            "required_object": "response_amplitude_A",
            "candidate_value_or_formula": f"{amplitude}",
            "required_tau_side_explanation": "derive_or_bound_A_from_tau_normalization_or_seed_capacity_without_endpoint_selection",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "REQ_ZERO_LIMIT",
            "required_object": "zero_response_limit",
            "candidate_value_or_formula": "A=0 -> R_tau^kk(L)=0",
            "required_tau_side_explanation": "closed_for_diagnostic_formula_family; full_tau_zero_source_theorem_remains_separate",
            "status": "closed_formula_level_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "REQ_CROSS_READOUT",
            "required_object": "same_candidate_on_planck_lensing_block",
            "candidate_value_or_formula": (
                f"Planck_delta_chi2_vs_null={holdout['candidate_delta_chi2_vs_null']:.12g}; "
                f"fractional_improvement={holdout['candidate_fractional_chi2_improvement_vs_null']:.12g}"
            ),
            "required_tau_side_explanation": "partially_addressed_by_unchanged_transfer; full_independent_likelihood_still_open",
            "status": "partially_addressed_not_closed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    route_path = DERIVED / f"{PREFIX}.csv"
    requirement_path = DERIVED / f"{PREFIX}_requirements.csv"
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    write_csv(route_path, route_rows, ROUTE_FIELDS)
    write_csv(requirement_path, requirement_rows, REQUIREMENT_FIELDS)

    summary = {
        "summary_id": "CMB_TAU_LENSING_RESPONSE_ORIGIN_ROUTE_AUDIT_V01",
        "status_summary_path": str(STATUS_SUMMARY.relative_to(ROOT)),
        "status_summary_sha256": sha256(STATUS_SUMMARY),
        "status_audit_path": str(STATUS_AUDIT.relative_to(ROOT)),
        "status_audit_sha256": sha256(STATUS_AUDIT),
        "formula_spec_path": str(FORMULA_SPEC.relative_to(ROOT)),
        "formula_spec_sha256": sha256(FORMULA_SPEC),
        "holdout_summary_path": str(HOLDOUT_SUMMARY.relative_to(ROOT)),
        "holdout_summary_sha256": sha256(HOLDOUT_SUMMARY),
        "route_audit_path": str(route_path.relative_to(ROOT)),
        "route_audit_sha256": sha256(route_path),
        "requirements_path": str(requirement_path.relative_to(ROOT)),
        "requirements_sha256": sha256(requirement_path),
        "candidate_id": candidate_id,
        "candidate_amplitude": amplitude,
        "candidate_ell_c": ell_c,
        "candidate_rise_power": rise_power,
        "candidate_fall_power": fall_power,
        "act_delta_chi2_vs_null": status["act_delta_chi2_vs_null"],
        "planck_delta_chi2_vs_null": status["planck_delta_chi2_vs_null"],
        "routes_declared": len(route_rows),
        "route_selected_now": False,
        "seed_only_route_status": "open_viable_but_unproved",
        "base_field_route_status": "open_viable_but_unproved",
        "hybrid_route_status": "open_high_burden_route",
        "route_decision_status": "undecided_origin_problem_now_explicit",
        "requirements_total": len(requirement_rows),
        "requirements_open": 4,
        "requirements_partial": 1,
        "requirements_closed_formula_level": 1,
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "derive_or_reject_seed_only_or_base_field_origin_route_for_L_c_p_q_A",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                str(summary["routes_declared"]),
                str(summary["route_selected_now"]).lower(),
                str(summary["requirements_open"]),
                str(summary["physical_tau_response_claim_allowed"]).lower(),
            ]
        )
    )


if __name__ == "__main__":
    main()
