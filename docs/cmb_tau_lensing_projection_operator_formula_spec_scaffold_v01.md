# CMB Tau Lensing Projection Operator Formula-Spec Scaffold v01

**Doc class:** projection-operator formula-spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** scaffold only; not an accepted operator, not a grid, not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_decision_gate_v01.md`

## Claim Boundary

```text
projection_operator_formula_spec_scaffold_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict
```

## Minimal Operator Shape

```text
tau_PP(L) = N_projection_physical * Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)]
```

This is a specification scaffold for:

```text
Projection_PP[Phi_lens_tau](L)
```

It does not assert that this operator has been derived from Tau Core. It only
fixes the smallest field list required to resume from the explicit non-score
operator failure.

## Required Fields

- `domain_object`: CONTRACT_LOCKED_NO_NUMERIC_FIELD | required: Phi_lens_tau(a,k) | acceptance: Phi_lens_tau is derived from endpoint-blind Phi_tau_eff and T_tau_CMB, not from ACT/Planck residuals.
- `projection_kernel`: KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED | required: K_tau_PP(L; a,k) or equivalent transfer/projection kernel | acceptance: Kernel, support, measure, and limits are fixed before score readout.
- `projection_equation`: PROJECTION_EQUATION_SPEC_DECLARED_NOT_FILLED | required: tau_PP(L) = N_projection_physical * Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)] | acceptance: Integral/sum convention is fully specified, including a,k/L mapping and PP versus delta_PP_tau convention.
- `normalization`: NORMALIZATION_SPEC_DECLARED_NOT_FILLED | required: N_projection_physical | acceptance: Normalization follows from the operator measure/sign/unit convention; it is not fitted from endpoint residuals.
- `output_grid`: OUTPUT_REPLAY_SPEC_DECLARED_NOT_FILLED | required: 3000 rows, L=10..3009, tau_PP(L) or delta_PP_tau(L) | acceptance: Replay emits finite values with exact L alignment before scoring.
- `zero_source_limit`: PROOF_OBLIGATION_DECLARED_NOT_DISCHARGED | required: Phi_lens_tau -> 0 implies tau_PP or delta_PP_tau contribution -> 0 | acceptance: Limit follows algebraically from the supplied operator and normalization.
- `dimension_and_sign_audit`: AUDIT_SCHEMA_DECLARED_NOT_FILLED | required: dimension/sign convention table | acceptance: Units/signs are checked before materialization and cannot be inferred after score.
- `endpoint_firewall`: POST_POPULATION_FIREWALL_SPEC_DECLARED_NOT_RUN | required: post-population firewall certificate | acceptance: Certificate reruns after operator, normalization, and replay values are populated.

## Currently Missing

- `projection_kernel`
- `projection_equation`
- `normalization`
- `output_grid`
- `zero_source_limit`
- `dimension_and_sign_audit`
- `endpoint_firewall`

## Blocked Shortcuts

- do not set N_projection_physical from post-score alpha_star
- do not treat B_ACT @ grid as the physical Phi_lens_tau-to-PP operator
- do not score the scaffold
- do not claim a dark-sector verdict from this scaffold

## Resume Condition

```text
Replace scaffold-only fields with endpoint-blind operator/kernel/normalization/replay values, then rerun physical projection packet, audit, decision gate, parent-projection packet, and score guard.
```

## Source Links

- `docs/cmb_tau_lensing_grid_equation_packet_v01.md`
- `docs/cmb_tau_lensing_projection_operator_rule_requirement_v01.md`
- `docs/cmb_tau_lensing_projection_operator_explicit_failure_v01.md`
- `docs/cmb_tau_lensing_projection_equation_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_output_replay_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_v01.md`
- `docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_zero_source_limit_obligation_v01.md`
- `docs/cmb_tau_lensing_projection_normalization_requirement_v01.md`
- `docs/cmb_tau_lensing_physical_projection_replay_requirement_v01.md`
