# Tau CMB Certificate Semantic Evidence Replacement Supply Audit v01

**Doc class:** semantic certificate evidence replacement supply audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_SUPPLY_AUDITED_DRAFTS_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_certificate_semantic_evidence_replacement_supply_audit_v01_audit_only_draft_replacements_supplied_not_accepted_no_proof_no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit verifies that the 28 draft replacement files exist and are
hash-bound, while remaining unaccepted and non-proof.

## Audit Rows

- `replacement_row_shape`: PASS_28_REPLACEMENT_ROWS_PRESENT | rows=28
- `draft_replacements`: PASS_DRAFT_REPLACEMENTS_HASH_BOUND | supplied=28, hash_matched=28
- `not_accepted_boundary`: PASS_REPLACEMENTS_NOT_ACCEPTED_NOT_PROOF | draft replacements contain no accepted semantic assertions or proof claims
- `promotion_firewall`: PASS_REPLACEMENT_FIREWALL_CLOSED | replacement supply does not open score, likelihood, or verdict
- `semantic_assertions`: BLOCKED_SUBSTANTIVE_SEMANTIC_ASSERTIONS_ABSENT | draft replacements are present but semantic assertions remain null
- `certificate_execution`: BLOCKED_CERTIFICATE_EXECUTION_NOT_ALLOWED | certificate rules remain non-executable until replacements are accepted

## Status

```text
CMB_CERTIFICATE_SEMANTIC_EVIDENCE_REPLACEMENT_SUPPLY_AUDITED_DRAFTS_NOT_ACCEPTED
```

The route has moved from missing replacement files to missing substantive
semantic assertions. Scoring remains closed.

## Next Minimal Unblock

```text
tau_cmb_certificate_semantic_evidence_substantive_assertion_supply_v01
```
