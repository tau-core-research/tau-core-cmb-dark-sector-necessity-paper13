# CMB Tau Lensing Projection Zero-Source Limit Obligation v01

**Doc class:** projection zero-source proof obligation
**Reader role:** Paper 13 Tau-grid implementer
**Status:** proof obligation declared; not discharged; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
projection_zero_source_limit_obligation_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict
```

## Target Statement

```text
Phi_lens_tau(a,k) -> 0 implies projected Tau contribution -> 0
```

## Scaffold Equation

```text
tau_PP(L) = N_projection_physical * Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)]
```

## Sufficient Conditions

- `linearity_or_declared_zero-preserving_nonlinearity`: PROJECTION_EQUATION_SPEC_DECLARED_NOT_FILLED | Projection_PP[0](L)=0, or every nonlinear term contains at least one Phi_lens_tau factor and no source-independent additive term.
- `finite_kernel_measure`: KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED | K_tau_PP(L; a,k)dmu(a,k) is finite/integrable on the declared support for each L=10..3009.
- `finite_normalization`: NORMALIZATION_SPEC_DECLARED_NOT_FILLED | N_projection_physical is finite and fixed before endpoint comparison.
- `no_hidden_baseline`: DECLARED_REQUIRED | Any fiducial PP baseline is outside the Tau contribution and is not counted as nonzero Tau response.
- `delta_route_consistency`: DECLARED_REQUIRED | If using delta_PP_tau, the zero-source limit applies to delta_PP_tau(L), not to the fiducial PP baseline.

## Algebraic Discharge Rule

```text
If the supplied operator is zero-preserving and the kernel measure and normalization are finite, then substituting Phi_lens_tau=0 gives tau_PP_tau_contribution(L)=0 for every L.
```

## Current Result

```text
NOT_DISCHARGED_BECAUSE_OPERATOR_KERNEL_AND_NORMALIZATION_NOT_SUPPLIED
```

## Blocked Shortcuts

- do not use the synthetic zero-control route as proof of the physical projection operator
- do not infer zero-source behavior from a scored residual
- do not hide a nonzero additive Tau term inside the fiducial PP baseline

## Source Links

- `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_equation_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_normalization_requirement_v01.md`
- `docs/cmb_tau_lensing_zero_response_control_v01.md`
