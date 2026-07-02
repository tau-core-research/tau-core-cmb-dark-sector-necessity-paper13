# Tau CMB Acoustic Role Reduced Benchmark v01

**Doc class:** reduced acoustic benchmark
**Status:** benchmark declared; no evaluation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_acoustic_role_reduced_benchmark.py
```

Derived outputs:

```text
data/derived/tau_cmb_acoustic_role_reduced_benchmark_v01.csv
data/derived/tau_cmb_acoustic_role_reduced_benchmark_summary_v01.csv
```

This artifact declares the reduced acoustic checks that must be evaluated
before a full CMB likelihood is worth attempting:

```text
potential source presence
acoustic phase support
relative peak-height support
baryon-loading compatibility
scale / sound-horizon convention
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_EVALUATED
```

The benchmark does not solve the photon-baryon Boltzmann system. It only states
what a Tau effective potential would have to preserve or reproduce at reduced
role level before the acoustic scorecard row can be promoted.

## Claim Boundary

This artifact declares reduced acoustic benchmark conditions only. It evaluates
no spectrum, computes no score, supplies no CMB likelihood, declares no acoustic
success or failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
