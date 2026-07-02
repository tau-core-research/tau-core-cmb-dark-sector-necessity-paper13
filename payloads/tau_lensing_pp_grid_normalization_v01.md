# Tau Lensing PP Grid Normalization v01

**Payload class:** PP-grid normalization
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_pp_grid_payload_submission_v01.md`

This payload records the normalization obligations for a future `tau_PP_grid`
or `delta_PP_tau` payload before projection into ACT bandpowers.

## Normalization Scope

The normalization applies after the transfer route:

```text
Phi_tau_eff(a,k) -> T_tau_CMB -> Psi_tau_lens(a,k) -> tau_PP_grid or delta_PP_tau
```

It must be compatible with the Phi source normalization, transfer
normalization, and the locked PP-grid index convention:

```text
grid_index i = 0..2999
L = 10 + i
```

## Allowed Normalization Forms

A score-eligible PP payload must use one of:

```text
fixed_endpoint_blind_amplitude
predeclared_parameter_prior_or_range
dimensionless_delta_PP_convention_against_named_fiducial
```

The selected form must be declared before score evaluation.

## Forbidden Normalization

The PP-grid normalization cannot be chosen from:

```text
ACT residual minimization
Planck residual minimization
post-hoc reduced chi2 tuning
desired dark-sector verdict
```

## Current Limitation

This file does not supply a numeric grid, amplitude, projected bandpower vector,
or score.

## Claim Boundary

```text
pp_grid_normalization_payload_only_no_numeric_grid_no_amplitude_no_projection_replay_no_tau_score_no_dark_sector_verdict
```
