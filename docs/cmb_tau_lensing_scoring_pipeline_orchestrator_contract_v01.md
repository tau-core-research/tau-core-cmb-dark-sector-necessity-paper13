# CMB Tau Lensing Scoring Pipeline Orchestrator Contract v01

**Doc class:** scoring pipeline contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, currently blocked by preflight
**Canonical parent:** `docs/cmb_tau_lensing_score_preflight_contract_v01.md`

This contract registers the single scoring pipeline command:

```text
scripts/run_tau_lensing_scoring_pipeline.py
```

The Makefile scoring entry point is guarded:

```text
scripts/run_tau_lensing_guarded_score_report.py
```

`make score` and `make score-report` must use the guarded entry point, so a
manual score command cannot bypass `make score-attempt-guard`.

The aggregate score gate is a current-state gate by default. Synthetic
regression smokes are only run through:

```text
scripts/run_tau_lensing_score_gate.py --with-regression-smokes
```

This keeps real route payload submission separate from mutating synthetic
regression checks.

The pipeline state can also be persisted:

```text
make score-report
```

Readiness consumers must call the pipeline in dry-run mode:

```text
scripts/run_tau_lensing_scoring_pipeline.py --dry-run --write-report
```

Dry-run mode may report `pipeline_ready: true`, but it must keep
`score_run: false` and `physical_tau_score_run: false`. It exists only to
separate score permission from score execution.

Default generated report:

```text
data/derived/cmb_tau_lensing_scoring_pipeline_report_v01.json
```

The next concrete missing-evidence todo is tracked at:

```text
data/source_manifest/cmb_tau_lensing_scoring_todo_contract_v01.csv
docs/cmb_tau_lensing_scoring_todo_contract_v01.md
scripts/extract_tau_lensing_scoring_todo.py
```

The no-route scoring-gates smoke check is tracked at:

```text
data/source_manifest/cmb_tau_lensing_scoring_gates_smoke_contract_v01.csv
docs/cmb_tau_lensing_scoring_gates_smoke_contract_v01.md
scripts/smoke_tau_lensing_scoring_gates.py
```

The single score-readiness decision is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_readiness_decision_contract_v01.csv
docs/cmb_tau_lensing_score_readiness_decision_contract_v01.md
scripts/decide_tau_lensing_score_readiness.py
```

## Behavior

```text
1. run route-evidence intake
2. check ACT-side scoring environment
3. attempt projection replay materialization
4. run preflight
5. if preflight is false, emit blocked report with intake, environment, materializer, and preflight state
6. if preflight is true and dry-run mode is active, emit a ready dry-run report without score execution
7. if preflight is true and dry-run mode is not active, run reduced score
8. validate reduced score output
9. emit reduced diagnostic pipeline result
```

## Current State

```text
implemented, blocked because preflight is false
```

Smoke run confirms:

```text
pipeline_ready: false
score_run: false
blocking_intake.intake_decision: ROUTE_EVIDENCE_INTAKE_BLOCKED
scoring_environment.environment_ready_for_reduced_score_once_tau_replay_exists: true
blocking_materializer.projection_replay_written: false
next_required_action: fill_exactly_one_staging_route_evidence_set_then_run_guarded_staging_promotion
```

## Claim Boundary

```text
scoring_pipeline_orchestrator_contract_only_no_score_run_no_dark_sector_verdict
```
