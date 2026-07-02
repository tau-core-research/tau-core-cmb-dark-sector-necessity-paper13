# CMB Tau Lensing Score Execution Precheck v01

**Doc class:** score execution precheck
**Reader role:** Paper 13 scoring implementer
**Status:** score execution blocked
**Canonical parent:** `docs/cmb_tau_lensing_reduced_score_runner_contract_v01.md`

This precheck decides whether the reduced score runner may be executed.

## Decision

```text
SCORE_EXECUTION_BLOCKED
```

The score runner exists, but the required projection replay JSON is missing:

```text
payloads/tau_lensing_pp_grid_projection_replay_v01.json
```

## Required Before Score

```text
route selected
3000-value numeric grid submitted
validator passes
projection replay JSON exists
replay has score_computed=false
replay has dark_sector_verdict=false
replay has projected_shape=[18]
```

## Claim Boundary

```text
score_execution_precheck_only_no_score_run_no_dark_sector_verdict
```
