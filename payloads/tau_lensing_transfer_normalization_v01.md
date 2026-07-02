# Tau Lensing Transfer Normalization v01

**Payload class:** transfer normalization
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_transfer_payload_submission_v01.md`

This payload records the normalization obligations for the transfer from
`Phi_tau_eff(a,k)` to `Psi_tau_lens(a,k)`.

## Normalization Scope

The normalization applies to the formal transfer route:

```text
Psi_tau_lens(a,k) = T_tau_CMB[Phi_tau_eff](a,k)
```

It must be compatible with both the Phi source normalization obligation and the
later `PP` grid or `delta_PP_tau` convention.

## Required Before Score

A later score-eligible package must declare:

```text
input normalization for Phi_tau_eff
transfer normalization for T_tau_CMB
output normalization for Psi_tau_lens
projection normalization into tau_PP_grid or delta_PP_tau
```

This payload does not set a numerical amplitude or fitted scale factor.

## Endpoint-Blind Rule

The transfer normalization cannot be selected from:

```text
ACT residuals
Planck residuals
reduced chi2
post-hoc dark-sector verdict preference
```

## Claim Boundary

```text
transfer_normalization_payload_only_no_numeric_amplitude_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
