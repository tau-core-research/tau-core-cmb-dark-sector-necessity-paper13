# CMB Tau Lensing Physical Projection Replay Requirement v01

**Doc class:** physical projection replay requirement
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocked; operator and normalization not supplied
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
physical_projection_replay_requirement_only_no_replay_no_score_no_dark_sector_verdict
```

## Distinction

```text
adapter replay:
B_ACT @ already materialized grid -> 18-vector; implemented by materialize-replay

physical projection replay:
Phi_lens_tau plus Projection_PP operator plus N_projection_physical -> 3000-row tau_PP or delta_PP grid
```

The current `materialize-replay` target covers adapter replay only. A physical
projection replay requires the physics-side operator and normalization first.

## Required Inputs

- accepted projection_domain row
- accepted projection_codomain row
- accepted projection_operator_rule row
- accepted projection_normalization row
- endpoint firewall certificate for populated values

## Required Replay Contents

- input source artifact paths and hashes
- operator rule artifact path and hash
- normalization artifact path/value/range and hash
- output grid path and sha256
- L alignment L=10..3009
- zero-source known-limit check
- claim boundary no score/no verdict

## Spec Scaffold Links

- `docs/cmb_tau_lensing_projection_output_replay_spec_scaffold_v01.md`
- `data/derived/cmb_tau_lensing_projection_output_replay_spec_scaffold_v01.csv`

## Current Decision

```text
PHYSICAL_REPLAY_NOT_MATERIALIZABLE_YET
```
