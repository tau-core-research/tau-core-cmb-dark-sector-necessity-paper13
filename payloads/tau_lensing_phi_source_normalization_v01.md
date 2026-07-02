# Tau Lensing Phi Source Normalization v01

**Payload class:** Phi source normalization
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_phi_source_payload_submission_v01.md`

This payload records the normalization obligations for `Phi_tau_eff(a,k)` before
it can be transferred into a CMB lensing `PP` grid.

## Normalization Object

The object to normalize is:

```text
Phi_tau_eff(a, k)
```

It is treated as a potential-like readout source. This file does not assign a
numerical amplitude, fit an amplitude, or select a normalization from ACT or
Planck residuals.

## Required Convention

A later accepted payload must specify one of the following before scoring:

```text
dimensionless_potential_convention
metric_potential_convention_with_units
delta_PP_relative_convention_against_named_fiducial_PP
```

The convention must be declared before the `tau_PP_grid` or `delta_PP_tau`
projection is evaluated.

## Relation To PP Grid

The normalization must define how the source enters:

```text
Phi_tau_eff(a, k) -> T_tau_CMB -> tau_PP_grid or delta_PP_tau
```

This file does not supply the transfer operator, projection kernel, grid values,
or bandpower vector.

## Endpoint-Blind Rule

The normalization cannot be selected by minimizing:

```text
ACT residuals
Planck residuals
reduced chi2
dark-sector verdict preference
```

## Claim Boundary

```text
phi_source_normalization_payload_only_no_numeric_amplitude_no_transfer_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
