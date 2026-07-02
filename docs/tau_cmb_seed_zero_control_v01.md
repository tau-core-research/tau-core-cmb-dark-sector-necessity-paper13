# Tau CMB Seed Zero Control v01

**Doc class:** zero-control candidate
**Status:** SEED_ZERO_CONTROL_DECLARED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_seed_zero_control_v01_control_candidate_only_zero_control_not_accepted_no_physical_response_no_domain_certificate_no_readout_no_score_no_verdict
```

## Purpose

This artifact declares the null-seed / zero-control side required by the CMB
seed route. It does not accept zero-control, claim a physical Tau response,
certify domain membership, evaluate readout, enter scoring, or decide the
dark-sector question.

## Control Replay

```text
payloads/seed_tau_zero_control_v01.replay.txt
```

## Rows

- `TCMBSZC01_001` `null_seed_definition`: NULL_SEED_DECLARED_NOT_ACCEPTED | `null_seed_tau_CMB := (null_morphology_control, CMB_readout_sector, canonical_scale_v01)`
- `TCMBSZC01_002` `same_domain_convention`: DOMAIN_CONTROL_DECLARED_NOT_CERTIFIED | `null_seed in Tau_CMB_parent_domain`
- `TCMBSZC01_003` `inactive_activation`: INACTIVE_ACTIVATION_DECLARED_NOT_PROVED | `Act_tau_CMB[null_seed](a,k) := 0 or inactive`
- `TCMBSZC01_004` `null_readout_role`: NULL_READOUT_DECLARED_NOT_EVALUATED | `R_CMB(null_seed) := null_readout`
- `TCMBSZC01_005` `forbidden_promotion`: PROMOTION_FORBIDDEN_DECLARED | `null_seed != physical Tau response`
- `TCMBSZC01_006` `quotient_survival_dependency`: QUOTIENT_NULL_SIDE_DECLARED_NOT_PROVED | `Null_R(seed_tau_CMB) iff R_CMB(seed_tau_CMB) ~ R_CMB(null_seed)`

## Status

```text
SEED_ZERO_CONTROL_DECLARED_NOT_ACCEPTED
```

The zero-control is now declared as a candidate control object over the same
support and canonical scale convention. It remains unaccepted until an audit
checks same-domain convention, inactive activation, null-readout role, and
forbidden promotion.

## Next Minimal Unblock

```text
tau_cmb_seed_zero_control_audit_v01
```
