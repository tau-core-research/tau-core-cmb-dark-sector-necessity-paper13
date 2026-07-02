# Tau Lensing Phi Source Cross-Readout Guard v01

**Payload class:** Phi source cross-readout guard
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_phi_source_payload_submission_v01.md`

This payload guards against inconsistent reuse of `Phi_tau_eff(a,k)` across CMB
readout roles.

## Guard Statement

`Phi_tau_eff(a,k)` may be used as a CMB lensing-route source only if later
payloads either:

```text
show compatibility with acoustic-density and growth-transfer assumptions
```

or explicitly mark those cross-readout roles as deferred.

## No Cross-Role Promotion

Acceptance for the lensing route alone must not be promoted into:

```text
acoustic peak explanation
growth history explanation
full CMB likelihood success
dark-sector necessity verdict
```

Those require separate role-specific evidence.

## Consistency Requirement

The lensing route must not choose a normalization, time/scale support, or
transfer convention that contradicts already declared Tau CMB density, acoustic,
or radiation-guard constraints.

## Current Limitation

This guard does not prove cross-readout compatibility. It only records the rule
that such compatibility must be checked before broader Paper 13 claims are made.

## Claim Boundary

```text
phi_source_cross_readout_guard_payload_only_no_cross_role_proof_no_transfer_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
