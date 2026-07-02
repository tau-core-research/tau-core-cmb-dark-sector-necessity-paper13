# Tau CMB Carrier Domain Certificate Candidate v01

**Doc class:** carrier/domain certificate candidate
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_DECLARED_UNPASSED
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_carrier_domain_certificate_candidate_v01_candidate_only_certificates_declared_unpassed_domain_unaccepted_R_CMB_not_materialized_no_score_no_likelihood_no_verdict
```

## Purpose

This artifact declares candidate certificate objects for `CarrierOK`,
`DomOK`, seed/null/source admissibility, quotient survival, codomain
compatibility, and endpoint-firewall replay. It does not pass the certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Candidate Certificate Rows

- `carrier_well_formedness`: CANDIDATE_DECLARED_CARRIER_CERTIFICATE_UNPASSED | `CarrierOK_candidate(x)` | blocks: CarrierOK_candidate is not proved or executable
- `domain_membership_rule`: CANDIDATE_DECLARED_DOMAIN_CERTIFICATE_UNPASSED | `DomOK_candidate(x)` | blocks: DomOK_candidate has no joint pass certificate
- `seed_admissibility`: CANDIDATE_DECLARED_SEED_ADMISSIBILITY_UNPASSED | `SeedInDomain_candidate(seed_tau_CMB)` | blocks: seed is not accepted as an in-domain object
- `null_control_admissibility`: CANDIDATE_DECLARED_NULL_CONTROL_UNPASSED | `NullControlInDomain_candidate(null_seed_tau_CMB)` | blocks: null control is not accepted as materialized in-domain control
- `source_object_admissibility`: CANDIDATE_DECLARED_SOURCE_OBJECT_UNPASSED | `SourceObjectInDomain_candidate(source_tau_CMB)` | blocks: no endpoint-blind source object certificate exists
- `quotient_and_equivalence_survival`: CANDIDATE_DECLARED_QUOTIENT_SURVIVAL_UNPASSED | `QuotientSurvival_candidate([x])` | blocks: non-null survival and representative independence are not proved
- `codomain_compatibility`: CANDIDATE_DECLARED_CODOMAIN_OUTPUT_UNPASSED | `CodomainOK_candidate(R_CMB(x))` | blocks: no concrete R_CMB output can be checked yet
- `endpoint_firewall_replay`: CANDIDATE_DECLARED_FIREWALL_UNPASSED | `EndpointBlindCarrierDomain_candidate` | blocks: endpoint firewall requires populated values and replay trace

## Status

```text
CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_DECLARED_UNPASSED
```

The route now has concrete candidate certificate names and payload slots, but
all pass/acceptance flags remain false.

## Next Minimal Unblock

```text
audit_tau_cmb_carrier_domain_certificate_candidate_v01
```
