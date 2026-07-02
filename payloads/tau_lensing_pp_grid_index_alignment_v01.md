# Tau Lensing PP Grid Index Alignment v01

**Payload class:** PP-grid index alignment
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_pp_grid_payload_submission_v01.md`

This payload declares the index-alignment convention required before any
`tau_PP_grid` or `delta_PP_tau` payload can be projected into ACT bandpowers.

## Alignment Convention

The reduced ACT adapter uses a 3000-column `PP` grid input. The working
alignment convention for a submitted Tau grid is:

```text
grid_index i = 0..2999
L = 10 + i
```

Therefore the submitted grid must be interpreted as:

```text
tau_PP_grid[L=10..3009]
```

or, for the delta route:

```text
delta_PP_tau[L=10..3009]
```

## Projection Rule

The accepted numeric grid must be projected only through the schema-locked ACT
binning matrix:

```text
B_ACT @ tau_PP_grid -> projected_shape_18
```

This file does not supply the 3000 grid values, the projected 18-vector, or a
score.

## Endpoint-Blind Rule

The alignment convention must be fixed before score evaluation and must not be
changed to improve ACT residuals or a dark-sector verdict.

## Claim Boundary

```text
pp_grid_index_alignment_payload_only_no_numeric_grid_no_projection_replay_no_tau_score_no_dark_sector_verdict
```
