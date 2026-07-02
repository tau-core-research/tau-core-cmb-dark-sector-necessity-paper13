# Tau CMB Seed Tau Payload Candidate v01

**Doc class:** endpoint-blind seed payload candidate
**Status:** SEED_TAU_PAYLOAD_CANDIDATE_MATERIALIZED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_seed_tau_payload_candidate_v01_concrete_candidate_only_not_accepted_no_domain_certificate_no_readout_evaluation_no_survival_no_A_tau_value_no_score_no_verdict
```

## Purpose

This artifact materializes a concrete `seed_tau` candidate payload from the
Tau-side morphological seed descriptor candidate. It is not accepted, does not
certify `seed_tau_CMB in Dom(R_CMB)`, does not evaluate CMB readout survival,
does not assign `A_tau(a,k)`, and does not enter scoring.

## Produced Candidate Files

- payload: `payloads/seed_tau_payload_candidate_v01.csv`
- provenance: `payloads/seed_tau_payload_candidate_v01.provenance.json`
- replay: `payloads/seed_tau_payload_candidate_v01.replay.txt`
- hashes: `payloads/seed_tau_payload_candidate_v01.hashes.json`
- firewall: `payloads/seed_tau_payload_candidate_v01.firewall.json`

## Status

```text
SEED_TAU_PAYLOAD_CANDIDATE_MATERIALIZED_NOT_ACCEPTED
```

The payload is now concrete enough to audit, but all acceptance permissions
remain closed until provenance, hash binding, endpoint firewall, dimension
roles, support convention, and zero-control evidence pass separate audit.

## Next Minimal Unblock

```text
audit_seed_tau_payload_candidate_provenance_hashes_firewall_and_dimension_roles
```
