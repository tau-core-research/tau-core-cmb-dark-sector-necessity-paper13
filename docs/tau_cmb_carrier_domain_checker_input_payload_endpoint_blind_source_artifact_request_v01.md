# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Request v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact request
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_DECLARED_NOT_SUPPLIED
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01_request_only_no_source_artifact_supplied_no_staging_write_no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This request names the endpoint-blind Tau-side source artifacts required before
staging-population execution can become possible. It does not supply or accept
source artifacts, write `payload_staging/`, accept payloads, execute checkers,
pass certificates, accept domain objects, materialize `R_CMB`, open score
entry, compute a likelihood, or decide the dark-sector question.

## Request Counts

- `carrier_well_formedness`: 6 source artifact requests
- `domain_membership_rule`: 7 source artifact requests
- `seed_admissibility`: 9 source artifact requests
- `null_control_admissibility`: 9 source artifact requests
- `source_object_admissibility`: 8 source artifact requests
- `quotient_and_equivalence_survival`: 10 source artifact requests
- `codomain_compatibility`: 9 source artifact requests
- `endpoint_firewall_replay`: 8 source artifact requests

## Summary

```text
request_rows=66
source_artifact_requests_declared=66
source_artifacts_supplied_rows=0
source_artifact_accepted_rows=0
staging_population_allowed_rows=0
payload_staging_written_rows=0
score_entry_allowed=False
likelihood_allowed=False
dark_sector_verdict_allowed=False
```

## Next Minimal Unblock

```text
audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01
```
