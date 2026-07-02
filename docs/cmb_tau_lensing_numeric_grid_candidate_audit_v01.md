# CMB Tau Lensing Numeric Grid Candidate Audit v01

**Doc class:** candidate audit
**Reader role:** Paper 13 scoring implementer
**Status:** no acceptable numeric grid candidate found
**Canonical parent:** `docs/cmb_tau_lensing_numeric_grid_materialization_request_v01.md`

This audit checks whether the repository already contains a usable numeric
`tau_PP_grid` or `delta_PP_tau` payload.

## Result

```text
NONE_ACCEPTABLE
```

No replayable endpoint-blind 3000-value Tau PP-grid payload was found.

## What Exists

- rule payloads for index alignment, normalization, delta route, and claim
  boundary;
- template grid files under `payload_templates/`, explicitly marked
  `TEMPLATE_NOT_PAYLOAD`;
- derived and source-manifest tables that declare requirements and blockers.

## What Does Not Exist

```text
payloads/tau_lensing_response_pp_grid_v01.csv
payloads/tau_lensing_response_delta_pp_v01.csv
```

No existing file is accepted as a numeric score input.

## Claim Boundary

```text
numeric_grid_candidate_audit_only_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
