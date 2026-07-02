# CMB Tau Lensing Projection Replay Materializer Contract v01

**Doc class:** projection-replay materializer contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, currently blocked by route-evidence intake
**Canonical parent:** `docs/cmb_tau_lensing_route_evidence_intake_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_projection_replay_materializer_contract_v01.csv`

This contract adds the route-aware command that turns an accepted direct or
delta route evidence set into the projection replay required by the reduced
score preflight. It does not compute a score and does not issue a dark-sector
verdict.

## Command

```text
make materialize-replay
```

Equivalent command:

```text
python3 scripts/materialize_tau_lensing_projection_replay.py
```

## Behavior

```text
1. run route-evidence intake
2. if no complete route exists, emit blocked report
3. if failure route is selected, emit blocked report
4. if direct route is selected, validate direct grid and write projection replay
5. if delta route is selected, validate delta grid and write projection replay
```

Default replay output:

```text
payloads/tau_lensing_pp_grid_projection_replay_v01.json
```

## Claim Boundary

```text
projection_replay_materializer_contract_only_no_score_no_dark_sector_verdict
```

The materializer only validates a predeclared grid and replays the locked ACT
binning projection. It is not a likelihood, not a Tau score, and not a
dark-sector decision.
