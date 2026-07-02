# CMB Tau Lensing Score Attempt Guard Contract v01

**Doc class:** score-attempt guard contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_score_gate_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_score_attempt_guard_contract_v01.csv`

This contract registers a final guard before any reduced Tau lensing score
attempt. It reads the aggregate score gate and emits either
`ALLOW_SCORE_ATTEMPT` or `BLOCK_SCORE_ATTEMPT`. It does not run a score, does
not write a score output, and does not issue a dark-sector verdict.

Existing score-output physical status is audited separately at:

```text
data/source_manifest/cmb_tau_lensing_score_output_status_audit_contract_v01.csv
docs/cmb_tau_lensing_score_output_status_audit_contract_v01.md
scripts/audit_tau_lensing_score_output_status.py
```

## Command

```text
make score-attempt-guard
```

Default generated guard:

```text
data/derived/cmb_tau_lensing_score_attempt_guard_v01.json
```

## Claim Boundary

```text
score_attempt_guard_contract_only_no_score_run_no_dark_sector_verdict
```
