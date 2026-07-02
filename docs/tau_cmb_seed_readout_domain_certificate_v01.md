# Tau CMB Seed Readout Domain Certificate v01

**Doc class:** readout-domain certificate requirements
**Status:** SEED_READOUT_DOMAIN_CERTIFICATE_DECLARED_BLOCKED

## Claim Boundary

```text
tau_cmb_seed_readout_domain_certificate_v01_certificate_requirements_only_domain_not_certified_no_readout_evaluation_no_survival_no_A_tau_value_no_score_no_verdict
```

## Purpose

This artifact states what must be true before the CMB morphological seed can be
treated as a legitimate Tau-side input to `R_CMB`. It does not certify domain
membership, evaluate a readout, prove quotient survival, assign `A_tau(a,k)`,
enter scoring, or decide the dark-sector question.

## Certificate Target

```text
seed_tau_CMB in Dom(R_CMB)
```

The target is not accepted in v01 because the concrete seed payload, support
domain, domain rule, endpoint firewall, and zero-seed control are still absent.

## Certificate Rows

- `TCMBSRDC01_001` `seed_object_identity`: EVIDENCE_PARTIAL_DESCRIPTOR_ONLY | blocks: identity exists only as an unaccepted descriptor candidate, not as a supplied payload
- `TCMBSRDC01_002` `support_domain`: REQUIRED_SUPPORT_NOT_SUPPLIED | blocks: no support coordinates or parent-domain construction are supplied
- `TCMBSRDC01_003` `intrinsic_descriptor`: DECLARED_NOT_MATERIALIZED | blocks: no concrete descriptor fields are materialized in an accepted payload
- `TCMBSRDC01_004` `readout_domain_membership`: DOMAIN_RULE_NOT_DEFINED | blocks: Dom(R_CMB) is not constructed and no membership replay exists
- `TCMBSRDC01_005` `endpoint_firewall`: FIREWALL_EVIDENCE_NOT_SUPPLIED | blocks: no seed payload hash manifest, replay, or firewall attestation is supplied
- `TCMBSRDC01_006` `zero_seed_membership`: CONTROL_DOMAIN_NOT_DEFINED | blocks: null_seed and its domain membership are not defined

## Status

```text
SEED_READOUT_DOMAIN_CERTIFICATE_DECLARED_BLOCKED
```

The domain gate is useful because it prevents a premature jump from a named
seed descriptor to CMB scoring. The next real unblock is not another broad
gate; it is a populated endpoint-blind `seed_tau` payload with provenance,
hashes, replay, support convention, and firewall evidence.

## Next Minimal Unblock

```text
materialize_endpoint_blind_seed_tau_payload_with_provenance_and_firewall
```
