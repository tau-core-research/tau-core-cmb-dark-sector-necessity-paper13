# CMB Tau Lensing Projection Operator Decision Gate v01

**Doc class:** projection-operator decision gate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** physical score retry blocked until operator core closes
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
projection_operator_decision_gate_only_no_operator_no_score_no_dark_sector_verdict
```

## Decision

```text
DO_NOT_SCORE_EXPLICIT_OPERATOR_FAILURE
```

## Formula-Spec Acceptance Matrix

```text
docs/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_v01.md
```

## Operator Core Status

```text
projection_operator_rule_supplied = False
projection_operator_explicit_failure = True
projection_normalization_supplied = False
projection_replay_supplied = False
```

## Admissible Next Actions

- `SUPPLY_OPERATOR`: provide endpoint-blind Projection_PP equation, kernel table, or transfer/projection integral with normalization and replay
- `FILL_FORMULA_SPEC_SCAFFOLD`: populate every blocking row in the formula-spec acceptance matrix with endpoint-blind equation, kernel/measure, normalization, zero-limit, dimension/sign audit, replay, and post-population firewall evidence
- `DECLARE_EXPLICIT_FAILURE`: record a non-score failure statement naming the missing operator, normalization, replay, and next theoretical blocker
- `RESUME_FROM_FAILURE`: replace the explicit failure with an endpoint-blind operator packet, then rerun normalization, replay, firewall, and gate

## Blocked Shortcuts

- do not use post-score alpha_star as Projection_PP normalization
- do not replay B_ACT @ grid as if it were physical Phi_lens_tau -> PP projection
- do not run physical score retry until operator, normalization, and replay are all accepted
