# Tau CMB Parent-Source Freeze Packet v01

**Doc class:** endpoint-blind CMB parent-source freeze packet
**Reader role:** Paper 13 / Tau CMB implementer
**Status:** declared but unpopulated; no source acceptance, no score, no verdict
**Source-grounding gate:** `docs/tau_cmb_source_grounding_gate_v01.md`
**Parent-input manifest:** `docs/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.md`
**Derivation spine:** `docs/tau_cmb_cosmology_derivation_spine_v01.md`
**Submission template:** `payload_templates/tau_cmb_parent_source_freeze_packet_submission_TEMPLATE_v01.csv`

## Claim Boundary

```text
tau_cmb_parent_source_freeze_packet_v01_freeze_packet_only_no_source_acceptance_no_phi_derivation_no_transfer_kernel_no_score_no_verdict
```

## Purpose

This packet is the first concrete source-freeze object under the CMB
source-grounding gate. It specifies what must be frozen before a Tau-side CMB
source can be considered for

```text
rho_tau_eff(a,k) -> Phi_tau_eff(a,k).
```

It does not populate those values. It does not accept a source. It does not
derive `Phi_tau_eff`, `T_tau_CMB`, or `K_tau_PP`, and it does not permit a score.

## Frozen Fields

- `TCMBPSF01_001` `freeze_packet_identity`: FREEZE_PACKET_DECLARED_NOT_ACCEPTED | freeze: `CMB_parent_source_freeze_packet_v01` | blocks: packet is not populated with accepted parent-side source records
- `TCMBPSF01_002` `base_field_state`: REQUIRED_NOT_SUPPLIED | freeze: `B_tau_base^CMB` | blocks: no concrete base-field descriptor is supplied
- `TCMBPSF01_003` `morphological_seed`: REQUIRED_NOT_SUPPLIED | freeze: `seed_tau^CMB` | blocks: no accepted morphology/seed descriptor is supplied
- `TCMBPSF01_004` `response_operator_input`: REQUIRED_NOT_SUPPLIED | freeze: `R_tau^CMB input set` | blocks: no replayable response-operator input set is supplied
- `TCMBPSF01_005` `gauge_normalization_metadata`: REQUIRED_NOT_LOCKED | freeze: `gauge_norm_tau^CMB` | blocks: metadata are not locked and audited
- `TCMBPSF01_006` `endpoint_firewall_certificate`: REQUIRED_NOT_EXECUTED | freeze: `source_freeze_firewall_certificate` | blocks: no packet-level endpoint firewall certificate is supplied
- `TCMBPSF01_007` `provenance_replay_rule`: REQUIRED_NOT_SUPPLIED | freeze: `freeze_packet_replay_rule` | blocks: no executable replay rule or hash certificate is supplied

## Forbidden Endpoint Inputs

The packet must not read or encode:

```text
ACT residuals
Planck residuals
CMB role score outputs
fit-improvement flags
post-hoc source choices
operator tuning from endpoint target shape
```

## Status

```text
PARENT_SOURCE_FREEZE_PACKET_DECLARED_UNPOPULATED
```

The packet is intentionally unpopulated in v01. Its value is that it turns the
next step into a finite deliverable: supply the frozen base-field state,
morphological seed, response-operator inputs, gauge/normalization metadata,
firewall certificate, and replay rule before any scoring route is opened.

The concrete submission shape is:

```text
payload_templates/tau_cmb_parent_source_freeze_packet_submission_TEMPLATE_v01.csv
```

The current replayable negative candidate is:

```text
payloads/tau_cmb_parent_source_freeze_packet_submission_candidate_v01.csv
```

## Next Minimal Unblock

```text
populate_endpoint_blind_CMB_parent_source_freeze_packet_with_hashable_replay
```
