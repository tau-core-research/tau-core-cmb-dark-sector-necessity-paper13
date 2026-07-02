# Tau CMB Phi Tau Parent Real Score-Ready Payload Template Manifest v01

**Doc class:** score-ready payload template manifest
**Status:** templates written; no real payload materialized

This artifact binds the 49 payload slots to seven reusable template files. The
templates are input shapes only. They are not real Tau-side CMB payloads, do not
carry physical values, and do not unlock scoring.

Template files:

- `data/score_ready_input_templates/acceptance_replay_template.json`
- `data/score_ready_input_templates/cmb_readout_mapping_template.csv`
- `data/score_ready_input_templates/dimension_replay_template.json`
- `data/score_ready_input_templates/endpoint_blind_provenance_template.json`
- `data/score_ready_input_templates/likelihood_adapter_template.json`
- `data/score_ready_input_templates/normalization_binding_template.csv`
- `data/score_ready_input_templates/phi_tau_eff_source_template.csv`

Summary:

```text
slot_rows_consumed=49
template_bindings_declared=49
template_files_declared=7
template_files_written=7
real_payload_materialized_rows=0
slot_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=49
```

## Claim Boundary

This artifact provides template shapes only. It materializes no real payload,
binds no payload hash, accepts no slot, accepts no scoring input, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, and permits no
no-dark or dark-sector verdict.
