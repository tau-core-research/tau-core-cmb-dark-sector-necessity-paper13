# CMB Tau Lensing PP Grid Projection Payload v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** PP-grid projection payload requirement, no grid
**Canonical parent:** `docs/cmb_tau_lensing_response_derivation_route_v01.md`

This packet states what is required to turn a lensing-era Tau potential response
into a projectable ACT DR6 lensing `PP`-style grid.

## Required Projection Contract

The reduced ACT adapter requires:

```text
tau_PP_grid: shape (3000,)
B_ACT:       shape (18, 3000)
m_ACT = B_ACT @ tau_PP_grid
```

or the perturbative form:

```text
tau_PP_grid = PP_fiducial + delta_PP_tau
delta_PP_tau: shape (3000,)
```

## Alignment Policy

The current sanity audit found `startL=10` as the strongest shape candidate for
the fiducial package `PP` column. This is not accepted as a proof.

A real Tau payload must declare its index alignment before scoring. The
alignment cannot be chosen by minimizing the ACT residual after seeing the data.

## Normalization Policy

The free `alpha` used in the adapter sanity check is not a physical Tau
parameter. A Tau projection payload must either:

- supply an absolute `PP` normalization; or
- declare any amplitude parameter and prior/range before scoring.

## Current Status

No `tau_PP_grid` or `delta_PP_tau` projection payload is submitted.

```text
BLOCKED_GRID_NOT_SUBMITTED
```

## Claim Boundary

```text
pp_grid_projection_payload_requirement_only_no_grid_no_tau_score_no_dark_sector_verdict
```

The PP-grid acceptance audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_pp_grid_acceptance_audit_v01.csv
docs/cmb_tau_lensing_pp_grid_acceptance_audit_v01.md
```
