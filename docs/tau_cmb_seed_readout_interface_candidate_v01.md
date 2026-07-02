# Tau CMB Seed Readout Interface Candidate v01

**Doc class:** readout-interface candidate scaffold
**Status:** SEED_READOUT_INTERFACE_CANDIDATE_DECLARED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_seed_readout_interface_candidate_v01_interface_schema_only_no_readout_evaluation_no_quotient_survival_no_seed_acceptance_no_A_tau_value_no_score_no_verdict
```

## Purpose

This artifact declares the minimum interface that would let the CMB
morphological seed enter a quotient/null survival test. It is a schema-level
candidate only: it does not evaluate a readout, prove survival, accept the seed,
assign `A_tau(a,k)`, enter scoring, or decide whether a Tau dark-sector
component is necessary.

## Candidate Interface Shape

```text
seed_tau_CMB in Dom(R_CMB)
R_CMB(seed_tau_CMB) -> CMB_role_space
R_CMB(seed_tau_CMB) ~ N_R^CMB is the later quotient/null comparison
```

## Interface Rows

- `TCMBSRIC01_001` `readout_domain`: DECLARED_SCHEMA_NOT_PROVED | blocks: no concrete Tau-side domain construction is supplied
- `TCMBSRIC01_002` `readout_codomain`: DECLARED_SCHEMA_NOT_MATERIALIZED | blocks: no basis, units, or transfer normalization for the role space is supplied
- `TCMBSRIC01_003` `endpoint_blindness`: REQUIRED_FIREWALL_NOT_PROVED | blocks: no replay certificate shows endpoint independence for this interface
- `TCMBSRIC01_004` `null_model_hook`: HOOK_DECLARED_NULL_NOT_SUPPLIED | blocks: no null model or equivalence relation is supplied
- `TCMBSRIC01_005` `dimension_role`: REQUIRED_DIMENSION_PROOF_NOT_SUPPLIED | blocks: no formula-level dimensional replay exists for the readout interface
- `TCMBSRIC01_006` `zero_seed_control_hook`: CONTROL_HOOK_DECLARED_NOT_PROVED | blocks: null_seed, null_readout, and zero-preserving replay are missing

## Status

```text
SEED_READOUT_INTERFACE_CANDIDATE_DECLARED_NOT_ACCEPTED
```

The interface is route-useful but not acceptance-useful. The next concrete
unblock is a domain certificate showing that `seed_tau_CMB` is a legitimate
Tau-side object in the domain of `R_CMB` without endpoint input.

## Next Minimal Unblock

```text
tau_cmb_seed_readout_domain_certificate_v01
```
