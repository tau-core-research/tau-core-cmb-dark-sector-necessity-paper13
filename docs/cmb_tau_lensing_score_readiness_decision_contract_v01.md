# CMB Tau Lensing Score Readiness Decision Contract v01

**Doc class:** score-readiness decision contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_scoring_pipeline_orchestrator_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_score_readiness_decision_contract_v01.csv`

This contract turns the current scoring pipeline report into one machine-readable
decision. It separates ACT-side environment readiness from Tau-side route
evidence, route evidence firewall, projection replay, and preflight blockers.
It calls the pipeline in dry-run mode, so a `READY_TO_SCORE` decision is a
permission state only, not a score execution.

## Command

```text
make score-readiness
```

Default generated decision:

```text
data/derived/cmb_tau_lensing_score_readiness_decision_v01.json
```

The compact score-unblock bundle is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_unblock_bundle_contract_v01.csv
docs/cmb_tau_lensing_score_unblock_bundle_contract_v01.md
scripts/build_tau_lensing_score_unblock_bundle.py
```

## Current Expected Decision

With no submitted route evidence, the expected decision is:

```text
BLOCKED_ON_TAU_ROUTE_EVIDENCE
```

If exactly one route exists but its declaration, provenance, hash, or placeholder
firewall fails, the decision must be:

```text
BLOCKED_ON_ROUTE_EVIDENCE_FIREWALL
```

If a route reaches preflight-ready state, the decision may be:

```text
READY_TO_SCORE
```

In that state this contract still requires:

```text
score_run: false
```

## Claim Boundary

```text
score_readiness_decision_contract_only_no_score_run_no_dark_sector_verdict
```
