#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREDERIVATION_SUMMARY = DERIVED / "cmb_tau_lensing_base_field_route_prederivation_packet_v01_summary.json"
PREDERIVATION_OPERATORS = DERIVED / "cmb_tau_lensing_base_field_route_prederivation_packet_v01_operator_targets.csv"
PREDERIVATION_TESTS = DERIVED / "cmb_tau_lensing_base_field_route_prederivation_packet_v01_acceptance_tests.csv"

PREFIX = "cmb_tau_lensing_base_field_operator_ansatz_packet_v01"
CLAIM_BOUNDARY = (
    "cmb_tau_lensing_base_field_operator_ansatz_packet_v01_operator_ansatz_only_"
    "mathematical_shape_compatibility_not_tau_side_derivation_no_physical_tau_claim_no_dark_sector_verdict"
)

ANSATZ_FIELDS = [
    "ansatz_row_id",
    "object",
    "ansatz_statement",
    "mathematical_role",
    "status",
    "claim_boundary",
]

PROPERTY_FIELDS = [
    "property_id",
    "property_name",
    "expected_result",
    "actual_result",
    "status",
    "claim_boundary",
]

GAP_FIELDS = [
    "gap_id",
    "gap_name",
    "why_it_remains_open",
    "required_closure_artifact",
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
        f"""# Tau Lensing Base-Field Operator Ansatz Packet v01

**Doc class:** operator ansatz and mathematical compatibility audit
**Status:** candidate broad low-L kernel materialized as a base-field response ansatz; Tau-side derivation still open
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact turns the selected base-field work route into a concrete
operator ansatz. It does not derive the ansatz from Tau Core. It only verifies
that the candidate kernel has the mathematical properties required of the next
Tau-side derivation target.

Minimal ansatz:

```text
M_tau = F_tau(M_seed, B_tau, constraints)
Phi_tau_eff = D_tau[M_tau; B_tau]
R_tau^kk(L) = A * K_lens(L)
K_lens(L) = x^p / (1+x^(p+q)) / max_x[x^p/(1+x^(p+q))]
x = L/L_c
```

Candidate values:

```text
A={summary["candidate_amplitude"]}
L_c={summary["candidate_ell_c"]}
p={summary["candidate_rise_power"]}
q={summary["candidate_fall_power"]}
```

Compatibility audit:

```text
properties_total={summary["properties_total"]}
properties_pass_formula_level={summary["properties_pass_formula_level"]}
open_physical_derivation_gaps={summary["open_physical_derivation_gaps"]}
shape_ansatz_materialized={summary["shape_ansatz_materialized"]}
physical_tau_response_claim_allowed={summary["physical_tau_response_claim_allowed"]}
```

Formula-level result: the kernel is dimensionless, normalized, has low-\(L\)
activation exponent \(p\), high-\(L\) suppression exponent \(q\), and preserves
the zero-response limit through \(A=0\). The open problem is still to derive
\(D_\\tau\), \(\\Pi_\\mathrm{{lens}}\), \(L_c,p,q\), and \(A\) from Tau-side
structure without endpoint selection.
""",
        encoding="utf-8",
    )


def main() -> None:
    pre = json.loads(PREDERIVATION_SUMMARY.read_text())
    amp = pre["candidate_amplitude"]
    ell_c = pre["candidate_ell_c"]
    p = pre["candidate_rise_power"]
    q = pre["candidate_fall_power"]
    high_l_exponent = -float(q)

    ansatz_rows = [
        {
            "ansatz_row_id": "ANSATZ_001",
            "object": "base_field_response_object",
            "ansatz_statement": "M_tau = F_tau(M_seed,B_tau,constraints); Phi_tau_eff = D_tau[M_tau;B_tau]",
            "mathematical_role": "encodes_seed_and_base_field_codetermined_tau_response",
            "status": "ansatz_declared_not_derived",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "ansatz_row_id": "ANSATZ_002",
            "object": "lensing_projection_readout",
            "ansatz_statement": "R_tau^kk(L) = Pi_lens[Phi_tau_eff](L)",
            "mathematical_role": "maps_tau_response_to_4D_lensing_bandpower_basis",
            "status": "ansatz_declared_not_derived",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "ansatz_row_id": "ANSATZ_003",
            "object": "normalized_broad_low_L_kernel",
            "ansatz_statement": f"K_lens(L)=x^{p}/(1+x^({p}+{q}))/max_x[x^{p}/(1+x^({p}+{q}))], x=L/{ell_c}",
            "mathematical_role": "minimal_activation_suppression_shape_target",
            "status": "formula_level_materialized",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "ansatz_row_id": "ANSATZ_004",
            "object": "response_amplitude",
            "ansatz_statement": f"R_tau^kk(L)={amp}*K_lens(L)",
            "mathematical_role": "sets_candidate_C_L_kk_scale_in_current_reduced_adapter_units",
            "status": "diagnostic_value_not_tau_normalization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    property_rows = [
        {
            "property_id": "PROP_001",
            "property_name": "dimensionless_shape_kernel",
            "expected_result": "K_lens_dimensionless_when_x=L/L_c",
            "actual_result": "pass_formula_level",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "property_id": "PROP_002",
            "property_name": "normalization",
            "expected_result": "max_L_K_lens=1",
            "actual_result": "pass_by_definition",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "property_id": "PROP_003",
            "property_name": "low_L_activation",
            "expected_result": f"K_lens_proportional_to_L^{p}_for_L_much_less_than_L_c",
            "actual_result": f"low_L_exponent={p}",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "property_id": "PROP_004",
            "property_name": "high_L_suppression",
            "expected_result": f"K_lens_proportional_to_L^(-{q})_for_L_much_greater_than_L_c",
            "actual_result": f"high_L_exponent={high_l_exponent}",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "property_id": "PROP_005",
            "property_name": "zero_response_limit",
            "expected_result": "A=0_implies_R_tau_kk=0_for_all_L",
            "actual_result": "pass_formula_level",
            "status": "pass_formula_level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "property_id": "PROP_006",
            "property_name": "endpoint_blind_physical_origin",
            "expected_result": "D_tau_Pi_lens_L_c_p_q_A_derived_without_endpoint_selection",
            "actual_result": "not_yet_supplied",
            "status": "open_physical_derivation_gap",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    gap_rows = [
        {
            "gap_id": "GAP_001",
            "gap_name": "D_tau_derivation",
            "why_it_remains_open": "the_tau_base_field_response_operator_is_declared_as_an_ansatz_not_derived_from_parent_tau_dynamics",
            "required_closure_artifact": "derive_or_reject_D_tau_from_tau_base_field_and_seed_capacity",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gap_id": "GAP_002",
            "gap_name": "Pi_lens_derivation",
            "why_it_remains_open": "the_projection_from_tau_response_to_4D_C_L_kk_units_is_declared_but_not_derived",
            "required_closure_artifact": "derive_or_reject_Pi_lens_readout_kernel_and_units_map",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gap_id": "GAP_003",
            "gap_name": "shape_parameter_origin",
            "why_it_remains_open": f"L_c={ell_c}, p={p}, q={q} are candidate parameters_not_tau_side_outputs",
            "required_closure_artifact": "derive_or_reject_shape_parameters_from_tau_morphology_or_response_spectrum",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gap_id": "GAP_004",
            "gap_name": "amplitude_origin",
            "why_it_remains_open": f"A={amp} is a diagnostic_candidate_amplitude_not_tau_normalization",
            "required_closure_artifact": "derive_or_bound_A_from_tau_normalization_without_endpoint_fit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    ansatz_path = DERIVED / f"{PREFIX}.csv"
    property_path = DERIVED / f"{PREFIX}_properties.csv"
    gap_path = DERIVED / f"{PREFIX}_open_gaps.csv"
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    write_csv(ansatz_path, ansatz_rows, ANSATZ_FIELDS)
    write_csv(property_path, property_rows, PROPERTY_FIELDS)
    write_csv(gap_path, gap_rows, GAP_FIELDS)

    pass_count = sum(row["status"] == "pass_formula_level" for row in property_rows)
    summary = {
        "summary_id": "CMB_TAU_LENSING_BASE_FIELD_OPERATOR_ANSATZ_PACKET_V01",
        "prederivation_summary_path": str(PREDERIVATION_SUMMARY.relative_to(ROOT)),
        "prederivation_summary_sha256": sha256(PREDERIVATION_SUMMARY),
        "prederivation_operator_targets_path": str(PREDERIVATION_OPERATORS.relative_to(ROOT)),
        "prederivation_operator_targets_sha256": sha256(PREDERIVATION_OPERATORS),
        "prederivation_tests_path": str(PREDERIVATION_TESTS.relative_to(ROOT)),
        "prederivation_tests_sha256": sha256(PREDERIVATION_TESTS),
        "ansatz_path": str(ansatz_path.relative_to(ROOT)),
        "ansatz_sha256": sha256(ansatz_path),
        "properties_path": str(property_path.relative_to(ROOT)),
        "properties_sha256": sha256(property_path),
        "open_gaps_path": str(gap_path.relative_to(ROOT)),
        "open_gaps_sha256": sha256(gap_path),
        "candidate_id": pre["candidate_id"],
        "candidate_amplitude": amp,
        "candidate_ell_c": ell_c,
        "candidate_rise_power": p,
        "candidate_fall_power": q,
        "high_l_suppression_exponent": high_l_exponent,
        "shape_ansatz_materialized": True,
        "properties_total": len(property_rows),
        "properties_pass_formula_level": pass_count,
        "open_physical_derivation_gaps": len(gap_rows),
        "D_tau_derived": False,
        "Pi_lens_derived": False,
        "shape_parameters_derived": False,
        "amplitude_derived": False,
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "derive_or_reject_D_tau_and_Pi_lens_from_tau_side_structure",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                str(summary["shape_ansatz_materialized"]).lower(),
                str(summary["properties_pass_formula_level"]),
                str(summary["open_physical_derivation_gaps"]),
                str(summary["physical_tau_response_claim_allowed"]).lower(),
            ]
        )
    )


if __name__ == "__main__":
    main()
