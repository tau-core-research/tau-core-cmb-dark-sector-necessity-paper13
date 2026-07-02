# CMB Tau Lensing Score Gate Contract v01

**Doc class:** aggregate score-gate contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_score_unblock_bundle_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_score_gate_contract_v01.csv`

This contract adds a single aggregate gate over the current scoring
preconditions. The default gate runs the ACT-side environment check,
score-readiness decision, score-unblock bundle, and route submission audit. It
does not run a physical Tau score and does not issue a dark-sector verdict.

The aggregate `score_gate_passed` field may become true only when the readiness
decision is `READY_TO_SCORE` and the ACT-side environment is ready.
Synthetic regression smokes are available through
`scripts/run_tau_lensing_score_gate.py --with-regression-smokes` and through
`make scoring-regression-all`; they are intentionally separate from the default
current-state gate so real route payload submission is not mixed with temporary
synthetic payload fixtures.
The score gate uses a local lock while running, so nested guard/audit calls do
not race over the gate report.
The `next_commands` sequence begins with the payload checklist so route evidence
submission can be checked before any replay or score step.
The final no-score guard before a score attempt is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_attempt_guard_contract_v01.csv
docs/cmb_tau_lensing_score_attempt_guard_contract_v01.md
scripts/guard_tau_lensing_score_attempt.py
```

## Command

```text
make score-gate
```

Default generated gate:

```text
data/derived/cmb_tau_lensing_score_gate_v01.json
```

## Current Expected Gate

```text
score_gate_passed = false
score_gate_pass_requires_all_smokes_and_environment = false
regression_smokes_run = false
positive_score_path_smoke_passed = true
firewall_blocker_smoke_passed = true
firewall_blocker_smoke_submission_audit_decision = null
good_route_submission_smoke_passed = true
good_route_submission_smoke_audit_decision = null
readiness_decision = BLOCKED_ON_TAU_ROUTE_EVIDENCE
route_submission_audit_decision = BLOCKED_SUBMIT_EXACTLY_ONE_ROUTE
```

## Claim Boundary

```text
score_gate_contract_only_no_score_run_no_dark_sector_verdict
```
