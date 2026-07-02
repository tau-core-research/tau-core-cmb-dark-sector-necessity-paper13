# CMB Tau Lensing Numeric Grid Route Selection Gate v01

**Doc class:** route gate
**Reader role:** Paper 13 scoring implementer
**Status:** route selection blocked
**Canonical parent:** `docs/cmb_tau_lensing_numeric_grid_route_decision_contract_v01.md`

This gate checks whether one allowed numeric-grid route has actually been
selected.

## Decision

```text
NUMERIC_GRID_ROUTE_SELECTION_BLOCKED
```

No allowed route has been submitted:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
explicit_failure_no_endpoint_blind_grid
```

The forbidden route remains rejected:

```text
posthoc_or_template_grid
```

## Next Required Action

Choose exactly one allowed route and submit the required payloads, or submit the
explicit failure statement if no endpoint-blind grid can be derived.

## Claim Boundary

```text
numeric_grid_route_selection_gate_only_no_selected_route_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
