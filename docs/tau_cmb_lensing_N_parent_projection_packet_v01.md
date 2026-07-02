# Tau CMB Lensing N Parent Projection Packet v01

**Doc class:** normalization packet skeleton
**Reader role:** Paper 13 Tau-grid implementer
**Status:** skeleton only; no numeric normalization
**Canonical parent:** `docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md`

## Claim Boundary

```text
parent_projection_packet_skeleton_only_no_numeric_normalization_no_score_no_dark_sector_verdict
```

This packet is the concrete container for the remaining Tau-side normalization:

```text
N_tau_remaining = N_parent_source * N_projection
```

It intentionally contains no numeric normalization. The empty value slots may
only be populated from endpoint-blind Tau-side derivation evidence.

## Packet

```text
data/derived/tau_cmb_lensing_N_parent_projection_packet_v01.csv
```

## Current Rows

- `N_parent_source`: BLOCKED_DIMENSION_OR_UNIT_PROOF_NOT_SUPPLIED; BLOCKED_ENDPOINT_FIREWALL_CERTIFICATE_NOT_SUPPLIED
- `N_projection`: EXPLICIT_NON_SCORE_FAILURE_PHYSICAL_PROJECTION_OPERATOR_NOT_SUPPLIED; FIREWALL_PASS_FOR_CURRENT_SKELETON_ONLY_RERUN_AFTER_VALUES
- `N_tau_remaining`: BLOCKED_PRODUCT_COMPONENTS_NOT_ACCEPTED; BLOCKED_PRODUCT_COMPONENTS_NOT_ACCEPTED

## Unblocks When

- N_parent_source has a source-side derivation and dimension/gauge/firewall certificate
- N_projection has a projection operator derivation and replay certificate
- N_tau_remaining is computed from accepted factors before formula materialization
- formula spec is updated before any new score attempt

## Forbidden Shortcut

```text
do not populate current_value from post-score alpha_star or endpoint residuals
```

## Projection Split

The `N_projection` row separates two notions:

```text
Route B adapter replay: B_ACT @ grid, convention-locked for diagnostics
Physical Tau projection: Projection_PP[Phi_lens_tau](L), explicit non-score failure in current packet
```

Tracked at:

```text
docs/cmb_tau_lensing_projection_normalization_split_v01.md
data/derived/cmb_tau_lensing_projection_normalization_split_v01.json
```
