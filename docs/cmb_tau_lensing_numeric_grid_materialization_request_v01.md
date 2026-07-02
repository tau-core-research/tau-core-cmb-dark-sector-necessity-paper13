# CMB Tau Lensing Numeric Grid Materialization Request v01

**Doc class:** data-frontier request
**Reader role:** Paper 13 scoring implementer
**Status:** request only, no grid payload
**Canonical parent:** `docs/cmb_tau_lensing_pp_grid_acceptance_audit_v02.md`

This request specifies the exact numeric payload needed to unblock the reduced
Tau lensing score path.

## Required Numeric Object

Submit exactly one of:

```text
payloads/tau_lensing_response_pp_grid_v01.csv
payloads/tau_lensing_response_delta_pp_v01.csv
```

The submitted file must contain exactly 3000 finite numeric values under the
predeclared alignment:

```text
grid_index i = 0..2999
L = 10 + i
```

## Required Companion Evidence

The grid submission must include:

```text
route declaration: direct_tau_PP_grid or delta_PP_tau
endpoint-blind provenance record
hashable numeric file
normalization route consistent with the PP-grid normalization policy
```

## Forbidden Construction

The numeric grid cannot be constructed by fitting or tuning against:

```text
ACT residuals
Planck residuals
reduced chi2
dark-sector verdict preference
```

## Next Step After Submission

Only after a real numeric grid exists can the projection replay be generated:

```text
B_ACT @ grid -> projected_shape_18
```

## Claim Boundary

```text
numeric_grid_materialization_request_only_no_grid_payload_no_projection_replay_no_tau_score_no_dark_sector_verdict
```
