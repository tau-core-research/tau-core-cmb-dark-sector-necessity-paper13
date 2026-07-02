# Tau CMB Seed Payload Unblock Triad v01

**Doc class:** seed-payload unblock plan
**Status:** SEED_PAYLOAD_UNBLOCK_TRIAD_DECLARED_BLOCKED

## Claim Boundary

```text
tau_cmb_seed_payload_unblock_triad_v01_unblock_plan_only_no_payload_acceptance_no_domain_certificate_no_readout_no_survival_no_A_tau_value_no_score_no_verdict
```

## Purpose

This artifact collapses the three remaining seed-payload audit blockers into a
single ordered unblock triad. It does not accept the payload, certify the
readout domain, evaluate CMB readout survival, assign `A_tau(a,k)`, enter
scoring, or decide the dark-sector question.

## Dependency Order

```text
support coordinate system
-> Tau-side normalization replay
-> null-limit / zero-control
```

The support-domain rule must come first because both normalization and
zero-control need to refer to the same parent-domain convention.

## Rows

- `TCMBSPUT01_001` `support_coordinate_system`: BLOCKED_SUPPORT_DOMAIN_RULE_MISSING | next: `tau_cmb_seed_support_domain_rule_candidate_v01`
- `TCMBSPUT01_002` `tau_side_normalization_replay`: BLOCKED_WAITING_FOR_SUPPORT_DOMAIN | next: `tau_cmb_seed_normalization_replay_candidate_v01`
- `TCMBSPUT01_003` `null_limit_zero_control`: BLOCKED_WAITING_FOR_SUPPORT_AND_NORMALIZATION | next: `tau_cmb_seed_zero_control_v01`

## Status

```text
SEED_PAYLOAD_UNBLOCK_TRIAD_DECLARED_BLOCKED
```

## Next Minimal Unblock

```text
tau_cmb_seed_support_domain_rule_candidate_v01
```
