# CMB Tau Lensing PP Grid Acceptance Audit v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** PP-grid acceptance audit, payload absent
**Canonical parent:** `docs/cmb_tau_lensing_pp_grid_projection_payload_v01.md`

This audit checks whether a real `tau_PP_grid` or `delta_PP_tau` projection
payload has been submitted.

## Result

Only template files are present:

```text
payload_templates/tau_lensing_response_pp_grid_v01.csv
payload_templates/tau_lensing_response_delta_pp_v01.csv
```

Templates are explicitly marked `TEMPLATE_NOT_PAYLOAD` and cannot be accepted as
scoring input.

## Decision

```text
REJECT_FOR_LENSING_RESPONSE_INPUT
```

No projectable `PP` grid is accepted. No Tau lensing score is allowed.

## Missing Requirements

```text
real 3000-value tau_PP_grid or delta_PP_tau
predeclared index-alignment policy
normalization policy
projection replay
delta-route policy if using delta_PP_tau
projection claim boundary
```

## Claim Boundary

```text
pp_grid_acceptance_audit_only_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
