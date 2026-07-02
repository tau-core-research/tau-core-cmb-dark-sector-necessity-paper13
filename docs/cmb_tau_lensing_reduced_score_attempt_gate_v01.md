# CMB Tau Lensing Reduced Score Attempt Gate v01

**Doc class:** scoring gate
**Reader role:** Paper 13 scoring implementer
**Status:** score attempt blocked
**Canonical parent:** `docs/cmb_tau_lensing_score_unblock_plan_v01.md`

This gate is the fifth unblock step. It decides whether a reduced Tau lensing
score attempt may begin after payload replay.

## Decision

```text
REDUCED_TAU_LENSING_SCORE_BLOCKED
```

The adapter and ACT data path are ready enough for a reduced diagnostic score.
The Phi and transfer packages are definition-ready only. The score remains
blocked because no numeric-grid route is selected, and the numeric
`tau_PP_grid` / `delta_PP_tau` payload and projection replay are missing.

## Blocking Conditions

- Phi source is accepted for transfer definition only, not as a numeric score
  input.
- Transfer is accepted for projection definition only, not as a numeric kernel.
- No numeric-grid route has been selected.
- No real 3000-value `tau_PP_grid` or `delta_PP_tau` payload.
- No projection replay showing `B_ACT @ grid -> shape (18,)`.
- No score-eligible payload hash/firewall replay.

## Next Narrow Action

Fulfill the two materialization requests:

```text
route selection -> numeric grid materialization -> projection replay materialization -> replay acceptance -> reduced score
```

## Claim Boundary

```text
reduced_score_attempt_gate_only_no_tau_score_no_dark_sector_verdict
```

This gate does not evaluate the CMB fit, Tau Core dark-sector necessity, or any
physical readout claim.
