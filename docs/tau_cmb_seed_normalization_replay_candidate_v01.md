# Tau CMB Seed Normalization Replay Candidate v01

**Doc class:** seed normalization replay candidate
**Status:** SEED_NORMALIZATION_REPLAY_CANDIDATE_DECLARED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_seed_normalization_replay_candidate_v01_replay_candidate_only_normalization_not_accepted_no_support_certification_no_domain_certificate_no_readout_no_score_no_verdict
```

## Purpose

This artifact declares a deterministic Tau-side normalization replay candidate
for the CMB `seed_tau` support tuple. It does not accept normalization, certify
support, accept the payload, certify the readout domain, evaluate readout
survival, assign `A_tau(a,k)`, enter scoring, or decide the dark-sector
question.

## Replay

```text
payloads/seed_tau_normalization_replay_candidate_v01.txt
```

## Rows

- `TCMBSNRC01_001` `normalization_input_tuple`: INPUT_TUPLE_DECLARED_NOT_ACCEPTED | `xi_seed_raw`
- `TCMBSNRC01_002` `scale_label_canonicalization`: CANONICAL_LABEL_DECLARED_NOT_ACCEPTED | `CMB_readout_sector_scale_label_canonical_v01`
- `TCMBSNRC01_003` `normalized_seed_descriptor`: NORMALIZED_DESCRIPTOR_DECLARED_NOT_ACCEPTED | `normalized_seed_tau_CMB_candidate_v01`
- `TCMBSNRC01_004` `forbidden_operations`: FIREWALL_DEPENDENCY_DECLARED_NOT_ACCEPTED | `forbidden_endpoint_inputs_not_used`
- `TCMBSNRC01_005` `zero_control_dependency`: DEPENDENCY_DECLARED_NOT_EXECUTED | `zero_control_pending_same_scale_convention`

## Status

```text
SEED_NORMALIZATION_REPLAY_CANDIDATE_DECLARED_NOT_ACCEPTED
```

The candidate removes ambiguity from the scale-label route, but it remains
unaccepted until an audit checks endpoint blindness, payload/hash consistency,
and compatibility with the support-domain rule.

## Next Minimal Unblock

```text
tau_cmb_seed_normalization_replay_candidate_audit_v01
```
