# CMB Tau Lensing Route Selection Submission Precheck v01

**Doc class:** route precheck
**Reader role:** Paper 13 scoring implementer
**Status:** route selection still blocked
**Canonical parent:** `docs/cmb_tau_lensing_route_selection_submission_packet_v01.md`

This precheck evaluates whether any allowed route submission is complete.

## Decision

```text
ROUTE_SELECTION_STILL_BLOCKED
```

No allowed route payload set has been submitted.

## Current State

```text
direct_tau_PP_grid: missing required files
delta_PP_tau_against_named_fiducial_PP: missing required files
explicit_failure_no_endpoint_blind_grid: missing failure statement
posthoc_or_template_grid: forbidden
```

## Next Required Action

Submit exactly one allowed route payload set. Do not use templates or
endpoint-fitted residual curves as substitutes.

## Claim Boundary

```text
route_selection_submission_precheck_only_no_selected_route_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
