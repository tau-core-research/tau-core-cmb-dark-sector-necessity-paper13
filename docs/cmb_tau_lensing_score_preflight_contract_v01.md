# CMB Tau Lensing Score Preflight Contract v01

**Doc class:** score preflight contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, blocked
**Canonical parent:** `docs/cmb_tau_lensing_score_execution_precheck_v01.md`

This contract registers the one-command preflight:

```text
scripts/preflight_tau_lensing_reduced_score.py
```

It reports whether the reduced score runner may be executed.

## Current Result

```text
ready_for_reduced_score_execution: false
```

Smoke run confirms the current blocker:

```text
selected_route_count: 0
firewall_passed: false
projection_replay_exists: false
runner_exists: true
output_validator_exists: true
```

## Required For True

```text
exactly one numeric route complete
route evidence firewall passed
projection replay exists
projection replay has projected_shape [18]
runner exists
score-output validator exists
```

Failure route completion does not make scoring ready; it records a clean stop.

## Claim Boundary

```text
score_preflight_contract_only_no_score_run_no_dark_sector_verdict
```
