# Tau CMB Seed Normalization Replay Candidate Audit v01

**Doc class:** seed normalization replay candidate audit
**Status:** SEED_NORMALIZATION_REPLAY_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_seed_normalization_replay_candidate_audit_v01_audit_only_normalization_not_accepted_no_support_certification_no_domain_certificate_no_readout_no_score_no_verdict
```

## Purpose

This audit checks whether the seed normalization replay candidate is
deterministic, endpoint-blind, and compatible with the support-domain rule
candidate. It does not accept normalization, certify support, certify domain
membership, evaluate readout survival, assign `A_tau(a,k)`, enter scoring, or
decide the dark-sector question.

## Audit Rows

- `normalization_table_shape`: PASS_NORMALIZATION_ROWS_PRESENT | components=['normalization_input_tuple', 'scale_label_canonicalization', 'normalized_seed_descriptor', 'forbidden_operations', 'zero_control_dependency']
- `canonical_mapping`: PASS_CANONICAL_MAPPING_DECLARED | candidate_not_normalized -> canonical_v01 mapping is present in table and replay
- `tuple_invariance`: PASS_TUPLE_INVARIANCE_DECLARED | replay keeps morphology class and readout sector fixed
- `endpoint_boundary`: PASS_ENDPOINT_BOUNDARY_DECLARED | firewall endpoint_inputs_used=[] and replay forbids endpoint inputs
- `support_rule_dependency`: PASS_SUPPORT_RULE_AUDITED_AS_CANDIDATE | support rule candidate audit has zero failures but remains uncertified
- `zero_control_dependency`: BLOCKED_ZERO_CONTROL_NOT_DEFINED | normalization correctly declares same-scale zero-control dependency
- `normalization_acceptance`: BLOCKED_NORMALIZATION_ACCEPTANCE_CLOSED | normalization candidate keeps acceptance permissions closed

## Status

```text
SEED_NORMALIZATION_REPLAY_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED
```

The normalization replay is now audited as a candidate, but acceptance remains
blocked because zero-control is not defined and normalization acceptance is a
separate later gate.

## Next Minimal Unblock

```text
tau_cmb_seed_zero_control_v01
```
