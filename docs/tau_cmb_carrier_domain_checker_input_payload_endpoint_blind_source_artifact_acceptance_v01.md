# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Acceptance v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact acceptance audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACTS_ACCEPTED_FOR_STAGING_POPULATION_ONLY
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_v01_source_artifact_candidates_accepted_for_staging_population_only_no_staging_write_no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This audit accepts endpoint-blind Tau-side source artifact candidate bundles
only for the next staging-population step. Acceptance here means that the
candidate bundle is present, hash-bound, provenance/replay/firewall accompanied,
endpoint-blind, and locally source-inventory complete. It does not write
`payload_staging/`, accept payloads, execute checkers, pass certificates, accept
domain objects, materialize `R_CMB`, open score entry, compute a likelihood, or
decide the dark-sector question.

## Acceptance Coverage

- `carrier_well_formedness`: 6 accepted source rows
- `domain_membership_rule`: 7 accepted source rows
- `seed_admissibility`: 9 accepted source rows
- `null_control_admissibility`: 9 accepted source rows
- `source_object_admissibility`: 8 accepted source rows
- `quotient_and_equivalence_survival`: 10 accepted source rows
- `codomain_compatibility`: 9 accepted source rows
- `endpoint_firewall_replay`: 8 accepted source rows

## Summary

```text
acceptance_rows=66
source_artifact_accepted_rows=66
staging_population_allowed_rows=66
payload_staging_written_rows=0
payload_accepted_rows=0
checker_executed_rows=0
score_entry_allowed=False
likelihood_allowed=False
dark_sector_verdict_allowed=False
```

## Status

```text
CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACTS_ACCEPTED_FOR_STAGING_POPULATION_ONLY
```

The source artifacts are accepted only as source inputs for the staging
population step. Downstream physical-readout and scoring claims remain closed.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01
```
