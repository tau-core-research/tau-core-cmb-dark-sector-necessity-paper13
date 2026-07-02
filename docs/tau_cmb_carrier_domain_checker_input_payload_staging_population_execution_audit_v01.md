# Tau CMB Carrier Domain Checker Input Payload Staging Population Execution Audit v01

**Doc class:** carrier/domain checker input payload staging population execution audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_AUDITED_PAYLOADS_POPULATED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_audit_v01_audit_only_staging_files_populated_not_payload_accepted_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit verifies that `payload_staging/` checker-input files were populated
from accepted endpoint-blind Tau-side source artifacts while remaining
unaccepted. It does not accept payloads, execute checkers, pass certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

- `execution_row_shape`: PASS_EXPECTED_EXECUTION_ROWS_PRESENT | rows=66
- `input_source_acceptance_chain`: PASS_EXECUTION_INPUT_CHAIN | staging execution follows accepted endpoint-blind source artifacts
- `staging_files_present_and_hash_bound`: PASS_STAGING_FILES_PRESENT_AND_HASH_BOUND | all populated staging files exist and match recorded hashes
- `staging_claim_boundary`: PASS_STAGING_CLAIM_BOUNDARY | all staging files remain not accepted and forbid execution/R_CMB/score/likelihood/verdict
- `execution_accounting`: PASS_EXECUTION_ACCOUNTING | rows=66, attempted=66, succeeded=66, staging_written=66, accepted=0
- `promotion_firewall`: PASS_EXECUTION_FIREWALL_CLOSED | staging execution does not open payload acceptance, checker execution, R_CMB, score, likelihood, or verdict
- `payload_acceptance`: BLOCKED_ACCEPTANCE_AUDIT_NOT_AVAILABLE | payloads are populated but not accepted
- `checker_execution_and_R_CMB`: BLOCKED_CHECKERS_AND_R_CMB | checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream

## Status

```text
CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_AUDITED_PAYLOADS_POPULATED_NOT_ACCEPTED
```

The staging files are populated and auditable, but payload acceptance remains
blocked.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_v01
```
