# CMB Tau Lensing Scoring Gates Smoke Contract v01

**Doc class:** scoring-gates smoke contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented
**Canonical parent:** `docs/cmb_tau_lensing_scoring_pipeline_orchestrator_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_scoring_gates_smoke_contract_v01.csv`

This contract adds a regression smoke test for the current no-route state. It
checks that all scoring-adjacent gates block safely without route evidence and
that none of them runs a score or issues a dark-sector verdict.
It also registers a focused firewall-blocker smoke path for a synthetic bad
direct route whose provenance hash does not match the submitted grid.

## Command

```text
make scoring-smoke
make scoring-firewall-smoke
make scoring-good-route-smoke
make scoring-guarded-entrypoint-smoke
make scoring-guarded-positive-smoke
make scoring-regression-all
```

The firewall-blocker smoke temporarily creates synthetic route payload names and
removes them before exit. Run the smoke commands sequentially, or use
`make scoring-regression-all`, so the no-route smoke is not racing against the
temporary bad-route fixture.
The good-route smoke also creates temporary route and replay payload names, so
it is included in the same sequential regression target.
The guarded-positive smoke temporarily creates a synthetic accepted route,
executes the guarded score entrypoint into `.tmp`, validates the output schema,
and removes all temporary route/replay/score files before exit. It is a plumbing
check only, not a physical Tau score.
The sequential regression target ends with the score-attempt guard, which must
block score execution unless the aggregate score gate passes.

## Checked Gates

```text
intake
evidence_firewall
materializer
scoring_environment
preflight
pipeline
todo
route_pack
firewall_blocker_readiness_split
guarded_score_entrypoint_block
guarded_score_entrypoint_synthetic_allow_path
```

## Claim Boundary

```text
scoring_gates_smoke_contract_only_no_score_run_no_dark_sector_verdict
```
