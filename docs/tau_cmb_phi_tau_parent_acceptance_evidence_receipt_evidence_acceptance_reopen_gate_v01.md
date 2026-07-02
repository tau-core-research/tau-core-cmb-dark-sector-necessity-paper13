# Tau CMB Phi Tau Parent Acceptance Evidence Receipt/Evidence Acceptance Reopen Gate v01

**Doc class:** parent-input receipt/evidence acceptance and decision-gate reopen artifact
**Status:** receipt/evidence accepted; decision gate reopened; scoring input still blocked

This artifact consumes the materialization audit and acceptance precheck package.
For all seven endpoint-blind evidence rows it accepts the receipt and evidence
objects and allows the decision gate to reopen. It does not accept a scoring
payload and does not open the scoring handoff.

```text
receipt_accepted_rows=7
evidence_accepted_rows=7
acceptance_record_created_rows=7
decision_gate_reopen_allowed_rows=7
payload_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact accepts receipt/evidence objects and reopens the decision gate
only. It accepts no scoring payload, accepts no scoring input, opens no scoring
handoff, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, and permits no no-dark or dark-sector verdict.
