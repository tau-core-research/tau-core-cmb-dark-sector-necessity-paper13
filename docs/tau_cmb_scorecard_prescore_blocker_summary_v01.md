# Tau CMB Scorecard Prescore Blocker Summary v01

**Doc class:** pre-score blocker summary
**Status:** all score rows blocked; no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scorecard_prescore_blocker_summary.py
```

Derived outputs:

```text
data/derived/tau_cmb_scorecard_prescore_blocker_summary_v01.csv
data/derived/tau_cmb_scorecard_prescore_blocker_summary_summary_v01.csv
```

This artifact summarizes the state after the focused v01 closure/evaluation
sequence. It does not add new physics. It records the minimum blocker for each
CMB role before scoring can begin.

Every score row remains blocked:

```text
score_ready_rows = 0
score_blocked_rows = 6
```

The pre-score blocker summary therefore prevents a premature scorecard
promotion and identifies the next contract to build:

```text
tau_cmb_minimal_scoring_input_contract_v01
```

## Claim Boundary

This artifact is a blocker summary only. It computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
