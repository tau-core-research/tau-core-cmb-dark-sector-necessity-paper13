# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Request Audit v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact request audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_AUDITED_NOT_SUPPLIED

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01_audit_only_request_clean_but_unsupplied_no_source_acceptance_no_staging_write_no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit checks that the endpoint-blind source artifact request is complete
and still unsupplied. It does not supply or accept source artifacts, populate
`payload_staging/`, accept payloads, execute checkers, pass certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Audit Rows

- `request_row_shape`: PASS_EXPECTED_SOURCE_REQUEST_ROWS_PRESENT | rows=66
- `input_execution_chain`: PASS_SOURCE_REQUEST_INPUT_CHAIN | source artifact request follows a clean audited blocked staging-population execution envelope
- `source_request_fields`: PASS_SOURCE_REQUEST_FIELDS_DECLARED | each row declares source artifact, hash, replay, provenance, firewall, and endpoint-blind acceptance condition
- `source_request_accounting`: PASS_SOURCE_REQUEST_ACCOUNTING | rows=66, declared=66, supplied=0, accepted=0, staging_allowed=0
- `promotion_firewall`: PASS_SOURCE_REQUEST_FIREWALL_CLOSED | source request does not open source acceptance, staging population, payload acceptance, R_CMB, score, likelihood, or verdict
- `claim_boundary`: PASS_SOURCE_REQUEST_CLAIM_BOUNDARY | row claim boundaries mark request-only source artifacts with no staging/write/score/verdict
- `source_artifact_supply`: BLOCKED_SOURCE_ARTIFACTS_NOT_SUPPLIED | endpoint-blind Tau-side source artifacts are requested but absent
- `source_artifact_acceptance`: BLOCKED_SOURCE_ACCEPTANCE_NOT_AVAILABLE | source artifacts cannot be accepted before supply, hash, replay, provenance, and firewall checks
- `staging_population`: BLOCKED_STAGING_POPULATION_NOT_ALLOWED | staging population remains blocked until source artifacts are accepted
- `checker_execution_and_R_CMB`: BLOCKED_CHECKERS_AND_R_CMB | checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream

## Status

```text
CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_AUDITED_NOT_SUPPLIED
```

The request is auditable, but the required endpoint-blind Tau-side source
artifacts are absent.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01
```
