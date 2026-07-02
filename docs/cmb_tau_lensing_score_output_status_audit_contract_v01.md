# CMB Tau Lensing Score Output Status Audit Contract v01

**Doc class:** score-output status audit contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no new score
**Canonical parent:** `docs/cmb_tau_lensing_score_attempt_guard_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_score_output_status_audit_contract_v01.csv`

This contract audits whether an existing `payloads/tau_lensing_reduced_score_v01.json`
may be treated as a physical Tau score. A score output is accepted as physical
only if the score schema validates, the score-attempt guard allows the score
attempt, and the score execution receipt is `REDUCED_SCORE_EXECUTION_COMPLETED`
with a SHA256 hash matching the score output. The audit does not run a new
score and does not issue a dark-sector verdict.

## Command

```text
make score-output-audit
```

Default generated audit:

```text
data/derived/cmb_tau_lensing_score_output_status_audit_v01.json
```

## Claim Boundary

```text
score_output_status_audit_contract_only_no_new_score_no_dark_sector_verdict
```
