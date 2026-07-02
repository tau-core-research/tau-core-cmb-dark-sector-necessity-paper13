# Tau CMB Minimal Scoring Input Contract v01

**Doc class:** minimal scoring input contract
**Status:** contract declared; all scoring inputs unsatisfied, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_minimal_scoring_input_contract.py
```

Derived outputs:

```text
data/derived/tau_cmb_minimal_scoring_input_contract_v01.csv
data/derived/tau_cmb_minimal_scoring_input_contract_summary_v01.csv
```

This artifact declares the minimum inputs required before the CMB scorecard is
allowed to run. It does not provide those inputs and does not compute scores.

Every contract row remains:

```text
UNSATISFIED_INPUT_MISSING
```

Therefore:

```text
score_entry_allowed_rows = 0
```

The contract is useful because it turns the current blockers into explicit
entry conditions for future scoring.

## Claim Boundary

This artifact is a scoring-input contract only. It computes no score, supplies
no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
