# CMB Tau Lensing Projection Replay Materialization Request v01

**Doc class:** data-frontier request
**Reader role:** Paper 13 scoring implementer
**Status:** request only, no replay payload
**Canonical parent:** `docs/cmb_tau_lensing_pp_grid_acceptance_audit_v02.md`

This request specifies the replay JSON required after a real 3000-value numeric
grid has been submitted.

## Required Replay File

Submit:

```text
payloads/tau_lensing_pp_grid_projection_replay_v01.json
```

only after a real numeric `tau_PP_grid` or `delta_PP_tau` payload exists.

## Required Replay Contents

The replay must record:

```text
input_grid_file
input_grid_sha256
route_id: direct_tau_PP_grid or delta_PP_tau
B_ACT source and shape
index alignment: L = 10 + i
projected_vector_shape: 18
projected_vector_sha256
claim_boundary_reference
```

## Required Computation

The replay must show the schema-locked projection:

```text
B_ACT @ grid -> projected_shape_18
```

It must not compute a score, select a normalization from residuals, or issue a
dark-sector verdict.

## Claim Boundary

```text
projection_replay_materialization_request_only_no_replay_payload_no_tau_score_no_dark_sector_verdict
```
