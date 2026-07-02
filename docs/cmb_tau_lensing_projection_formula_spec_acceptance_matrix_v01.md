# CMB Tau Lensing Projection Formula-Spec Acceptance Matrix v01

**Doc class:** formula-spec acceptance matrix
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocked until endpoint-blind operator packet is supplied; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
projection_formula_spec_acceptance_matrix_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict
```

## Target

```text
accepted endpoint-blind Projection_PP[Phi_lens_tau](L) formula-spec
```

## Acceptance Matrix

- `TCMBPFSAM01_001` `projection_equation`: PROJECTION_EQUATION_SPEC_DECLARED_NOT_FILLED | artifact: `docs/cmb_tau_lensing_projection_equation_spec_scaffold_v01.md` | blocks: physical Tau-grid materialization and score
- `TCMBPFSAM01_002` `kernel_measure`: KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED | artifact: `docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md` | blocks: finite PP-grid replay
- `TCMBPFSAM01_003` `normalization`: NORMALIZATION_SPEC_DECLARED_NOT_FILLED | artifact: `docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md` | blocks: accepted physical projection operator packet
- `TCMBPFSAM01_004` `output_replay`: OUTPUT_REPLAY_SPEC_DECLARED_NOT_FILLED | artifact: `docs/cmb_tau_lensing_projection_output_replay_spec_scaffold_v01.md` | blocks: score input handoff
- `TCMBPFSAM01_005` `zero_source_limit`: PROOF_OBLIGATION_DECLARED_NOT_DISCHARGED | artifact: `docs/cmb_tau_lensing_projection_zero_source_limit_obligation_v01.md` | blocks: known-limit and null-control acceptance
- `TCMBPFSAM01_006` `dimension_sign_audit`: AUDIT_SCHEMA_DECLARED_NOT_FILLED | artifact: `docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md` | blocks: review-safe operator acceptance
- `TCMBPFSAM01_007` `post_population_firewall`: POST_POPULATION_FIREWALL_SPEC_DECLARED_NOT_RUN | artifact: `docs/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_v01.md` | blocks: endpoint-blind score attempt

## Only Valid Next Paths

- `SUPPLY_ENDPOINT_BLIND_OPERATOR_PACKET`
- `KEEP_EXPLICIT_NON_SCORE_FAILURE`

## Endpoint-Blind Operator Packet Request

```text
docs/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.md
```

## Blocked Shortcuts

- do not score from the scaffold
- do not use post-score alpha_star as physical normalization
- do not use B_ACT adapter replay as the physical source-to-PP operator
- do not issue a dark-sector verdict before an accepted score route exists
