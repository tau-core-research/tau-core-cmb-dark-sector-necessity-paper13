# Tau CMB Seed Chain Pre-Acceptance Gate v01

**Doc class:** seed-chain pre-acceptance gate
**Status:** SEED_CHAIN_PRE_ACCEPTANCE_GATE_CLEAN_BLOCKED_ON_READOUT_QUOTIENT

## Claim Boundary

```text
tau_cmb_seed_chain_pre_acceptance_gate_v01_pre_acceptance_only_clean_audit_chain_not_accepted_no_domain_certificate_no_concrete_R_CMB_no_quotient_no_score_no_verdict
```

## Purpose

This gate checks whether the seed support-domain rule audit, normalization
replay audit, and zero-control audit form a clean candidate chain. It does not
accept the seed, certify a domain, define concrete `R_CMB`, prove quotient
survival, enter scoring, or decide the dark-sector question.

## Gate Rows

- `TCMBSCPAG01_001` `data/derived/tau_cmb_seed_support_domain_rule_candidate_audit_v01.json`: PASS_CLEAN_BLOCKED_AUDIT_INPUT | SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_AUDITED_BLOCKED_NOT_CERTIFIED
- `TCMBSCPAG01_002` `data/derived/tau_cmb_seed_normalization_replay_candidate_audit_v01.json`: PASS_CLEAN_BLOCKED_AUDIT_INPUT | SEED_NORMALIZATION_REPLAY_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED
- `TCMBSCPAG01_003` `data/derived/tau_cmb_seed_zero_control_audit_v01.json`: PASS_CLEAN_BLOCKED_AUDIT_INPUT | SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED

## Decision

```text
seed_chain_audit_clean = true
chain_pre_acceptance_allowed = true
status = SEED_CHAIN_PRE_ACCEPTANCE_GATE_CLEAN_BLOCKED_ON_READOUT_QUOTIENT
```

The chain is clean at audit level when all required input audits have zero
failed rows and the expected non-accepted/non-certified status. This is only a
pre-acceptance condition. It does not remove the readout/quotient blockers.

## Remaining Blockers

- `concrete_R_CMB_missing`
- `quotient_equivalence_relation_missing`
- `domain_certificate_acceptance_missing`
- `score_entry_closed`

## Next Minimal Unblock

```text
tau_cmb_seed_readout_quotient_relation_candidate_v01
```
