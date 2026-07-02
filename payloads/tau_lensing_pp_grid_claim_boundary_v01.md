# Tau Lensing PP Grid Claim Boundary v01

**Payload class:** PP-grid claim boundary
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_pp_grid_payload_submission_v01.md`

This payload fixes the claim boundary for any future reduced PP-grid score.

## Allowed Claim

If a valid numeric `tau_PP_grid` or `delta_PP_tau` payload is later accepted and
projected through the schema-locked ACT adapter, the allowed result is only:

```text
reduced diagnostic ACT lensing bandpower comparison
```

## Forbidden Promotion

The reduced PP-grid route cannot by itself claim:

```text
full CMB likelihood success
Planck validation
ACT validation
dark-sector necessity
dark-sector exclusion
physical Tau field detection
acoustic peak explanation
growth-history explanation
```

## Required Before Any Score

The following must exist before a reduced score attempt:

```text
real 3000-value tau_PP_grid or delta_PP_tau
index alignment
normalization policy
projection replay with projected shape 18
payload hashes
endpoint-blind firewall replay
```

## Claim Boundary

```text
pp_grid_claim_boundary_payload_only_no_numeric_grid_no_projection_replay_no_tau_score_no_dark_sector_verdict
```
