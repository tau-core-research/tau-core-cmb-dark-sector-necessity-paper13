# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Acceptance Decision Gate Audit v01

**Doc class:** parent-input evidence payload scoring handoff unblock-condition evidence receipt acceptance decision gate audit
**Status:** closed decision gate audited; scoring remains blocked

The audit verifies that the closed gate is internally consistent: all seven
rows are audited, the gate is closed, no evidence or receipt is accepted, no
handoff is opened, and no scoring permission is granted.

```text
decision_gate_audit_passed_rows=7
decision_gate_closed_rows=7
receipt_accepted_rows=0
evidence_accepted_rows=0
open_handoff_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact audits a closed decision gate only. It accepts no evidence object,
accepts no receipt, opens no scoring handoff, executes nothing, accepts no
payload or scoring input, derives no `Phi_tau_eff`, computes no score, supplies
no CMB likelihood, and permits no no-dark or dark-sector verdict.
