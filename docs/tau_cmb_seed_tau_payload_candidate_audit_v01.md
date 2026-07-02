# Tau CMB Seed Tau Payload Candidate Audit v01

**Doc class:** endpoint-blind seed payload candidate audit
**Status:** SEED_TAU_PAYLOAD_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_seed_tau_payload_candidate_audit_v01_audit_only_payload_not_accepted_no_domain_certificate_no_readout_no_survival_no_A_tau_value_no_score_no_verdict
```

## Purpose

This audit checks whether the materialized `seed_tau` payload candidate is
present, hash-bound, replayable, and endpoint-firewall clean as a candidate. It
does not accept the payload, certify the readout domain, evaluate quotient
survival, assign `A_tau(a,k)`, enter scoring, or decide the dark-sector
question.

## Audit Rows

- `payload_presence`: PASS_CANDIDATE_PRESENT | 1 payload row(s) present
- `hash_manifest`: PASS_HASHES_MATCH | payloads/seed_tau_payload_candidate_v01.csv expected=512c2f923cb1c85eeee80baf4efd12bb3f1814453fff99bfbdd12166bc8c5fb6 actual=512c2f923cb1c85eeee80baf4efd12bb3f1814453fff99bfbdd12166bc8c5fb6 ok=True; payloads/seed_tau_payload_candidate_v01.provenance.json expected=7caef7a0d945a7bf2e8cc61ce51dfba3a2acfac50e5697185d8b6a63527528ea actual=7caef7a0d945a7bf2e8cc61ce51dfba3a2acfac50e5697185d8b6a63527528ea ok=True; payloads/seed_tau_payload_candidate_v01.replay.txt expected=71e3530f66ae4c995399415e0b10f7e999d09b727195638c519b0f41108929a8 actual=71e3530f66ae4c995399415e0b10f7e999d09b727195638c519b0f41108929a8 ok=True; payloads/seed_tau_payload_candidate_v01.firewall.json expected=635a7b0dc25c577a391b2b2b78a8d038d2510c68c8ea0a0a39738444b34e58da actual=635a7b0dc25c577a391b2b2b78a8d038d2510c68c8ea0a0a39738444b34e58da ok=True
- `provenance_boundary`: PASS_PROVENANCE_BOUNDARY_CLOSED | provenance links payload and keeps acceptance permissions closed
- `replay_presence`: PASS_REPLAY_DECLARED | replay command declares deterministic candidate rebuild
- `endpoint_firewall_candidate`: PASS_CANDIDATE_FIREWALL_ATTESTED_NOT_ACCEPTED | endpoint_inputs_used=[]; textual_token_hits=['ACT residual', 'Planck residual', 'CMB role score', 'likelihood delta', 'peak residual shape', 'lensing residual direction', 'score output', 'post-endpoint tuning']
- `dimension_and_normalization`: BLOCKED_NORMALIZATION_REPLAY_MISSING | dimension role is declared, but normalization replay remains pending
- `support_convention`: BLOCKED_SUPPORT_COORDINATE_NOT_CONCRETE | support is a sector label, not a concrete support coordinate system
- `null_limit_role`: BLOCKED_NULL_LIMIT_NOT_DEFINED | null-limit role is explicitly required but not defined

## Status

```text
SEED_TAU_PAYLOAD_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED
```

Candidate-level evidence is now present, but acceptance remains blocked by
missing concrete support coordinates, Tau-side normalization replay, and
null-limit/zero-control definitions.

## Next Minimal Unblock

```text
define_seed_support_coordinates_normalization_replay_and_null_limit_role
```
