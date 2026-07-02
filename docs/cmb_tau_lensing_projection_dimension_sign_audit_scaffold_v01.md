# CMB Tau Lensing Projection Dimension/Sign Audit Scaffold v01

**Doc class:** projection dimension/sign audit scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** audit schema declared; values not filled; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
projection_dimension_sign_audit_scaffold_only_no_operator_acceptance_no_score_no_dark_sector_verdict
```

## Purpose

This table narrows the `dimension_and_sign_audit` blocker in the projection
operator formula-spec scaffold. It does not accept a physical projection
operator and does not populate `N_projection_physical`.

## Audit Rows

- `TCMBPDSAS01_001` `Phi_lens_tau_domain`: DECLARED_REQUIRED_NOT_FILLED | required: dimension and sign convention for Phi_lens_tau(a,k) | failure if: potential sign or dimension is chosen after seeing ACT/Planck score behavior
- `TCMBPDSAS01_002` `kernel_measure`: KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED | required: dimension of K_tau_PP(L; a,k) dmu(a,k) | failure if: kernel absorbs an arbitrary post-score amplitude or has unspecified integration/sum measure
- `TCMBPDSAS01_003` `N_projection_physical`: NORMALIZATION_SPEC_DECLARED_NOT_FILLED | required: unit/sign role of N_projection_physical | failure if: normalization is set from alpha_star, chi2 minimization, or residual matching
- `TCMBPDSAS01_004` `PP_codomain`: CODOMAIN_CONTRACT_LOCKED_NO_VALUES | required: PP versus delta_PP_tau convention and L=10..3009 alignment | failure if: tau_PP and delta_PP_tau are mixed without an explicit fiducial PP reference
- `TCMBPDSAS01_005` `zero_source_limit`: PROOF_OBLIGATION_DECLARED_NOT_DISCHARGED | required: Phi_lens_tau -> 0 implies projection contribution -> 0 | failure if: operator has an additive nonzero term not declared as a separate baseline/fiducial contribution
- `TCMBPDSAS01_006` `endpoint_firewall`: REQUIRED_AFTER_VALUES | required: no endpoint score quantities used in convention choices | failure if: any convention row cites score outputs, residuals, or dark-sector verdict preference

## Unblocks When

- each declaration row is filled from endpoint-blind operator evidence
- zero-source limit is proved from the supplied operator
- post-population endpoint firewall passes
- N_projection_physical is derived or declared as a pre-score diagnostic parameter range
