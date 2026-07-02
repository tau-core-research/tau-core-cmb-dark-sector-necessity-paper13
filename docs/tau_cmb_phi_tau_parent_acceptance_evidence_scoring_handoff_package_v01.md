# Tau CMB Phi Tau Parent Acceptance Evidence Scoring Handoff Package v01

**Doc class:** parent-input scoring handoff package from accepted evidence
**Status:** scoring handoff opened; scoring input remains unaccepted

This artifact consumes the receipt/evidence acceptance reopen-gate package. It
packages all seven accepted endpoint-blind evidence rows into a scoring-handoff
candidate and opens the handoff route to the scoring-input acceptance gate.

```text
receipt_accepted_rows=7
evidence_accepted_rows=7
scoring_handoff_package_created_rows=7
scoring_handoff_opened_rows=7
scoring_input_candidate_created_rows=7
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact opens a scoring handoff from accepted evidence only. It accepts no
scoring input, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, and permits no no-dark or dark-sector verdict.
