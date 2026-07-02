# CMB Tau Lensing Prescore Readiness Lock v01

**Doc class:** prescore readiness lock
**Reader role:** Paper 13 scoring implementer
**Status:** blocked on route, grid, and replay
**Canonical parent:** `docs/cmb_tau_lensing_reduced_score_attempt_gate_v01.md`

This lock summarizes the reduced Tau lensing score path immediately before any
score attempt.

## Status

```text
BLOCKED_ON_ROUTE_GRID_REPLAY
```

## Ready

```text
ACT adapter contract: ready for diagnostic adapter use
```

## Definition-Ready Only

```text
Phi source: accepted for transfer definition only
Transfer: accepted for projection definition only
PP rule scaffold: partial rules accepted for projection review only
```

## Blocking

```text
route selection: missing
numeric 3000-value grid: missing
projection replay: missing
reduced Tau score: not allowed
```

## Single Next Action

Choose exactly one route and submit its required evidence:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
explicit_failure_no_endpoint_blind_grid
```

## Claim Boundary

```text
prescore_readiness_lock_only_no_tau_score_no_dark_sector_verdict
```
