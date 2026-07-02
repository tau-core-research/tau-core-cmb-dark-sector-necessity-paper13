# CMB Tau Lensing Scoring Todo Contract v01

**Doc class:** scoring-todo contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_scoring_pipeline_orchestrator_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_scoring_todo_contract_v01.csv`

This contract extracts the next concrete scoring todo from the current pipeline
report. It is a handoff helper only: it does not validate a grid, does not
write a projection replay, does not compute a score, and does not issue a
dark-sector verdict.

## Command

```text
make score-todo
```

Default generated todo:

```text
data/derived/cmb_tau_lensing_scoring_todo_v01.json
```

## Current Expected Status

Until one route evidence set is complete, the todo status is expected to be:

```text
SUBMIT_EXACTLY_ONE_ROUTE_EVIDENCE_SET
```

The todo lists missing files for the direct, delta, and explicit failure routes
so the next work item is not inferred manually from a long pipeline report.

The route-specific evidence pack is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_evidence_pack_contract_v01.csv
docs/cmb_tau_lensing_route_evidence_pack_contract_v01.md
scripts/build_tau_lensing_route_evidence_pack.py
```

## Claim Boundary

```text
scoring_todo_contract_only_no_score_run_no_dark_sector_verdict
```
