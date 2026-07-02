# CMB Tau Lensing Scoring Status Summary Contract v01

**Doc class:** scoring status contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no new score
**Canonical parent:** `docs/cmb_tau_lensing_score_attempt_guard_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_scoring_status_summary_contract_v01.csv`

This contract registers one compact status command for the physical Tau lensing
score attempt:

```text
make scoring-status
```

Default generated status:

```text
data/derived/cmb_tau_lensing_scoring_status_summary_v01.json
```

The status summary consumes the existing score-attempt guard and score-output
audit. It does not create a separate scoring decision and must not execute a
new score.
If a score execution receipt exists, the summary also exposes the receipt
status and score-output hash binding. Missing receipts are reported as
`NO_RECEIPT_PRESENT`.

## Allowed Status Values

```text
BLOCKED_BEFORE_PHYSICAL_TAU_SCORE
READY_TO_RUN_PHYSICAL_TAU_SCORE
PHYSICAL_TAU_SCORE_ACCEPTED
```

## Current Expected Status

With no submitted Tau route evidence, the expected status is:

```text
BLOCKED_BEFORE_PHYSICAL_TAU_SCORE
```

## Claim Boundary

```text
scoring_status_summary_contract_only_no_new_score_no_dark_sector_verdict
```
