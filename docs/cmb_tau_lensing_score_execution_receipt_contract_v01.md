# CMB Tau Lensing Score Execution Receipt Contract v01

**Doc class:** score execution receipt contract
**Reader role:** Paper 13 scoring implementer/reviewer
**Status:** implemented, current receipt blocked before score
**Canonical parent:** `docs/cmb_tau_lensing_score_attempt_guard_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_score_execution_receipt_contract_v01.csv`

This contract registers the score execution receipt written by the guarded
score entrypoint:

```text
scripts/run_tau_lensing_guarded_score_report.py --write-receipt
```

Default receipt:

```text
data/derived/cmb_tau_lensing_score_execution_receipt_v01.json
```

The receipt records whether the score attempt was blocked before execution or
completed as a reduced diagnostic score. It binds the guard decision, readiness
decision, selected route count, output path, output SHA256, output validation,
route id, grid hash, and claim boundary when a score is actually produced.

## Allowed Receipt Status

```text
BLOCKED_BEFORE_SCORE_EXECUTION
REDUCED_SCORE_EXECUTION_COMPLETED
```

## Current Expected Receipt

With no submitted Tau route evidence, the expected receipt status is:

```text
BLOCKED_BEFORE_SCORE_EXECUTION
```

## Claim Boundary

```text
score_execution_receipt_contract_only_no_unvalidated_score_no_dark_sector_verdict
```
