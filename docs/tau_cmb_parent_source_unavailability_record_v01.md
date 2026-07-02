# Tau CMB Parent-Source Unavailability Record v01

**Doc class:** CMB parent-source unavailability record
**Status:** PARENT_SOURCE_UNAVAILABILITY_RECORDED_CLEAN_NEGATIVE_AUDIT
**Source audit:** `data/derived/tau_cmb_parent_source_freeze_packet_submission_candidate_audit_v01.json`

## Claim Boundary

```text
tau_cmb_parent_source_unavailability_record_v01_record_only_no_physical_failure_claim_no_source_acceptance_no_phi_derivation_no_score_no_verdict
```

## Purpose

This artifact records the current stop-state after the freeze-packet submission
candidate audit. The audit found a clean negative candidate: required rows and
hashes are present and no endpoint-token hit is detected, but no populated
Tau-side source values are supplied.

This is not a physical failure claim. It only says that the repository does not
currently contain an acceptable endpoint-blind CMB parent-source payload.

## Unavailable Components

- `B_tau_base_CMB_descriptor`
- `seed_tau_CMB_descriptor`
- `R_tau_CMB_input_set`
- `gauge_norm_tau_CMB_metadata`
- `source_freeze_firewall_certificate`
- `freeze_packet_replay_rule`

## Interpretation

```text
The repository currently lacks the endpoint-blind CMB parent-source payload needed to accept the freeze packet. This is a source-availability blocker, not evidence that Tau Core fails CMB physics.
```

## Status

```text
PARENT_SOURCE_UNAVAILABILITY_RECORDED_CLEAN_NEGATIVE_AUDIT
```

No source may be accepted from this record. No `Phi_tau_eff` derivation, CMB
score, no-dark claim, Tau-response success claim, or dark-sector verdict is
allowed.

## Next Minimal Unblock

```text
supply_endpoint_blind_values_for_one_freeze_packet_component_or_keep_unavailability_record_as_stop_state
```
