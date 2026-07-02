# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Score Attempt Unblock Conditions v01

**Doc class:** parent-input evidence payload scoring input payload submission evidence object receipt scoring handoff score attempt unblock conditions
**Status:** unblock conditions declared; scoring remains blocked

This artifact declares the minimal conditions that must be satisfied before a
score attempt can be considered. Each condition is required, but none is
currently satisfied.

```text
score_attempt_unblock_conditions_satisfied=false
score_attempt_allowed_now=false
score_attempt_blocked_now=true
```

The required conditions are accepted records for payload, completion evidence,
provenance, replay, hash manifest, endpoint firewall, and the combined payload
and scoring-input acceptance gate.

Next focused artifact:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01
```

## Claim Boundary

This artifact declares unblock conditions only. It opens no scoring handoff,
accepts no evidence object or receipt, executes nothing, accepts no scoring
input, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
and permits no verdict.
