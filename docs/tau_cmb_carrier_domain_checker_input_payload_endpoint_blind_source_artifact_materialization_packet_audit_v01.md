# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Materialization Packet Audit v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact materialization audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_MATERIALIZATION_AUDITED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_audit_v01_audit_only_source_artifact_candidates_materialized_not_accepted_no_staging_write_no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit verifies that endpoint-blind Tau-side source artifact candidate
bundles were materialized, hash-bound, provenance/replay/firewall accompanied,
and kept unaccepted. It does not populate `payload_staging/`, accept payloads,
execute checkers, pass certificates, accept domain objects, materialize
`R_CMB`, open score entry, compute a likelihood, or decide the dark-sector
question.

## Audit Rows

- `input_and_row_count`: PASS_MATERIALIZATION_INPUT_AND_ROW_COUNT | requested=66, materialized=66
- `bundle_files_present`: PASS_ALL_SOURCE_BUNDLE_FILES_PRESENT | all artifact/hash/provenance/replay/firewall files exist
- `hash_binding`: PASS_SOURCE_BUNDLE_HASH_BINDING | hash manifests match artifact, provenance, replay, and firewall files
- `source_inventory`: PASS_SOURCE_INVENTORY_REFERENCES_EXIST | all source inventory references exist
- `claim_boundary`: PASS_SOURCE_MATERIALIZATION_CLAIM_BOUNDARY | all bundle files preserve not-accepted/no-staging boundary
- `promotion_firewall`: PASS_SOURCE_MATERIALIZATION_FIREWALL_CLOSED | materialization does not open acceptance, staging, execution, R_CMB, score, likelihood, or verdict
- `source_acceptance`: BLOCKED_SOURCE_ACCEPTANCE_NOT_AVAILABLE | source candidates are materialized but not accepted
- `staging_population`: BLOCKED_STAGING_POPULATION_NOT_ALLOWED | staging population remains blocked until source candidates are accepted
- `checker_execution_and_R_CMB`: BLOCKED_CHECKERS_AND_R_CMB | checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream

## Status

```text
CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_MATERIALIZATION_AUDITED_NOT_ACCEPTED
```

The source candidates are present and auditable, but source acceptance remains
blocked.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_audit_v01
```
