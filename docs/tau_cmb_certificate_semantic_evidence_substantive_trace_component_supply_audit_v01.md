# Tau CMB Certificate Semantic Evidence Substantive Trace Component Supply Audit v01

**Doc class:** semantic certificate evidence trace component supply audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUPPLY_AUDITED_DRAFT_CONTENT_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply_audit_v01_audit_only_component_draft_content_supplied_not_accepted_no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit verifies that trace-component draft content exists and remains
non-certifying.

## Audit Rows

- `component_row_shape`: PASS_COMPONENT_ROWS_PRESENT | rows=128
- `component_drafts`: PASS_COMPONENT_DRAFTS_HASH_BOUND | supplied=128, hash_matched=128
- `not_proof_boundary`: PASS_COMPONENTS_NOT_ACCEPTED_NOT_PROOF | component drafts do not open component acceptance, trace acceptance, or certificate execution
- `promotion_firewall`: PASS_COMPONENT_FIREWALL_CLOSED | component supply does not open score, likelihood, or verdict
- `component_acceptance`: BLOCKED_COMPONENT_ACCEPTANCE_NOT_PERFORMED | component drafts are supplied but not accepted as substantive proof components
- `trace_acceptance`: BLOCKED_TRACE_ACCEPTANCE_NOT_ALLOWED | traces remain unaccepted until all required components are accepted

## Status

```text
CMB_CERTIFICATE_SEMANTIC_EVIDENCE_TRACE_COMPONENT_SUPPLY_AUDITED_DRAFT_CONTENT_NOT_ACCEPTED
```

The route has moved from missing component files to component acceptance.
Scoring remains closed.

## Next Minimal Unblock

```text
tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance_audit_v01
```
