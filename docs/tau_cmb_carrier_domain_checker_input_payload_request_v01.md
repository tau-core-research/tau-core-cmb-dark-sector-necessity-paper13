# Tau CMB Carrier Domain Checker Input Payload Request v01

**Doc class:** carrier/domain checker input payload request
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_DECLARED_NOT_FULFILLED
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_carrier_domain_checker_input_payload_request_v01_request_only_payloads_not_supplied_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict
```

## Purpose

This artifact requests the concrete input payloads required before the
carrier/domain checkers can become executable. It does not supply or accept
payloads, execute checkers, pass certificates, accept domain objects,
materialize `R_CMB`, open score entry, compute a likelihood, or decide the
dark-sector question.

## Request Rows

- `carrier_well_formedness`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_carrier_ok_checker` | request: carrier_payload.json | blocks: carrier input payload bundle is absent
- `domain_membership_rule`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_dom_ok_checker` | request: domain_payload.json; support_record.json; normalization_record.json | blocks: joint domain input payload bundle is absent
- `seed_admissibility`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_seed_admissibility_checker` | request: seed_domain_payload.json; seed_descriptor_pass.json; activation_pass.json; quotient_survival_witness.json | blocks: seed admissibility payload and quotient witness are absent
- `null_control_admissibility`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_null_control_checker` | request: null_control_payload.json; null_readout_candidate.json; no_response_proof_candidate.json | blocks: null control payload and null readout materialization are absent
- `source_object_admissibility`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_source_object_checker` | request: source_object_payload.json; source_derivation_transcript.json; known_limit_check.json | blocks: endpoint-blind source object payload is absent
- `quotient_and_equivalence_survival`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_quotient_survival_checker` | request: quotient_payload.json; equivalence_relation.json; null_class.json; representative_family.json; non_null_witness.json | blocks: non-null witness and representative-family payload are absent
- `codomain_compatibility`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_codomain_ok_checker` | request: codomain_payload.json; r_cmb_output_candidate.json; role_coordinate_basis.json; numeric_guard_records.json | blocks: concrete R_CMB output candidate is absent
- `endpoint_firewall_replay`: INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED | `run_endpoint_firewall_checker` | request: firewall_payload.json; populated_records.json | blocks: populated values and endpoint access logs are absent

## Status

```text
CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_DECLARED_NOT_FULFILLED
```

The route now has a concrete payload request list, but all fulfillment,
acceptance, execution, pass, and scoring flags remain false.

## Next Minimal Unblock

```text
audit_tau_cmb_carrier_domain_checker_input_payload_request_v01
```
