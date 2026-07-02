# Tau CMB Carrier Domain Certificate Requirements v01

**Doc class:** carrier/domain certificate requirements
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_carrier_domain_certificate_requirements_v01_requirements_only_carrier_not_certified_domain_not_certified_R_CMB_not_materialized_no_score_no_verdict
```

## Purpose

This artifact turns the carrier/domain predicate candidate into a finite
certificate requirement set. It does not certify the carrier, certify
`Dom(R_CMB)`, materialize `R_CMB`, open score entry, compute a likelihood, or
decide the dark-sector question.

## Certificate Requirement Rows

- `carrier_well_formedness`: REQUIREMENT_DECLARED_CARRIER_NOT_CERTIFIED | `CarrierOK(x) := WellFormedRoleRepresentative_CMB(x) and RoleTyped_CMB(x)` | blocks: no accepted CarrierOK proof/checker exists
- `domain_membership_rule`: REQUIREMENT_DECLARED_DOMAIN_NOT_CERTIFIED | `DomOK(x) := ParentSideCMBObject(x) and SupportOK(x) and NormalizationOK(x) and FirewallOK(x)` | blocks: no joint DomOK certificate exists
- `seed_admissibility`: REQUIREMENT_DECLARED_SEED_NOT_ACCEPTED | `seed_tau_CMB in Dom(R_CMB) only if SeedDescriptorOK and ActivationOK and QuotientSurvivalOK` | blocks: quotient survival and accepted activation are not proved
- `null_control_admissibility`: REQUIREMENT_DECLARED_NULL_NOT_ACCEPTED | `null_seed_tau_CMB in Dom(R_CMB) and R_CMB(null_seed_tau_CMB) = null_readout` | blocks: null domain membership and null readout materialization are missing
- `source_object_admissibility`: REQUIREMENT_DECLARED_SOURCE_OBJECTS_NOT_ACCEPTED | `source_tau_CMB in Dom(R_CMB) only if endpoint_blind_source_object(source_tau_CMB)` | blocks: no endpoint-blind source object derivation is accepted
- `quotient_and_equivalence_survival`: REQUIREMENT_DECLARED_QUOTIENT_SURVIVAL_NOT_PROVED | `[x]_~ != [null] and R_CMB respects the declared equivalence relation` | blocks: no non-null survival certificate exists for domain objects
- `codomain_compatibility`: REQUIREMENT_DECLARED_CODOMAIN_PARTIAL | `R_CMB(x) in V_CMB^roles with acoustic/density/lensing/growth/radiation/null typing` | blocks: role codomain is audit-visible but not yet a concrete output target
- `endpoint_firewall_replay`: REQUIREMENT_DECLARED_FIREWALL_NOT_REPLAYED | `not UsesEndpointResidualsOrScores(x, CarrierOK, DomOK)` | blocks: endpoint firewall requires populated values

## Status

```text
CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED
```

The shortest path to a concrete `R_CMB` now requires discharging these
carrier/domain certificate requirements. All scoring and verdict permissions
remain closed.

## Next Minimal Unblock

```text
audit_tau_cmb_carrier_domain_certificate_requirements_v01
```
