#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

ANSATZ_SUMMARY = DERIVED / "cmb_tau_lensing_base_field_operator_ansatz_packet_v01_summary.json"
ANSATZ_PROPERTIES = DERIVED / "cmb_tau_lensing_base_field_operator_ansatz_packet_v01_properties.csv"
ANSATZ_GAPS = DERIVED / "cmb_tau_lensing_base_field_operator_ansatz_packet_v01_open_gaps.csv"

PREFIX = "cmb_tau_lensing_factorized_response_derivation_attempt_v01"
CLAIM_BOUNDARY = (
    "cmb_tau_lensing_factorized_response_derivation_attempt_v01_formula_factorization_only_"
    "seed_activation_transfer_screening_readout_split_not_tau_side_derivation_no_physical_tau_claim_no_verdict"
)

FACTOR_FIELDS = [
    "factor_id",
    "factor_name",
    "formula_piece",
    "tau_core_interpretation",
    "mathematical_status",
    "physical_derivation_status",
    "claim_boundary",
]

ASSESSMENT_FIELDS = [
    "assessment_id",
    "criterion",
    "result",
    "status",
    "claim_boundary",
]

NEXT_FIELDS = [
    "next_step_id",
    "target",
    "required_derivation",
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
        f"""# Tau Lensing Factorized Response Derivation Attempt v01

**Doc class:** formula-level factorized derivation attempt
**Status:** candidate lensing kernel split into seed activation, base-field screening, readout normalization, and amplitude slots
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact factors the current base-field lensing ansatz into smaller
derivation targets. It does not derive the factors from Tau Core. It records a
minimal decomposition that a later Tau-side proof must justify or reject.

Candidate response:

```text
R_tau^kk(L) = A * K_lens(L)
x = L/L_c
K_lens(L) = x^p / (1 + x^(p+q)) / N
N = max_x[x^p/(1+x^(p+q))]
```

Factorized route:

```text
seed activation:        x^p
base-field screening:  1/(1+x^(p+q))
readout normalization: 1/N
amplitude slot:        A
```

Candidate values:

```text
A={summary["candidate_amplitude"]}
L_c={summary["candidate_ell_c"]}
p={summary["candidate_rise_power"]}
q={summary["candidate_fall_power"]}
```

Formula-level status:

```text
factors_total={summary["factors_total"]}
formula_factorization_exact={summary["formula_factorization_exact"]}
open_tau_side_factor_derivations={summary["open_tau_side_factor_derivations"]}
physical_tau_response_claim_allowed={summary["physical_tau_response_claim_allowed"]}
```

## Claim Boundary

This is only a factorization of the diagnostic kernel. It does not prove that
the Tau seed produces \(x^p\), that the Tau base field produces
\(1/(1+x^{{p+q}})\), that the readout normalization is physically fixed, or
that the amplitude \(A\) follows from Tau normalization.
""",
        encoding="utf-8",
    )


def main() -> None:
    ansatz = json.loads(ANSATZ_SUMMARY.read_text())
    amp = ansatz["candidate_amplitude"]
    ell_c = ansatz["candidate_ell_c"]
    p = ansatz["candidate_rise_power"]
    q = ansatz["candidate_fall_power"]
    pq = float(p) + float(q)

    factor_rows = [
        {
            "factor_id": "FACTOR_001",
            "factor_name": "dimensionless_scale_coordinate",
            "formula_piece": f"x=L/{ell_c}",
            "tau_core_interpretation": "readout_scale_coordinate_relative_to_candidate_transition_scale",
            "mathematical_status": "materialized",
            "physical_derivation_status": "open_L_c_origin",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor_id": "FACTOR_002",
            "factor_name": "seed_activation_factor",
            "formula_piece": f"x^{p}",
            "tau_core_interpretation": "candidate_low_L_activation_from_seed_or_seed_base_field_coupling",
            "mathematical_status": "materialized_low_L_exponent",
            "physical_derivation_status": "open_seed_activation_derivation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor_id": "FACTOR_003",
            "factor_name": "base_field_screening_factor",
            "formula_piece": f"1/(1+x^{pq})",
            "tau_core_interpretation": "candidate_high_L_suppression_from_tau_base_field_transfer_or_screening",
            "mathematical_status": "materialized_high_L_suppression",
            "physical_derivation_status": "open_base_field_screening_derivation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor_id": "FACTOR_004",
            "factor_name": "readout_normalization_factor",
            "formula_piece": f"1/max_x[x^{p}/(1+x^{pq})]",
            "tau_core_interpretation": "normalizes_the_4D_lensing_readout_shape_before_amplitude_assignment",
            "mathematical_status": "materialized_by_definition",
            "physical_derivation_status": "open_readout_normalization_derivation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor_id": "FACTOR_005",
            "factor_name": "amplitude_slot",
            "formula_piece": f"A={amp}",
            "tau_core_interpretation": "candidate_response_strength_from_tau_normalization_seed_capacity_or_base_field_coupling",
            "mathematical_status": "diagnostic_value_materialized",
            "physical_derivation_status": "open_amplitude_derivation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    assessment_rows = [
        {
            "assessment_id": "ASSESS_001",
            "criterion": "exact_reconstruction_of_ansatz_kernel",
            "result": "K_lens=x^p/(1+x^(p+q))/N_reconstructed_by_factor_product",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "assessment_id": "ASSESS_002",
            "criterion": "low_L_activation_visible",
            "result": f"low_L_factor_is_x^{p}",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "assessment_id": "ASSESS_003",
            "criterion": "high_L_screening_visible",
            "result": f"screening_factor_yields_high_L_exponent=-{q}",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "assessment_id": "ASSESS_004",
            "criterion": "zero_limit_visible",
            "result": "A=0_zeroes_full_factorized_response",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "assessment_id": "ASSESS_005",
            "criterion": "tau_side_derivation_supplied",
            "result": "not_supplied_for_any_factor",
            "status": "open_physical_derivation_gap",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    next_rows = [
        {
            "next_step_id": "NEXT_001",
            "target": "seed_activation_factor",
            "required_derivation": f"derive_or_reject_x^{p}_activation_from_seed_admissibility_or_seed_base_field_coupling",
            "acceptance_condition": "p_obtained_without_ACT_or_Planck_endpoint_selection",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_step_id": "NEXT_002",
            "target": "base_field_screening_factor",
            "required_derivation": f"derive_or_reject_1_over_1_plus_x^{pq}_screening_from_tau_base_field_transfer",
            "acceptance_condition": "p_plus_q_obtained_without_endpoint_selection_and_zero_limit_preserved",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_step_id": "NEXT_003",
            "target": "transition_scale",
            "required_derivation": f"derive_or_reject_L_c={ell_c}_from_tau_morphological_scale_or_response_spectrum",
            "acceptance_condition": "L_c_not_selected_by_lensing_endpoint_fit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_step_id": "NEXT_004",
            "target": "amplitude_slot",
            "required_derivation": f"derive_or_bound_A={amp}_from_tau_normalization_seed_capacity_or_coupling_strength",
            "acceptance_condition": "A_not_selected_by_ACT_or_Planck_endpoint_minimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    factor_path = DERIVED / f"{PREFIX}.csv"
    assessment_path = DERIVED / f"{PREFIX}_assessment.csv"
    next_path = DERIVED / f"{PREFIX}_next_steps.csv"
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    write_csv(factor_path, factor_rows, FACTOR_FIELDS)
    write_csv(assessment_path, assessment_rows, ASSESSMENT_FIELDS)
    write_csv(next_path, next_rows, NEXT_FIELDS)

    summary = {
        "summary_id": "CMB_TAU_LENSING_FACTORIZED_RESPONSE_DERIVATION_ATTEMPT_V01",
        "ansatz_summary_path": str(ANSATZ_SUMMARY.relative_to(ROOT)),
        "ansatz_summary_sha256": sha256(ANSATZ_SUMMARY),
        "ansatz_properties_path": str(ANSATZ_PROPERTIES.relative_to(ROOT)),
        "ansatz_properties_sha256": sha256(ANSATZ_PROPERTIES),
        "ansatz_gaps_path": str(ANSATZ_GAPS.relative_to(ROOT)),
        "ansatz_gaps_sha256": sha256(ANSATZ_GAPS),
        "factorization_path": str(factor_path.relative_to(ROOT)),
        "factorization_sha256": sha256(factor_path),
        "assessment_path": str(assessment_path.relative_to(ROOT)),
        "assessment_sha256": sha256(assessment_path),
        "next_steps_path": str(next_path.relative_to(ROOT)),
        "next_steps_sha256": sha256(next_path),
        "candidate_id": ansatz["candidate_id"],
        "candidate_amplitude": amp,
        "candidate_ell_c": ell_c,
        "candidate_rise_power": p,
        "candidate_fall_power": q,
        "candidate_p_plus_q": pq,
        "factors_total": len(factor_rows),
        "formula_factorization_exact": True,
        "formula_level_assessments_pass": 4,
        "open_tau_side_factor_derivations": len(next_rows),
        "seed_activation_derived": False,
        "base_field_screening_derived": False,
        "transition_scale_derived": False,
        "amplitude_derived": False,
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "derive_or_reject_seed_activation_and_base_field_screening_factors",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                str(summary["formula_factorization_exact"]).lower(),
                str(summary["formula_level_assessments_pass"]),
                str(summary["open_tau_side_factor_derivations"]),
                str(summary["physical_tau_response_claim_allowed"]).lower(),
            ]
        )
    )


if __name__ == "__main__":
    main()
