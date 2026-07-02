# Tau Lensing Phi Source Lensing Interface v01

**Payload class:** Phi source lensing interface
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_phi_source_payload_submission_v01.md`

This payload declares how `Phi_tau_eff(a,k)` may hand off to the later transfer
and projection route.

## Interface Statement

`Phi_tau_eff(a,k)` is allowed to enter the CMB lensing route only through an
explicit transfer object:

```text
Phi_tau_eff(a, k) -> T_tau_CMB -> tau_PP_grid or delta_PP_tau
```

The transfer object must be supplied and accepted separately. This interface
does not define the transfer operator.

## Required Handoff Conditions

Before a reduced Tau lensing score attempt, the route must provide:

```text
accepted Phi source identity
accepted Phi provenance
accepted Phi normalization convention
accepted Phi time/scale support
accepted transfer domain and codomain
accepted projection payload into PP-grid convention
```

## Forbidden Shortcut

The following shortcut is not admissible:

```text
ACT or Planck bandpower residual -> chosen Phi_tau_eff -> score
```

That would turn the source into an endpoint-fitted residual object rather than a
Tau-side prediction candidate.

## Current Limitation

This file does not compute lensing kernels, does not generate a `PP` grid, and
does not evaluate a covariance-weighted score.

## Claim Boundary

```text
phi_source_lensing_interface_payload_only_no_transfer_operator_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
