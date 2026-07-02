# CMB Tau Lensing PP Grid Payload Submission v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** submission packet, payload not submitted
**Canonical parent:** `docs/cmb_tau_lensing_score_unblock_plan_v01.md`

This packet defines the concrete files required to close the third unblock
step: the projectable `tau_PP_grid` or `delta_PP_tau` payload.

## Required Files

At least one numeric grid file:

```text
tau_lensing_response_pp_grid_v01.csv
```

or:

```text
tau_lensing_response_delta_pp_v01.csv
```

Supporting files:

```text
tau_lensing_pp_grid_index_alignment_v01.md
tau_lensing_pp_grid_normalization_v01.md
tau_lensing_pp_grid_projection_replay_v01.json
tau_lensing_delta_pp_policy_v01.md
tau_lensing_pp_grid_claim_boundary_v01.md
```

## Acceptance Rule

The numeric file must contain exactly 3000 finite values and must not be a
template. The payload must declare index alignment and normalization before any
score attempt. The projection replay must show:

```text
B_ACT @ tau_PP_grid -> shape (18,)
```

The grid cannot be chosen from ACT residual minimization unless the relevant
parameters and priors were declared in advance.

## Current Status

```text
PAYLOAD_NOT_SUBMITTED
```

No `PP` projection payload is accepted and no Tau score is allowed.

## Claim Boundary

```text
pp_grid_submission_packet_only_no_grid_payload_no_tau_score_no_dark_sector_verdict
```

## Partial Submission Update

The PP-grid index-alignment, normalization, delta policy, and claim-boundary
components have now been submitted for review at:

```text
payloads/tau_lensing_pp_grid_index_alignment_v01.md
payloads/tau_lensing_pp_grid_normalization_v01.md
payloads/tau_lensing_delta_pp_policy_v01.md
payloads/tau_lensing_pp_grid_claim_boundary_v01.md
```

This does not close the PP-grid payload. A real 3000-value `tau_PP_grid` or
`delta_PP_tau` and projection replay remain missing.
