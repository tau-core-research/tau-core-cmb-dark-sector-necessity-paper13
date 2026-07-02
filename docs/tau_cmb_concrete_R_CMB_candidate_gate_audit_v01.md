# Tau CMB Concrete R_CMB Candidate Gate Audit v01

**Doc class:** concrete readout candidate gate audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_AUDITED_NOT_PHYSICAL

## Claim Boundary

```text
tau_cmb_concrete_R_CMB_candidate_gate_audit_v01_audit_only_structural_candidate_shell_not_physical_R_CMB_no_codomain_pass_no_checker_execution_no_score_no_likelihood_no_verdict
```

## Purpose

This audit checks the structural `R_CMB` candidate shell. It does not certify a
physical readout, pass codomain compatibility, execute checkers, open score
entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

- `source_records`: PASS_SOURCE_RECORDS_BOUND | all source records exist and are hash-bound
- `structural_signature`: PASS_STRUCTURAL_SIGNATURE | formal readout signature and six role slots are declared
- `candidate_gate_status`: PASS_STRUCTURAL_CANDIDATE_AVAILABLE | structural candidate shell is available for codomain precheck
- `promotion_firewall`: PASS_CANDIDATE_FIREWALL_CLOSED | candidate shell does not open physical R_CMB, execution, score, likelihood, or verdict
- `physical_R_CMB`: BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED | candidate shell has no physical/numeric readout values
- `carrier_domain_certification`: BLOCKED_CARRIER_DOMAIN_NOT_CERTIFIED | carrier/domain certificate remains blocked

## Status

```text
CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_AUDITED_NOT_PHYSICAL
```

The structural candidate can be used to refresh the codomain precheck, but
physical materialization and carrier/domain certification remain blocked.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_checker_execution_packet_refresh_v02_with_structural_R_CMB_candidate
```
