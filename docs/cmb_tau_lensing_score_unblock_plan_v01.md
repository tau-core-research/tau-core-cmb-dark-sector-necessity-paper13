# CMB Tau Lensing Score Unblock Plan v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** unblock plan, no score
**Canonical parent:** `docs/cmb_tau_lensing_response_score_gate_v01.md`

This plan orders the remaining work required before a reduced Tau lensing score
attempt can be admissible.

## Order

```text
1. close Phi_tau_eff source payload
2. close T_tau_CMB transfer payload
3. close tau_PP_grid or delta_PP_tau projection payload
4. replay payload acceptance and hashes
5. only then run reduced Tau lensing score attempt
```

The order matters. A `PP` grid without a `Phi` source and transfer rule would be
a fitted shape, not a Tau Core prediction.

## Current Status

Every step is pending. The adapter sanity contract exists, but Tau scoring is
blocked by missing Tau-side inputs.

## Minimal Completion Conditions

- `Phi_tau_eff` accepted with endpoint-blind provenance and normalization;
- `T_tau_CMB` accepted with domain, codomain, time/scale convention, and
  operator rule;
- `tau_PP_grid` or `delta_PP_tau` accepted as a 3000-value projectable grid;
- payload hashes and firewall statements pass replay;
- reduced score report preserves diagnostic-only claim boundary.

## Claim Boundary

```text
tau_lensing_unblock_plan_only_no_tau_score_no_dark_sector_verdict
```

The first-step Phi source submission packet is tracked at:

```text
data/source_manifest/cmb_tau_lensing_phi_source_payload_submission_v01.csv
docs/cmb_tau_lensing_phi_source_payload_submission_v01.md
```

The first-step Phi source acceptance audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_phi_source_acceptance_audit_v02.csv
docs/cmb_tau_lensing_phi_source_acceptance_audit_v02.md
```

The second-step transfer submission packet is tracked at:

```text
data/source_manifest/cmb_tau_lensing_transfer_payload_submission_v01.csv
docs/cmb_tau_lensing_transfer_payload_submission_v01.md
```

The second-step transfer acceptance audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_transfer_acceptance_audit_v02.csv
docs/cmb_tau_lensing_transfer_acceptance_audit_v02.md
```

The third-step PP-grid submission packet is tracked at:

```text
data/source_manifest/cmb_tau_lensing_pp_grid_payload_submission_v01.csv
docs/cmb_tau_lensing_pp_grid_payload_submission_v01.md
```

The third-step PP-grid acceptance audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_pp_grid_acceptance_audit_v02.csv
docs/cmb_tau_lensing_pp_grid_acceptance_audit_v02.md
```

The numeric grid materialization request is tracked at:

```text
data/source_manifest/cmb_tau_lensing_numeric_grid_materialization_request_v01.csv
docs/cmb_tau_lensing_numeric_grid_materialization_request_v01.md
```

The projection replay materialization request is tracked at:

```text
data/source_manifest/cmb_tau_lensing_projection_replay_materialization_request_v01.csv
docs/cmb_tau_lensing_projection_replay_materialization_request_v01.md
```

The grid validator contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_grid_validator_contract_v01.csv
docs/cmb_tau_lensing_grid_validator_contract_v01.md
scripts/validate_tau_lensing_grid_payload.py
```

The numeric grid candidate audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_numeric_grid_candidate_audit_v01.csv
docs/cmb_tau_lensing_numeric_grid_candidate_audit_v01.md
```

The numeric grid route decision contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_numeric_grid_route_decision_contract_v01.csv
docs/cmb_tau_lensing_numeric_grid_route_decision_contract_v01.md
```

The numeric grid route selection gate is tracked at:

```text
data/source_manifest/cmb_tau_lensing_numeric_grid_route_selection_gate_v01.csv
docs/cmb_tau_lensing_numeric_grid_route_selection_gate_v01.md
```

The route selection submission packet is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_selection_submission_packet_v01.csv
docs/cmb_tau_lensing_route_selection_submission_packet_v01.md
```

The route selection submission precheck is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_selection_submission_precheck_v01.csv
docs/cmb_tau_lensing_route_selection_submission_precheck_v01.md
```

The route choice rubric is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_choice_rubric_v01.csv
docs/cmb_tau_lensing_route_choice_rubric_v01.md
```

The route decision checklist is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_decision_checklist_v01.csv
docs/cmb_tau_lensing_route_decision_checklist_v01.md
```

The route decision evidence request is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_decision_evidence_request_v01.csv
docs/cmb_tau_lensing_route_decision_evidence_request_v01.md
```

The route decision evidence receipt audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_decision_evidence_receipt_audit_v01.csv
docs/cmb_tau_lensing_route_decision_evidence_receipt_audit_v01.md
```

The next evidence handoff packet is tracked at:

```text
data/source_manifest/cmb_tau_lensing_next_evidence_handoff_packet_v01.csv
docs/cmb_tau_lensing_next_evidence_handoff_packet_v01.md
```

The route evidence intake contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_evidence_intake_contract_v01.csv
docs/cmb_tau_lensing_route_evidence_intake_contract_v01.md
scripts/intake_tau_lensing_route_evidence.py
```

The projection replay materializer contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_projection_replay_materializer_contract_v01.csv
docs/cmb_tau_lensing_projection_replay_materializer_contract_v01.md
scripts/materialize_tau_lensing_projection_replay.py
```

The prescore readiness lock is tracked at:

```text
data/source_manifest/cmb_tau_lensing_prescore_readiness_lock_v01.csv
docs/cmb_tau_lensing_prescore_readiness_lock_v01.md
```

The reduced score runner contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_reduced_score_runner_contract_v01.csv
docs/cmb_tau_lensing_reduced_score_runner_contract_v01.md
scripts/run_tau_lensing_reduced_score.py
```

The score execution precheck is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_execution_precheck_v01.csv
docs/cmb_tau_lensing_score_execution_precheck_v01.md
```

The reduced score output schema lock is tracked at:

```text
data/source_manifest/cmb_tau_lensing_reduced_score_output_schema_lock_v01.csv
docs/cmb_tau_lensing_reduced_score_output_schema_lock_v01.md
```

The reduced score output validator contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_reduced_score_output_validator_contract_v01.csv
docs/cmb_tau_lensing_reduced_score_output_validator_contract_v01.md
scripts/validate_tau_lensing_reduced_score_output.py
```

The score preflight contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_preflight_contract_v01.csv
docs/cmb_tau_lensing_score_preflight_contract_v01.md
scripts/preflight_tau_lensing_reduced_score.py
```

The scoring pipeline orchestrator contract is tracked at:

```text
data/source_manifest/cmb_tau_lensing_scoring_pipeline_orchestrator_contract_v01.csv
docs/cmb_tau_lensing_scoring_pipeline_orchestrator_contract_v01.md
scripts/run_tau_lensing_scoring_pipeline.py
```

The scoring command manifest is tracked at:

```text
data/source_manifest/cmb_tau_lensing_scoring_command_manifest_v01.csv
docs/cmb_tau_lensing_scoring_command_manifest_v01.md
Makefile
```

The score readiness snapshot is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_readiness_snapshot_v01.csv
docs/cmb_tau_lensing_score_readiness_snapshot_v01.md
```

The fourth-step payload replay acceptance gate is tracked at:

```text
data/source_manifest/cmb_tau_lensing_payload_replay_acceptance_v01.csv
docs/cmb_tau_lensing_payload_replay_acceptance_v01.md
```

The fifth-step reduced score attempt gate is tracked at:

```text
data/source_manifest/cmb_tau_lensing_reduced_score_attempt_gate_v01.csv
docs/cmb_tau_lensing_reduced_score_attempt_gate_v01.md
```
