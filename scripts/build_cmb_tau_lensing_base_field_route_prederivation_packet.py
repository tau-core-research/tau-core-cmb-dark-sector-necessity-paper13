#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

ROUTE_SUMMARY = DERIVED / "cmb_tau_lensing_response_origin_route_audit_v01_summary.json"
ROUTE_AUDIT = DERIVED / "cmb_tau_lensing_response_origin_route_audit_v01.csv"
ROUTE_REQUIREMENTS = DERIVED / "cmb_tau_lensing_response_origin_route_audit_v01_requirements.csv"

PREFIX = "cmb_tau_lensing_base_field_route_prederivation_packet_v01"
CLAIM_BOUNDARY = (
    "cmb_tau_lensing_base_field_route_prederivation_packet_v01_prederivation_target_only_"
    "base_field_route_selected_as_next_work_route_not_physical_tau_response_no_dark_sector_verdict"
)

DECISION_FIELDS = [
    "decision_row_id",
    "route_id",
    "route_name",
    "decision_for_next_work",
    "reason",
    "not_a_physical_selection_because",
    "claim_boundary",
]

OPERATOR_FIELDS = [
    "operator_row_id",
    "operator_object",
    "target_formula",
    "tau_side_interpretation",
    "acceptance_condition",
    "status",
    "claim_boundary",
]

TEST_FIELDS = [
    "test_id",
    "test_name",
    "required_result",
    "current_status",
    "claim_boundary",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# Tau Lensing Base-Field Route Prederivation Packet v01

**Doc class:** base-field route prederivation target
**Status:** ROUTE_02 selected as next derivation work route, not as a physical truth claim
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact takes the origin-route audit and chooses the seed-induced Tau
base-field response route as the next derivation target. This is not a
selection of the true physical route. It is a work-priority decision: the broad
low-\(L\) shape and independent amplitude burden are more naturally expressed
as a response operator than as a direct seed-only projection.

Target chain:

```text
M_seed + B_tau
-> M_tau = F_tau(M_seed, B_tau, constraints)
-> Phi_tau_eff = D_tau[M_tau; B_tau]
-> R_tau^kk(L) = Pi_lens[Phi_tau_eff](L)
-> A*S(L; L_c,p,q)
```

Candidate values to derive or reject:

```text
A={summary["candidate_amplitude"]}
L_c={summary["candidate_ell_c"]}
p={summary["candidate_rise_power"]}
q={summary["candidate_fall_power"]}
```

Prederivation status:

```text
selected_next_work_route={summary["selected_next_work_route"]}
physical_tau_response_claim_allowed={summary["physical_tau_response_claim_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
acceptance_tests_total={summary["acceptance_tests_total"]}
acceptance_tests_open={summary["acceptance_tests_open"]}
```

## Claim Boundary

The packet only defines the next derivation target. It does not prove the Tau
base field, does not derive \(D_\\tau\), does not derive \(\\Pi_\\mathrm{{lens}}\),
does not establish the amplitude, and does not decide dark-sector necessity.
""",
        encoding="utf-8",
    )


def main() -> None:
    route_summary = json.loads(ROUTE_SUMMARY.read_text())
    routes = {row["route_id"]: row for row in read_csv(ROUTE_AUDIT)}

    decision_rows = [
        {
            "decision_row_id": "DECISION_00_NULL",
            "route_id": "ROUTE_00_NULL",
            "route_name": routes["ROUTE_00_NULL"]["route_name"],
            "decision_for_next_work": "not_selected_as_derivation_target_except_known_limit_control",
            "reason": "ACT_and_Planck_reduced_diagnostics_prefer_nonzero_candidate_over_null",
            "not_a_physical_selection_because": "null_remains_required_known_limit_control",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_row_id": "DECISION_01_SEED_ONLY",
            "route_id": "ROUTE_01_SEED_ONLY",
            "route_name": routes["ROUTE_01_SEED_ONLY"]["route_name"],
            "decision_for_next_work": "deferred_secondary_route",
            "reason": "seed_only_route_has_simpler_ontology_but_high_burden_to_explain_broad_nonlocal_scale_and_amplitude_directly",
            "not_a_physical_selection_because": "not_rejected; may_return_if_base_field_route_fails",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_row_id": "DECISION_02_BASE_FIELD",
            "route_id": "ROUTE_02_BASE_FIELD",
            "route_name": routes["ROUTE_02_BASE_FIELD"]["route_name"],
            "decision_for_next_work": "selected_as_next_derivation_work_route",
            "reason": "response_operator_can_carry_low_L_activation_high_L_suppression_and_normalization_burden_explicitly",
            "not_a_physical_selection_because": "D_tau_and_Pi_lens_are_not_derived_yet",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_row_id": "DECISION_03_HYBRID",
            "route_id": "ROUTE_03_HYBRID",
            "route_name": routes["ROUTE_03_HYBRID"]["route_name"],
            "decision_for_next_work": "deferred_high_burden_route",
            "reason": "hybrid_route_risks_double_counting_until_direct_and_induced_terms_are_independently_defined",
            "not_a_physical_selection_because": "no_term_separation_or_no_double_counting_proof_exists",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    amp = route_summary["candidate_amplitude"]
    ell_c = route_summary["candidate_ell_c"]
    p = route_summary["candidate_rise_power"]
    q = route_summary["candidate_fall_power"]
    raw_shape = f"((L/{ell_c})^{p})/(1+(L/{ell_c})^({p}+{q}))"
    normalized_shape = f"{raw_shape}/max_L({raw_shape})"

    operator_rows = [
        {
            "operator_row_id": "OP_001",
            "operator_object": "seed_to_effective_tau_response",
            "target_formula": "M_tau = F_tau(M_seed,B_tau,constraints); Phi_tau_eff = D_tau[M_tau;B_tau]",
            "tau_side_interpretation": "the_initial_morphological_seed_and_tau_base_field_properties_codetermine_a_stabilized_response_morphology",
            "acceptance_condition": "D_tau_defined_without_ACT_or_Planck_endpoint_selection",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "operator_row_id": "OP_002",
            "operator_object": "lensing_projection_kernel",
            "target_formula": "R_tau^kk(L)=Pi_lens[Phi_tau_eff](L)",
            "tau_side_interpretation": "the_tau_response_is_read_out_as_an_effective_4D_lensing_response",
            "acceptance_condition": "Pi_lens_maps_tau_response_to_C_L^kk_units_and_preserves_zero_limit",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "operator_row_id": "OP_003",
            "operator_object": "minimal_broad_low_L_response_kernel",
            "target_formula": f"K_lens(L)={normalized_shape}",
            "tau_side_interpretation": "low_L_activation_with_high_L_suppression_is_the_shape_target_for_D_tau_followed_by_Pi_lens",
            "acceptance_condition": f"derive_or_reject_L_c={ell_c}_p={p}_q={q}_from_tau_side_structure",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "operator_row_id": "OP_004",
            "operator_object": "amplitude_normalization",
            "target_formula": f"A={amp}",
            "tau_side_interpretation": "amplitude_must_come_from_tau_normalization_seed_capacity_or_response_strength",
            "acceptance_condition": "A_is_not_selected_by_ACT_or_Planck_endpoint_minimization",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "operator_row_id": "OP_005",
            "operator_object": "zero_source_limit",
            "target_formula": "M_seed_absent_or_response_strength_zero -> Phi_tau_eff=0 -> R_tau^kk(L)=0",
            "tau_side_interpretation": "base_field_route_must_recover_the_existing_null_control",
            "acceptance_condition": "zero_limit_matches_formula_level_null_response_in_all_lensing_bins",
            "status": "required_known_limit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    test_rows = [
        {
            "test_id": "BF_TEST_001",
            "test_name": "endpoint_blind_shape_derivation",
            "required_result": f"derive_L_c={ell_c}_p={p}_q={q}_without_ACT_or_Planck_endpoint_fit",
            "current_status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "test_id": "BF_TEST_002",
            "test_name": "endpoint_blind_amplitude_derivation",
            "required_result": f"derive_or_bound_A={amp}_without_endpoint_selection",
            "current_status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "test_id": "BF_TEST_003",
            "test_name": "zero_limit_recovery",
            "required_result": "M_seed_absent_or_A=0_recovers_y_tau=0",
            "current_status": "formula_level_closed_operator_level_open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "test_id": "BF_TEST_004",
            "test_name": "cross_readout_replay",
            "required_result": "same_derived_route_replays_ACT_and_Planck_reduced_lensing_diagnostics",
            "current_status": "diagnostic_transfer_done_full_route_replay_open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "test_id": "BF_TEST_005",
            "test_name": "no_double_counting_guard",
            "required_result": "base_field_response_not_double_counted_as_direct_seed_projection",
            "current_status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    decision_path = DERIVED / f"{PREFIX}.csv"
    operator_path = DERIVED / f"{PREFIX}_operator_targets.csv"
    test_path = DERIVED / f"{PREFIX}_acceptance_tests.csv"
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    write_csv(decision_path, decision_rows, DECISION_FIELDS)
    write_csv(operator_path, operator_rows, OPERATOR_FIELDS)
    write_csv(test_path, test_rows, TEST_FIELDS)

    summary = {
        "summary_id": "CMB_TAU_LENSING_BASE_FIELD_ROUTE_PREDERIVATION_PACKET_V01",
        "route_summary_path": str(ROUTE_SUMMARY.relative_to(ROOT)),
        "route_summary_sha256": sha256(ROUTE_SUMMARY),
        "route_audit_path": str(ROUTE_AUDIT.relative_to(ROOT)),
        "route_audit_sha256": sha256(ROUTE_AUDIT),
        "route_requirements_path": str(ROUTE_REQUIREMENTS.relative_to(ROOT)),
        "route_requirements_sha256": sha256(ROUTE_REQUIREMENTS),
        "decision_path": str(decision_path.relative_to(ROOT)),
        "decision_sha256": sha256(decision_path),
        "operator_targets_path": str(operator_path.relative_to(ROOT)),
        "operator_targets_sha256": sha256(operator_path),
        "acceptance_tests_path": str(test_path.relative_to(ROOT)),
        "acceptance_tests_sha256": sha256(test_path),
        "candidate_id": route_summary["candidate_id"],
        "candidate_amplitude": amp,
        "candidate_ell_c": ell_c,
        "candidate_rise_power": p,
        "candidate_fall_power": q,
        "selected_next_work_route": "ROUTE_02_BASE_FIELD",
        "route_selected_as_physical": False,
        "seed_only_route_rejected": False,
        "hybrid_route_rejected": False,
        "operator_targets_total": len(operator_rows),
        "acceptance_tests_total": len(test_rows),
        "acceptance_tests_open": 5,
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "derive_or_reject_D_tau_and_Pi_lens_for_base_field_route",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                summary["selected_next_work_route"],
                str(summary["route_selected_as_physical"]).lower(),
                str(summary["acceptance_tests_open"]),
            ]
        )
    )


if __name__ == "__main__":
    main()
