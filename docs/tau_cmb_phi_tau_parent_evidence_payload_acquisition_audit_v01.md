# Tau CMB Phi Tau Parent Evidence Payload Acquisition Audit v01

**Doc class:** parent evidence-payload acquisition audit
**Reader role:** Paper 13 CMB scoring path
**Status:** candidate payloads are present and hash-bound, but not accepted as parent inputs
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact audits the payload acquisition candidate. It distinguishes a real
candidate payload source from an accepted parent input: the former is now
present and hash-bound; the latter still requires parent package acceptance and
certificate pass.

## Summary

```text
audit_rows_declared=7
source_artifact_present_rows=7
hash_bound_rows=7
candidate_payload_supplied_rows=7
candidate_payload_audit_passed_rows=7
certificate_passed_rows=0
parent_payload_accepted_rows=0
score_ready_rows=0
```

## Claim Boundary

```text
tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01_audit_only_payload_candidates_present_hash_bound_but_not_parent_accepted_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict
```

The audit does not accept parent-side Tau inputs, does not close the certificate
layer, does not derive `Phi_tau_eff`, does not compute a CMB score or
likelihood, and does not decide whether a dark sector is needed.
