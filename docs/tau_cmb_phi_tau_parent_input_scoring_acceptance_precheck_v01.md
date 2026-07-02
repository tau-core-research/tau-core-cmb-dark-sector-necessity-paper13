# Tau CMB Phi Tau Parent Input Scoring Acceptance Precheck v01

**Doc class:** parent-input scoring acceptance precheck
**Status:** scoring acceptance precheck executed and blocked; no scoring acceptance, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_summary_v01.csv
```

This artifact performs the scoring-acceptance precheck for parent-side Tau
inputs. All five precheck rows are blocked because the evidence package,
certificate pass, payload acceptance, and `Phi_tau_eff` derivation gates have
not passed.

The scoring acceptance precheck is not satisfied:

```text
scoring_acceptance_precheck_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01
```

## Claim Boundary

This artifact performs a scoring-acceptance precheck only. It accepts no
parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score, supplies no
CMB likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
