# Tau CMB Morphological Seed Activation Rule Candidate v01

**Doc class:** morphological-seed activation rule candidate
**Status:** MORPHOLOGICAL_SEED_ACTIVATION_RULE_CANDIDATE_DECLARED_NOT_DERIVED

## Claim Boundary

```text
tau_cmb_morphological_seed_activation_rule_candidate_v01_rule_candidate_only_no_activation_proof_no_A_tau_value_no_source_acceptance_no_phi_derivation_no_score_no_verdict
```

## Purpose

This artifact declares the smallest conditional activation-rule skeleton from a
CMB morphological seed toward a possible `A_tau(a,k)` candidate. It does not
derive `A_tau`, supply an amplitude, accept the seed, or accept a source.

## Candidate Rule Skeleton

```text
seed_tau_CMB in Dom(Act_tau_CMB)
Act_tau_CMB[seed_tau_CMB](a,k) -> A_tau_candidate(a,k)
```

The skeleton is only meaningful if quotient/null survival, closure stability,
readout survival, gauge/normalization, and firewall/replay certificates are
later supplied.

## Rule Rows

- `TCMBMSARC01_001` `activation_domain`: DOMAIN_DECLARED_NOT_ACCEPTED | `seed_tau_CMB in Dom(Act_tau_CMB)`
- `TCMBMSARC01_002` `conditional_activation_map`: MAP_SKELETON_DECLARED_NOT_DERIVED | `Act_tau_CMB[seed_tau_CMB](a,k) -> A_tau_candidate(a,k)`
- `TCMBMSARC01_003` `zero_seed_limit`: LIMIT_REQUIRED_NOT_PROVED | `seed_tau_CMB = null_seed => A_tau_candidate(a,k) = 0 or inactive`
- `TCMBMSARC01_004` `endpoint_blindness_constraint`: FIREWALL_CONSTRAINT_DECLARED_NOT_CERTIFIED | `Act_tau_CMB independent of endpoint residuals and scores`
- `TCMBMSARC01_005` `spine_binding`: BINDING_DECLARED_NOT_ACCEPTED | `A_tau_candidate(a,k) -> rho_tau_eff(a,k) role slot only after acceptance`

## Status

```text
MORPHOLOGICAL_SEED_ACTIVATION_RULE_CANDIDATE_DECLARED_NOT_DERIVED
```

No activation acceptance, `A_tau(a,k)` value, source acceptance, `Phi_tau_eff`
derivation, score entry, or dark-sector verdict is allowed.

## Next Minimal Unblock

```text
audit_tau_cmb_morphological_seed_activation_rule_candidate_v01
```
