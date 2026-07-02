# Tau CMB Radiation Guard Evaluation v01

**Doc class:** radiation-guard reduced evaluation
**Status:** partial evaluation; radiation score still blocked, no bound score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_radiation_guard_evaluation.py
```

Derived outputs:

```text
data/derived/tau_cmb_radiation_guard_evaluation_v01.csv
data/derived/tau_cmb_radiation_guard_evaluation_summary_v01.csv
```

This artifact evaluates the radiation guard only at reduced protocol level. The
external-bound convention guard is closed as a required precondition.

The physics-bearing guard remains open because no Tau-side contribution is
derived and no numerical inequality is evaluated:

```text
Delta_N_eff_tau <= Delta_N_eff_bound
```

The radiation score therefore remains blocked.

## Claim Boundary

This artifact is a partial reduced evaluation only. It evaluates no numerical
bound, computes no radiation score, supplies no CMB likelihood, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
