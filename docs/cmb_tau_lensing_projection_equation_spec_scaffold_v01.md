# CMB Tau Lensing Projection Equation Spec Scaffold v01

**Doc class:** projection equation spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** equation schema declared; no equation accepted; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
projection_equation_spec_scaffold_only_no_equation_acceptance_no_grid_no_score_no_dark_sector_verdict
```

## Target

```text
Projection_PP[Phi_lens_tau](L)
```

## Minimal Scaffold Equation

```text
tau_PP_tau_contribution(L) = N_projection_physical * Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)]
```

## Required Rows

- `TCMBPESS01_001` `operator_equation_form`: REQUIRED_NOT_FILLED | required: closed equation, discrete sum, kernel table rule, or explicit failure | failure if: operator form is chosen after inspecting score behavior
- `TCMBPESS01_002` `linearity_policy`: REQUIRED_NOT_FILLED | required: linear, affine-with-baseline, or declared zero-preserving nonlinear operator policy | failure if: operator includes undeclared source-independent additive Tau term
- `TCMBPESS01_003` `baseline_delta_policy`: REQUIRED_NOT_FILLED | required: declare tau_PP direct output or delta_PP_tau relative to named fiducial PP | failure if: fiducial PP and Tau contribution are mixed without a named delta convention
- `TCMBPESS01_004` `composition_order`: REQUIRED_NOT_FILLED | required: Phi_tau_eff -> T_tau_CMB -> Phi_lens_tau -> Projection_PP -> PP/delta_PP_tau | failure if: adapter replay B_ACT @ grid is substituted for the physical projection equation
- `TCMBPESS01_005` `materialization_rule`: REQUIRED_NOT_FILLED | required: recipe to produce exactly 3000 finite values for L=10..3009 | failure if: materialization requires score output, residuals, or hand-edited endpoint fitting
- `TCMBPESS01_006` `formula_artifact`: REQUIRED_NOT_SUPPLIED | required: equation/table/integral artifact with provenance, hash, and claim boundary | failure if: formula artifact is missing or generated from post-score diagnostics

## Blocked Shortcuts

- do not use B_ACT @ grid as the physical projection equation
- do not hide a nonzero Tau term in the fiducial PP baseline
- do not choose operator form from post-score residuals
