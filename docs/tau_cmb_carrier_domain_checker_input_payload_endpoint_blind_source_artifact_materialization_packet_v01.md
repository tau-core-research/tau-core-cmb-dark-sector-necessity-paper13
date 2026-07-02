# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Materialization Packet v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact materialization packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_CANDIDATES_MATERIALIZED_NOT_ACCEPTED
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01_source_artifact_candidates_materialized_not_accepted_no_staging_write_no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This packet materializes endpoint-blind Tau-side source artifact candidate
bundles under `payload_sources/`. The bundles are built from local Tau Core
theory/protocol artifacts and are not accepted source inputs. The packet does
not populate `payload_staging/`, accept payloads, execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Summary

```text
requested_rows=66
source_artifact_bundles_materialized=66
source_artifact_accepted_rows=0
staging_population_allowed_rows=0
payload_staging_written_rows=0
score_entry_allowed=False
likelihood_allowed=False
dark_sector_verdict_allowed=False
```

## Next Minimal Unblock

```text
audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01
```
