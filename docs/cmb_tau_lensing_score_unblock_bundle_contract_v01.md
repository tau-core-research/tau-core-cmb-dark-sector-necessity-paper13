# CMB Tau Lensing Score Unblock Bundle Contract v01

**Doc class:** score-unblock bundle contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_score_readiness_decision_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_score_unblock_bundle_contract_v01.csv`

This contract builds one compact handoff artifact from the current score
readiness decision, scoring todo, route evidence pack, and payload acceptance
checklist. The handoff also points to the staging promotion precheck before any
guarded promotion into `payloads/`. It does not create real payloads by itself,
does not write a projection replay, does not run a score, and does not issue a
dark-sector verdict.
The handoff requires a `make staging-promote-*-dry-run` command before the
matching `make staging-promote-*` copy command, so reviewed route evidence
cannot bypass the promotion guard.
The handoff requires `make score-attempt-guard` before any score report command,
and `make score-output-audit` after any score artifact exists.

## Command

```text
make score-unblock
```

Default generated bundle:

```text
data/derived/cmb_tau_lensing_score_unblock_bundle_v01.json
```

The aggregate score gate is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_gate_contract_v01.csv
docs/cmb_tau_lensing_score_gate_contract_v01.md
scripts/run_tau_lensing_score_gate.py
```

The final score-attempt and score-output guards are tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_attempt_guard_contract_v01.csv
data/source_manifest/cmb_tau_lensing_score_output_status_audit_contract_v01.csv
```

## Current Expected Blocker

```text
BLOCKED_ON_TAU_ROUTE_EVIDENCE
```

## Claim Boundary

```text
score_unblock_bundle_contract_only_no_score_run_no_dark_sector_verdict
```
