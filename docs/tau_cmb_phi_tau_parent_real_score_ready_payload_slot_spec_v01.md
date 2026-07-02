# Tau CMB Phi Tau Parent Real Score-Ready Payload Slot Spec v01

**Doc class:** real score-ready payload slot specification
**Status:** slot specification declared; no payload materialized

This artifact expands the real score-ready input supply contract into concrete
payload slots. Each locked route row receives seven expected artifact paths and
field schemas. The package does not materialize any payload file and does not
accept any scoring input.

Required material schemas:

- `phi_tau_eff_source`: `source_id|k_grid|a_grid|phi_tau_eff_values|units|sign_convention|derivation_rule_id`
- `dimension_replay`: `replay_command|input_hashes|output_hash|unit_audit|convention_audit`
- `normalization_binding`: `normalization_id|gauge_choice|amplitude_reference|zero_source_limit`
- `endpoint_blind_provenance`: `provenance_id|source_hash|endpoint_label_firewall|freeze_timestamp`
- `cmb_readout_mapping`: `mapping_id|observable_family|ell_or_k_mapping|transfer_interface`
- `likelihood_adapter`: `adapter_id|data_vector_binding|covariance_binding|likelihood_command`
- `acceptance_replay`: `acceptance_id|validator_command|expected_pass_fields|acceptance_hash`

Summary:

```text
contract_rows=7
payload_slot_rows_declared=49
expected_artifact_paths_declared=49
payload_materialized_rows=0
slot_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=49
```

## Claim Boundary

This artifact is a slot specification only. It supplies no score-ready payload,
binds no payload hash, accepts no scoring input, derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, and permits no no-dark or
dark-sector verdict.
