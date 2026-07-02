# Tau CMB Effective Potential Source Handoff v01

**Doc class:** effective-potential source handoff
**Status:** handoff declared but blocked; no source derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_effective_potential_source_handoff.py
```

Derived outputs:

```text
data/derived/tau_cmb_effective_potential_source_handoff_v01.csv
data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv
```

This artifact declares the common handoff needed before acoustic and lensing
scoring can share a Tau effective potential source:

```text
Phi_tau_eff(a,k)
```

It does not derive `Phi_tau_eff`. The source slot is declared, but endpoint-blind
provenance, normalization, timing/sign, baryon-photon coupling, and lensing
projection response remain missing.

Therefore the effective-potential source handoff is not completed.

## Claim Boundary

This artifact is a handoff contract only. It derives no physical source,
computes no score, supplies no CMB likelihood, declares no reproduction or
failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
