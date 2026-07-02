# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Acceptance Decision Gate v01

**Doc class:** parent-input evidence payload scoring handoff unblock-condition evidence receipt acceptance decision gate
**Status:** acceptance decision gate closed; scoring remains blocked

The gate records the current endpoint-blind decision after the unblock-plan
audit. Acceptance stays closed because the required materialization audit,
accepted receipt, accepted evidence object, and open scoring handoff are absent.

```text
decision_gate_closed_rows=7
unblock_plan_audit_passed_rows=0
receipt_accepted_rows=0
evidence_accepted_rows=0
open_handoff_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact is a decision gate only. It accepts no evidence object, accepts no
receipt, opens no scoring handoff, executes nothing, accepts no payload or
scoring input, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, and permits no no-dark or dark-sector verdict.
