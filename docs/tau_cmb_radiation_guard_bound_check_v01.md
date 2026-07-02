# Tau CMB Radiation Guard Bound Check v01

**Doc class:** radiation-guard bound-check scaffold
**Status:** guard requirements declared; no bound evaluation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_radiation_guard_bound_check.py
```

Derived outputs:

```text
data/derived/tau_cmb_radiation_guard_bound_check_v01.csv
data/derived/tau_cmb_radiation_guard_bound_check_summary_v01.csv
```

This artifact declares what the radiation guard must check:

```text
Delta_N_eff_tau definition
external Delta_N_eff_bound convention
damping-tail inequality
cross-role consistency
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_EVALUATED
```

The artifact does not evaluate a numerical Neff bound and does not compare to
Planck, ACT, or other damping-tail data. It only records the guard that must be
run before the radiation row can be scored.

## Claim Boundary

This artifact declares radiation-guard requirements only. It evaluates no bound,
computes no score, supplies no CMB likelihood, validates no Tau-response source,
and permits no no-dark or dark-sector verdict.
