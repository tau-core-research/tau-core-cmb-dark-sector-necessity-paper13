# Tau CMB Carrier Domain Predicate Candidate Audit v01

**Doc class:** carrier/domain predicate candidate audit
**Status:** CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDITED_BLOCKED_NOT_SCORE_READY

## Claim Boundary

```text
tau_cmb_carrier_domain_predicate_candidate_audit_v01_audit_only_predicate_shape_clean_but_carrier_not_certified_domain_not_certified_R_CMB_not_materialized_no_score_no_verdict
```

## Purpose

This audit checks the candidate carrier/domain predicate for the CMB readout
route. It verifies predicate-row shape, upstream certificate-audit lineage,
field completeness, accounting, promotion-firewall closure, and claim-boundary
discipline. It does not certify the carrier, certify `Dom(R_CMB)`, materialize
`R_CMB`, open score entry, or decide the dark-sector question.

## Audit Rows

- `predicate_row_shape`: PASS_EXPECTED_PREDICATE_ROWS_PRESENT | predicate_components=['carrier_membership', 'domain_membership', 'null_control_admissibility', 'source_object_admissibility', 'forbidden_endpoint_dependency']
- `input_certificate_chain`: PASS_CERTIFICATE_AUDIT_CHAIN | predicate candidate follows the audited concrete R_CMB carrier-certificate requirements
- `predicate_fields_declared`: PASS_PREDICATE_FIELDS_DECLARED | each predicate row declares formal predicate, candidate rule, evidence, and blocker
- `candidate_accounting`: PASS_CANDIDATE_ACCOUNTING | predicate_rows=5, candidate_rows=4, firewall_rows=1
- `promotion_firewall`: PASS_PREDICATE_FIREWALL_CLOSED | carrier, domain, concrete R_CMB, score, and verdict permissions remain closed
- `claim_boundary`: PASS_CANDIDATE_CLAIM_BOUNDARY | row claim boundaries mark the artifact as candidate-only with no score and no verdict
- `carrier_certificate`: BLOCKED_CARRIER_PREDICATE_NOT_PROVED | WellFormedRoleRepresentative_CMB is declared but not proved as a carrier certificate
- `domain_certificate`: BLOCKED_DOMAIN_RULE_NOT_CERTIFIED | Dom(R_CMB) requires support, normalization, firewall, and replay evidence not yet certified jointly
- `concrete_readout_map`: BLOCKED_R_CMB_NOT_MATERIALIZED | predicate audit does not materialize a concrete CMB readout map
- `source_object_and_null_admissibility`: BLOCKED_SOURCE_AND_NULL_OBJECTS_NOT_ACCEPTED | source objects and null control remain candidate/admissibility rules rather than accepted domain elements

## Status

```text
CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDITED_BLOCKED_NOT_SCORE_READY
```

The predicate candidate is audit-visible and internally clean, but still
blocked. It narrows the next proof obligation to a carrier/domain certificate
requirements artifact.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_certificate_requirements_v01
```
