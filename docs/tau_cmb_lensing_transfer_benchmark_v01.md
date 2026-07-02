# Tau CMB Lensing Transfer Benchmark v01

**Doc class:** reduced lensing-transfer benchmark
**Status:** benchmark declared; no evaluation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_lensing_transfer_benchmark.py
```

Derived outputs:

```text
data/derived/tau_cmb_lensing_transfer_benchmark_v01.csv
data/derived/tau_cmb_lensing_transfer_benchmark_summary_v01.csv
```

This artifact declares the reduced checks that must be evaluated before a CMB
lensing score can be promoted:

```text
lensing potential source presence
transfer kernel presence
projection geometry convention
amplitude / shape support
cross-readout consistency
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_EVALUATED
```

The benchmark does not evaluate Planck or ACT lensing data. It only states what
`Phi_tau_eff` and `T_tau_CMB` would have to provide before the lensing scorecard
row can be promoted.

## Claim Boundary

This artifact declares reduced lensing-transfer benchmark conditions only. It
evaluates no lensing spectrum, computes no score, supplies no CMB likelihood,
declares no lensing success or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
