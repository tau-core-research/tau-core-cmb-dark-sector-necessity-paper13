# Tau CMB Lensing Transfer Reduced Evaluation v01

**Doc class:** reduced lensing-transfer evaluation
**Status:** partial evaluation; lensing score still blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_lensing_transfer_reduced_evaluation.py
```

Derived outputs:

```text
data/derived/tau_cmb_lensing_transfer_reduced_evaluation_v01.csv
data/derived/tau_cmb_lensing_transfer_reduced_evaluation_summary_v01.csv
```

This artifact evaluates the declared lensing-transfer benchmark only at reduced
protocol level. It does not evaluate Planck or ACT lensing data and does not
compute a CMB lensing spectrum.

The formal projection-geometry guard is closed as a required precondition. The
failure branch is partially ready. The physics-bearing checks remain blocked
because the Tau effective potential, transfer kernel, amplitude/shape response,
and cross-readout consistency are not yet supplied.

The lensing score therefore remains blocked.

## Claim Boundary

This artifact is a partial reduced evaluation only. It computes no lensing
score, supplies no CMB likelihood, declares no lensing reproduction or failure,
validates no Tau-response source, and permits no no-dark or dark-sector verdict.
