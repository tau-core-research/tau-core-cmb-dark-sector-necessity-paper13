# Tau Lensing Delta PP Policy v01

**Payload class:** delta PP policy
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_pp_grid_payload_submission_v01.md`

This payload declares how a future `delta_PP_tau` route may be used instead of
a directly submitted `tau_PP_grid`.

## Route Options

A score-eligible PP payload may use exactly one of:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
```

The selected route must be declared before score evaluation.

## Delta Route Rule

If the delta route is used, the total projected grid must be formed as:

```text
tau_PP_grid_total(L) = fiducial_PP_named(L) + delta_PP_tau(L)
```

under the predeclared index alignment:

```text
L = 10 + i
i = 0..2999
```

The fiducial source must be named, hashable, and fixed before projection replay.

## Direct Route Rule

If a direct `tau_PP_grid` is submitted, the delta route is marked not used and
no hidden residual correction is allowed.

## Endpoint-Blind Rule

The choice between direct and delta route cannot be selected from ACT residuals,
Planck residuals, reduced chi2, or a desired dark-sector verdict.

## Current Limitation

This file does not submit a numeric direct grid, a numeric delta grid, a named
fiducial file, or a projection replay.

## Claim Boundary

```text
delta_pp_policy_payload_only_no_numeric_grid_no_fiducial_hash_no_projection_replay_no_tau_score_no_dark_sector_verdict
```
