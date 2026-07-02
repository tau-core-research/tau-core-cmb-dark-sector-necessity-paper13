# Tau CMB Phi Tau Parent Acceptance Evidence Null-Response Lock v01

**Doc class:** null-response lock for accepted-evidence scoring route
**Status:** null response locked after score-attempt guard denial

This artifact consumes the score-attempt guard. Since the guard was executed and
all seven score attempts were denied because no score-ready input exists, the
accepted-evidence route is locked in null-response state until a real
score-ready input with accepted scoring input is supplied.

```text
score_attempt_guard_executed_rows=7
score_attempt_denied_rows=7
explicit_null_response_routed_rows=7
null_response_locked_rows=7
score_ready_input_available_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact locks the null-response state only. It accepts no scoring input,
supplies no score-ready input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
