# CMB Tau Lensing Scoring Command Manifest v01

**Doc class:** command manifest
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, score still blocked by preflight
**Canonical parent:** `docs/cmb_tau_lensing_scoring_pipeline_orchestrator_contract_v01.md`

This manifest records the concrete commands for the reduced scoring path.

## Commands

```text
make intake
make evidence-check
make route-submission-audit
make payload-checklist
make score-fulfillment
make skeleton-direct
make skeleton-delta
make skeleton-failure
make staging-precheck-direct
make staging-precheck-delta
make staging-precheck-failure
make staging-promote-direct-dry-run
make staging-promote-delta-dry-run
make staging-promote-failure-dry-run
make staging-promote-direct
make staging-promote-delta
make staging-promote-failure
make staging-positive-smoke
make env-check
make materialize-replay
make preflight
make validate-direct-grid
make validate-delta-grid
make score
make score-report
make score-todo
make score-readiness
make route-pack
make score-unblock
make score-gate
make score-attempt-guard
make score-output-audit
make scoring-status
make scoring-smoke
make scoring-positive-smoke
make scoring-firewall-smoke
make scoring-good-route-smoke
make scoring-guarded-entrypoint-smoke
make scoring-guarded-positive-smoke
make scoring-stale-receipt-smoke
make scoring-matching-receipt-smoke
make staging-promotion-guard-smoke
make staging-promotion-copy-smoke
make scoring-regression-all
make prepare-direct-hash
make prepare-delta-hash
```

Projection replay commands are explicit in the CSV because they write the replay
JSON only after a numeric grid validates.
The hash preparation commands do not validate the grid or compute a score; they
only report the SHA256 provenance fields required by the route evidence
firewall after a real route payload exists.

## Current State

```text
make preflight: implemented, ready=false expected
make score: implemented, blocks while preflight=false
```

Smoke runs confirm both commands currently stop before score execution.

## Claim Boundary

```text
scoring_command_manifest_only_no_score_run_no_dark_sector_verdict
```
