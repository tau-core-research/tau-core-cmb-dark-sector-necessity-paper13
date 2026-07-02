# Tau CMB Carrier Domain Checker Input Payload Acceptance Audit v01

**Doc class:** carrier/domain checker input payload acceptance audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ACCEPTANCE_AUDITED_PAYLOADS_ACCEPTED_AS_CHECKER_INPUTS_ONLY
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_acceptance_audit_v01_payload_staging_files_accepted_as_checker_inputs_only_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit accepts populated `payload_staging/` files only as checker-input
payloads. It verifies file presence, staging hash agreement, not-yet-accepted
boundary cleanliness, endpoint-blind firewall cleanliness, and source-artifact
traceability. It does not execute checkers, pass certificates, accept domain
objects, materialize `R_CMB`, open score entry, compute a likelihood, or decide
the dark-sector question.

## Acceptance Coverage

- `carrier_well_formedness`: 6 accepted checker-input files
- `domain_membership_rule`: 7 accepted checker-input files
- `seed_admissibility`: 9 accepted checker-input files
- `null_control_admissibility`: 9 accepted checker-input files
- `source_object_admissibility`: 8 accepted checker-input files
- `quotient_and_equivalence_survival`: 10 accepted checker-input files
- `codomain_compatibility`: 9 accepted checker-input files
- `endpoint_firewall_replay`: 8 accepted checker-input files

## Summary

```text
acceptance_rows=66
payload_accepted_rows=66
checker_input_available_rows=66
checker_execution_allowed_rows=0
checker_executed_rows=0
certificate_passed_rows=0
score_entry_allowed=False
likelihood_allowed=False
dark_sector_verdict_allowed=False
```

## Status

```text
CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ACCEPTANCE_AUDITED_PAYLOADS_ACCEPTED_AS_CHECKER_INPUTS_ONLY
```

The staging payloads are accepted as checker inputs only. Checker execution
requires a refreshed execution packet and remains downstream.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_checker_execution_packet_refresh_v01
```
