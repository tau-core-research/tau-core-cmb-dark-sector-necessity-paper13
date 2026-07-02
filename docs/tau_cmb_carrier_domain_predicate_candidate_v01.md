# Tau CMB Carrier Domain Predicate Candidate v01

**Doc class:** carrier/domain predicate candidate
**Status:** CARRIER_DOMAIN_PREDICATE_CANDIDATE_DECLARED_NOT_CERTIFIED

## Claim Boundary

```text
tau_cmb_carrier_domain_predicate_candidate_v01_candidate_only_carrier_not_certified_domain_not_certified_R_CMB_not_materialized_no_score_no_verdict
```

## Purpose

This artifact declares a candidate carrier/domain predicate for the CMB readout
route. It does not certify the carrier, certify `Dom(R_CMB)`, materialize
`R_CMB`, open score entry, or decide the dark-sector question.

## Predicate Rows

- `carrier_membership`: CANDIDATE_DECLARED_NOT_CERTIFIED | `x in C_CMB^seed iff WellFormedRoleRepresentative_CMB(x)`
- `domain_membership`: CANDIDATE_DECLARED_DOMAIN_NOT_CERTIFIED | `x in Dom(R_CMB) iff ParentSideCMBObject(x) and SupportOK(x) and NormalizationOK(x) and FirewallOK(x)`
- `null_control_admissibility`: CANDIDATE_DECLARED_NULL_NOT_ACCEPTED | `null_seed_tau_CMB in Dom(R_CMB) and R_CMB(null_seed_tau_CMB) = null_readout`
- `source_object_admissibility`: CANDIDATE_DECLARED_SOURCE_OBJECTS_NOT_ACCEPTED | `source_tau_CMB in Dom(R_CMB) only if endpoint_blind_source_object(source_tau_CMB)`
- `forbidden_endpoint_dependency`: FIREWALL_RULE_DECLARED_NOT_REPLAYED | `not UsesEndpointResidualsOrScores(x)`

## Status

```text
CARRIER_DOMAIN_PREDICATE_CANDIDATE_DECLARED_NOT_CERTIFIED
```

The candidate narrows what carrier/domain certification must mean, but all
certification permissions remain closed.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_predicate_candidate_audit_v01
```
