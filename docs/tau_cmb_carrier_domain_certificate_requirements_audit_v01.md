# Tau CMB Carrier Domain Certificate Requirements Audit v01

**Doc class:** carrier/domain certificate requirements audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED_NOT_SCORE_READY

## Claim Boundary

```text
tau_cmb_carrier_domain_certificate_requirements_audit_v01_audit_only_requirements_clean_but_carrier_not_certified_domain_not_certified_R_CMB_not_materialized_no_score_no_likelihood_no_verdict
```

## Purpose

This audit checks the finite carrier/domain certificate requirement set. It
verifies row shape, upstream lineage, field completeness, accounting, promotion
firewall closure, and claim-boundary discipline. It does not certify the
carrier, certify `Dom(R_CMB)`, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

- `requirement_row_shape`: PASS_EXPECTED_REQUIREMENT_ROWS_PRESENT | certificate_areas=['carrier_well_formedness', 'domain_membership_rule', 'seed_admissibility', 'null_control_admissibility', 'source_object_admissibility', 'quotient_and_equivalence_survival', 'codomain_compatibility', 'endpoint_firewall_replay']
- `input_chain`: PASS_REQUIREMENTS_INPUT_CHAIN | requirements follow the predicate audit and single-pass blocked route
- `requirement_fields_declared`: PASS_REQUIREMENT_FIELDS_DECLARED | each requirement row declares formal requirement, acceptance condition, evidence, and blocker
- `requirement_accounting`: PASS_REQUIREMENT_ACCOUNTING | requirement_rows=8, blocked_requirement_rows=8
- `promotion_firewall`: PASS_REQUIREMENTS_FIREWALL_CLOSED | carrier, domain, concrete R_CMB, score, likelihood, and verdict permissions remain closed
- `claim_boundary`: PASS_REQUIREMENTS_CLAIM_BOUNDARY | row claim boundaries mark the artifact as requirements-only with no score and no verdict
- `carrier_and_domain_certificate`: BLOCKED_CARRIER_AND_DOMAIN_CERTIFICATES_NOT_BUILT | CarrierOK and DomOK are finite requirements but no certificate object is built
- `seed_null_source_admissibility`: BLOCKED_ADMISSIBILITY_OBJECTS_NOT_ACCEPTED | seed, null control, and source objects remain admissibility requirements rather than accepted domain elements
- `quotient_and_codomain`: BLOCKED_QUOTIENT_SURVIVAL_AND_CODOMAIN_OUTPUT | non-null quotient survival and concrete role-codomain output are not yet proved
- `concrete_R_CMB_and_firewall`: BLOCKED_R_CMB_MATERIALIZATION_AND_FIREWALL | concrete R_CMB materialization and post-population endpoint firewall remain downstream

## Status

```text
CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED_NOT_SCORE_READY
```

The requirement set is audit-visible and internally clean, but still blocked.
The next object may be a certificate candidate; it still cannot open scoring.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_certificate_candidate_v01
```
