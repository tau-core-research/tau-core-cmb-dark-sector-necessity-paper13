# CMB Tau Lensing Score Readiness Snapshot v01

**Doc class:** scoring-readiness audit snapshot
**Reader role:** Paper 13 scoring implementer
**Status:** blocked, no score run
**Canonical data:** `data/source_manifest/cmb_tau_lensing_score_readiness_snapshot_v01.csv`

This snapshot records the current reduced Tau lensing scoring state after the
preflight and command wrappers were added.

## Result

The scoring machinery is present, but the score is still not admissible:

```text
preflight_ready = false
pipeline_ready = false
score_run = false
selected_route_count = 0
projection_replay_exists = false
```

The runner and output validator exist:

```text
runner_exists = true
output_validator_exists = true
```

## Blocking Gate

The current blocking gate is:

```text
BLOCKED_ROUTE_GRID_REPLAY_MISSING
```

No Tau score may be reported until exactly one allowed route has been selected
and the corresponding payload has been validated into a projection replay.

## Allowed Unblock Routes

Exactly one of the following routes must be completed:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
explicit_failure_no_endpoint_blind_grid
```

The direct route needs a 3000-point Tau PP grid, provenance, and route
declaration. The delta route needs a 3000-point delta grid, named fiducial
reference, provenance, and route declaration. The failure route needs an
explicit failure statement and keeps the score blocked.

## Claim Boundary

```text
score_readiness_snapshot_only_no_score_run_no_dark_sector_verdict
```

This artifact is a readiness snapshot only. It does not contain a Tau score,
does not run a likelihood, and does not decide whether a dark-sector response is
required.
