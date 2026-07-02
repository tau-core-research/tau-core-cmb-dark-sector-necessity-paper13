# Tau CMB Scoring Execution Gate v01

**Doc class:** scoring execution gate
**Status:** scoring blocked; no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scoring_execution_gate.py
```

Derived outputs:

```text
data/derived/tau_cmb_scoring_execution_gate_v01.csv
data/derived/tau_cmb_scoring_execution_gate_summary_v01.csv
```

This artifact decides whether the CMB scorecard is allowed to run from the
minimal scoring input contract. In v01 every contract input is unsatisfied, so
every execution gate row remains:

```text
SCORING_BLOCKED
```

Therefore no score is computed:

```text
run_allowed_rows = 0
score_computed_rows = 0
```

This is the last guard before a future scoring attempt. It prevents the paper
from converting scaffolds, blockers, or unresolved decisions into numerical
scores.

## Claim Boundary

This artifact is a scoring execution gate only. It computes no score, supplies
no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
