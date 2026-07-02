# Tau CMB Scoring Input Fulfillment Plan v01

**Doc class:** scoring-input fulfillment plan
**Status:** plan declared; no input completed, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scoring_input_fulfillment_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_scoring_input_fulfillment_plan_v01.csv
data/derived/tau_cmb_scoring_input_fulfillment_plan_summary_v01.csv
```

This artifact converts the blocked scoring execution gate into a ranked
fulfillment plan. It does not complete any scoring input and does not compute a
score.

The first required artifact is:

```text
tau_cmb_effective_potential_source_handoff_v01
```

because acoustic and lensing scoring both depend on a common endpoint-blind
Tau effective-potential handoff. In v01:

```text
completed_rows = 0
pending_rows = 6
```

## Claim Boundary

This artifact is a fulfillment plan only. It computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
