# Tau CMB Acoustic Reduced Evaluation v01

**Doc class:** reduced acoustic evaluation
**Status:** partial evaluation; acoustic score still blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_acoustic_reduced_evaluation.py
```

Derived outputs:

```text
data/derived/tau_cmb_acoustic_reduced_evaluation_v01.csv
data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv
```

This artifact evaluates the declared acoustic benchmark only at reduced protocol
level. It does not solve the photon-baryon Boltzmann system and does not compute
a CMB spectrum.

The formal scale/sound-horizon convention guard is closed as a required
precondition. The failure branch is partially ready. The physics-bearing
acoustic checks remain blocked because the Tau effective potential,
endpoint-blind amplitude, source timing/sign, and baryon-loading coupling are
not yet supplied.

The acoustic score therefore remains blocked.

## Claim Boundary

This artifact is a partial reduced evaluation only. It computes no acoustic
score, supplies no CMB likelihood, declares no acoustic reproduction or failure,
validates no Tau-response source, and permits no no-dark or dark-sector verdict.
