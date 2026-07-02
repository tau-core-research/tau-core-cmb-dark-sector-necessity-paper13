# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Acceptance Unblock Plan v01

**Doc class:** parent-input evidence payload scoring handoff unblock-condition evidence receipt acceptance unblock plan
**Status:** unblock plan declared but not completed; scoring remains blocked

This artifact declares the concrete exit requirements after the
unblock-condition evidence receipt acceptance precheck. The score attempt can
only proceed after materialization audit pass, accepted receipt, accepted
evidence object, accepted payload/scoring input, and open handoff are recorded.

```text
unblock_condition_evidence_receipt_acceptance_unblock_plan_satisfied=false
materialization_audit_required_rows=7
receipt_acceptance_required_rows=7
evidence_acceptance_required_rows=7
handoff_open_required_rows=7
unblock_completed_rows=0
score_attempt_blocked_now_rows=7
```

Next focused artifact:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01
```

## Claim Boundary

This artifact declares unblock requirements only. It materializes no evidence
object, accepts no receipt, accepts no evidence object, opens no scoring
handoff, executes nothing, accepts no payload or scoring input, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, and permits no
no-dark or dark-sector verdict.
