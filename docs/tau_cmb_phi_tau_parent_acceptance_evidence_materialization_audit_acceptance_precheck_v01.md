# Tau CMB Phi Tau Parent Acceptance Evidence Materialization Audit and Acceptance Precheck v01

**Doc class:** parent-input materialization audit plus receipt/evidence acceptance precheck
**Status:** materialization audit passed; receipt/evidence acceptance prechecks passed; final acceptance and scoring remain blocked

This artifact audits the forty-nine hashed material records created by the
materialization package. It verifies file presence, SHA-256 hashes, byte sizes,
endpoint-blind status, and required material-type coverage for all seven
evidence rows.

```text
materialization_audit_passed_rows=7
receipt_acceptance_precheck_passed_rows=7
evidence_acceptance_precheck_passed_rows=7
material_hashes_verified_total=49
receipt_accepted_rows=0
evidence_accepted_rows=0
decision_gate_reopen_allowed_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact audits materialized evidence materials and passes receipt/evidence
acceptance prechecks only. It accepts no receipt, accepts no evidence object,
reopens no decision gate, opens no scoring handoff, derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, and permits no no-dark or
dark-sector verdict.
