# Tau CMB Certificate Semantic Evidence Artifact Supply Audit v01

**Doc class:** semantic certificate evidence artifact supply audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** CMB_CERTIFICATE_SEMANTIC_EVIDENCE_ARTIFACT_SUPPLY_AUDITED_CANDIDATES_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_certificate_semantic_evidence_artifact_supply_audit_v01_audit_only_candidate_artifacts_supplied_not_accepted_not_proof_no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit verifies that the 28 semantic evidence candidate artifacts exist and
are hash-bound, while remaining unaccepted and non-proof.

## Audit Rows

- `supply_row_shape`: PASS_28_SUPPLY_ROWS_PRESENT | rows=28
- `candidate_artifacts`: PASS_CANDIDATE_ARTIFACTS_HASH_BOUND | materialized=28, hash_matched=28
- `not_proof_boundary`: PASS_CANDIDATES_NOT_ACCEPTED_NOT_PROOF | candidate artifacts do not claim evidence acceptance, proof, executability, or certificate pass
- `promotion_firewall`: PASS_SUPPLY_FIREWALL_CLOSED | candidate supply does not open score, likelihood, or verdict
- `evidence_acceptance`: BLOCKED_EVIDENCE_ACCEPTANCE_NOT_PERFORMED | candidate artifacts are supplied but not accepted as semantic evidence
- `certificate_execution`: BLOCKED_CERTIFICATE_EXECUTION_NOT_ALLOWED | certificate rules remain non-executable until evidence is accepted

## Status

```text
CMB_CERTIFICATE_SEMANTIC_EVIDENCE_ARTIFACT_SUPPLY_AUDITED_CANDIDATES_NOT_ACCEPTED
```

The route has moved from missing semantic evidence files to evidence acceptance
or replacement. Scoring remains closed.

## Next Minimal Unblock

```text
tau_cmb_certificate_semantic_evidence_acceptance_audit_v01
```
