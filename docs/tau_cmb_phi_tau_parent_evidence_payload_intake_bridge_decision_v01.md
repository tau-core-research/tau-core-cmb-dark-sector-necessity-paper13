# Tau CMB Phi Tau Parent Evidence Payload Intake Bridge Decision v01

**Doc class:** parent evidence-payload intake bridge decision
**Reader role:** Paper 13 CMB scoring path
**Status:** candidate payload acquired; canonical repackaging and receipt binding required before acceptance
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact bridges the newly acquired hash-bound candidate payloads into the
older canonical submission/materialization route. It makes the state explicit:
candidate payloads exist, but they are not yet canonical parent payload packets
with receipt, dimension, replay, firewall, and certificate acceptance binding.

## Summary

```text
bridge_rows_declared=7
candidate_payload_audit_passed_rows=7
canonical_submission_packet_present_rows=0
receipt_binding_present_rows=0
canonical_repackaging_required_rows=7
intake_bridge_passed_rows=0
parent_payload_accepted_rows=0
certificate_passed_rows=0
score_ready_rows=0
```

## Claim Boundary

```text
tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01_bridge_decision_only_candidate_payload_acquired_but_requires_canonical_repackaging_no_parent_acceptance_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict
```

This bridge decision does not accept parent-side Tau inputs, does not close the
certificate layer, does not derive `Phi_tau_eff`, does not compute a CMB score
or likelihood, and does not decide whether a dark sector is needed.
