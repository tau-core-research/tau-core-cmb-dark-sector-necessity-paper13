# CMB Tau Lensing Route Choice Rubric v01

**Doc class:** decision rubric
**Reader role:** Paper 13 scoring implementer
**Status:** route choice guidance, no route selected
**Canonical parent:** `docs/cmb_tau_lensing_numeric_grid_route_decision_contract_v01.md`

This rubric gives the narrow decision rule for choosing the next route.

## Preferred Order

```text
1. direct_tau_PP_grid, if an endpoint-blind absolute Tau PP grid exists
2. delta_PP_tau_against_named_fiducial_PP, if Tau gives a correction to a locked fiducial
3. explicit_failure_no_endpoint_blind_grid, if neither numeric route can be derived
```

The posthoc/template route is forbidden.

## Meaning

Direct is the cleanest prediction route, but hardest because it needs an
absolute 3000-value Tau PP grid.

Delta is acceptable only if the fiducial and delta construction are locked
before score evaluation.

Failure is not a defeat. It is the correct scientific stop if no endpoint-blind
grid can be produced.

## Claim Boundary

```text
route_choice_rubric_only_no_selected_route_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
