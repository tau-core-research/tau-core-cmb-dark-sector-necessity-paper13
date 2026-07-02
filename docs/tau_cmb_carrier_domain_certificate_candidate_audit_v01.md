# Tau CMB Carrier Domain Certificate Candidate Audit v01

**Doc class:** carrier/domain certificate candidate audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_AUDITED_UNPASSED_NOT_SCORE_READY

## Claim Boundary

```text
tau_cmb_carrier_domain_certificate_candidate_audit_v01_audit_only_candidate_shape_clean_but_certificates_unpassed_domain_unaccepted_R_CMB_not_materialized_no_score_no_likelihood_no_verdict
```

## Purpose

This audit checks the carrier/domain certificate candidate. It verifies row
shape, upstream lineage, payload-slot completeness, accounting, promotion
firewall closure, and claim-boundary discipline. It does not pass certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

- `candidate_row_shape`: PASS_EXPECTED_CANDIDATE_ROWS_PRESENT | certificate_areas=['carrier_well_formedness', 'domain_membership_rule', 'seed_admissibility', 'null_control_admissibility', 'source_object_admissibility', 'quotient_and_equivalence_survival', 'codomain_compatibility', 'endpoint_firewall_replay']
- `input_requirements_chain`: PASS_CANDIDATE_INPUT_CHAIN | candidate follows the audited carrier/domain certificate requirements
- `candidate_fields_declared`: PASS_CANDIDATE_FIELDS_DECLARED | each candidate row declares object, content, required payload, current payload, and blocker
- `candidate_accounting`: PASS_CANDIDATE_ACCOUNTING | candidate_rows=8, declared=8, carrier_passed=0, domain_passed=0, accepted_domain_objects=0
- `promotion_firewall`: PASS_CANDIDATE_FIREWALL_CLOSED | candidate declares no pass, no accepted domain object, no concrete R_CMB, no score, no likelihood, and no verdict
- `claim_boundary`: PASS_CANDIDATE_CLAIM_BOUNDARY | row claim boundaries mark the artifact as candidate-only with no score, no likelihood, and no verdict
- `proof_checker_payloads`: BLOCKED_PROOF_CHECKER_PAYLOADS_MISSING | CarrierOK, DomOK, admissibility, quotient, codomain, and firewall candidates lack proof/checker payloads
- `certificate_passes`: BLOCKED_CERTIFICATES_UNPASSED | no carrier or domain certificate pass is recorded
- `domain_acceptance`: BLOCKED_DOMAIN_OBJECTS_UNACCEPTED | seed, null, and source domain objects remain unaccepted
- `concrete_R_CMB`: BLOCKED_R_CMB_NOT_MATERIALIZED | no concrete R_CMB can be materialized until certificates pass and domain objects are accepted

## Status

```text
CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_AUDITED_UNPASSED_NOT_SCORE_READY
```

The candidate is audit-visible and internally clean, but no certificate has
passed. The next object should provide proof/checker payloads for the named
candidate certificates.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_proof_checker_payload_packet_v01
```
