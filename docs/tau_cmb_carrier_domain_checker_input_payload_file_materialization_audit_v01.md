# Tau CMB Carrier Domain Checker Input Payload File Materialization Audit v01

**Doc class:** carrier/domain checker input payload template-file materialization audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_TEMPLATE_FILES_AUDITED_PAYLOADS_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_file_materialization_audit_v01_audit_only_template_files_clean_payload_staging_absent_no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit verifies that the declared checker-input template files exist and
are hash-bound while remaining unpopulated and non-accepting. It does not
populate `payload_staging/`, accept payloads, execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Audit Rows

- `file_materialization_row_shape`: PASS_EXPECTED_FILE_MATERIALIZATION_ROWS_PRESENT | rows=66
- `input_materialization_chain`: PASS_FILE_MATERIALIZATION_INPUT_CHAIN | file materialization follows a clean audited schema-only materialization packet
- `template_file_hash_binding`: PASS_TEMPLATE_FILES_HASH_BOUND | all template files exist and match recorded sha256
- `template_content_boundary`: PASS_TEMPLATE_CONTENT_BOUNDARY | all template files are explicitly unpopulated and non-accepting
- `file_materialization_accounting`: PASS_FILE_MATERIALIZATION_ACCOUNTING | rows=66, templates=66, staging=0, accepted=0
- `promotion_firewall`: PASS_FILE_MATERIALIZATION_FIREWALL_CLOSED | template file materialization does not open payload staging, acceptance, execution, R_CMB, score, likelihood, or verdict
- `payload_staging_population`: BLOCKED_PAYLOAD_STAGING_FILES_ABSENT | payload_staging files are still absent
- `binding_checks`: BLOCKED_BINDINGS_NOT_AVAILABLE | hash, provenance, replay, and firewall bindings cannot pass without populated staging payloads
- `payload_acceptance`: BLOCKED_ACCEPTANCE_AUDIT_NOT_AVAILABLE | payloads cannot be accepted from templates alone
- `checker_execution_and_R_CMB`: BLOCKED_EXECUTION_AND_R_CMB | checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream

## Status

```text
CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_TEMPLATE_FILES_AUDITED_PAYLOADS_NOT_MATERIALIZED
```

The template files are materialized and auditable, but actual staging payloads
are still absent.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01
```
