# Tau CMB Seed Support Domain Rule Candidate v01

**Doc class:** support-domain rule candidate
**Status:** SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_DECLARED_NOT_CERTIFIED

## Claim Boundary

```text
tau_cmb_seed_support_domain_rule_candidate_v01_rule_candidate_only_support_not_certified_no_payload_acceptance_no_domain_certificate_no_readout_no_score_no_verdict
```

## Purpose

This artifact declares a candidate support-domain rule for the CMB
`seed_tau` payload. It does not certify support, accept the payload, certify
`seed_tau_CMB in Dom(R_CMB)`, evaluate readout survival, assign `A_tau(a,k)`,
enter scoring, or decide the dark-sector question.

## Candidate Rule Shape

```text
Tau_CMB_parent_domain := {morphology_readout_sector = CMB}
xi_seed := (morphology_class, readout_sector, scale_label)
seed_tau_CMB in Tau_CMB_parent_domain iff xi_seed is well-formed and endpoint-blind
```

## Rows

- `TCMBSSDRC01_001` `parent_domain_symbol`: DECLARED_SYMBOL_NOT_CERTIFIED | `Tau_CMB_parent_domain := {morphology_readout_sector=CMB}`
- `TCMBSSDRC01_002` `support_coordinate_basis`: CANDIDATE_BASIS_DECLARED_NOT_ACCEPTED | `xi_seed := (morphology_class, readout_sector, scale_label)`
- `TCMBSSDRC01_003` `membership_rule`: MEMBERSHIP_RULE_DECLARED_NOT_PROVED | `seed_tau_CMB in Tau_CMB_parent_domain iff xi_seed is well-formed and endpoint-blind`
- `TCMBSSDRC01_004` `forbidden_endpoint_dependence`: FIREWALL_RULE_DECLARED_NOT_ACCEPTED | `xi_seed independent of O_CMB_endpoint`
- `TCMBSSDRC01_005` `normalization_dependency`: DEPENDENCY_DECLARED_NOT_EXECUTED | `N_seed may only act after xi_seed is fixed`
- `TCMBSSDRC01_006` `zero_control_dependency`: DEPENDENCY_DECLARED_NOT_EXECUTED | `null_seed in Tau_CMB_parent_domain uses same xi_seed convention`

## Status

```text
SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_DECLARED_NOT_CERTIFIED
```

The rule is useful because it gives normalization replay and zero-control a
shared parent-domain convention, but it remains uncertified until a support
audit checks well-formedness, hash/provenance binding, and endpoint blindness.

## Next Minimal Unblock

```text
tau_cmb_seed_support_domain_rule_candidate_audit_v01
```
